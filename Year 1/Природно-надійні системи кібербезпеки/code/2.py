import numpy
import sklearn.metrics
import matplotlib.pyplot

n = 1


class NumpyCMAC:
    def __init__(self, quantization, associative_unit_size, step):
        self.quantization = quantization
        self.n_assoc = associative_unit_size
        self.step = step

        self.n_weights = self.quantization + self.n_assoc
        self.weights = numpy.zeros(self.n_weights)

        self.min_val = 0
        self.max_val = 2 * numpy.pi
        self.data_range = self.max_val - self.min_val

    def _get_active_indices(self, x_input):
        scaled_x = (x_input[0] - self.min_val) / self.data_range * (self.quantization - 1)

        start_index = int(numpy.floor(scaled_x))

        indices = numpy.arange(start_index, start_index + self.n_assoc)

        indices = indices % self.n_weights
        return indices.astype(int)

    def train(self, input_train, target_train, epochs):
        for _ in range(epochs):
            for x, y_target in zip(input_train, target_train):
                active_indices = self._get_active_indices(x)
                y_pred = numpy.sum(self.weights[active_indices])

                error = y_target[0] - y_pred

                correction = self.step * error / self.n_assoc
                self.weights[active_indices] += correction

    def predict(self, input_data):
        predictions = []
        for x in input_data:
            active_indices = self._get_active_indices(x)
            y_pred = numpy.sum(self.weights[active_indices])
            predictions.append(y_pred)
        return numpy.array(predictions)


train_space = numpy.linspace(0, 2 * numpy.pi, 100)
test_space = numpy.linspace(numpy.pi, 2 * numpy.pi, 50)

X_train = numpy.reshape(train_space, (100, 1))
X_test = numpy.reshape(test_space, (50, 1))

y_train = numpy.sin(X_train)
y_test = numpy.sin(X_test)

cmac = NumpyCMAC(
    quantization=100 + n,
    associative_unit_size=n + 2,
    step=0.2
)

cmac.train(input_train=X_train, target_train=y_train, epochs=100)

y_pred = cmac.predict(input_data=X_test)

error = sklearn.metrics.mean_squared_error(y_true=y_test, y_pred=y_pred)
print(f"Mean Squared Error (Помилка): {error}")

fig, ax = matplotlib.pyplot.subplots()
ax.plot(X_test, y_test, "o", label="data")
ax.plot(X_test, y_pred, label="model")
matplotlib.pyplot.legend(labels=["data", "model"])
matplotlib.pyplot.title("Результат Лабораторної 2 (Білозор Дмитро)")
matplotlib.pyplot.show()