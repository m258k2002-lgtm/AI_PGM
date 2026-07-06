import sys

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "오류: 0으로 나눌 수 없습니다."
    return x / y

def main():
    print("=" * 30)
    print("      CLI 파이썬 계산기      ")
    print("=" * 30)
    print("사용할 연산을 선택하세요:")
    print("1. 더하기 (+)")
    print("2. 빼기 (-)")
    print("3. 곱하기 (*)")
    print("4. 나누기 (/)")
    print("5. 종료")
    print("=" * 30)

    while True:
        choice = input("\n연산 선택 (1/2/3/4/5): ")

        if choice == '5':
            print("계산기 프로그램을 종료합니다.")
            sys.exit()

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("첫 번째 숫자를 입력하세요: "))
                num2 = float(input("두 번째 숫자를 입력하세요: "))
            except ValueError:
                print("잘못된 입력입니다. 올바른 '숫자'를 입력해주세요.")
                continue

            if choice == '1':
                print(f"\n결과: {num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"\n결과: {num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"\n결과: {num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                print(f"\n결과: {num1} / {num2} = {divide(num1, num2)}")
        else:
            print("잘못된 선택입니다. 1에서 5 사이의 번호를 입력해주세요.")

if __name__ == "__main__":
    main()