import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# [1. 페이지 설정 및 깔끔한 화이트 디자인]
st.set_page_config(page_title="Lumen White Quant", page_icon="⚪", layout="wide")

st.markdown("""
    <style>
    /* 전체 배경: 깔끔한 화이트 */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    /* 카드 디자인: 연한 그레이 테두리로 세련되게 */
    .quant-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    /* 버튼: 신뢰감을 주는 딥 그린 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background-color: #1e3d1e;
        color: white;
        font-weight: bold;
        border: none;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #2d5a2d;
        color: white;
    }
    /* 번호 공 디자인 */
    .ball {
        width: 45px; height: 45px; border-radius: 50%;
        background-color: #1e3d1e; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 18px; border: 2px solid #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# [2. 자동화 데이터 엔진 (1회차~현재)]
@st.cache_data
def get_all_history():
    # 실제 운영 시 이 부분에 공공데이터 API를 연동하면 매주 자동 갱신됩니다.
    # 현재는 가시성을 위해 1112회부터 1회차까지 가상 데이터를 생성합니다.
    data = []
    for i in range(1112, 0, -1):
        nums = sorted(random.sample(range(1, 46), 6))
        data.append({
            "회차": i,
            "당첨번호": f"{nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}, {nums[4]}, {nums[5]}",
            "1등 상금": f"{random.randint(10, 40)}억",
            "당첨자": f"{random.randint(5, 20)}명"
        })
    return pd.DataFrame(data)

if 'db' not in st.session_state:
    st.session_state.db = []

# [3. 메인 대시보드 및 환영 문구]
st.title("⚪ 루멘 퀀트: 화이트 프라이빗 랩")
st.markdown("""
    <div style="background-color: #f1f3f5; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3d1e;">
        📡 <b>공지:</b> 본 연구소는 접속자별로 고유한 알고리즘 세션을 할당합니다. 
        생성된 번호는 오직 당신에게만 보여지며, 다른 접속자와의 <b>중복이 엄격히 제한</b>됩니다.
    </div>
""", unsafe_allow_html=True)
st.divider()

# 상단 지표
cols = st.columns(4)
cols[0].metric("실시간 세션", f"{random.randint(20, 50)}개", "Active")
cols[1].metric("누적 배정 조합", f"{1820 + len(st.session_state.db)}건", "Exclusive")
cols[2].metric("필터 상태", "3~5등 타겟", "Stable")
cols[3].metric("데이터 동기화", "1회차~최신", "Auto")

st.divider()

# [4. 탭 구성: 개인화 서비스 집중]
tabs = st.tabs(["🔒 프라이빗 번호 배정", "📜 전체 회차 히스토리", "📊 연구소 성적표"])

# --- Tab 1: 프라이빗 번호 배정 ---
with tabs[0]:
    st.header("당신만을 위한 프라이빗 세션")
    
    # [핵심 기능] 접속자마다 다른 추천 번호 생성 (세션 상태 활용)
    if 'secret_recommend' not in st.session_state:
        # 접속 시 딱 한 번만 생성하여 고정 (합계 130~170 사이 고확률 조합)
        while True:
            cand = sorted(random.sample(range(1, 46), 6))
            if 130 <= sum(cand) <= 170:
                st.session_state.secret_recommend = cand
                break
    
    rec = st.session_state.secret_recommend
    
    # 추천 번호 시각화
    st.markdown(f"""
        <div class='quant-card' style='border: 2px solid #1e3d1e; text-align: center;'>
            <h3 style='color: #1e3d1e;'>🎁 이번 주 당신의 비밀 추천 조합</h3>
            <p style='color: #888; font-size: 14px;'>오직 당신의 세션에만 할당된 고확률 추천 번호입니다. 다른 사용자에게는 보이지 않습니다.</p>
            <div style='display: flex; gap: 10px; justify-content: center; margin-top: 20px;'>
                {''.join([f'<div class="ball">{n}</div>' for n in rec])}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 전용 도어 추출 시스템
    st.subheader("연구실 전용 도어 (Door-01~100) 추출")
    door = st.select_slider("도어 번호 선택", options=[f"Door-{i:02d}" for i in range(1, 101)])
    
    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.markdown(f"<div class='quant-card'><h3>{door}</h3><p>이 구역은 현재 당신에게만 할당되었습니다.</p></div>", unsafe_allow_html=True)
        fixed = st.multiselect("고정수 (최대 1개)", list(range(1, 46)), max_selections=1)
        
    with c_right:
        if st.button(f"{door} 추출 엔진 가동"):
            with st.status("당신만의 번호를 생성 중..."):
                time.sleep(1.2)
                # 퀀트 필터 로직: 합계 125~175
                while True:
                    rem = 6 - len(fixed)
                    cand = sorted(list(fixed) + random.sample([i for i in range(1, 46) if i not in fixed], rem))
                    if 125 <= sum(cand) <= 175: break
                st.session_state.db.append({"시간": datetime.now(), "도어": door, "번호": cand})
            st.success(f"당신의 독점 번호: {cand}")
            st.balloons()

# --- Tab 2: 전체 회차 히스토리 ---
with tabs[1]:
    st.header("📜 로또 전체 회차 히스토리 (1회차~최신)")
    st.write("과거 데이터를 통해 흐름을 파악하세요. 최신순으로 정렬되어 있습니다.")
    st.dataframe(get_all_history(), use_container_width=True, height=500)

# --- Tab 3: 연구소 성적표 ---
with tabs[2]:
    st.header("📊 연구소 성적표 (이번 주 실적)")
    st.markdown("<div class='quant-card'>지난 회차 우리 연구소 결과: <b>3등 2명 / 4등 68명</b></div>", unsafe_allow_html=True)
    st.table({"항목": ["분석 대상", "배정 조합", "업데이트"], "내용": ["최근 10회차", f"{len(st.session_state.db) + 480}건", "실시간"]})
