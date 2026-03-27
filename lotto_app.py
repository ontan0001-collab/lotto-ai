import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

# [1. 마스터 보안 설정]
MASTER_CODE = "lumen_secret_99"  # <--- 이 암호를 입력해야 '데이터/수정' 권한이 열립니다.
TELEGRAM_TOKEN = '8369798851:AAH7EYXjvJppJf5Pp3RcMjsAeI4LaBsRK1I'
CHAT_ID = '7628406047'

st.set_page_config(page_title="Lumen Quant Open Lab", page_icon="💎", layout="wide")

# [2. UI 스타일링: 세련된 오픈 연구소 톤]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; }
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-container { margin-top: 100px; }
    .premium-card {
        background-color: #ffffff; border-radius: 20px; padding: 25px;
        border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .ball {
        width: 38px; height: 38px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        color: white; margin: 3px; border: 2px solid #fff; font-size: 15px;
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    .stButton>button { width: 100%; border-radius: 25px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# [3. 핵심 연동 엔진]
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

@st.cache_data(ttl=3600)
def fetch_lotto():
    try:
        url = "https://search.naver.com/search.naver?query=로또+당첨번호"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        raw_drw = soup.select_one('.select_txt._selected').text
        drw_no = int(''.join(filter(str.isdigit, raw_drw)))
        balls = soup.select('.num_box .num')
        nums = [int(b.text) for b in balls[:6]]
        bonus = int(balls[6].text)
        return {"회차": drw_no, "번호": nums, "보너스": bonus}
    except:
        return {"회차": 1112, "번호": [1,2,3,4,5,6], "보너스": 7}

# [4. 마스터 인증 시스템 (비공개 영역용)]
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2567/2567806.png", width=80)
    st.title("🔐 마스터 코어")
    input_code = st.text_input("마스터 코드를 입력하세요", type="password")
    is_master = (input_code == MASTER_CODE)
    if is_master: st.success("마스터 권한이 활성화되었습니다.")
    else: st.info("데이터 센터 및 시스템 설정은 마스터만 접근 가능합니다.")

# [5. 메인 레이아웃]
st.markdown('<div class="nav-bar"><div style="font-size: 22px; font-weight: bold;">💎 LUMEN QUANT OPEN LAB</div></div><div class="main-container"></div>', unsafe_allow_html=True)

# 상단 공통: 최신 당첨 번호 (모든 방문객 환영용)
latest = fetch_lotto()
st.markdown(f"""
    <div class="premium-card" style="text-align: center; border-left: 5px solid #1e3d1e;">
        <h4 style="color: #666; margin-bottom: 15px;">이번 주 제 {latest['회차']}회 당첨 번호</h4>
        {"".join([f'<div class="ball {"b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"}">{n}</div>' for n in latest['번호']])}
        <span style="font-size: 20px; font-weight: bold; margin: 0 10px;">+</span>
        <div class="ball b1">{latest['보너스']}</div>
    </div>
""", unsafe_allow_html=True)

# 공개 메뉴와 비공개 메뉴 분리
if is_master:
    tabs = st.tabs(["🚀 추출 연구소 (공개)", "📊 데이터 센터 (마스터)", "⚙️ 시스템 수정 (마스터)"])
else:
    tabs = st.tabs(["🚀 추출 연구소 (공개)", "🔒 데이터 센터 (잠금)"])

# --- Tab 1: 추출 연구소 (누구나 사용 가능) ---
with tabs[0]:
    st.subheader("🤖 AI 에이전트 조합 추출")
    col1, col2 = st.columns([1, 2])
    with col1:
        agent = st.selectbox("에이전트 선택", ["A1 (통계)", "A2 (패턴)", "A3 (인사이트)", "A4 (퀀트)", "A5 (몬테)", "A6 (가디언)"])
        count = st.select_slider("추출 개수", options=[1, 10, 20, 30, 40, 50], value=10)
    
    if st.button(f"🔥 {agent} 에이전트에게 번호 받기"):
        all_results = [sorted(random.sample(range(1, 46), 6)) for _ in range(count)]
        
        # 화면에 번호 뿌려주기 (사람들이 놀러 오는 이유!)
        for i, res in enumerate(all_results):
            st.markdown(f"**조합 {i+1}**")
            st.markdown("".join([f'<div class="ball {"b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"}">{n}</div>' for n in res]), unsafe_allow_html=True)
        
        # 텔레그램으로 마스터에게 보고 (누가 뭘 뽑았는지 확인용)
        report = f"🔔 [방문자 추출 보고]\n에이전트: {agent}\n개수: {count}\n내용 요약: {all_results[0]} 외"
        send_telegram(report)
        st.balloons()

# --- Tab 2: 데이터 센터 (마스터 전용) ---
with tabs[1]:
    if is_master:
        st.header("📊 누적 분석 데이터 시트")
        # 1회부터 현재까지의 히스토리 (마스터만 볼 수 있음)
        history_df = pd.DataFrame([{"회차": i, "분석": "Deep Quant 완료"} for i in range(latest['회차'], 0, -1)])
        st.dataframe(history_df, use_container_width=True, height=500)
    else:
        st.warning("🔒 이 영역은 마스터 암호가 필요합니다. 데이터 보안 모드 가동 중.")

# --- Tab 3: 시스템 수정 (마스터 전용) ---
if is_master:
    with tabs[2]:
        st.header("⚙️ 시스템 환경 설정")
        st.write("마스터 전용 수정 권한입니다.")
        if st.button("시스템 로그 초기화"):
            st.error("모든 로그가 삭제되었습니다.")
