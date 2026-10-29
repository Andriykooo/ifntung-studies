/*
 * Лабораторна робота 6, варіант 4.
 * У масиві B замінити всі від'ємні елементи на парних місцях максимальним
 * елементом масиву, а на непарних місцях - максимальним серед від'ємних.
 * Гілка feature/keyboard-input: розмір і елементи масиву вводяться з клавіатури.
 */
#include <stdio.h>

#define NMAX 100

void print_array(const char *title, const int b[], int n)
{
    printf("%s", title);
    for (int i = 0; i < n; i++)
        printf("%d ", b[i]);
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
    int b[NMAX], c[NMAX], n;

    printf("Введіть розмір масиву (1..%d): ", NMAX);
    if (scanf("%d", &n) != 1 || n < 1 || n > NMAX) {
        printf("Некоректний розмір масиву\n");
        return 1;
    }
    printf("Введіть %d цілих чисел: ", n);
    for (int i = 0; i < n; i++)
        if (scanf("%d", &b[i]) != 1) {
            printf("Некоректне значення елемента\n");
            return 1;
        }
    printf("\n");

    print_array("Заданий масив B:       ", b, n);
    transform(b, c, n);
    print_array("Новоутворений масив C: ", c, n);
    return 0;
}
