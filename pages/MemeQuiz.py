import streamlit as st

# 페이지 설정
st.set_page_config(page_title="😂 Meme English Quiz", page_icon="😂")

st.title("😂 Meme English Quiz")

# 퀴즈 데이터
quiz = [
    {
        "img": "https://i.imgflip.com/30b1gx.jpg",
        "sentence": "This is so _____!",
        "choices": ["funny", "sad", "boring"],
        "answer": "funny",
        "explanation": "This meme is supposed to be funny."
    },
    {
        "img": "https://i.imgflip.com/26am.jpg",
        "sentence": "I can't _____ this.",
        "choices": ["believe", "cook", "finish"],
        "answer": "believe",
        "explanation": "The common phrase is 'I can't believe this.'"
    },
    {
        "img": "https://i.imgflip.com/1bij.jpg",
        "sentence": "When homework is due, I feel _____.",
        "choices": ["excited", "tired", "invisible"],
        "answer": "tired",
        "explanation": "Homework often makes students feel tired."
    }
]

# 상태 초기화
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0

q = quiz[st.session_state.q_index]

# 문제 표시
st.image(q["img"], caption="Meme Quiz", use_column_width=True)
st.write(q["sentence"])

choice = st.radio("Choose the best answer:", q["choices"], index=None)

# 정답 확인
if st.button("Check Answer"):
    if choice == q["answer"]:
        st.success("🎉 Correct!")
        st.session_state.score += 1
    else:
        st.error("😅 Nope, try again!")
        st.info(f"Hint: {q['explanation']}")

# 다음 문제
if st.button("Next Question"):
    if st.session_state.q_index < len(quiz) - 1:
        st.session_state.q_index += 1
    else:
        st.write("✅ Quiz Finished!")
        st.write(f"Your score: {st.session_state.score}/{len(quiz)}")
        # 리셋
        if st.button("Restart"):
            st.session_state.q_index = 0
            st.session_state.score = 0
