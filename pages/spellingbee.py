import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="🐝 Mini Spelling Bee",
    page_icon="🐝",
    layout="centered"
)

# CSS 스타일 - 8비트/픽셀 느낌 + 꽃밭 배경
st.markdown("""
<style>
    /* 전체 배경 스타일 */
    .stApp {
        background: linear-gradient(45deg, #e3f2fd 0%, #f3e5f5 50%, #e8f5e8 100%);
        font-family: 'Courier New', monospace;
    }
    
    /* 꽃밭 배경 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, #ff69b4 4px, #ffb6c1 6px, transparent 8px),
            radial-gradient(circle at 80% 20%, #87ceeb 4px, #add8e6 6px, transparent 8px),
            radial-gradient(circle at 15% 80%, #98fb98 4px, #90ee90 6px, transparent 8px),
            radial-gradient(circle at 70% 70%, #dda0dd 4px, #e6e6fa 6px, transparent 8px),
            radial-gradient(circle at 45% 15%, #f0e68c 4px, #fff8dc 6px, transparent 8px),
            radial-gradient(circle at 60% 40%, #ffc0cb 3px, #ffe4e1 4px, transparent 5px),
            radial-gradient(circle at 25% 60%, #e0ffff 3px, #f0ffff 4px, transparent 5px),
            radial-gradient(circle at 85% 85%, #f5fffa 3px, #f0fff0 4px, transparent 5px),
            radial-gradient(circle at 35% 25%, #ffb347 2px, transparent 2px),
            radial-gradient(circle at 90% 50%, #ff6347 2px, transparent 2px),
            radial-gradient(circle at 10% 10%, #da70d6 2px, transparent 2px),
            radial-gradient(circle at 50% 90%, #40e0d0 2px, transparent 2px),
            radial-gradient(ellipse 8px 2px at 30% 85%, #32cd32, transparent),
            radial-gradient(ellipse 6px 2px at 75% 90%, #228b22, transparent),
            radial-gradient(ellipse 10px 2px at 55% 95%, #9acd32, transparent);
        background-size: 
            120px 120px, 150px 150px, 100px 100px, 180px 180px, 130px 130px,
            80px 80px, 90px 90px, 70px 70px,
            60px 60px, 65px 65px, 55px 55px, 75px 75px,
            200px 50px, 180px 45px, 220px 55px;
        z-index: -1;
        opacity: 0.3;
        animation: gentle-sway 20s ease-in-out infinite;
    }
    
    @keyframes gentle-sway {
        0%, 100% { transform: translateX(0px) translateY(0px); }
        25% { transform: translateX(2px) translateY(-1px); }
        50% { transform: translateX(-1px) translateY(1px); }
        75% { transform: translateX(1px) translateY(-2px); }
    }
    
    /* 8비트 스타일 컨테이너 */
    .pixel-container {
        background: white;
        border: 3px solid #333;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 6px 6px 0 rgba(0,0,0,0.2);
        border-radius: 0;
    }
    
    /* 점수 배지 */
    .score-badge {
        background: #4caf50;
        color: white;
        padding: 10px 15px;
        border: 3px solid #333;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* 단어 점 표시 */
    .word-dots {
        text-align: center;
        font-size: 3rem;
        color: #666;
        letter-spacing: 8px;
        margin: 20px 0;
        font-family: monospace;
    }
    
    /* 힌트 스타일 */
    .hint-box {
        background: #fff3cd;
        border: 3px solid #333;
        padding: 15px;
        margin: 10px 0;
        color: #856404;
        font-weight: bold;
        text-align: center;
    }
    
    /* 성공/실패 메시지 */
    .success-box {
        background: #c8e6c9;
        border: 3px solid #333;
        padding: 15px;
        margin: 10px 0;
        color: #2e7d32;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    
    .error-box {
        background: #ffcdd2;
        border: 3px solid #333;
        padding: 15px;
        margin: 10px 0;
        color: #c62828;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    
    /* 로그 스타일 */
    .log-item {
        display: flex;
        align-items: center;
        padding: 8px;
        border-bottom: 2px dotted #ccc;
        font-family: 'Courier New', monospace;
    }
    
    .log-item:last-child {
        border-bottom: none;
    }
    
    /* Streamlit 버튼 커스터마이징 */
    .stButton > button {
        background: #2196f3;
        color: white;
        border: 3px solid #333;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        padding: 10px 20px;
        border-radius: 0;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.2);
        transition: all 0.1s;
    }
    
    .stButton > button:hover {
        background: #1976d2;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 rgba(0,0,0,0.3);
    }
    
    /* 입력창 스타일 */
    .stTextInput > div > div > input {
        border: 3px solid #333;
        border-radius: 0;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: inset 0 0 0 2px #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# 단어 데이터
WORDS_DATA = {
    "achievement": "성취",
    "adventure": "모험", 
    "ancient": "고대의",
    "attitude": "태도",
    "celebrate": "축하하다",
    "community": "공동체",
    "curious": "호기심 많은",
    "dangerous": "위험한",
    "environment": "환경",
    "experience": "경험",
    "festival": "축제",
    "friendship": "우정",
    "impossible": "불가능한",
    "interesting": "흥미로운",
    "knowledge": "지식",
    "language": "언어",
    "memorable": "기억할 만한",
    "ordinary": "평범한",
    "responsible": "책임감 있는",
    "tradition": "전통"
}

# 세션 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'current_word' not in st.session_state:
    st.session_state.current_word = ''
if 'words_list' not in st.session_state:
    st.session_state.words_list = list(WORDS_DATA.keys())
    random.shuffle(st.session_state.words_list)
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'total_count' not in st.session_state:
    st.session_state.total_count = 0
if 'game_log' not in st.session_state:
    st.session_state.game_log = []
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def get_next_word():
    """새로운 단어 선택"""
    if not st.session_state.words_list:
        st.session_state.words_list = list(WORDS_DATA.keys())
        random.shuffle(st.session_state.words_list)
    
    st.session_state.current_word = st.session_state.words_list.pop()
    st.session_state.show_hint = False
    st.session_state.is_answered = False
    st.session_state.user_input = ''

def check_answer():
    """정답 확인"""
    user_answer = st.session_state.user_input.strip().lower()
    correct_answer = st.session_state.current_word.lower()
    
    if not user_answer:
        st.warning("단어를 입력해주세요!")
        return
    
    st.session_state.is_answered = True
    st.session_state.total_count += 1
    
    is_correct = user_answer == correct_answer
    
    if is_correct:
        st.session_state.correct_count += 1
    
    # 로그에 추가 (최근 3개만 유지)
    st.session_state.game_log.insert(0, {
        'word': st.session_state.current_word,
        'is_correct': is_correct
    })
    if len(st.session_state.game_log) > 3:
        st.session_state.game_log = st.session_state.game_log[:3]

# 메인 UI
st.markdown('<div class="pixel-container">', unsafe_allow_html=True)

# 헤더
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🐝 Mini Spelling Bee")
with col2:
    if st.session_state.game_started:
        st.markdown(f'<div class="score-badge">{st.session_state.correct_count}/{st.session_state.total_count}</div>', 
                   unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 게임 시작 전
if not st.session_state.game_started:
    st.markdown('<div class="pixel-container">', unsafe_allow_html=True)
    st.markdown("### 영어 철자 맞히기 게임! 🌻")
    st.write("단어의 철자를 정확히 입력해보세요!")
    
    if st.button("🐝 게임 시작", key="start_btn"):
        st.session_state.game_started = True
        get_next_word()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 게임 진행 중
else:
    # 게임 화면
    st.markdown('<div class="pixel-container">', unsafe_allow_html=True)
    
    # 단어 점 표시
    dots = '●' * len(st.session_state.current_word)
    st.markdown(f'<div class="word-dots">{dots}</div>', unsafe_allow_html=True)
    
    # 힌트 버튼
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💡 힌트 보기" if not st.session_state.show_hint else "🙈 힌트 숨기기"):
            st.session_state.show_hint = not st.session_state.show_hint
            st.rerun()
    
    # 힌트 표시
    if st.session_state.show_hint:
        hint_text = f"💡 {WORDS_DATA[st.session_state.current_word]}"
        st.markdown(f'<div class="hint-box">{hint_text}</div>', unsafe_allow_html=True)
    
    # 입력창
    if not st.session_state.is_answered:
        user_input = st.text_input("영어 단어를 입력하세요", 
                                 value=st.session_state.user_input,
                                 key="input_field",
                                 placeholder="여기에 입력...",
                                 on_change=lambda: setattr(st.session_state, 'user_input', st.session_state.input_field))
        
        # 채점 버튼
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📝 채점하기", key="check_btn"):
                check_answer()
                st.rerun()
    
    # 결과 표시
    if st.session_state.is_answered:
        user_answer = st.session_state.user_input.strip().lower()
        correct_answer = st.session_state.current_word.lower()
        
        if user_answer == correct_answer:
            st.markdown('<div class="success-box">🐝 정답입니다!</div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f'<div class="error-box">😅 틀렸습니다!<br>정답: <strong>{st.session_state.current_word}</strong></div>', 
                       unsafe_allow_html=True)
        
        # 다음 문제 버튼
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("➡️ 다음 문제", key="next_btn"):
                get_next_word()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 로그 섹션
    if st.session_state.game_log:
        st.markdown('<div class="pixel-container">', unsafe_allow_html=True)
        st.markdown("#### 📋 최근 결과")
        
        for log_item in st.session_state.game_log:
            icon = "🐝" if log_item['is_correct'] else "😅"
            st.markdown(f'<div class="log-item"><span style="margin-right: 10px; font-size: 1.2rem;">{icon}</span><span>{log_item["word"]}</span></div>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
