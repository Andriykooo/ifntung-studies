#include <iostream>

void addTo(double& target, double value);
double plusOne(const double& value);
bool negate(double* target);

int main()
{
    double a;
    double b;
    double c;
    std::cout << "Enter a, b, c (-100.0..100.0): ";
    std::cin >> a >> b >> c;
    std::cout << std::boolalpha;

    // Етап A. Значення, посилання та вказівник
    addTo(a, b);
    std::cout << "After addTo(a, b) by reference: a = " << a << "\n";

    double readResult = plusOne(c);
    std::cout << "plusOne(c) by const reference: " << readResult
              << ", c = " << c << "\n";

    double* pointer = &a;
    bool changed = negate(pointer);
    std::cout << "negate(&a): " << changed << ", a = " << a << "\n";

    changed = negate(nullptr);
    std::cout << "negate(nullptr): " << changed << ", a = " << a << "\n";

    std::cout << "Checkpoint: a = " << a << ", b = " << b << ", c = " << c << "\n";

    // Етап B. Один динамічний об'єкт
    double* dynamic = new double;
    *dynamic = a * b + c;
    std::cout << "Dynamic value a * b + c = " << *dynamic << "\n";

    *dynamic += 2.0;
    std::cout << "Dynamic value after + 2.0 = " << *dynamic << "\n";

    delete dynamic;
    dynamic = nullptr;
    std::cout << "Dynamic object deleted, pointer is nullptr: "
              << (dynamic == nullptr) << "\n";
    return 0;
}

// Параметр-посилання: змінює першу змінну (a += b)
void addTo(double& target, double value)
{
    target += value;
}

// const-посилання: лише читає значення і повертає c + 1.0
double plusOne(const double& value)
{
    return value + 1.0;
}

// Параметр-вказівник: перевіряє вказівник, змінює знак значення (-a)
bool negate(double* target)
{
    if (target == nullptr)
    {
        return false;
    }
    *target = -(*target);
    return true;
}
