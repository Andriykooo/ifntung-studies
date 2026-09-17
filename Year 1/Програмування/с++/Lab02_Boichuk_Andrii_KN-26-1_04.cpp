#include <iostream>

int main()
{
    int a;
    int b;
    int c;
    std::cout << "Enter a, b, c (0..100): ";
    std::cin >> a >> b >> c;

    int sum = a + b + c;
    const int divisor = 6;
    int integerResult = (a + b) * c;
    int remainder = sum % divisor;
    double realResult = static_cast<double>(sum) / divisor;

    std::cout << "integerResult = " << integerResult << "\n";
    std::cout << "remainder = " << remainder << "\n";
    std::cout << "realResult = " << realResult << "\n";
    return 0;
}
