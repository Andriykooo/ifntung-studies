#include <iostream>

int main()
{
    const int SIZE = 10;
    int values[SIZE];

    std::cout << "Enter 10 integers (-1000..1000): ";
    for (int i = 0; i < SIZE; ++i)
    {
        std::cin >> values[i];
    }

    std::cout << "Array:\n";
    for (int i = 0; i < SIZE; ++i)
    {
        std::cout << i << ": " << values[i] << "\n";
    }

    int count = 0;
    int sum = 0;
    int firstIndex = -1;
    int lastIndex = -1;
    std::cout << "Even element indices:";
    for (int i = 0; i < SIZE; ++i)
    {
        if (values[i] % 2 == 0)
        {
            ++count;
            sum += values[i];
            if (firstIndex == -1)
            {
                firstIndex = i;
            }
            lastIndex = i;
            std::cout << " " << i;
        }
    }
    std::cout << "\n";

    std::cout << "count = " << count << "\n";
    std::cout << "sum = " << sum << "\n";
    std::cout << "firstIndex = " << firstIndex << "\n";
    std::cout << "lastIndex = " << lastIndex << "\n";
    if (count > 0)
    {
        double average = static_cast<double>(sum) / count;
        std::cout << "average = " << average << "\n";
    }
    else
    {
        std::cout << "average: no data\n";
    }

    std::cout << "Reverse pass, even indices:";
    for (int i = SIZE - 1; i >= 0; --i)
    {
        if (values[i] % 2 == 0)
        {
            std::cout << " " << i;
            values[i] = 0;
        }
    }
    std::cout << "\n";

    std::cout << "Array after change:\n";
    for (int i = 0; i < SIZE; ++i)
    {
        std::cout << i << ": " << values[i] << "\n";
    }
    return 0;
}
