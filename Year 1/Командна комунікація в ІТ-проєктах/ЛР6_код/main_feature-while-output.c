/*
 * Лабораторна робота 6, варіант 4.
 * У масиві B з 14 елементів замінити всі від'ємні елементи на парних місцях
 * максимальним елементом масиву, а на непарних місцях - максимальним серед
 * від'ємних елементів. Особливий випадок: від'ємних елементів немає.
 * Гілка feature/while-output: вивід елементів масиву циклом while.
 */
#include <stdio.h>

#define N 14

void print_array(const char *title, const int b[], int n)
{
    int i = 0;

    printf("%s", title);
    while (i < n) {
        printf("%d ", b[i]);
        i++;
    }
    printf("\n");
}

/* Повертає кількість від'ємних елементів (0 - замін не було) */
int transform(const int b[], int c[], int n)
{
    int max = b[0], max_neg = 0, cnt_neg = 0;

    for (int i = 0; i < n; i++) {
        c[i] = b[i];
        if (b[i] > max)
            max = b[i];
        if (b[i] < 0 && (cnt_neg == 0 || b[i] > max_neg))
            max_neg = b[i];
        if (b[i] < 0)
            cnt_neg++;
    }
    if (cnt_neg == 0) {
        printf("Від'ємних елементів немає: масив залишається без змін\n");
        return 0;
    }
    printf("max = %d, max серед від'ємних = %d\n", max, max_neg);
    for (int i = 0; i < n; i++) {
        int pos = i + 1;                 /* номер місця (з 1) */
        if (b[i] < 0)
            c[i] = (pos % 2 == 0) ? max : max_neg;
    }
    return cnt_neg;
}

int main(void)
{
    int b[N] = {3, -5, 7, -2, -8, 4, -1, 9, -6, 2, -3, 5, 1, -4};
    int c[N];

    print_array("Заданий масив B:       ", b, N);
    transform(b, c, N);
    print_array("Новоутворений масив C: ", c, N);
    return 0;
}
