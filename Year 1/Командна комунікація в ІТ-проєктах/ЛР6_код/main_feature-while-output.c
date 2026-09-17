/*
 * Лабораторна робота 6, варіант 2.
 * Гілка feature/while-output: вивід елементів масиву організовано
 * з використанням циклу while.
 */
#include <stdio.h>

#define N 14

void print_array(const char *title, const double a[], int n)
{
    int i = 0;
    printf("%s", title);
    while (i < n) {
        printf("%g", a[i]);
        if (i < n - 1)
            printf(", ");
        i++;
    }
    printf("\n");
}

void transform(const double a[], double c[], int n)
{
    double sum_neg = 0, sum_pos = 0;
    int cnt_neg = 0, cnt_pos = 0;

    for (int i = 0; i < n; i++) {
        if (a[i] < 0) { sum_neg += a[i]; cnt_neg++; }
        else if (a[i] > 0) { sum_pos += a[i]; cnt_pos++; }
    }

    for (int i = 0; i < n; i++)
        c[i] = a[i];

    if (cnt_neg == 0) {
        printf("Від'ємних елементів немає: парні позиції замінено на 1\n");
        for (int i = 1; i < n; i += 2)
            c[i] = 1;
        return;
    }
    if (cnt_pos == 0) {
        printf("Додатних елементів немає: від'ємні елементи замінено на 0\n");
        for (int i = 0; i < n; i++)
            c[i] = 0;
        return;
    }

    double mean_neg = sum_neg / cnt_neg;
    double mean_pos = sum_pos / cnt_pos;
    printf("Середнє від'ємних = %g, середнє додатних = %g\n", mean_neg, mean_pos);

    for (int i = 0; i < n; i++) {
        int pos = i + 1;
        if (a[i] < 0)
            c[i] = (pos % 2 == 0) ? mean_neg : mean_pos;
    }
}

int main(void)
{
    double a[N] = {5, -2, 3, -4, 5, 6, -7, 8, 9, -1, 2, 3, -6, 4};
    double c[N];

    print_array("Заданий масив A:       ", a, N);
    transform(a, c, N);
    print_array("Новоутворений масив C: ", c, N);
    return 0;
}
