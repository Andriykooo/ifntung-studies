import random
import string
import re
import numpy
import tensorflow

# --- Параметри моделі ---
n = 1
vocab_size = 15000
sequence_length = 20
embed_dim = 256
batch_size = 64
transformer_layers = 1 # Кількість блоків кодера/декодера

with open("spa-eng/spa.txt") as f:
    lines = f.read().split("\n")[:-1]

text_pairs = []
for line in lines:
    eng, spa = line.split("\t")
    spa = "[start] " + spa + " [end]"
    text_pairs.append((eng, spa))

# --- Розбиття набору даних ---
random.shuffle(text_pairs)
num_val_samples = int(0.15 * len(text_pairs))
num_train_samples = len(text_pairs) - 2 * num_val_samples
train_pairs = text_pairs[:num_train_samples]
val_pairs = text_pairs[num_train_samples : num_train_samples + num_val_samples]
test_pairs = text_pairs[num_train_samples + num_val_samples :]

# --- Векторизація (Токенізація) ---
strip_chars = string.punctuation + "¿"
strip_chars = strip_chars.replace("[", "")
strip_chars = strip_chars.replace("]", "")

def custom_standardization(input_string):
    lowercase = tensorflow.strings.lower(input_string)
    return tensorflow.strings.regex_replace(
        lowercase, "[%s]" % re.escape(strip_chars), ""
    )

eng_vectorization = tensorflow.keras.layers.TextVectorization(
    max_tokens=vocab_size,
    output_mode="int",
    output_sequence_length=sequence_length,
)
spa_vectorization = tensorflow.keras.layers.TextVectorization(
    max_tokens=vocab_size,
    output_mode="int",
    output_sequence_length=sequence_length + 1,
    standardize=custom_standardization,
)

train_eng_texts = [pair[0] for pair in train_pairs]
train_spa_texts = [pair[1] for pair in train_pairs]
eng_vectorization.adapt(train_eng_texts)
spa_vectorization.adapt(train_spa_texts)

# --- Створення набору даних (Dataset pipeline) ---
def format_dataset(eng, spa):
    eng = eng_vectorization(eng)
    spa = spa_vectorization(spa)
    return (
        {"encoder_inputs": eng, "decoder_inputs": spa[:, :-1],},
        spa[:, 1:],
    )

def make_dataset(pairs):
    eng_texts, spa_texts = zip(*pairs)
    eng_texts = list(eng_texts)
    spa_texts = list(spa_texts)
    dataset = tensorflow.data.Dataset.from_tensor_slices((eng_texts, spa_texts))
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(format_dataset)
    return dataset.shuffle(2048).prefetch(16).cache()

train_ds = make_dataset(train_pairs)
val_ds = make_dataset(val_pairs)

# --- Клас Позиційного Кодування ---
class PositionalEmbedding(tensorflow.keras.layers.Layer):
    def __init__(self, sequence_length, vocab_size, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.token_embeddings = tensorflow.keras.layers.Embedding(
            input_dim=vocab_size, output_dim=embed_dim
        )
        self.position_embeddings = tensorflow.keras.layers.Embedding(
            input_dim=sequence_length, output_dim=embed_dim
        )
        self.sequence_length = sequence_length
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim

    def call(self, inputs):
        length = tensorflow.shape(inputs)[-1]
        positions = tensorflow.range(start=0, limit=length, delta=1)
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tensorflow.keras.ops.not_equal(inputs, 0)

# --- Клас Шифратора (Кодер) Трансформера ---
class TransformerEncoder(tensorflow.keras.layers.Layer):
    def __init__(self, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.attention = tensorflow.keras.layers.MultiHeadAttention(
            num_heads=8, key_dim=embed_dim
        )
        self.dense_proj = tensorflow.keras.Sequential(
            [
                tensorflow.keras.layers.Dense(units=embed_dim, activation="relu"),
                tensorflow.keras.layers.Dense(units=embed_dim),
            ]
        )
        self.layernorm_1 = tensorflow.keras.layers.LayerNormalization()
        self.layernorm_2 = tensorflow.keras.layers.LayerNormalization()
        self.supports_masking = True

    def call(self, inputs, mask=None):
        attention_output = self.attention(
            query=inputs, value=inputs, key=inputs, attention_mask=None
        )
        proj_input = self.layernorm_1(inputs + attention_output)
        proj_output = self.dense_proj(proj_input)
        return self.layernorm_2(proj_input + proj_output)

# --- Клас Дешифратора (Декодер) Трансформера ---
class TransformerDecoder(tensorflow.keras.layers.Layer):
    def __init__(self, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.attention_1 = tensorflow.keras.layers.MultiHeadAttention(
            num_heads=8, key_dim=embed_dim
        )
        self.attention_2 = tensorflow.keras.layers.MultiHeadAttention(
            num_heads=8, key_dim=embed_dim
        )
        self.dense_proj = tensorflow.keras.Sequential(
            [
                tensorflow.keras.layers.Dense(units=embed_dim, activation="relu"),
                tensorflow.keras.layers.Dense(units=embed_dim),
            ]
        )
        self.layernorm_1 = tensorflow.keras.layers.LayerNormalization()
        self.layernorm_2 = tensorflow.keras.layers.LayerNormalization()
        self.layernorm_3 = tensorflow.keras.layers.LayerNormalization()
        self.supports_masking = True

    def get_causal_attention_mask(self, inputs):
        # Створює маску для запобігання "загляданню у майбутнє"
        input_shape = tensorflow.shape(inputs)
        batch_size, sequence_length = input_shape[0], input_shape[1]
        i = tensorflow.range(sequence_length)[:, tensorflow.newaxis]
        j = tensorflow.range(sequence_length)
        mask = tensorflow.cast(i >= j, dtype="int32")
        mask = tensorflow.reshape(mask, (1, sequence_length, sequence_length))
        mult = tensorflow.concat(
            [tensorflow.expand_dims(batch_size, -1),
             tensorflow.constant([1, 1], dtype=tensorflow.int32)],
            axis=0,
        )
        return tensorflow.tile(mask, mult)

    def call(self, inputs, encoder_outputs, mask=None):
        causal_mask = self.get_causal_attention_mask(inputs)
        attention_output_1 = self.attention_1(
            query=inputs, value=inputs, key=inputs, attention_mask=causal_mask
        )
        out_1 = self.layernorm_1(inputs + attention_output_1)

        attention_output_2 = self.attention_2(
            query=out_1,
            value=encoder_outputs,
            key=encoder_outputs,
            attention_mask=None,
        )
        out_2 = self.layernorm_2(out_1 + attention_output_2)

        proj_output = self.dense_proj(out_2)
        return self.layernorm_3(out_2 + proj_output)

# --- Збирання моделі Трансформера ---
encoder_inputs = tensorflow.keras.Input(shape=(None,), dtype="int64", name="encoder_inputs")
x = PositionalEmbedding(sequence_length, vocab_size, embed_dim)(encoder_inputs)
x = TransformerEncoder(embed_dim)(x)
encoder_outputs = x
encoder = tensorflow.keras.Model(encoder_inputs, encoder_outputs)

decoder_inputs = tensorflow.keras.Input(shape=(None,), dtype="int64", name="decoder_inputs")
encoded_seq_inputs = tensorflow.keras.Input(shape=(None, embed_dim), name="encoder_outputs")
x = PositionalEmbedding(sequence_length, vocab_size, embed_dim)(decoder_inputs)
x = TransformerDecoder(embed_dim)(x, encoded_seq_inputs)
decoder_outputs = tensorflow.keras.layers.Dense(vocab_size, activation="softmax")(x)
decoder = tensorflow.keras.Model([decoder_inputs, encoded_seq_inputs], decoder_outputs)

# Повна модель
decoder_outputs = decoder([decoder_inputs, encoder(encoder_inputs)])
transformer = tensorflow.keras.Model(
    [encoder_inputs, decoder_inputs], decoder_outputs, name="transformer"
)

# --- Навчання ---
transformer.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

transformer.fit(train_ds, epochs=n, validation_data=val_ds)

# --- Дешифрація (Inference) ---
spa_vocab = spa_vectorization.get_vocabulary()
spa_index_lookup = dict(zip(range(len(spa_vocab)), spa_vocab))
max_decoded_sentence_length = sequence_length

def decode_sequence(input_sentence):
    tokenized_input_sentence = eng_vectorization([input_sentence])
    decoded_sentence = "[start]"
    for i in range(max_decoded_sentence_length):
        tokenized_target_sentence = spa_vectorization([decoded_sentence])[:, :-1]
        predictions = transformer([tokenized_input_sentence, tokenized_target_sentence])

        # Вибираємо токен на позиції 'i'
        sampled_token_index = numpy.argmax(predictions[0, i, :])
        sampled_token = spa_index_lookup[sampled_token_index]
        decoded_sentence += " " + sampled_token

        if sampled_token == "[end]":
            break

    return decoded_sentence.replace("[start] ", "").replace(" [end]", "")

# --- Тестування ---
test_eng_texts = [pair[0] for pair in test_pairs]
for _ in range(10):
    input_sentence = random.choice(test_eng_texts)
    print("-")
    print("Input sentence:", input_sentence)
    translated = decode_sequence(input_sentence)
    print("Decoded sentence:", translated)