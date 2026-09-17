#include <iostream>

int main()
{
    int a;
    int b;

    do
    {
        std::cout << "Enter a and b (1 <= a <= b <= 10000): ";
        std::cin >> a >> b;
        if (a < 1 || b < a || b > 10000)
        {
            std::cout << "Invalid range, try again.\n";
        }
    } while (a < 1 || b < a || b > 10000);

    int count = 0;
    int sum = 0;
    for (int value = a; value <= b; ++value)
    {
        if (value % 3 != 0)
        {
            ++count;
            sum += value;
        }
    }

    std::cout << "Count: " << count << "\n";
    std::cout << "Sum: " << sum << "\n";
    return 0;
}
