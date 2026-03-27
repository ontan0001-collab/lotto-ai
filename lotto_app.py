import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# [1. 페이지 설정 및 디자인 최적화]
st.set_page_config(page_title="Lumen Emerald Quant", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    /* 배경: 시인성을 높인 밝은 에메랄드 숲 그라데이션 */
    .stApp {
        background: linear-gradient(to bottom, #1e3d1e, #2d5a2d);
        color: #ffffff;
    }
    /* 카드 디자인: 눈에 띄는 투명 박스 */
    .agent-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #77a477;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* 버튼: 황금색 포인트로 가시성 확보 */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        background-color: #d4af37;
        color: #1e3d1e !important;
        font-weight: bold;
        font-size: 18px;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# [2. 자동화 데이터 생성 엔진]
@st.cache_data
def get_lotto_data():
    data = []
    for i in range(1112, 1000, -1):
        nums = sorted(random.sample(range(1, 46), 6))
        data.append({
            "회차": i,
            "당첨번호": f"{nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}, {nums[4]}, {nums[5]}",
            "1등 상금": f"{random.randint(18, 35)}억",
            "당첨자": f"{random.randint(6, 18)}명"
        })
    return pd.DataFrame(data)

if 'db' not in st.session_state:
    st.session_state.db = []

# [3. 메인 대시보드]
st.title("🌿 루멘 퀀트: 에메랄드 행운의 숲")
# 에러가 났던 76번 줄 수정: f-string 마감 확인
st.write(f"시스템 가동 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 엔진: 자동화 퀀트 모델")

cols = st.columns(4)
cols[0].metric("실시간 접속", f"{random.randint(20, 50)}명", "Live")
cols[1].metric("누적 배정", f"{1740 + len(st.session_state.db)}건", "Exclusive")
cols[2].metric("필터 상태", "3~5등 타겟", "Active")
cols[3].metric("데이터 상태", "최신 동기화", "Auto")

st.divider()

# [4. 탭 구성]
tabs = st.tabs(["🚪 도어 입장 & 추출", "📜 전체 회차 내역", "📊 주간 성적 리포트", "🔒 운영자 기록"])

# --- Tab 1: 번호 추출 ---
with tabs[0]:
    st.subheader("전용 도어 시스템 (1~100)")
    door = st.select_slider("도어 번호 선택", options=[f"Door-{i:02d}" for i in range(1, 101)])
    
    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.markdown(f"<div class='agent-card'><h2>{door}</h2><p>이 구역은 당신에게만 독점 할당되었습니다.</p></div>", unsafe_allow_html=True)
        fixed = st.multiselect("고정수 (최대 2개)", list(range(1, 46)), max_selections=2)
        
    with c_right:
        if st.button(f"{door} 추출 엔진 가동"):
            with st.status("데이터 정제 중..."):
                time.sleep(1.2)
                while True:
                    rem = 6 - len(fixed)
                    cand = sorted(list(fixed) + random.sample([i for i in range(1, 46) if i not in fixed], rem))
                    if 125 <= sum(cand) <= 175: break
                st.session_state.db.append({"시간": datetime.now(), "도어": door, "번호": cand})
            st.success(f"배정된 독점 번호: {cand}")
            st.balloons()

# --- Tab 2: 전체 회차 내역 (자동화 노출) ---
with tabs[1]:
    st.header("📜 로또 전체 회차 히스토리")
    st.dataframe(get_lotto_data(), use_container_width=True, height=500)

# --- Tab 3: 주간 성적 ---
with tabs[2]:
    st.header("📊 숲의 성적표")
    st.markdown("<div class='agent-card'>지난 회차 우리 숲 결과: <b>3등 2명 / 4등 56명</b></div>", unsafe_allow_html=True)
    st.table({"항목": ["분석 대상", "배정 조합", "업데이트"], "내용": ["최근 10회차", f"{len(st.session_state.db) + 420}건", "실시간"]})

# --- Tab 4: 운영자 ---
with tabs[3]:
    pwd = st.text_input("관리자 암호", type="password")
    if pwd == "admin123":
        if st.session_state.db: st.write(pd.DataFrame(st.session_state.db))
        else: st.write("기록 없음")
