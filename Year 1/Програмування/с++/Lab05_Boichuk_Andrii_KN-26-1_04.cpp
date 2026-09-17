#include <iostream>

int characteristic(int n);
bool qualifies(int n);
int countQualifying(int a, int b, int c);

int main()
{
    int a;
    int b;
    int c;
    std::cout << "Enter a, b, c (positive, up to 999999): ";
    std::cin >> a >> b >> c;

    int result = countQualifying(a, b, c);
    std::cout << "Numbers with max digit 9: " << result << "\n";
    return 0;
}

// Характеристика: найбільша цифра числа n
int characteristic(int n)
{
    int maxDigit = 0;
    while (n > 0)
    {
        int digit = n % 10;
        if (digit > maxDigit)
        {
            maxDigit = digit;
        }
        n /= 10;
    }
    return maxDigit;
}

// Критерій варіанта 4: найбільша цифра дорівнює 9
bool qualifies(int n)
{
    return characteristic(n) == 9;
}

// Кількість чисел серед трьох, що задовольняють критерій
int countQualifying(int a, int b, int c)
{
    int count = 0;
    if (qualifies(a))
    {
        ++count;
    }
    if (qualifies(b))
    {
        ++count;
    }
    if (qualifies(c))
    {
        ++count;
    }
    return count;
}
