import streamlit as st
import random

# spellingbee.py - Mini Spelling Bee Game
# Streamlit 멀티페이지 앱용 페이지

# 페이지 설정
st.set_page_config(
    page_title="🐝 Mini Spelling Bee",
    page_icon="🐝",
    layout="centered"
)

# CSS 스타일 - 심플 + 꽃밭 배경
st.markdown("""
<style>
    /* 전체 배경을 꽃밭으로 */
    .stApp {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 50%, #fff0f5 100%);
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    
    /* 꽃밭 배경 패턴 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            /* 큰 꽃들 */
            radial-gradient(circle at 20% 30%, #ff69b4 4px, #ffb6c1 6px, transparent 8px),
            radial-gradient(circle at 80% 20%, #87ceeb 4px, #add8e6 6px, transparent 8px),
            radial-gradient(circle at 15% 80%, #98fb98 4px, #90ee90 6px, transparent 8px),
            radial-gradient(circle at 70% 70%, #dda0dd 4px, #e6e6fa 6px, transparent 8px),
            radial-gradient(circle at 45% 15%, #f0e68c 4px, #fff8dc 6px, transparent 8px),
            /* 중간 꽃들 */
            radial-gradient(circle at 60% 40%, #ffc0cb 3px, #ffe4e1 4px, transparent 5px),
            radial-gradient(circle at 25% 60%, #e0ffff 3px, #f0ffff 4px, transparent 5px),
            radial-gradient(circle at 85% 85%, #f5fffa 3px, #f0fff0 4px, transparent 5px),
            /* 작은 꽃들 */
            radial-gradient(circle at 35% 25%, #ffb347 2px, transparent 2px),
            radial-gradient(circle at 90% 50%, #ff6347 2px, transparent 2px),
            radial-gradient(circle at 10% 10%, #da70d6 2px, transparent 2px),
            radial-gradient(circle at 50% 90%, #40e0d0 2px, transparent 2px),
            /* 잔디/잎 효과 */
            radial-gradient(ellipse 8px 2px at 30% 85%, #32cd32, transparent),
            radial-gradient(ellipse 6px 2px at 75% 90%, #228b22, transparent),
            radial-gradient(ellipse 10px 2px at 55% 95%, #9acd32, transparent);
        background-size: 
            120px 120px, 150px 150px, 100px 100px, 180px 180px, 130px 130px,
            80px 80px, 90px 90px, 70px 70px,
            60px 60px, 65px 65px, 55px 55px, 75px 75px,
            200px 50px, 180px 45px, 220px 55px;
        z-index: 0;
        opacity: 0.4;
        animation: gentle-sway 20s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes gentle-sway {
        0%, 100% { transform: translateX(0px) translateY(0px); }
        25% { transform: translateX(2px) translateY(-1px); }
        50% { transform: translateX(-1px) translateY(1px); }
        75% { transform: translateX(1px) translateY(-2px); }
    }
    
    /* 모든 Streamlit 컨테이너 숨기기 */
    .block-container {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 3rem 1rem 1rem 1rem !important;
        max-width: 600px !important;
    }
    
    /* 헤더 영역 숨기기 */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 사이드바 숨기기 (이 페이지에서만) */
    .css-1d391kg {
        display: none !important;
    }
    
    /* 제목 스타일 */
    .main-title {
        text-align: center;
        font-size: 3rem;
        color: #ff69b4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        z-index: 10;
        position: relative;
        background: rgba(255,255,255,0.8);
        border-radius: 20px;
        padding: 20px;
        border: 3px dotted #ff69b4;
    }
    
    /* 점수 스타일 */
    .score-display {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #4caf50;
        background: rgba(255,255,255,0.9);
        padding: 10px;
        border-radius: 15px;
        border: 2px dotted #4caf50;
        margin-bottom: 20px;
    }
    
    /* 문제 영역 */
    .problem-area {
        background: rgba(255,255,255,0.95);
        padding: 30px;
        border-radius: 25px;
        border: 3px dotted #dda0dd;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* 단어 힌트 스타일 */
    .word-hint {
        font-size: 2.5rem;
        color: #8b4513;
        font-weight: bold;
        margin: 20px 0;
        letter-spacing: 3px;
    }
    
    /* 뜻 표시 */
    .meaning-text {
        font-size: 1.5rem;
        color: #666;
        margin: 15px 0;
        font-style: italic;
    }
    
    /* 추가 힌트 */
    .extra-hint {
        background: rgba(255, 243, 205, 0.9);
        padding: 15px;
        border-radius: 15px;
        border: 2px dotted #ff9800;
        margin: 15px 0;
        color: #856404;
        font-weight: bold;
    }
    
    /* 성공 메시지 */
    .success-msg {
        background: rgba(200, 230, 201, 0.95);
        padding: 20px;
        border-radius: 20px;
        border: 3px dotted #4caf50;
        color: #2e7d32;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        animation: bounce 0.6s ease-in-out;
    }
    
    /* 실패 메시지 */
    .error-msg {
        background: rgba(255, 205, 210, 0.95);
        padding: 20px;
        border-radius: 20px;
        border: 3px dotted #f44336;
        color: #c62828;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    
    /* 로그 영역 */
    .log-area {
        background: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 20px;
        border: 2px dotted #ccc;
        margin-top: 20px;
    }
    
    .log-item {
        display: flex;
        align-items: center;
        padding: 8px;
        border-bottom: 1px dotted #ddd;
        font-size: 1.1rem;
    }
    
    .log-item:last-child {
        border-bottom: none;
    }
    
    /* 바운스 애니메이션 */
    @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        80% { transform: translateY(-5px); }
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        background: linear-gradient(45deg, #ff69b4, #ffb6c1) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 30px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4) !important;
    }
    
    /* 텍스트 입력 스타일 */
    .stTextInput > div > div > input {
        text-align: center !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        border: 3px solid #ff69b4 !important;
        background: rgba(255,255,255,0.95) !important;
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
if 'show_extra_hint' not in st.session_state:
    st.session_state.show_extra_hint = False
if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False

def get_next_word():
    """새로운 단어 선택"""
    if not st.session_state.words_list:
        st.session_state.words_list = list(WORDS_DATA.keys())
        random.shuffle(st.session_state.words_list)
    
    st.session_state.current_word = st.session_state.words_list.pop()
    st.session_state.show_extra_hint = False
    st.session_state.is_answered = False

def get_word_hint(word):
    """첫 글자 + 빈칸 형태로 힌트 생성"""
    if len(word) <= 2:
        return word[0] + "_" * (len(word) - 1)
    else:
        return word[0] + "_" * (len(word) - 2) + "_"

def get_extra_hint(word):
    """추가 힌트 - 마지막 글자도 공개"""
    if len(word) <= 2:
        return word
    else:
        return word[0] + "_" * (len(word) - 2) + word[-1]

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
    
    # 로그에 추가 (최근 5개만 유지)
    st.session_state.game_log.insert(0, {
        'word': st.session_state.current_word,
        'is_correct': is_correct
    })
    if len(st.session_state.game_log) > 5:
        st.session_state.game_log = st.session_state.game_log[:5]

# 메인 UI
st.markdown('<div class="main-title">🐝 Mini Spelling Bee</div>', unsafe_allow_html=True)

# 게임 시작 전
if not st.session_state.game_started:
    st.markdown('<div class="problem-area">', unsafe_allow_html=True)
    st.markdown("### 영어 철자 맞히기 게임! 🌻")
    st.write("첫 글자와 뜻을 보고 단어를 맞춰보세요!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🐝 게임 시작", key="start_btn"):
        st.session_state.game_started = True
        get_next_word()
        st.rerun()

# 게임 진행 중
else:
    # 점수 표시
    if st.session_state.total_count > 0:
        accuracy = int((st.session_state.correct_count / st.session_state.total_count) * 100)
        st.markdown(f'<div class="score-display">점수: {st.session_state.correct_count}/{st.session_state.total_count} ({accuracy}%)</div>', 
                   unsafe_allow_html=True)
    
    # 문제 영역
    st.markdown('<div class="problem-area">', unsafe_allow_html=True)
    
    # 단어 힌트 (첫 글자 + 언더바)
    word_hint = get_word_hint(st.session_state.current_word)
    st.markdown(f'<div class="word-hint">{word_hint}</div>', unsafe_allow_html=True)
    
    # 뜻 표시
    meaning = WORDS_DATA[st.session_state.current_word]
    st.markdown(f'<div class="meaning-text">뜻: {meaning}</div>', unsafe_allow_html=True)
    
    # 추가 힌트 버튼 & 표시
    if not st.session_state.is_answered:
        if st.button("💡 추가 힌트 (마지막 글자)", key="hint_btn"):
            st.session_state.show_extra_hint = True
            st.rerun()
        
        if st.session_state.show_extra_hint:
            extra_hint = get_extra_hint(st.session_state.current_word)
            st.markdown(f'<div class="extra-hint">추가 힌트: {extra_hint}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 입력 & 결과
    if not st.session_state.is_answered:
        user_input = st.text_input("영어 단어를 입력하세요", 
                                 key="user_input",
                                 placeholder="여기에 입력...")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📝 정답 확인", key="check_btn"):
                check_answer()
                st.rerun()
    
    # 결과 표시
    if st.session_state.is_answered:
        user_answer = st.session_state.user_input.strip().lower()
        correct_answer = st.session_state.current_word.lower()
        
        if user_answer == correct_answer:
            st.markdown('<div class="success-msg">🐝 정답입니다!</div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f'<div class="error-msg">😅 틀렸습니다!<br>정답: <strong>{st.session_state.current_word}</strong></div>', 
                       unsafe_allow_html=True)
        
        # 다음 문제 버튼
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("➡️ 다음 문제", key="next_btn"):
                get_next_word()
                st.rerun()
    
    # 게임 로그
    if st.session_state.game_log:
        st.markdown('<div class="log-area">', unsafe_allow_html=True)
        st.markdown("#### 📋 최근 결과")
        
        for log_item in st.session_state.game_log:
            icon = "🐝" if log_item['is_correct'] else "😅"
            st.markdown(f'<div class="log-item"><span style="margin-right: 10px; font-size: 1.3rem;">{icon}</span><span>{log_item["word"]}</span></div>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
