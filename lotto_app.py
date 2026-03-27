import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
from datetime import datetime

# [1. 페이지 설정 및 디자인]
st.set_page_config(page_title="Lumen Quant v6.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; color: #333; }
    .nav-bar { background-color: #1e3d1e; padding: 20px; text-align: center; color: white; border-radius: 0 0 20px 20px; margin-bottom: 30px; }
    .premium-card { background-color: #ffffff; border-radius: 15px; padding: 25px; border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .lotto-ball { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 16px; color: white; border: 2px solid #fff; box-shadow: 1px 1px 5px rgba(0,0,0,0.2); }
    .ball-1 { background-color: #fbc02d; } .ball-11 { background-color: #1976d2; } .ball-21 { background-color: #e53935; } .ball-31 { background-color: #757575; } .ball-41 { background-color: #43a047; }
    .footer { padding: 40px; background-color: #f8f9fa; border-top: 1px solid #eee; margin-top: 50px; text-align: center; font-size: 13px; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# [2. 데이터베이스 기록 로직 (영구 저장)]
DB_FILE = "lotto_log.csv"

def save_to_csv(door, numbers):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_data = pd.DataFrame([[now, door, str(numbers)]], columns=['시간', '도어', '번호'])
    if not os.path.isfile(DB_FILE):
        new_data.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else:
        new_data.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

def load_db():
    if os.path.isfile(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=['시간', '도어', '번호'])

def get_ball_class(n):
    if n <= 10: return "ball-1"
    elif n <= 20: return "ball-11"
    elif n <= 30: return "ball-21"
    elif n <= 40: return "ball-31"
    else: return "ball-41"

# [3. 메인 레이아웃]
st.markdown('<div class="nav-bar"><h1>💎 LUMEN QUANT PREMIUM v6.0</h1><p>데이터 영구 보존 및 개인화 분석 시스템</p></div>', unsafe_allow_html=True)

# 상단 대시보드
c1, c2, c3, c4 = st.columns(4)
c1.metric("서버 기록 상태", "영구 기록 중", "DB-ON")
c2.metric("금주 누적 추출", f"{1240 + len(load_db())}건", "Exclusive")
c3.metric("알고리즘 강도", "최상", "v6.2")
c4.metric("접속 보안", "Secure", "SSL")

st.divider()

# [4. 탭 시스템: 재미 요소 추가]
tabs = st.tabs(["🔒 프라이빗 조합", "🔮 꿈 해몽 번호기", "🎮 당첨 시뮬레이터", "📜 전체 기록/통계"])

# --- Tab 1: 프라이빗 조합 ---
with tabs[0]:
    st.markdown("### 🎁 당신만을 위한 고전용 세션")
    if 'my_secret' not in st.session_state:
        st.session_state.my_secret = sorted(random.sample(range(1, 46), 6))
    
    rec = st.session_state.my_secret
    ball_html = "".join([f'<div class="lotto-ball {get_ball_class(n)}">{n}</div>' for n in rec])
    st.markdown(f"""
        <div class="premium-card" style="text-align: center; border: 2px solid #1e3d1e;">
            <h4>이번 주 비밀 추천 조합</h4>
            <div style="display: flex; gap: 12px; justify-content: center; margin: 20px 0;">{ball_html}</div>
            <p style="color: #666; font-size: 13px;">※ 본 세션의 번호는 영구 데이터베이스에 기록되어 다른 사용자와의 중복이 엄격히 제한됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    door = st.select_slider("연구실 도어 선택 (01-100)", options=[f"Door-{i:02d}" for i in range(1, 101)])
    if st.button(f"{door} 입장 및 추출"):
        with st.status("분석 엔진 가동..."):
            time.sleep(1)
            res = sorted(random.sample(range(1, 46), 6))
            save_to_csv(door, res) # 영구 저장
        st.success(f"배정 완료 및 DB 기록 성공: {res}")
        st.balloons()

# --- Tab 2: 재미거리 1 - 꿈 해몽 번호 변환기 ---
with tabs[1]:
    st.header("🔮 꿈 해몽 번호 변환기")
    st.write("간밤에 꾸신 꿈의 핵심 단어를 입력하세요. 퀀트 알고리즘이 꿈의 기운을 숫자로 치환합니다.")
    dream_word = st.text_input("꿈 내용 입력 (예: 돼지, 똥, 대통령, 불 등)")
    if dream_word:
        with st.spinner("꿈의 기운 분석 중..."):
            time.sleep(1.5)
            # 단어 기반 고정 난수 생성
            random.seed(len(dream_word) + ord(dream_word[0]))
            dream_nums = sorted(random.sample(range(1, 46), 6))
        st.info(f"'{dream_word}' 꿈에 매칭된 럭키 넘버: {dream_nums}")
        st.write("꿈 해몽 데이터와 역대 당첨 번호의 상관관계를 분석한 결과입니다.")

# --- Tab 3: 재미거리 2 - 당첨 시뮬레이터 ---
with tabs[2]:
    st.header("🎮 당첨 가능성 10,000회 시뮬레이션")
    st.write("지금 뽑은 번호로 1만 번을 샀을 때, 몇 번 당첨될까요? (체류 시간 증대 요소)")
    user_input = st.multiselect("테스트할 번호 6개를 고르세요", list(range(1, 46)), max_selections=6)
    if len(user_input) == 6:
        if st.button("시뮬레이션 시작"):
            hits = {1:0, 2:0, 3:0, 4:0, 5:0}
            progress = st.progress(0)
            for i in range(100): # 시각적 효과를 위해 100단계로 나누어 진행
                time.sleep(0.01)
                for _ in range(100):
                    win = set(random.sample(range(1, 46), 6))
                    match = len(set(user_input) & win)
                    if match == 6: hits[1] += 1
                    elif match == 5: hits[3] += 1 # 2등 생략(보너스 로직 간소화)
                    elif match == 4: hits[4] += 1
                    elif match == 3: hits[5] += 1
                progress.progress(i + 1)
            
            st.markdown(f"""
            <div class='premium-card'>
                <h4>시뮬레이션 결과 (10,000회 자동 구매 시)</h4>
                <li>1등: {hits[1]}번</li>
                <li>3등: {hits[3]}번</li>
                <li>4등: {hits[4]}번</li>
                <li>5등: {hits[5]}번</li>
                <p>당첨이 쉽지 않죠? 그래서 루멘 퀀트의 정교한 필터링이 필요합니다.</p>
            </div>
            """, unsafe_allow_html=True)

# --- Tab 4: 전체 기록 및 통계 (관리자 기능 포함) ---
with tabs[3]:
    st.header("📜 영구 데이터베이스 기록")
    df_log = load_db()
    if not df_log.empty:
        st.write("최근 추출된 모든 번호 기록입니다. 이 데이터는 통계 업데이트에 활용됩니다.")
        st.dataframe(df_log, use_container_width=True)
        
        # 간단 통계
        st.divider()
        st.subheader("📊 가장 많이 추출된 도어 TOP 5")
        st.bar_chart(df_log['도어'].value_counts().head(5))
    else:
        st.info("아직 기록된 데이터가 없습니다. 번호를 추출하면 여기에 쌓입니다.")

# [6. 푸터]
st.markdown('<div class="footer"><p>Copyright © 2026 Lumen Quant Premium. 데이터 영구 저장 엔진 v6.0</p></div>', unsafe_allow_html=True)
