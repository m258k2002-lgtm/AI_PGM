import streamlit as st
import google.generativeai as genai

# 1. 가상의 데이터베이스 (그룹사 -> 계열사 -> 자소서 문항)
# 초보자용 시제품이므로 자주 나오는 문항을 미리 입력해 두었습니다.
MOCK_DB = {
    "삼성": {
        "삼성전자": "본인의 성장과정을 간략히 기술하되 현재의 자신에게 가장 큰 영향을 끼친 사건, 인물 등을 포함하여 기술하시기 바랍니다.",
        "삼성SDS": "본인이 회사를 선택하는 기준은 무엇이며, 왜 삼성SDS가 그 기준에 적합한지 기술하시기 바랍니다."
    },
    "현대자동차": {
        "현대자동차": "본인이 지원한 직무를 수행하기 위해 가장 필요한 역량은 무엇이라고 생각하며, 해당 역량을 갖추기 위해 어떠한 노력을 해왔는지 구체적으로 기술해 주십시오.",
        "기아": "기아에 지원하게 된 동기와 입사 후 포부를 구체적으로 작성해 주십시오."
    },
    "SK": {
        "SK하이닉스": "자발적으로 최고 수준의 목표를 세우고 끈질기게 성취한 경험에 대해 서술해 주십시오.",
        "SK텔레콤": "본인에게 주어졌던 일 중 가장 어려웠던 경험은 무엇이었으며, 그 일을 해결하기 위해 어떤 노력을 했는지 서술해 주십시오."
    }
}

st.title("🚀 자동 자기소개서 생성기")

# API 키 입력받기 
api_key = st.text_input("Google Gemini API 키를 입력하세요 (Google AI Studio에서 무료 발급):", type="password")

# 2. UI 구성: 그룹사 및 회사 선택
group_list = list(MOCK_DB.keys())
selected_group = st.selectbox("1. 그룹사를 선택하세요", group_list)

company_list = list(MOCK_DB[selected_group].keys())
selected_company = st.selectbox("2. 회사를 선택하세요", company_list)

# 선택된 회사의 자소서 문항 가져오기
question = MOCK_DB[selected_group][selected_company]
st.info(f"**[{selected_company} 채용 문항]**\n\n{question}")

# 3. 사용자 경험 입력
st.write("### 3. 본인의 경험을 핵심만 간단히 입력해 주세요 (단어나 짧은 문장도 좋습니다)")
exp1 = st.text_area("경험 1 (예: 대학 시절 코딩 동아리 기장 역임)")
exp2 = st.text_area("경험 2 (예: 팀원 간의 갈등 발생, 대화로 해결)")
exp3 = st.text_area("경험 3 (예: 최종적으로 공모전 대상 수상)")

# 4. 자소서 생성 버튼 및 AI 연동 로직
if st.button("✨ 자기소개서 생성하기"):
    if not api_key:
        st.error("위쪽에 API 키를 먼저 입력해 주세요!")
    elif not exp1 and not exp2 and not exp3:
        st.warning("경험을 최소 1개 이상 입력해 주세요.")
    else:
        with st.spinner("AI가 자기소개서를 정성껏 작성 중입니다. 잠시만 기다려주세요..."):
            try:
                # Gemini API 설정
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                # AI에게 내릴 명령어(프롬프트) 상세 구성
                prompt = f"""
                너는 10년 차 전문 취업 컨설턴트야.
                지원 회사는 '{selected_group}' 그룹의 '{selected_company}'이고,
                답변해야 할 자기소개서 문항은 다음과 같아: "{question}"

                지원자가 어필하고 싶은 경험은 다음과 같아:
                1. {exp1}
                2. {exp2}
                3. {exp3}

                이 경험들을 바탕으로 문항의 의도에 딱 맞는 500자 내외의 자기소개서를 완성해 줘.
                다음 규칙을 지켜줘:
                - 매력적인 소제목을 맨 위에 적을 것.
                - STAR(상황-과제-행동-결과) 기법을 활용하여 논리적으로 작성할 것.
                - 지원자의 경험이 잘 녹아들고, 자신감 있으면서도 겸손한 어조를 사용할 것.
                """

                # AI에게 글쓰기 요청
                response = model.generate_content(prompt)

                # 결과 출력
                st.success("자기소개서 초안 생성이 완료되었습니다!")
                st.write("---")
                st.write(response.text)
                st.write("---")
                st.caption("💡 팁: AI가 작성한 초안을 바탕으로 본인만의 말투로 조금만 다듬어 보세요!")

            except Exception as e:
                st.error(f"오류가 발생했습니다. API 키가 정확한지 확인해 주세요.\n\n오류 내용: {e}")