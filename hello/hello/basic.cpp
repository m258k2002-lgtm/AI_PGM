#include <iostream>
using namespace std;

int g = 20; /* 전역 변수 */

int add(int x, int y) { // 전역 함수
	return x + y;
}

int main() {
	int a, b, sum; // 지역 변수
	cin >> a >> b; // 입력
	sum = a + b;
	cout << sum; // 출력
	return 0;
}
