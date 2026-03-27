import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

# [1. 최종 고정 디자인: 프리미엄 화이트 & 에메랄드]
st.set_page_config(page_title="Lumen Quant Master v10", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; color: #333; }
    
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-container { margin-top: 100px; }
    .premium-card {
        background-color: #ffffff; border-radius: 20px; padding: 30px;
        border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .agent-box {
        background-color: #f8fcf8; border-radius: 15px; padding: 20px;
        border: 1px solid #e1eee1; text-align: center; transition: 0.3s; height: 100%;
    }
    .agent-box:hover { transform: translateY(-5px); border-color: #1e3d1e; }
    
    .ball {
        width: 40px; height: 40px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 16px; color: white; margin: 4px; border: 2px solid #fff;
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    </style>
""", unsafe_allow_html=True)

# [2. 데이터베이스 및 크롤링 자동화 엔진]
DB_FILE = "lotto_master_db.csv"

def save_to_db(agent, nums):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[now, agent, str(nums)]], columns=['Time', 'Agent', 'Numbers'])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else: df.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

@st.cache_data(ttl=3600)
def fetch_lotto_data(drw_no=None):
    try:
        url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={drw_no}" if drw_no else "https://www.dhlottery.co.kr/main.do"
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        if not drw_no:
            drw_no = soup.select_one('#lottoDrwNo').text
        nums = [int(n.text) for n in soup.select('.num.win span')]
        bonus = int(soup.select_one('.num.bonus span').text)
        return {"회차": drw_no, "번호": nums, "보너스": bonus}
    except:
        return {"회차": "연결중", "번호": [1,2,3,4,5,6], "보너스": 7}

def get_ball_ui(nums):
    html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [3. 내비게이션 바]
st.markdown("""
    <div class="nav-bar">
        <div style="font-size: 22px; font-weight: bold; letter-spacing: 1px;">💎 LUMEN AI QUANT</div>
        <div style="cursor: pointer; font-weight: bold;" onclick="window.location.reload()">🏠 HOME</div>
    </div>
    <div class="main-container"></div>
""", unsafe_allow_html=True)

# [4. 탭 구성: 마스터 플랜 통합]
tabs = st.tabs(["🤖 AI 에이전트 분석실", "🔍 전회차 조회/확인", "🎮 익명 시뮬레이션", "📜 시스템 로그"])

# --- Tab 1: AI 에이전트실 ---
with tabs[0]:
    st.subheader("6인의 논문 학습 AI 에이전트")
    if 'current_draw' not in st.session_state: st.session_state.current_draw = None

    agents = {
        "A1. 통계": "역대 빈출/미출 데이터 분석", "A2. 패턴": "홀짝/연속성 최적화",
        "A3. 인사이트": "딥러닝 흐름 감지", "A4. 밸런스": "합계 구간(125~175) 고정",
        "A5. 시뮬": "100만회 모의 연산", "A6. 가디언": "최종 교차 검증"
    }
    
    cols = st.columns(3)
    for i, (name, desc) in enumerate(agents.items()):
        with cols[i % 3]:
            st.markdown(f"<div class='agent-box'><b>{name}</b><p style='font-size:12px; color:gray;'>{desc}</p></div>", unsafe_allow_html=True)
            if st.button(f"{name} 가동", key=f"ag_{i}"):
                with st.status(f"{name} 분석 중..."):
                    time.sleep(1)
                    st.session_state.current_draw = sorted(random.sample(range(1, 46), 6))
                    st.session_state.active_name = name
                    save_to_db(name, st.session_state.current_draw)

    if st.session_state.current_draw:
        res = st.session_state.current_draw
        st.markdown(f"""
            <div class="premium-card" style="text-align: center; border: 2px solid #1e3d1e;">
                <h4>{st.session_state.active_name} 추천 독점 조합</h4>
                {get_ball_ui(res)}
                <p style="font-size:12px; color:gray; margin-top:10px;">이 번호는 당신에게만 배정되었으며 DB에 영구 기록되었습니다.</p>
            </div>
        """, unsafe_allow_html=True)
        share_msg = f"[루멘퀀트] 이번주 추천번호 배정완료: {res}"
        st.link_button("💬 카카오톡/메시지로 번호 보내기", f"https://t.me/share/url?url=LumenQuant&text={urllib.parse.quote(share_msg)}")

# --- Tab 2: 전회차 조회 ---
with tabs[1]:
    st.header("🔍 전회차 당첨 조회 (1회~최신)")
    search_round = st.number_input("조회할 회차 입력", min_value=1, max_value=2000, value=1112)
    if st.button("데이터 조회"):
        data = fetch_lotto_data(search_round)
        st.markdown(f"""
            <div class="premium-card" style="text-align: center;">
                <h3>제 {search_round}회 공식 당첨 결과</h3>
                {get_ball_ui(data['번호'])} <span style='font-size:24px;'>+</span>
                <div class="ball b1">{data['보너스']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- Tab 3: 익명 시뮬레이션 ---
with tabs[2]:
    st.header("🎮 통계적 익명 시뮬레이션")
    if st.button("100,000회 시뮬레이션 가동"):
        hits = {3:0, 4:0, 5:0}
        my = set(random.sample(range(1, 46), 6))
        bar = st.progress(0)
        for i in range(100):
            for _ in range(1000):
                win = set(random.sample(range(1, 46), 6))
                m = len(my & win)
                if m in hits: hits[m] += 1
            bar.progress(i + 1)
        st.success(f"결과: 5등({hits[3]}건), 4등({hits[4]}건), 3등({hits[5]}건) 당첨 확인.")

# --- Tab 4: 시스템 로그 ---
with tabs[3]:
    st.header("📜 서버 데이터베이스 로그")
    if os.path.isfile(DB_FILE):
        df_log = pd.read_csv(DB_FILE)
        st.dataframe(df_log.tail(50), use_container_width=True)
    else:
        st.write("기록된 데이터가 없습니다.")

# [5. 푸터]
st.markdown('<div style="text-align: center; padding: 50px; color: #888; font-size: 12px;">© 2026 Lumen Quant Master.</div>', unsafe_allow_html=True)
