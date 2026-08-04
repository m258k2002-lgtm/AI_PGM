import os
import tkinter as tk
from tkinter import messagebox, ttk

# 데이터 저장을 위한 파일 이름
FILENAME = "library_data.txt"


class Book:

  def __init__(self, book_id, title, author, is_borrowed=False):
    self.id = book_id
    self.title = title
    self.author = author
    self.is_borrowed = is_borrowed

  def to_file_string(self):
    return f"{self.id}|{self.title}|{self.author}|{int(self.is_borrowed)}"


class Library:

  def __init__(self):
    self.books = []
    self.load_from_file()

  def save_to_file(self):
    with open(FILENAME, "w", encoding="utf-8") as f:
      for book in self.books:
        f.write(book.to_file_string() + "\n")

  def load_from_file(self):
    if not os.path.exists(FILENAME):
      return
    with open(FILENAME, "r", encoding="utf-8") as f:
      for line in f:
        tokens = line.strip().split("|")
        if len(tokens) == 4:
          self.books.append(
              Book(int(tokens[0]), tokens[1], tokens[2], bool(int(tokens[3])))
          )

  def find_book_index_by_id(self, book_id):
    for i, book in enumerate(self.books):
      if book.id == book_id:
        return i
    return -1

  def add_book(self, book_id_str, title, author):
    if not book_id_str.isdigit():
      return "도서 ID는 숫자로 입력해주세요."
    book_id = int(book_id_str)

    if not title or not author:
      return "제목과 저자를 모두 입력해주세요."

    if self.find_book_index_by_id(book_id) != -1:
      return "이미 존재하는 도서 ID입니다."

    self.books.append(Book(book_id, title, author))
    self.save_to_file()
    return "도서가 성공적으로 등록되었습니다."

  def borrow_book(self, book_id):
    idx = self.find_book_index_by_id(book_id)
    if idx != -1:
      if self.books[idx].is_borrowed:
        return "이미 대출 중인 도서입니다."
      self.books[idx].is_borrowed = True
      self.save_to_file()
      return "도서가 대출되었습니다."
    return "존재하지 않는 도서입니다."

  def return_book(self, book_id):
    idx = self.find_book_index_by_id(book_id)
    if idx != -1:
      if not self.books[idx].is_borrowed:
        return "대출되지 않은 도서입니다."
      self.books[idx].is_borrowed = False
      self.save_to_file()
      return "도서가 반납되었습니다."
    return "존재하지 않는 도서입니다."

  def delete_book(self, book_id):
    idx = self.find_book_index_by_id(book_id)
    if idx != -1:
      if self.books[idx].is_borrowed:
        return "대출 중인 도서는 삭제할 수 없습니다."
      del self.books[idx]
      self.save_to_file()
      return "도서가 삭제되었습니다."
    return "존재하지 않는 도서입니다."


class LibraryApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Python 도서 관리 시스템")
    self.root.geometry("850x550")

    self.library = Library()

    # 상단 입력 프레임
    input_frame = tk.LabelFrame(root, text=" 새 도서 등록 ", font=("Malgun Gothic", 11, "bold"), padx=10, pady=10)
    input_frame.pack(fill="x", padx=15, pady=10)

    tk.Label(input_frame, text="도서 ID:", font=("Malgun Gothic", 10)).grid(row=0, column=0, sticky="w", padx=5)
    self.entry_id = tk.Entry(input_frame, width=10, font=("Malgun Gothic", 10))
    self.entry_id.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="제목:", font=("Malgun Gothic", 10)).grid(row=0, column=2, sticky="w", padx=5)
    self.entry_title = tk.Entry(input_frame, width=25, font=("Malgun Gothic", 10))
    self.entry_title.grid(row=0, column=3, padx=5)

    tk.Label(input_frame, text="저자:", font=("Malgun Gothic", 10)).grid(row=0, column=4, sticky="w", padx=5)
    self.entry_author = tk.Entry(input_frame, width=20, font=("Malgun Gothic", 10))
    self.entry_author.grid(row=0, column=5, padx=5)

    btn_add = tk.Button(input_frame, text="도서 등록", bg="#4CAF50", fg="white", font=("Malgun Gothic", 10, "bold"), command=self.add_book_action)
    btn_add.grid(row=0, column=6, padx=10)

    # 중단 검색 프레임
    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=15, pady=5)

    tk.Label(search_frame, text="검색어 (제목):", font=("Malgun Gothic", 10)).pack(side="left", padx=5)
    self.entry_search = tk.Entry(search_frame, width=30, font=("Malgun Gothic", 10))
    self.entry_search.pack(side="left", padx=5)
    self.entry_search.bind("<KeyRelease>", self.update_table)

    # 도서 목록 테이블 (Treeview) 프레임
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=15, pady=10)

    columns = ("ID", "제목", "저자", "상태")
    self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    
    self.tree.heading("ID", text="도서 ID")
    self.tree.heading("제목", text="제목")
    self.tree.heading("저자", text="저자")
    self.tree.heading("상태", text="대출 상태")

    self.tree.column("ID", width=80, anchor="center")
    self.tree.column("제목", width=300, anchor="w")
    self.tree.column("저자", width=200, anchor="w")
    self.tree.column("상태", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 하단 버튼 제어 프레임
    control_frame = tk.Frame(root)
    control_frame.pack(fill="x", padx=15, pady=10)

    btn_borrow = tk.Button(control_frame, text="선택 도서 대출", bg="#2196F3", fg="white", font=("Malgun Gothic", 10, "bold"), command=self.borrow_action)
    btn_borrow.pack(side="left", padx=5)

    btn_return = tk.Button(control_frame, text="선택 도서 반납", bg="#FF9800", fg="white", font=("Malgun Gothic", 10, "bold"), command=self.return_action)
    btn_return.pack(side="left", padx=5)

    btn_delete = tk.Button(control_frame, text="선택 도서 삭제", bg="#F44336", fg="white", font=("Malgun Gothic", 10, "bold"), command=self.delete_action)
    btn_delete.pack(side="left", padx=5)

    # 초기 테이블 데이터 로드
    self.update_table()

  def update_table(self, event=None):
    # 기존 테이블 목록 초기화
    for row in self.tree.get_children():
      self.tree.delete(row)

    keyword = self.entry_search.get().strip().lower()

    for book in self.library.books:
      if keyword and keyword not in book.title.lower():
        continue
      status = "대출 중" if book.is_borrowed else "대출 가능"
      self.tree.insert("", "end", values=(book.id, book.title, book.author, status))

  def add_book_action(self):
    msg = self.library.add_book(
        self.entry_id.get(),
        self.entry_title.get().strip(),
        self.entry_author.get().strip(),
    )
    messagebox.showinfo("알림", msg)
    if "성공" in msg:
      self.entry_id.delete(0, tk.END)
      self.entry_title.delete(0, tk.END)
      self.entry_author.delete(0, tk.END)
      self.update_table()

  def get_selected_book_id(self):
    selected_items = self.tree.selection()
    if not selected_items:
      return None
    item = self.tree.item(selected_items[0])
    return int(item["values"][0])

  def borrow_action(self):
    book_id = self.get_selected_book_id()
    if book_id is None:
      messagebox.showwarning("경고", "대출할 도서를 선택해주세요.")
      return
    msg = self.library.borrow_book(book_id)
    messagebox.showinfo("알림", msg)
    self.update_table()

  def return_action(self):
    book_id = self.get_selected_book_id()
    if book_id is None:
      messagebox.showwarning("경고", "반납할 도서를 선택해주세요.")
      return
    msg = self.library.return_book(book_id)
    messagebox.showinfo("알림", msg)
    self.update_table()

  def delete_action(self):
    book_id = self.get_selected_book_id()
    if book_id is None:
      messagebox.showwarning("경고", "삭제할 도서를 선택해주세요.")
      return
    msg = self.library.delete_book(book_id)
    messagebox.showinfo("알림", msg)
    self.update_table()


if __name__ == "__main__":
  root = tk.Tk()
  app = LibraryApp(root)
  root.mainloop()