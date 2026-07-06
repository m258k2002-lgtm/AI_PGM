import tkinter as tk
from tkinter import messagebox

# --- 함수 정의 ---
def button_click(item):
    """버튼 클릭 시 입력창에 숫자/연산자 추가"""
    current = display_var.get()
    display_var.set(current + str(item))

def button_clear():
    """입력창 초기화 (C 버튼)"""
    display_var.set("")

def button_equal():
    """수식 계산 (= 버튼)"""
    try:
        # eval() 함수를 사용하여 문자열 수식을 계산
        result = str(eval(display_var.get()))
        display_var.set(result)
    except ZeroDivisionError:
        messagebox.showerror("계산 오류", "0으로 나눌 수 없습니다.")
        display_var.set("")
    except Exception as e:
        messagebox.showerror("입력 오류", "잘못된 수식입니다.")
        display_var.set("")

# --- 메인 윈도우 설정 ---
window = tk.Tk()
window.title("파이썬 GUI 계산기")
window.geometry("320x420")
window.resizable(0, 0) # 창 크기 조절 비활성화

# --- 입력창 (Display) 설정 ---
display_var = tk.StringVar()
display = tk.Entry(window, textvariable=display_var, font=('Helvetica', 20, 'bold'), 
                   bg="#f0f0f0", bd=10, justify="right")
display.pack(fill=tk.BOTH, ipadx=8, pady=15, padx=15)

# --- 버튼 프레임 설정 ---
btn_frame = tk.Frame(window)
btn_frame.pack()

# --- 버튼 레이아웃 정의 (텍스트, 행, 열) ---
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# --- 버튼 생성 및 배치 ---
for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(btn_frame, text=text, font=('Helvetica', 15, 'bold'), 
                        width=5, height=2, bg="#add8e6", command=button_equal)
    elif text == 'C':
        btn = tk.Button(btn_frame, text=text, font=('Helvetica', 15, 'bold'), 
                        width=5, height=2, bg="#ffb6c1", command=button_clear)
    else:
        # lambda 함수를 사용하여 각 버튼에 맞는 텍스트(숫자/기호)를 전달
        btn = tk.Button(btn_frame, text=text, font=('Helvetica', 15, 'bold'), 
                        width=5, height=2, command=lambda t=text: button_click(t))
    
    # 격자 모양으로 버튼 배치
    btn.grid(row=row, column=col, padx=5, pady=5)

# --- 프로그램 실행 ---
window.mainloop()