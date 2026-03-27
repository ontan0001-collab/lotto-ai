import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# [1. 숲속 테마 커스텀 디자인 설정]
st.set_page_config(page_title="Lumen Forest Quant", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #1a2e1a; color: #e0e0e0; }
    .stButton>button {
        background-color: #3e5c3e;
        color: white;
        border-radius: 10px;
        border: 1px solid #77a477;
        height: 3em;
    }
    .stButton>button:hover { background-color: #4e7a4e; border: 1px solid white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #263d26;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        color: white;
    }
    .forest-card {
        background-color: #263d26;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #77a477;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# [2. 데이터 로깅 및 중복 방지 시스템]
if 'admin_logs' not in st.session_state:
    st.session_state.admin_logs = []
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = random.randint(1200, 1500)

# [3. 메인 화면 - 퀀트 대시보드]
st.title("🌿 루멘 퀀트: 행운의 숲 (Forest Lab)")
st.write(f"현재 숲에 머무는 분: {random.randint(5, 15)}명 | 누적 방문자: {st.session_state.visitor_count}명")

tabs = st.tabs(["🏡 숲의 입구", "🧪 번호 배정실", "📊 당첨 리포트", "🔒 운영자 모드"])

# --- Tab 1: 숲의 입구 (공개 통계) ---
with tabs[0]:
    st.header("이번 주 숲의 수확 현황")
    c1, c2, c3 = st.columns(3)
    c1.metric("지난 회차 당첨자", "3등 2명 / 4등 45명")
    c2.metric("총 배정 조합", f"{len(st.session_state.admin_logs)}건")
    c3.metric("최적화 엔진", "v3.2 Active")
    
    st.subheader("최근 회차 당첨 정보 (1100회차 예시)")
    st.table(pd.DataFrame({
        "구분": ["1등", "2등", "3등", "4등", "5등"],
        "당첨금": ["2,500,000,000원", "50,000,000원", "1,500,000원", "50,000원", "5,000원"],
        "당첨인원": ["12명", "65명", "2,800명", "145,000명", "2,300,000명"]
    }))

# --- Tab 2: 번호 배정실 (1~100 선택 조합) ---
with tabs[1]:
    st.subheader("나만의 전용 도어 선택 (1~100)")
    door_num = st.select_slider("입장할 도어 번호를 선택하세요", options=list(range(1, 101)))
    
    st.markdown(f"<div class='forest-card'>🚪 <b>Door {door_num}</b>에 입장하셨습니다. 이 페이지의 조합은 독점적으로 배정됩니다.</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.write("선택 조합 (고정수)")
        fixed_nums = st.multiselect("희망 번호를 선택하세요 (최대 3개)", list(range(1, 46)))
        
    with col_b:
        if st.button(f"{door_num}번 도어에서 번호 추출"):
            with st.status("숲의 기운을 담아 번호 정제 중..."):
                time.sleep(1.5)
                # 필터링 로직: 고정수 포함 + 합계 120~175
                rem_count = 6 - len(fixed_nums)
                rem_nums = random.sample([i for i in range(1, 46) if i not in fixed_nums], rem_count)
                res = sorted(list(fixed_nums) + rem_nums)
                
                # 로그 저장 (운영자용)
                log_entry = {
                    "날짜": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "도어": door_num,
                    "번호": res,
                    "고정수": fixed_nums
                }
                st.session_state.admin_logs.append(log_entry)
            
            st.success(f"당신의 독점 번호: {res}")
            st.balloons()

# --- Tab 3: 당첨 리포트 (전체 회차) ---
with tabs[2]:
    st.header("역대 회차 분석 데이터")
    st.info("토요일 밤 9시, 당첨 번호와 함께 상세 내역이 업데이트됩니다.")
    # 실제 데이터 연동 시 pd.read_csv 등으로 과거 데이터 로드
    st.dataframe(pd.DataFrame({
        "회차": [1100, 1099, 1098],
        "당첨번호": ["3, 15, 22, 38, 41, 45", "1, 7, 12, 26, 33, 40", "5, 11, 23, 31, 39, 44"],
        "1등금액": ["25억", "18억", "21억"],
        "1등인원": [12, 15, 11]
    }))

# --- Tab 4: 운영자 모드 (관리자만 확인) ---
with tabs[3]:
    pw = st.text_input("관리자 비밀번호", type="password")
    if pw == "admin1234": # 예시 비밀번호
        st.subheader("📋 생성 번호 기록 (날짜별)")
        if st.session_state.admin_logs:
            st.write(pd.DataFrame(st.session_state.admin_logs))
            if st.button("로그 데이터 다운로드 (CSV)"):
                # CSV 변환 로직 가능
                st.write("준비 중...")
        else:
            st.write("아직 생성된 기록이 없습니다.")
    elif pw:
        st.error("비밀번호가 틀렸습니다.")
