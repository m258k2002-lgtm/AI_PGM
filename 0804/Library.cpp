#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdio.h>

// ImGui 헤더
#include "imgui.h"
#include "backends/imgui_impl_glfw.h"
#include "backends/imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#pragma execution_character_set("utf-8")
using namespace std;

// ==========================================
// 1. 도서 관리 로직 (콘솔 입출력 제거 버전)
// ==========================================
class Book {
public:
    int id;
    string title;
    string author;
    bool isBorrowed;

    Book(int id, string title, string author, bool isBorrowed = false)
        : id(id), title(title), author(author), isBorrowed(isBorrowed) {
    }

    string toFileString() const {
        return to_string(id) + "|" + title + "|" + author + "|" + to_string(isBorrowed);
    }
};

class Library {
private:
    vector<Book> books;
    string filename = "library_data.txt";

    void saveToFile() {
        ofstream outFile(filename);
        if (outFile.is_open()) {
            for (const auto& book : books) {
                outFile << book.toFileString() << "\n";
            }
            outFile.close();
        }
    }

    void loadFromFile() {
        ifstream inFile(filename);
        string line;
        if (inFile.is_open()) {
            while (getline(inFile, line)) {
                stringstream ss(line);
                string item;
                vector<string> tokens;
                while (getline(ss, item, '|')) {
                    tokens.push_back(item);
                }
                if (tokens.size() == 4) {
                    books.emplace_back(stoi(tokens[0]), tokens[1], tokens[2], stoi(tokens[3]));
                }
            }
            inFile.close();
        }
    }

    int findBookIndexById(int id) {
        for (int i = 0; i < books.size(); ++i) {
            if (books[i].id == id) return i;
        }
        return -1;
    }

public:
    Library() { loadFromFile(); }
    ~Library() { saveToFile(); }

    const vector<Book>& getBooks() const { return books; }

    // 도서 등록
    string addBook(int id, string title, string author) {
        if (title.empty() || author.empty()) return "제목과 저자를 입력해주세요.";
        if (findBookIndexById(id) != -1) return "이미 존재하는 도서 ID입니다.";

        books.emplace_back(id, title, author);
        saveToFile();
        return "도서가 성공적으로 등록되었습니다.";
    }

    // 대출
    string borrowBook(int id) {
        int index = findBookIndexById(id);
        if (index != -1) {
            if (books[index].isBorrowed) return "이미 대출 중인 도서입니다.";
            books[index].isBorrowed = true;
            saveToFile();
            return "도서가 대출되었습니다.";
        }
        return "존재하지 않는 도서입니다.";
    }

    // 반납
    string returnBook(int id) {
        int index = findBookIndexById(id);
        if (index != -1) {
            if (!books[index].isBorrowed) return "대출되지 않은 도서입니다.";
            books[index].isBorrowed = false;
            saveToFile();
            return "도서가 반납되었습니다.";
        }
        return "존재하지 않는 도서입니다.";
    }

    // 삭제
    string deleteBook(int id) {
        int index = findBookIndexById(id);
        if (index != -1) {
            if (books[index].isBorrowed) return "대출 중인 도서는 삭제할 수 없습니다.";
            books.erase(books.begin() + index);
            saveToFile();
            return "도서가 삭제되었습니다.";
        }
        return "존재하지 않는 도서입니다.";
    }
};

// GLFW 에러 콜백
static void glfw_error_callback(int error, const char* description) {
    fprintf(stderr, "GLFW Error %d: %s\n", error, description);
}

// ==========================================
// 2. 메인 함수 및 ImGui 렌더링
// ==========================================
int main(int, char**) {
    glfwSetErrorCallback(glfw_error_callback);
    if (!glfwInit()) return 1;

    const char* glsl_version = "#version 130";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);

    GLFWwindow* window = glfwCreateWindow(1000, 600, "ImGui 도서 관리 시스템", nullptr, nullptr);
    if (window == nullptr) return 1;
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    ImGui::StyleColorsDark();

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    // [중요] 한글 폰트 로드 (윈도우의 맑은 고딕 사용)
    // 경로에 폰트가 없으면 기본 영어 폰트로 렌더링됩니다.
    ImFont* font = io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\malgun.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesKorean());

    // 도서 관리 시스템 객체 생성
    Library library;

    // UI 상태 저장을 위한 변수들
    int input_id = 0;
    char input_title[128] = "";
    char input_author[128] = "";
    char search_keyword[128] = "";
    string status_message = "환영합니다! 도서 관리 시스템입니다.";

    ImVec4 clear_color = ImVec4(0.15f, 0.15f, 0.20f, 1.00f);

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        // 메인 윈도우 생성
        ImGui::SetNextWindowPos(ImVec2(20, 20), ImGuiCond_FirstUseEver);
        ImGui::SetNextWindowSize(ImVec2(940, 520), ImGuiCond_FirstUseEver);
        ImGui::Begin("도서 관리 시스템", nullptr, ImGuiWindowFlags_NoCollapse);

        // 상단 알림 메시지 영역
        ImGui::TextColored(ImVec4(1.0f, 0.8f, 0.2f, 1.0f), "[알림] %s", status_message.c_str());
        ImGui::Separator();
        ImGui::Spacing();

        // 1. 새 도서 등록 섹션
        ImGui::Text("■ 새 도서 등록");
        ImGui::InputInt("도서 ID", &input_id);
        ImGui::InputText("제목", input_title, IM_ARRAYSIZE(input_title));
        ImGui::InputText("저자", input_author, IM_ARRAYSIZE(input_author));

        if (ImGui::Button("도서 등록##Add", ImVec2(120, 30))) {
            status_message = library.addBook(input_id, string(input_title), string(input_author));
            // 입력창 초기화
            input_id = 0;
            input_title[0] = '\0';
            input_author[0] = '\0';
        }

        ImGui::Spacing();
        ImGui::Separator();
        ImGui::Spacing();

        // 2. 도서 검색 섹션
        ImGui::Text("■ 도서 검색 및 목록");
        ImGui::InputText("검색어 (제목)", search_keyword, IM_ARRAYSIZE(search_keyword));

        ImGui::Spacing();

        // 3. 도서 목록 테이블
        if (ImGui::BeginTable("BookTable", 5, ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg | ImGuiTableFlags_SizingFixedFit)) {
            ImGui::TableSetupColumn("ID", ImGuiTableColumnFlags_WidthFixed, 50.0f);
            ImGui::TableSetupColumn("제목", ImGuiTableColumnFlags_WidthStretch);
            ImGui::TableSetupColumn("저자", ImGuiTableColumnFlags_WidthStretch);
            ImGui::TableSetupColumn("상태", ImGuiTableColumnFlags_WidthFixed, 80.0f);
            ImGui::TableSetupColumn("관리", ImGuiTableColumnFlags_WidthFixed, 150.0f);
            ImGui::TableHeadersRow();

            string keyword_str = search_keyword;

            for (const auto& book : library.getBooks()) {
                // 검색어가 있고, 제목에 포함되지 않으면 건너뜀
                if (!keyword_str.empty() && book.title.find(keyword_str) == string::npos) {
                    continue;
                }

                ImGui::TableNextRow();

                ImGui::TableNextColumn(); ImGui::Text("%d", book.id);
                ImGui::TableNextColumn(); ImGui::Text("%s", book.title.c_str());
                ImGui::TableNextColumn(); ImGui::Text("%s", book.author.c_str());

                ImGui::TableNextColumn();
                if (book.isBorrowed) {
                    ImGui::TextColored(ImVec4(1.0f, 0.4f, 0.4f, 1.0f), "대출 중");
                }
                else {
                    ImGui::TextColored(ImVec4(0.4f, 1.0f, 0.4f, 1.0f), "대출 가능");
                }

                // 관리 버튼 영역 (ID 충돌을 막기 위해 PushID 사용)
                ImGui::TableNextColumn();
                ImGui::PushID(book.id);

                if (book.isBorrowed) {
                    if (ImGui::Button("반납")) {
                        status_message = library.returnBook(book.id);
                    }
                }
                else {
                    if (ImGui::Button("대출")) {
                        status_message = library.borrowBook(book.id);
                    }
                }

                ImGui::SameLine();
                if (ImGui::Button("삭제")) {
                    status_message = library.deleteBook(book.id);
                    // 삭제 시 벡터 크기가 변하므로 에러 방지를 위해 루프 즉시 종료
                    ImGui::PopID();
                    break;
                }
                ImGui::PopID();
            }
            ImGui::EndTable();
        }
        ImGui::End();

        // 렌더링 처리
        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(clear_color.x * clear_color.w, clear_color.y * clear_color.w, clear_color.z * clear_color.w, clear_color.w);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        glfwSwapBuffers(window);
    }

    // 프로그램 종료 시 정리
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();
    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}