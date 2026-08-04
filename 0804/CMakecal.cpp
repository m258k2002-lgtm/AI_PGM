#include <windows.h>
#include <string>

// 전역 변수 (UI 요소 및 계산기 상태 저장)
HWND hEdit;                 // 결과를 보여줄 텍스트 박스
std::wstring currentText = L"0";
double firstOperand = 0.0;
wchar_t currentOp = 0;
bool isNewInput = true;

// 버튼 클릭을 처리하는 함수
void HandleButtonClick(const wchar_t* btnText) {
    if (wcscmp(btnText, L"C") == 0) {
        currentText = L"0";
        firstOperand = 0.0;
        currentOp = 0;
        isNewInput = true;
    }
    else if (wcscmp(btnText, L"=") == 0) {
        if (currentOp != 0) {
            double secondOperand = std::stod(currentText);
            double result = 0.0;

            switch (currentOp) {
            case L'+': result = firstOperand + secondOperand; break;
            case L'-': result = firstOperand - secondOperand; break;
            case L'*': result = firstOperand * secondOperand; break;
            case L'/': result = (secondOperand != 0) ? firstOperand / secondOperand : 0; break;
            }

            // 결과를 텍스트로 변환 (소수점 정리)
            wchar_t buf[32];
            swprintf(buf, 32, L"%g", result);
            currentText = buf;
            currentOp = 0;
            isNewInput = true;
        }
    }
    else if (wcscmp(btnText, L"+") == 0 || wcscmp(btnText, L"-") == 0 ||
        wcscmp(btnText, L"*") == 0 || wcscmp(btnText, L"/") == 0) {
        firstOperand = std::stod(currentText);
        currentOp = btnText[0];
        isNewInput = true;
    }
    else { // 숫자 버튼인 경우
        if (isNewInput || currentText == L"0") {
            currentText = btnText;
            isNewInput = false;
        }
        else {
            currentText += btnText;
        }
    }

    // 텍스트 박스 화면 업데이트
    SetWindowTextW(hEdit, currentText.c_str());
}

// 윈도우에서 일어나는 모든 이벤트(클릭 등)를 감지하는 함수
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    // 버튼들의 글자 배열
    const wchar_t* btnLabels[] = {
        L"7", L"8", L"9", L"/",
        L"4", L"5", L"6", L"*",
        L"1", L"2", L"3", L"-",
        L"C", L"0", L"=", L"+"
    };

    switch (msg) {
    case WM_CREATE: // 창이 처음 만들어질 때
    {
        // 1. 계산기 결과창 (텍스트 박스) 생성
        hEdit = CreateWindowW(L"EDIT", L"0",
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_RIGHT | ES_READONLY,
            10, 10, 210, 40, hwnd, (HMENU)100, NULL, NULL);

        // 2. 16개의 버튼을 반복문으로 바둑판 배치
        int x = 10, y = 60;
        for (int i = 0; i < 16; i++) {
            CreateWindowW(L"BUTTON", btnLabels[i],
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                x, y, 50, 50, hwnd, (HMENU)(200 + i), NULL, NULL);

            x += 53; // 오른쪽으로 이동
            if ((i + 1) % 4 == 0) { // 4개가 배치되면 다음 줄로
                x = 10;
                y += 53;
            }
        }
        break;
    }
    case WM_COMMAND: // 버튼이 클릭되었을 때
    {
        int wmId = LOWORD(wParam);
        if (wmId >= 200 && wmId < 216) { // 우리가 만든 버튼(200~215번)이 맞다면
            int btnIndex = wmId - 200;
            HandleButtonClick(btnLabels[btnIndex]); // 해당 버튼의 글자를 로직에 전달
        }
        break;
    }
    case WM_DESTROY: // 창의 X 버튼을 눌렀을 때
        PostQuitMessage(0); // 프로그램 완전 종료
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

// C++ 프로그램의 진짜 시작점 (WinMain)
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const wchar_t CLASS_NAME[] = L"CalcWindow";

    WNDCLASSW wc = { };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1); // 배경색 지정

    RegisterClassW(&wc);

    // 윈도우 창 크기 및 기본 설정
    HWND hwnd = CreateWindowExW(
        0, CLASS_NAME, L"Win32 Calculator",
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 245, 320, // 창 크기(가로 245, 세로 320)
        NULL, NULL, hInstance, NULL
    );

    if (hwnd == NULL) return 0;

    ShowWindow(hwnd, nCmdShow);

    // 윈도우 메시지 루프 (사용자의 클릭을 계속 대기함)
    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}