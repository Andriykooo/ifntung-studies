#include <iostream>

int main()
{
    int speed;
    int limit;
    std::cout << "Enter speed and limit: ";
    std::cin >> speed >> limit;

    if (speed < 0 || limit <= 0)
    {
        std::cout << "invalid\n";
    }
    else if (speed < limit)
    {
        std::cout << "slow\n";
    }
    else if (speed == limit)
    {
        std::cout << "at_limit\n";
    }
    else
    {
        std::cout << "over_limit\n";
    }
    return 0;
}
