#include <iostream>
using namespace std;

int main() {
	int a = 5, b = 10, c;

	cout << (a + b / 3 * 3) << "\n";
	cout << (b << 2)<<"\n";
	cout << (a != b)<<"\n";
	cout << (b % a)<<"\n";
	cout << ((a > b) ? a : b)<<"\n";
	cout << (sizeof(a)) << "\n";
	cout << (c = a++) << "\n";
	cout << (a += b) << "\n";
	cout << (a & b) << "\n";
	cout << (c = (a + b, a - b)) << "\n";
}