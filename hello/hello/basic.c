#include <stdio.h>

int g = 20;

int add(int x, int y) {
	return x + y;
}
int main() {
	int a, b, sum;
	scanf_s("%d %d", &a, &b);
	sum = a + b;
	printf("%d", sum);
}