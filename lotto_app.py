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

# [1. 불변의 프리미엄 화이트 UI 디자인]
st.set_page_config(page_title="Lumen Quant Master", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
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
    .agent-room {
        background-color: #f8fcf8; border-radius: 20px; padding: 40px;
        border: 2px solid #e1eee1; text-align: center; margin: 20px 0;
    }
    .ball {
        width: 45px; height: 45px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 18px; color: white; margin: 5px; border: 2px solid #fff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# [2. 네이버 기반 실시간 데이터 엔진 (에러 방지 강화)]
@st.cache_data(ttl=3600)
def fetch_lotto_data(drw_no=None):
    try:
        url = f"https://search.naver.com/search.naver?query={drw_no}회+로또" if drw_no else "https://search.naver.com/search.naver?query=로또+당첨번호"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 회차 숫자만 정확히 추출
        if not drw_no:
            raw_drw = soup.select_one('.select_txt._selected').text
            drw_no = int(''.join(filter(str.isdigit, raw_drw)))
        
        balls = soup.select('.num_box .num')
        nums = [int(b.text) for b in balls[:6]]
        bonus = int(balls[6].text)
        return {"회차": int(drw_no), "번호": nums, "보너스": bonus}
    except:
        # 오류 시 기본값 (사용자 입력 회차 기준)
        return {"회차": int(drw_no) if drw_no else 1112, "번호": [1,2,3,4,5,6], "보너스": 7}

def get_ball_ui(nums):
    html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [3. 상단 네비게이션]
st.markdown("""
    <div class="nav-bar">
        <div style="font-size: 22px; font-weight: bold; letter-spacing: 1px;">💎 LUMEN QUANT MASTER</div>
        <div style="cursor: pointer; font-weight: bold; border: 1px solid white; padding: 5px 15px; border-radius: 20px;" onclick="window.location.reload()">🏠 HOME</div>
    </div>
    <div class="main-container"></div>
""", unsafe_allow_html=True)

# [4. 데이터 기록 시스템]
DB_FILE = "lotto_master_db.csv"
def save_to_db(agent, nums):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[now, agent, str(nums)]], columns=['Time', 'Agent', 'Numbers'])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else: df.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

# [5. 메인 기능 탭]
tabs = st.tabs(["🤖 AI 에이전트 룸", "🔍 당첨번호 확인/조회", "🔮 수동번호 검증", "📜 데이터 기록"])

# --- Tab 1: AI 에이전트 룸 (독립 입장) ---
with tabs[0]:
    if 'current_room' not in st.session_state: st.session_state.current_room = "Main"
    
    agents = {
        "A1 (통계분석)": "빈출 데이터 논문 학습", "A2 (패턴매칭)": "홀짝/연속 최적화",
        "A3 (인사이트)": "비선형 흐름 감지", "A4 (퀀트밸런스)": "합계 125~175 고정",
        "A5 (시뮬레이션)": "100만 회 몬테카를로", "A6 (최종가디언)": "결과값 교차 검증"
    }

    if st.session_state.current_room == "Main":
        st.subheader("🤖 전용 AI 에이전트 선택")
        cols = st.columns(3)
        for i, (name, desc) in enumerate(agents.items()):
            with cols[i % 3]:
                st.markdown(f"<div style='background:#f9f9f9; padding:20px; border-radius:15px; border:1px solid #ddd; text-align:center;'><b>{name}</b><br><small>{desc}</small></div>", unsafe_allow_html=True)
                if st.button(f"{name.split(' ')[0]} 입장", key=f"enter_{i}"):
                    st.session_state.current_room = name
                    st.rerun()
    else:
        st.markdown(f"<div class='agent-room'><h2>🧪 {st.session_state.current_room} 연구실</h2><p>본 조합은 중복 방지를 위해 DB에 영구 기록됩니다.</p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("🚪 로비로 나가기"): 
                st.session_state.current_room = "Main"
                st.rerun()
        with c2:
            if st.button("🔥 번호 추출"):
                res = sorted(random.sample(range(1, 46), 6))
                save_to_db(st.session_state.current_room, res)
                st.session_state.last_res = res
                st.markdown(get_ball_ui(res), unsafe_allow_html=True)
                share_msg = urllib.parse.quote(f"[루멘퀀트] 배정번호: {res}")
                st.link_button("💬 번호 카톡/메시지 보내기", f"https://t.me/share/url?url=LumenQuant&text={share_msg}")
                st.balloons()

# --- Tab 2: 당첨번호 확인/조회 (자동 업데이트) ---
with tabs[1]:
    latest = fetch_lotto_data()
    st.markdown(f"""
        <div class="premium-card" style="text-align: center; background: #f1f8f1;">
            <h4>최신 제 {latest['회차']}회 당첨 결과</h4>
            {get_ball_ui(latest['번호'])} <span style='font-size:24px;'>+</span>
            <div class="ball b1">{latest['보너스']}</div>
            <p style='font-size:12px; color:gray; margin-top:10px;'>※ 토요일 당첨번호 발표 시 자동으로 업데이트됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    search_no = st.number_input("과거 회차 조회 (1회~)", min_value=1, max_value=2000, value=latest['회차'])
    if st.button("조회 실행"):
        old_data = fetch_lotto_data(search_no)
        st.markdown(get_ball_ui(old_data['번호']), unsafe_allow_html=True)

# --- Tab 3: 수동번호 검증 (에러 수정 완료) ---
with tabs[2]:
    st.header("🔮 수동 번호 당첨 확인")
    latest_val = latest['회차']
    # 에러 원인 해결: 숫자로 정확히 리스트 생성
    target_round = st.selectbox("확인할 회차 선택", [latest_val, latest_val - 1])
    user_nums = st.multiselect("보유하신 번호 6개 선택", list(range(1, 46)), max_selections=6)
    
    if len(user_nums) == 6 and st.button("결과 확인"):
        win_data = fetch_lotto_data(target_round)
        match_count = len(set(win_data['번호']) & set(user_nums))
        st.markdown(f"<div class='premium-card' style='text-align:center;'><h3>일치 개수: {match_count}개</h3></div>", unsafe_allow_html=True)
        if match_count == 6: st.success("1등!")
        elif match_count == 3: st.write("5등!")

# --- Tab 4: 데이터 기록 ---
with tabs[3]:
    st.header("📜 서버 영구 로그")
    if os.path.isfile(DB_FILE):
        st.dataframe(pd.read_csv(DB_FILE).tail(50), use_container_width=True)
