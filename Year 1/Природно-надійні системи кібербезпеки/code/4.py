import numpy
import tensorflow

batch_size = 64
n = 50
latent_dim = 256
num_samples = 1000

input_texts = []
target_texts = []
input_characters = set()
target_characters = set()

with open("fra-eng/fra.txt", "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

for line in lines[: min(num_samples, len(lines) - 1)]:
    input_text, target_text, _ = line.split("\t")
    target_text = "\t" + target_text + "\n"
    input_texts.append(input_text)
    target_texts.append(target_text)
    for char in input_text:
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text:
        if char not in target_characters:
            target_characters.add(char)

input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])

input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

encoder_input_data = numpy.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32"
)
decoder_input_data = numpy.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32"
)
decoder_target_data = numpy.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32"
)

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    encoder_input_data[i, t + 1:, input_token_index[" "]] = 1.0
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0
    decoder_input_data[i, t + 1:, target_token_index[" "]] = 1.0
    decoder_target_data[i, t:, target_token_index[" "]] = 1.0

# --- Побудова моделі з LSTM ---
encoder_inputs = tensorflow.keras.Input(shape=(None, num_encoder_tokens))
encoder = tensorflow.keras.layers.LSTM(latent_dim, return_state=True)
encoder_lstm_outputs, encoder_state_h, encoder_state_c = encoder(encoder_inputs)
# Ми зберігаємо обидва стани: h (прихований стан) та c (стан комірки)
encoder_states = [encoder_state_h, encoder_state_c]

decoder_inputs = tensorflow.keras.Input(shape=(None, num_decoder_tokens))
decoder_lstm = tensorflow.keras.layers.LSTM(latent_dim, return_sequences=True, return_state=True)
# Подаємо стани кодера як початкові стани декодера
decoder_lstm_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)

decoder_dense = tensorflow.keras.layers.Dense(num_decoder_tokens, activation="softmax")
decoder_outputs = decoder_dense(decoder_lstm_outputs)

model = tensorflow.keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

model.compile(
    optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"]
)

model.fit(
    [encoder_input_data, decoder_input_data],
    decoder_target_data,
    batch_size=batch_size,
    epochs=n,
    validation_split=0.2,
)

# --- Побудова моделей для дешифрування ---
encoder_model = tensorflow.keras.Model(encoder_inputs, encoder_states)

decoder_inputs = model.input[1]
decoder_input_state_h = tensorflow.keras.Input(shape=(latent_dim,))
decoder_input_state_c = tensorflow.keras.Input(shape=(latent_dim,))
decoder_inputs_states = [decoder_input_state_h, decoder_input_state_c]

decoder_lstm = model.layers[3]
decoder_lstm_outputs, decoder_state_h, decoder_state_c = decoder_lstm(
    decoder_inputs, initial_state=decoder_inputs_states
)
decoder_states = [decoder_state_h, decoder_state_c]

decoder_dense = model.layers[4]
decoder_outputs = decoder_dense(decoder_lstm_outputs)

decoder_model = tensorflow.keras.Model(
    [decoder_inputs] + decoder_inputs_states, [decoder_outputs] + decoder_states
)

reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())

for seq_index in range(20):
    input_seq = encoder_input_data[seq_index: seq_index + 1]

    # Кодер LSTM повертає два стани (h і c)
    states_value = encoder_model.predict(input_seq, verbose=0)

    target_seq = numpy.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, target_token_index["\t"]] = 1.0
    stop_condition = False
    decoded_sentence = ""

    while not stop_condition:
        # Декодер LSTM вимагає обидва стани (h і c)
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value, verbose=0
        )

        sampled_token_index = numpy.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        if sampled_char == "\n" or len(decoded_sentence) > max_decoder_seq_length:
            stop_condition = True

        target_seq = numpy.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.0

        # Оновлюємо обидва стани для наступної ітерації
        states_value = [h, c]

    print("-")
    print("Input sentence:", input_texts[seq_index])
    print("Decoded sentence:", decoded_sentence)