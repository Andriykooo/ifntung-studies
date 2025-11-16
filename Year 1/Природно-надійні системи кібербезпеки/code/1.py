import numpy

n = 1

def draw_bin_image(image_matrix):
    image_matrix = image_matrix.reshape((6, 5))
    for row in image_matrix.tolist():
        print('|' + ''.join([' * '[int(val)] for val in row]))

def to_bipolar(data):
    return numpy.where(data == 0, -1, 1)

def to_binary(data):
    return numpy.where(data == -1, 0, 1)

zero_bin = numpy.array([
    0, 1, 1, 1, 0,
    1, 0, 0, 0, 1,
    1, 0, 0, 0, 1,
    1, 0, 0, 0, 1,
    1, 0, 0, 0, 1,
    0, 1, 1, 1, 0])

one_bin = numpy.array([
    0, 1, 1, 0, 0,
    0, 0, 1, 0, 0,
    0, 0, 1, 0, 0,
    0, 0, 1, 0, 0,
    0, 0, 1, 0, 0,
    0, 0, 1, 0, 0])

half_zero_bin = numpy.array([
    0, 1, 1, 1, 0,
    1, 0, 0, 0, 1,
    1, 0, 0, 0, 1,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0])

X = to_bipolar(zero_bin)
Y = to_bipolar(one_bin)

W = numpy.outer(X, Y)

print("Запуск відновлення...")

X_corrupted = to_bipolar(half_zero_bin)

Y_recovered_bipolar = numpy.sign(numpy.dot(X_corrupted, W))

X_recovered_bipolar = numpy.sign(numpy.dot(Y_recovered_bipolar, W.T))

Y_final_bipolar = numpy.sign(numpy.dot(X_recovered_bipolar, W))

Y_final_binary = to_binary(Y_final_bipolar)

print("Вхід (пошкоджений 'zero'):")
draw_bin_image(half_zero_bin)

print("\nВідновлений вихід (має бути 'one'):")
draw_bin_image(Y_final_binary)

if numpy.array_equal(one_bin, Y_final_binary):
    print("\nРезультат: Успіх! Відновлений образ збігається з 'one'.")
else:
    print("\nРезультат: Помилка. Відновлений образ не збігається.")