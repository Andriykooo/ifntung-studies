#include <iostream>

int main()
{
    const int ROWS = 5;
    const int COLS = 4;
    int table[ROWS][COLS];

    std::cout << "Enter " << ROWS * COLS << " integers (-1000..1000), row by row:\n";
    for (int r = 0; r < ROWS; ++r)
    {
        for (int c = 0; c < COLS; ++c)
        {
            std::cin >> table[r][c];
        }
    }

    std::cout << "Table " << ROWS << " x " << COLS << ":\n";
    for (int r = 0; r < ROWS; ++r)
    {
        for (int c = 0; c < COLS; ++c)
        {
            std::cout << table[r][c] << "\t";
        }
        std::cout << "\n";
    }

    int zeroCount = 0;
    for (int r = 0; r < ROWS; ++r)
    {
        for (int c = 0; c < COLS; ++c)
        {
            if (table[r][c] == 0)
            {
                ++zeroCount;
            }
        }
    }
    std::cout << "Zero elements in table: " << zeroCount << "\n";

    for (int c = 0; c < COLS; ++c)
    {
        int nonZeroSum = 0;
        for (int r = 0; r < ROWS; ++r)
        {
            if (table[r][c] != 0)
            {
                nonZeroSum += table[r][c];
            }
        }
        std::cout << "Column " << c << ": sum of non-zero = " << nonZeroSum << "\n";
    }
    return 0;
}
