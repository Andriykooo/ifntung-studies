/*
 * Лабораторна робота 6, варіант 2.
 * Гілка feature/random-fill: масив заповнюється генератором випадкових
 * чисел у діапазоні [-10; 10], розмір масиву вводиться з клавіатури.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 100

void print_array(const char *title, const double a[], int n)
{
    printf("%s", title);
    for (int i = 0; i < n; i++)
        printf("%g ", a[i]);
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
    double a[MAX_N], c[MAX_N];
    int n;

    printf("Введіть розмір масиву (1..%d): ", MAX_N);
    if (scanf("%d", &n) != 1 || n < 1 || n > MAX_N) {
        printf("Некоректний розмір масиву\n");
        return 1;
    }

    srand((unsigned) time(NULL));
    for (int i = 0; i < n; i++)
        a[i] = rand() % 21 - 10;        /* випадкове ціле з [-10; 10] */
    printf("\n");

    print_array("Заданий масив A:       ", a, n);
    transform(a, c, n);
    print_array("Новоутворений масив C: ", c, n);
    return 0;
}
