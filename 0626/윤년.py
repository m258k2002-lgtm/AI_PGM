year = int(input("년도 입력 : "))
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 :
    print(f"{year}년은 윤년입니다.")
else :
    print(f"{year}년은 윤년이 아닙니다.")
