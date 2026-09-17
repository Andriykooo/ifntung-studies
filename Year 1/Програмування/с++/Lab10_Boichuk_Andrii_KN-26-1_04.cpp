#include <iostream>
#include <fstream>

int main()
{
    std::ifstream input("input.txt");
    if (!input.is_open())
    {
        std::cout << "Error: cannot open input.txt\n";
        return 1;
    }

    int count = 0;
    int sum = 0;
    int value;
    while (input >> value)
    {
        if (value % 2 != 0)
        {
            ++count;
            sum += value;
        }
    }
    input.close();

    std::ofstream output("output.txt");
    if (!output.is_open())
    {
        std::cout << "Error: cannot open output.txt\n";
        return 2;
    }

    output << "count: " << count << "\n";
    output << "sum: " << sum << "\n";
    if (count > 0)
    {
        double average = static_cast<double>(sum) / count;
        output << "average: " << average << "\n";
    }
    else
    {
        output << "average: no data\n";
    }
    output.close();

    std::cout << "Processed odd numbers: " << count
              << ", result written to output.txt\n";
    return 0;
}
