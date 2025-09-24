import streamlit as st
import random

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Word Scramble",
    page_icon="🎯",
    layout="centered"
)

# --- CSS 스타일 ---
# 전체적인 크기와 폰트 통일을 위해 CSS 수정
def local_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
            
            /* 전체 폰트 적용 */
            html, body, [class*="st-"], .st-emotion-cache-1g8m52r, .st-emotion-cache-de1xpr {
                font-family: 'Press Start 2P', cursive;
            }
            
            /* 기본 배경색 */
            body {
                background-color: #f0f2f6;
            }

            /* 제목 스타일 (크기 축소) */
            h1 {
                font-size: 2.2rem;
                color: #ff69b4;
                text-align: center;
                text-shadow: 2px 2px 0px #404040;
            }
            
            /* 점수판 (메트릭) 스타일 */
            .stMetric {
                background-color: #ffffff;
                border: 3px solid #404040;
                border-radius: 10px;
                padding: 10px;
                text-align: center;
                box-shadow: 4px 4px 0px #404040;
            }
            
            /* 점수판 라벨 (크기 조절) */
            .stMetric .st-emotion-cache-1g8m52r {
                font-size: 0.8rem;
                color: #404040;
            }
            
            /* 점수판 값 (크기 조절) */
            .stMetric .st-emotion-cache-de1xpr {
                 font-size: 1.5rem;
                 color: #32cd32;
            }

            /* 단어 카드 스타일 */
            .card {
                background-color: #add8e6;
                border: 3px solid #404040;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                margin: 1.5rem 0;
                box-shadow: 4px 4px 0px #404040;
            }
            
            /* 섞인 단어 (크기 축소) */
            .scrambled-word {
                font-size: 2.0rem;
                letter-spacing: 0.4rem;
                color: #ffffff;
                text-shadow: 2px 2px 0px #404040;
                word-break: break-all; /* 긴 단어가 화면을 벗어나지 않도록 줄바꿈 */
            }

            /* 버튼 스타일 (폰트 적용) */
            .stButton>button {
                font-family: 'Press Start 2P', cursive;
                color: #404040;
                background-color: #ffd700;
                border: 2px solid #404040;
                border-radius: 8px;
                transition: all 0.1s ease-in-out;
            }
            
            /* 입력창 스타일 (폰트 적용) */
            .stTextInput input {
                 font-family: 'Press Start 2P', cursive;
                 text-align: center;
                 font-size: 1.2rem;
            }
            
            /* 힌트 박스 스타일 */
            .hint-box {
                font-size: 0.8rem; /* 힌트 글씨 크기 조절 */
                color: #ff4500;
                text-align: center;
                margin-top: 1rem;
                padding: 1rem;
                background-color: #fffacd;
                border: 2px dashed #ff4500;
                border-radius: 10px;
            }
            
            /* 알림 메시지 폰트 적용 */
            .stAlert {
                font-family: 'Press Start 2P', cursive;
                font-size: 0.8rem;
            }

        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 단어 리스트 및 뜻 (Dictionary 형태로 변경) ---
WORD_DEFINITIONS = {
    "orange": "A round sweet fruit that is a color between red and yellow.",
    "computer": "An electronic device for storing and processing data.",
    "friend": "A person who you know well and who you like a lot.",
    "study": "To spend time learning about a subject.",
    "happy": "Feeling, showing, or causing pleasure or satisfaction.",
    "beautiful": "Pleasing the senses or mind aesthetically.",
    "language": "The method of human communication, either spoken or written.",
    "community": "A group of people living in the same place or having a particular characteristic in common."
}

# --- 세션 상태 초기화 ---
if 'word_scramble_initialized' not in st.session_state:
    st.session_state.word_scramble_initialized = True
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.hint_shown = False
    st.session_state.current_word = ""
    st.session_state.current_definition = ""
    st.session_state.scrambled_word = ""
    st.session_state.message = None # 메시지 상태 추가

# --- 핵심 함수 ---
def setup_new_word():
    """새로운 단어와 뜻을 선택하고 섞어서 세션 상태를 업데이트합니다."""
    word, definition = random.choice(list(WORD_DEFINITIONS.items()))
    
    st.session_state.current_word = word
    st.session_state.current_definition = definition
    
    scrambled = list(word)
    while "".join(scrambled) == word:
        random.shuffle(scrambled)
    
    st.session_state.scrambled_word = "".join(scrambled)
    st.session_state.hint_shown = False
    st.session_state.message = None # 메시지 초기화
    st.session_state.user_input = "" # 입력 필드 초기화를 위해 키 값 변경 유도

# --- 앱 시작 시 첫 단어 설정 ---
if not st.session_state.current_word:
    setup_new_word()

# --- UI 렌더링 ---
st.title("🎯 Word Scramble")

# 점수판
col1, col2 = st.columns(2)
col1.metric("✅ Correct", f"{st.session_state.score}")
col2.metric("🔄 Attempts", f"{st.session_state.attempts}")

st.markdown("---")

# 문제 카드
st.markdown(f'<div class="card"><p class="scrambled-word">{st.session_state.scrambled_word.upper()}</p></div>', unsafe_allow_html=True)

# 사용자 입력
user_input = st.text_input(
    "Enter your guess:",
    key=f"input_{st.session_state.scrambled_word}", # 다음 문제로 넘어갈 때 입력창 초기화
    placeholder="Type here...",
    label_visibility="collapsed"
).lower().strip()

# 알림 메시지 표시 (버튼보다 위에 위치)
# st.empty()를 사용해 메시지 표시 영역을 미리 확보
message_placeholder = st.empty()
if st.session_state.message:
    if st.session_state.message['type'] == 'success':
        message_placeholder.success(st.session_state.message['text'])
    else:
        message_placeholder.error(st.session_state.message['text'])

# 버튼 레이아웃
col1, col2 = st.columns(2)

with col1:
    if st.button("✔️ Grade", use_container_width=True):
        if user_input: # 입력값이 있을 때만 채점
            st.session_state.attempts += 1
            if user_input == st.session_state.current_word:
                st.session_state.score += 1
                # 메시지를 session_state에 저장
                st.session_state.message = {'type': 'success', 'text': '🎉 Well done!'}
                st.balloons()
            else:
                st.session_state.message = {'type': 'error', 'text': '😅 Oops, try again!'}
            # 페이지를 다시 실행하여 메시지를 즉시 표시
            st.rerun()

with col2:
    if st.button("⏩ Next Question", use_container_width=True):
        setup_new_word()
        st.rerun()

# 힌트 보기 버튼
if st.button("💡 Show Hint", use_container_width=True):
    st.session_state.hint_shown = True
    # 힌트를 누르면 메시지는 사라지도록 함
    st.session_state.message = None
    st.rerun()

# 힌트 표시
if st.session_state.hint_shown:
    first_letter = st.session_state.current_word[0].upper()
    definition = st.session_state.current_definition
    st.markdown(
        f'<div class="hint-box">'
        f'<p><b>First letter:</b> "{first_letter}"</p>'
        f'<p><b>Meaning:</b> {definition}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
