import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# [1. 페이지 설정 및 디자인]
st.set_page_config(page_title="Lumen Forest Quant Lab", page_icon="🌿", layout="wide")

# CSS 디자인 (따옴표 마감 처리 완벽 확인)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1a0d; 
        background-image: linear-gradient(160deg, #0d1a0d 0%, #1a2e19 100%);
        color: #e0e0e0;
    }
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #2e4d2e;
        color: #d4af37;
        font-weight: bold;
        border: 1px solid #d4af37;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: #0d1a0d;
    }
    </style>
    """, unsafe_allow_html=True)

# [2. 데이터 생성 로직]
def get_lotto_history():
    data = []
    # 1112회부터 1050회까지 가상 데이터 생성
    for i in range(1112, 1050, -1):
        nums = sorted(random.sample(range(1, 46), 6))
        bonus = random.choice([n for n in range(1, 46) if n not in nums])
        data.append({
            "회차": i,
            "당첨번호": f"{nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}, {nums[4]}, {nums[5]} + {bonus}",
            "1등 당첨금": f"{random.randint(15, 30)}억",
            "1등 인원": f"{random.randint(5, 15)}명"
        })
    return pd.DataFrame(data)

if 'db' not in st.session_state:
    st.session_state.db = []

# [3. 메인 화면 상단 지표]
st.title("🌿 루멘 퀀트: 행운의 숲 연구소")
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("실시간 접속자", f"{random.randint(15, 40)}명", "Live")
c2.metric("누적 배정 조합", f"{1620 + len(st.session_state.db)}건", "Exclusive")
c3.metric("엔진 상태", "A1-A6 최적화", "Stable")
c4.metric("데이터 동기화", "정상", "Sync")

# [4. 메인 탭 구성]
tabs = st.tabs(["🚪 도어 입장 & 추출", "📜 전체 회차 내역", "📊 주간 당첨 리포트", "🔒 운영자 기록"])

# --- Tab 1
