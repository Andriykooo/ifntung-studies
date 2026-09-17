#include <iostream>
#include <string>

bool isGroupA(char symbol);
bool isGroupB(char symbol);

int main()
{
    std::string text;
    std::cout << "Enter a line (ASCII, up to 200 characters): ";
    std::getline(std::cin, text);

    int countA = 0;
    int countB = 0;
    std::string modified = text;

    for (std::size_t i = 0; i < text.size(); ++i)
    {
        if (isGroupA(text[i]))
        {
            ++countA;
            modified[i] = '#';
        }
        if (isGroupB(text[i]))
        {
            ++countB;
        }
    }

    std::cout << "Count A: " << countA << "\n";
    std::cout << "Count B: " << countB << "\n";
    std::cout << "Modified: " << modified << "\n";
    return 0;
}

// Група A варіанта 4: k l m n o
bool isGroupA(char symbol)
{
    return symbol == 'k' || symbol == 'l' || symbol == 'm'
        || symbol == 'n' || symbol == 'o';
}

// Група B варіанта 4: p q r s t
bool isGroupB(char symbol)
{
    return symbol == 'p' || symbol == 'q' || symbol == 'r'
        || symbol == 's' || symbol == 't';
}
