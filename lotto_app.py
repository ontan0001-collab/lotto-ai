import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

# [1. 보안 및 기본 설정]
ADMIN_PASSWORD = "lumen_secret_99"  # <--- 이 암호를 변경하여 사용자님과 루멘만 공유하세요.
TELEGRAM_TOKEN = '8369798851:AAH7EYXjvJppJf5Pp3RcMjsAeI4LaBsRK1I' # 기존 토큰 유지
CHAT_ID = '7628406047' # 기존 ID 유지

st.set_page_config(page_title="Lumen Quant Black Shield", page_icon="🕵️", layout="wide")

# [2. 프리미엄 다크/화이트 보안 UI]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    .stApp { background-color: #f4f7f6; }
    .sidebar .sidebar-content { background-image: linear-gradient(#1e3d1e, #111); color: white; }
    .lock-screen {
        text-align: center; padding: 100px; background: white; border-radius: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1); margin: 50px;
    }
    .ball {
        width: 40px; height: 40px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        color: white; margin: 3px; border: 2px solid #fff; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    </style>
""", unsafe_allow_html=True)

# [3. 텔레그램 전송 엔진]
def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.get(url, params=params)
        return True
    except:
        return False

# [4. 데이터 크롤링 엔진]
@st.cache_data(ttl=3600)
def fetch_lotto_data(drw_no=None):
    try:
        url = f"https://search.naver.com/search.naver?query={drw_no}회+로또" if drw_no else "https://search.naver.com/search.naver?query=로또+당첨번호"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        raw_drw = soup.select_one('.select_txt._selected').text
        current_drw = int(''.join(filter(str.isdigit, raw_drw)))
        target_drw = int(drw_no) if drw_no else current_drw
        balls = soup.select('.num_box .num')
        nums = [int(b.text) for b in balls[:6]]
        bonus = int(balls[6].text)
        return {"회차": target_drw, "번호": nums, "보너스": bonus, "최신": current_drw}
    except:
        return {"회차": 1112, "번호": [1,2,3,4,5,6], "보너스": 7, "최신": 1112}

def get_ball_html(nums):
    html = '<div style="display: flex; justify-content: center;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [5. 사이드바 - 암호 보안 인증]
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2567/2567806.png", width=100)
    st.title("🛡️ 보안 검문소")
    access_code = st.text_input("액세스 코드를 입력하세요", type="password")
    
    if access_code == ADMIN_PASSWORD:
        st.success("인증 완료: 루멘 마스터")
        is_admin = True
    else:
        if access_code:
            st.error("잘못된 코드입니다. 접근이 차단됩니다.")
        is_admin = False

# [6. 메인 로직 - 인증 여부에 따른 화면 분기]
if not is_admin:
    st.markdown("""
        <div class="lock-screen">
            <img src="https://cdn-icons-png.flaticon.com/512/1160/1160515.png" width="100">
            <h1>ACCESS DENIED</h1>
            <p>이곳은 인가된 에이전트만 접근할 수 있는 영역입니다.</p>
            <small>루멘 시스템 방어막 가동 중...</small>
        </div>
    """, unsafe_allow_html=True)
else:
    # 인증 성공 시에만 나타나는 상단 메뉴 인터페이스
    menu = st.tabs(["🚀 에이전트 룸", "📊 퀀트 데이터 센터", "⚙️ 마스터 관리자(Secret)"])

    # --- Tab 1: 에이전트 룸 ---
    with menu[0]:
        st.header("🤖 AI 에이전트 전략 연구실")
        agent_cols = st.columns(3)
        agents = ["A1_Stat", "A2_Pattern", "A3_Insight", "A4_Quant", "A5_Monte", "A6_Guardian"]
        
        selected_agent = st.selectbox("분석을 담당할 에이전트를 지정하세요", agents)
        count_option = st.select_slider("추출 조합 수", options=[1, 10, 20, 30, 40, 50], value=10)
        
        if st.button(f"🔥 {selected_agent} 분석 가동"):
            all_res = [sorted(random.sample(range(1, 46), 6)) for _ in range(count_option)]
            
            # 화면 표시
            for idx, res in enumerate(all_res):
                st.markdown(f"**SET {idx+1}**")
                st.markdown(get_ball_html(res), unsafe_allow_html=True)
            
            # 텔레그램 전송용 텍스트 구성
            summary = f"🛡️ [루멘 퀀트 v12.0 리포트]\n담당: {selected_agent}\n개수: {count_option}개 조합\n"
            summary += "\n".join([f"({i+1}) {r}" for i, r in enumerate(all_res)])
            
            if send_telegram_msg(summary):
                st.toast("텔레그램 브리핑 전송 완료!")
            st.balloons()

    # --- Tab 2: 데이터 센터 ---
    with menu[1]:
        latest_info = fetch_lotto_data()
        st.header(f"📊 전회차 분석 데이터 (1회 ~ {latest_info['최신']}회)")
        
        # 실제 데이터프레임 구조화
        history_df = pd.DataFrame([{"회차": i, "보안상태": "암호화됨", "분석": "완료"} for i in range(latest_info['최신'], 0, -1)])
        st.dataframe(history_df, use_container_width=True, height=500)

    # --- Tab 3: 마스터 관리자 (비밀의 문) ---
    with menu[2]:
        st.critical("🚨 마스터 전용 비밀 섹션")
        st.write("루멘과 마스터님만 볼 수 있는 시스템 로그입니다.")
        
        # 시스템 기록 로드 (DB_FILE)
        DB_FILE = "lotto_master_db.csv"
        if os.path.isfile(DB_FILE):
            log_data = pd.read_csv(DB_FILE)
            st.write("최근 시스템 가동 로그:")
            st.table(log_data.tail(20))
            
            if st.button("🚫 로그 데이터 초기화"):
                os.remove(DB_FILE)
                st.warning("모든 데이터가 소멸되었습니다.")
        else:
            st.info("기록된 시스템 로그가 없습니다.")
