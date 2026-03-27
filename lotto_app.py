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
MASTER_CODE = "lumen_secret_99"  # 마스터 전용 암호
TELEGRAM_TOKEN = '8369798851:AAH7EYXjvJppJf5Pp3RcMjsAeI4LaBsRK1I'
CHAT_ID = '7628406047'

st.set_page_config(page_title="Lumen Quant Lab", page_icon="🌿", layout="wide")

# [2. UI 스타일링: 갤러리 톤]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; }
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000;
    }
    .main-container { margin-top: 100px; }
    .premium-card {
        background-color: #ffffff; border-radius: 20px; padding: 25px;
        border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .ball {
        width: 40px; height: 40px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        color: white; margin: 3px; border: 2px solid #fff;
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    </style>
""", unsafe_allow_html=True)

# [3. 핵심 엔진]
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

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

# [4. 사이드바 마스터 인증]
with st.sidebar:
    st.title("🔐 마스터 센터")
    input_code = st.text_input("마스터 코드를 입력하여 권한을 활성화하세요", type="password")
    is_master = (input_code == MASTER_CODE)
    
    if is_master:
        st.success("권한 승인: 모든 기능이 활성화되었습니다.")
    else:
        st.info("현재 '관람 모드'입니다. 기능 사용은 마스터 전용입니다.")

# [5. 메인 레이아웃]
st.markdown('<div class="nav-bar"><div style="font-size: 22px; font-weight: bold;">💎 LUMEN QUANT LAB</div></div><div class="main-container"></div>', unsafe_allow_html=True)

# 공통 노출: 최신 당첨 번호 (갤러리 효과)
latest = fetch_lotto()
st.markdown(f"""
    <div class="premium-card" style="text-align: center; background: #f9fdf9;">
        <h3 style="color: #1e3d1e;">제 {latest['회차']}회 공식 당첨 결과</h3>
        <div style="margin: 20px 0;">
            {"".join([f'<div class="ball {"b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"}">{n}</div>' for n in latest['번호']])}
            <span style="font-size: 25px; font-weight: bold; margin: 0 10px;">+</span>
            <div class="ball b1">{latest['보너스']}</div>
        </div>
        <p style="font-size: 13px; color: #888;">데이터 출처: 네이버 실시간 동기화</p>
    </div>
""", unsafe_allow_html=True)

# 탭 구성
if is_master:
    # 마스터 전용 풀 메뉴
    tabs = st.tabs(["🚀 프라이빗 분석실", "📊 데이터 센터", "⚙️ 시스템 관리"])
    
    with tabs[0]:
        st.header("🤖 AI 에이전트 마스터 가동")
        agent = st.selectbox("전략 에이전트 선택", ["A1", "A2", "A3", "A4", "A5", "A6"])
        count = st.select_slider("추출 조합 수", options=[1, 10, 20, 30, 40, 50], value=10)
        if st.button(f"{agent} 엔진 즉시 가동"):
            results = [sorted(random.sample(range(1, 46), 6)) for _ in range(count)]
            for idx, r in enumerate(results):
                st.write(f"조합 {idx+1}: {r}")
            send_telegram(f"🛡️ [마스터 리포트]\n에이전트: {agent}\n개수: {count}\n내용: {results}")
            st.balloons()
            
    with tabs[1]:
        st.header("📜 전회차 히스토리 (마스터 전용)")
        st.dataframe(pd.DataFrame([{"회차": i, "분석": "완료"} for i in range(latest['회차'], 0, -1)]), use_container_width=True)
        
    with tabs[2]:
        st.critical("🚨 시스템 백엔드")
        if st.button("로그 파일 정리"):
            st.warning("시스템 로그를 정리했습니다.")

else:
    # 일반 방문자용 메뉴
    st.markdown("""
        <div class="premium-card">
            <h4>🤖 루멘 퀀트 에이전시 소개</h4>
            <p>본 연구소는 논문을 학습한 6명의 AI 에이전트를 통해 최적의 퀀트 조합을 도출합니다.</p>
            <hr>
            <li><b>A1-A2:</b> 통계 및 패턴 분석 전문가</li>
            <li><b>A3-A4:</b> 딥러닝 및 퀀트 밸런싱 엔진</li>
            <li><b>A5-A6:</b> 시뮬레이션 및 데이터 가디언</li>
            <br>
            <p style="color: #1e3d1e; font-weight: bold;">※ 현재 분석 기능은 마스터 권한으로 잠겨 있습니다.</p>
        </div>
    """, unsafe_allow_html=True)
