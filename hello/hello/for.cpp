#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;

int main() {
	system("chcp 65001");

	int count;
	cout << "학생수를 입력하세요";
	cin >> count;

	string student_id;
	string name;

	for (int i = 1; i <= count; i++)
		cout << "\n[" << i << "번쨰 학생 정보 입력]\n";
	cout << "학번 : ";
	cin >> student_id;
	cout << "이름 : ";
	cin >> name;
	cout << "-> 출력 : 학번은 " << student_id << ", 이름은" << name << "입니다.\n";



}