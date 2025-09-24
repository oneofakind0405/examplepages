import streamlit as st
import random

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Word Scramble",
    page_icon="🎯",
    layout="centered"
)

# --- CSS 스타일 ---
# 픽셀 아트 스타일의 폰트와 디자인을 위한 CSS
def local_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
            
            html, body, [class*="st-"] {
                font-family: 'Press Start 2P', cursive;
                background-color: #f0f2f6; /* 파스텔톤 배경 */
            }
            
            .st-emotion-cache-1y4p8pa { /* Streamlit 메인 컨테이너 */
                max-width: 600px;
                padding: 2rem;
            }

            h1 {
                font-size: 2.5rem;
                color: #ff69b4; /* 핫핑크 */
                text-align: center;
                text-shadow: 3px 3px 0px #404040;
            }
            
            .stMetric {
                background-color: #ffffff;
                border: 4px solid #404040;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                box-shadow: 5px 5px 0px #404040;
            }
            
            .stMetric .st-emotion-cache-1g8m52r { /* 메트릭 라벨 */
                font-size: 1rem;
                color: #404040;
            }
            
            .stMetric .st-emotion-cache-1g8m52r + div { /* 메트릭 값 */
                 font-size: 2rem;
                 color: #32cd32; /* 라임 그린 */
            }

            .card {
                background-color: #add8e6; /* 라이트 블루 */
                border: 4px solid #404040;
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin: 2rem 0;
                box-shadow: 5px 5px 0px #404040;
            }
            
            .scrambled-word {
                font-size: 2.5rem;
                letter-spacing: 0.5rem;
                color: #ffffff;
                text-shadow: 2px 2px 0px #404040;
            }

            .stButton>button {
                width: 100%;
                font-family: 'Press Start 2P', cursive;
                color: #404040;
                background-color: #ffd700; /* 골드 */
                border: 3px solid #404040;
                border-radius: 8px;
                padding: 10px 0;
                font-size: 1rem;
                transition: all 0.1s ease-in-out;
            }
            
            .stButton>button:hover {
                background-color: #ffc700;
                box-shadow: 3px 3px 0px #404040;
                transform: translateY(-2px);
            }
            
            .stButton>button:active {
                box-shadow: 0px 0px 0px #404040;
                transform: translateY(2px);
            }
            
            .stTextInput input {
                 font-family: 'Press Start 2P', cursive;
                 text-align: center;
                 font-size: 1.5rem;
            }
            
            .hint-box {
                font-size: 1.2rem;
                color: #ff4500; /* 오렌지 레드 */
                text-align: center;
                margin-top: 1rem;
            }

        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 단어 리스트 ---
WORD_LIST = ["orange", "computer", "friend", "study", "happy", "beautiful", "language", "community", "python", "streamlit"]

# --- 세션 상태 초기화 ---
if 'initialized' not in st.session_state:
    st.session_state.word_list = WORD_LIST
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.hint_shown = False
    st.session_state.current_word = ""
    st.session_state.scrambled_word = ""
    st.session_state.user_input = ""
    st.session_state.message = ""
    st.session_state.initialized = True

# --- 핵심 함수 ---
def setup_new_word():
    """새로운 단어를 선택하고 섞어서 세션 상태를 업데이트합니다."""
    # 이미 푼 단어는 리스트에서 제외 (선택 사항)
    if not st.session_state.word_list:
        st.session_state.word_list = WORD_LIST # 모든 단어를 다 풀면 리스트 리셋
    
    word = random.choice(st.session_state.word_list)
    st.session_state.current_word = word
    # st.session_state.word_list.remove(word) # 중복 방지
    
    # 단어 섞기 (원래 단어와 같지 않도록 보장)
    scrambled = list(word)
    while "".join(scrambled) == word:
        random.shuffle(scrambled)
    
    st.session_state.scrambled_word = "".join(scrambled)
    st.session_state.hint_shown = False
    st.session_state.message = ""
    st.session_state.user_input = "" # 입력 필드 초기화


# --- 앱 시작 시 첫 단어 설정 ---
if not st.session_state.current_word:
    setup_new_word()

# --- UI 렌더링 ---
st.title("🎯 Word Scramble")

# 점수판
col1, col2 = st.columns(2)
with col1:
    st.metric(label="✅ Correct", value=f"{st.session_state.score}")
with col2:
    st.metric(label="🔄 Attempts", value=f"{st.session_state.attempts}")

st.markdown("---")

# 문제 카드
st.markdown(f'<div class="card"><p class="scrambled-word">{st.session_state.scrambled_word.upper()}</p></div>', unsafe_allow_html=True)

# 힌트 표시
if st.session_state.hint_shown:
    first_letter = st.session_state.current_word[0]
    st.markdown(f'<p class="hint-box">💡 Hint: The word starts with " {first_letter.upper()} "</p>', unsafe_allow_html=True)


# 사용자 입력
user_input = st.text_input(
    "Enter your guess:", 
    key="input_field", 
    placeholder="Type here...", 
    label_visibility="collapsed"
).lower()


# 버튼 레이아웃
col1, col2, col3 = st.columns([1, 0.3, 1])

with col1:
    if st.button("✔️ Grade"):
        st.session_state.attempts += 1
        if user_input == st.session_state.current_word:
            st.session_state.score += 1
            st.session_state.message = "🎉 Well done!"
            st.balloons()
            # 정답을 맞추면 자동으로 다음 문제로 넘어가지 않고, "Next" 버튼을 누르도록 유도
        else:
            st.session_state.message = "😅 Oops, try again!"

with col3:
    if st.button("⏩ Next Question"):
        setup_new_word()
        st.rerun() # UI 즉시 새로고침

# 채점 메시지 표시
if st.session_state.message:
    if "Well done" in st.session_state.message:
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)

# 힌트 보기 버튼 (가운데 정렬을 위한 추가 열)
st.markdown("<br>", unsafe_allow_html=True) # 간격 조절
_, mid_col, _ = st.columns([1, 1.3, 1])
with mid_col:
    if st.button("💡 Show Hint", disabled=st.session_state.hint_shown):
        st.session_state.hint_shown = True
        st.rerun()
