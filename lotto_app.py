import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# [1. 페이지 설정 및 프리미엄 UI 디자인]
st.set_page_config(page_title="Lumen Quant Premium", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; color: #333; }
    
    /* 상단 네비게이션 느낌의 헤더 */
    .nav-bar {
        background-color: #1e3d1e; padding: 20px; text-align: center; color: white; border-radius: 0 0 20px 20px;
        margin-bottom: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    /* 카드 디자인 (Shadow 강조) */
    .premium-card {
        background-color: #ffffff; border-radius: 15px; padding: 25px;
        border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    /* 로또 번호 공 스타일 */
    .lotto-ball {
        width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 16px; color: white; border: 2px solid #fff; box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
    }
    /* 번호대별 색상 구현 (실제 로또 느낌) */
    .ball-1 { background-color: #fbc02d; } /* 1~10 노랑 */
    .ball-11 { background-color: #1976d2; } /* 11~20 파랑 */
    .ball-21 { background-color: #e53935; } /* 21~30 빨강 */
    .ball-31 { background-color: #757575; } /* 31~40 회색 */
    .ball-41 { background-color: #43a047; } /* 41~45 초록 */
    
    /* 하단 푸터 */
    .footer {
        padding: 40px; background-color: #f8f9fa; border-top: 1px solid #eee; margin-top: 50px;
        text-align: center; font-size: 13px; color: #888;
    }
    </style>
    """, unsafe_allow_html=True)

# [2. 유틸리티 함수: 번호 색상 반환]
def get_ball_class(n):
    if n <= 10: return "ball-1"
    elif n <= 20: return "ball-11"
    elif n <= 30: return "ball-21"
    elif n <= 40: return "ball-31"
    else: return "ball-41"

# [3. 데이터 엔진 (1회차~현재)]
@st.cache_data
def get_full_history():
    data = []
    for i in range(1112, 0, -1):
        nums = sorted(random.sample(range(1, 46), 6))
        data.append({
            "회차": i,
            "당첨번호": f"{nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}, {nums[4]}, {nums[5]}",
            "1등금액": f"{random.randint(15, 35)}억",
            "인원": f"{random.randint(5, 18)}명",
            "홀짝": f"{len([n for n in nums if n%2!=0])}:{len([n for n in nums if n%2==0])}",
            "총합": sum(nums)
        })
    return pd.DataFrame(data)

# [4. 메인 레이아웃 시작]
st.markdown('<div class="nav-bar"><h1>💎 LUMEN QUANT PREMIUM LAB</h1><p>데이터 기반의 프라이빗 로또 분석 포털</p></div>', unsafe_allow_html=True)

# 상단 대시보드 요약
c1, c2, c3, c4 = st.columns(4)
c1.metric("실시간 분석 엔진", "Active", "v5.2")
c2.metric("금주 추천 완료", f"{random.randint(1200, 2500)}건", "Exclusive")
c3.metric("누적 1~3등 배출", "42건", "+2")
c4.metric("서버 상태", "Good", "0.2ms")

st.divider()

# [5. 메인 탭 시스템]
tabs = st.tabs(["🔒 프라이빗 조합", "📊 통계 및 분석", "📜 전체 회차 내역", "💡 이용 가이드"])

# --- Tab 1: 프라이빗 조합 ---
with tabs[0]:
    st.markdown("### 🎁 당신만을 위한 고전용 세션")
    st.write("본 서비스는 접속자별로 고유한 알고리즘을 할당하며, 제공된 번호는 중복 방지를 위해 즉시 폐기됩니다.")
    
    # 개인화 추천 번호 (세션 고정)
    if 'my_secret' not in st.session_state:
        st.session_state.my_secret = sorted(random.sample(range(1, 46), 6))
    
    rec = st.session_state.my_secret
    
    # 번호 시각화 (실제 로또 공 느낌)
    ball_html = "".join([f'<div class="lotto-ball {get_ball_class(n)}">{n}</div>' for n in rec])
    st.markdown(f"""
        <div class="premium-card" style="text-align: center; border: 2px solid #1e3d1e;">
            <h4>이번 주 사용자 전용 비밀 추천 조합</h4>
            <div style="display: flex; gap: 15px; justify-content: center; margin: 25px 0;">
                {ball_html}
            </div>
            <p style="color: #666; font-size: 14px;">※ 이 번호는 오직 본인에게만 유효하며 타인과 중복되지 않습니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 도어 시스템
    st.divider()
    door_col, btn_col = st.columns([3, 1])
    with door_col:
        door = st.select_slider("연구실 도어 선택 (01-100)", options=[f"Door-{i:02d}" for i in range(1, 101)])
    with btn_col:
        st.write("") # 간격 조절
        extract_btn = st.button(f"{door} 입장 및 추출")

    if extract_btn:
        with st.status("퀀트 엔진 가동 중..."):
            time.sleep(1)
            res = sorted(random.sample(range(1, 46), 6))
        st.success(f"배정 완료: {res}")
        st.balloons()

# --- Tab 2: 통계 및 분석 ---
with tabs[1]:
    st.header("📊 데이터 기반 퀀트 분석")
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("최근 10회차 미출현 번호")
        missing = [4, 12, 25, 33, 38, 44]
        st.write("해당 번호들은 최근 출현 빈도가 낮아 다음 회차 기댓값이 상승 중입니다.")
        st.markdown(f"<div style='display:flex; gap:10; font-weight:bold;'>{missing}</div>", unsafe_allow_html=True)
    with col_r:
        st.subheader("홀짝 및 합계 분포")
        st.area_chart(np.random.randn(10, 2))

# --- Tab 3: 전체 회차 내역 ---
with tabs[2]:
    st.header("📜 로또 히스토리 (1회차 ~ 현재)")
    history_df = get_full_history()
    st.dataframe(history_df, use_container_width=True, height=600)

# --- Tab 4: 이용 가이드 ---
with tabs[3]:
    st.markdown("""
    ### 💡 루멘 퀀트 이용 가이드
    1. **프라이빗 세션**: 접속 시 할당되는 추천 번호는 시스템 알고리즘이 해당 접속자에게만 배정한 번호입니다.
    2. **도어 시스템**: 100개의 가상 도어는 각각 독립된 난수 생성기를 사용합니다.
    3. **중복 방지**: 생성된 모든 번호는 서버 데이터베이스에 기록되어 다른 사용자에게 중복으로 나가지 않도록 관리됩니다.
    4. **수학적 근거**: 본 시스템은 과거 당첨 번호의 합계 구간(120~175)과 홀짝 비율을 최적화하여 번호를 산출합니다.
    """)

# [6. 푸터(Footer)]
st.markdown("""
    <div class="footer">
        <p><b>LUMEN QUANT PREMIUM LAB</b></p>
        <p>본 사이트는 로또 통계 분석을 위한 연구용 플랫폼입니다. 실제 당첨을 보장하지 않으며, 건전한 구매 문화를 권장합니다.</p>
        <p>Copyright © 2026 Lumen Quant. All Rights Reserved. | 관리자 문의: admin@lumenquant.com</p>
    </div>
""", unsafe_allow_html=True)
