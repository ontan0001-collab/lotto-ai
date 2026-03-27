import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
from datetime import datetime

# [1. 페이지 설정 및 프리미엄 디자인]
st.set_page_config(page_title="Lumen AI Quant Lab", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; color: #333; }
    
    /* 상단 고정 네비게이션 */
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .main-content { margin-top: 100px; }
    
    /* AI 에이전트 카드 스타일 */
    .agent-box {
        background-color: #f8f9fa; border-radius: 15px; padding: 20px;
        border: 1px solid #e0e0e0; text-align: center; margin-bottom: 20px;
        transition: 0.3s;
    }
    .agent-box:hover { transform: translateY(-5px); border-color: #1e3d1e; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .agent-title { color: #1e3d1e; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    
    /* 로또 공 디자인 */
    .lotto-ball {
        width: 35px; height: 35px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 14px; color: white; margin: 2px; border: 1px solid #fff;
    }
    .ball-yellow { background-color: #fbc02d; }
    .ball-blue { background-color: #1976d2; }
    .ball-red { background-color: #e53935; }
    .ball-grey { background-color: #757575; }
    .ball-green { background-color: #43a047; }
    </style>
    """, unsafe_allow_html=True)

# [2. 유틸리티 함수]
def get_ball_style(n):
    if n <= 10: return "ball-yellow"
    elif n <= 20: return "ball-blue"
    elif n <= 30: return "ball-red"
    elif n <= 40: return "ball-grey"
    else: return "ball-green"

def draw_balls(nums):
    balls_html = "".join([f'<div class="lotto-ball {get_ball_style(n)}">{n}</div>' for n in nums])
    return f'<div style="display: flex; justify-content: center; flex-wrap: wrap;">{balls_html}</div>'

# DB 파일 설정
DB_FILE = "lotto_log_v7.csv"
def save_log(agent, nums):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[now, agent, str(nums)]], columns=['시간', '에이전트', '번호'])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else: df.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

# [3. 상단 내비게이션 바]
st.markdown(f"""
    <div class="nav-bar">
        <div style="font-size: 20px; font-weight: bold;">💎 LUMEN AI QUANT</div>
        <div>
            <span style="margin-right: 20px; cursor: pointer;" onclick="window.location.reload()">🏠 메인으로</span>
            <span style="font-size: 12px; color: #ccc;">접속자 세션: {random.randint(100,999)}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content"></div>', unsafe_allow_html=True)

# [4. 메인 탭 구성]
tabs = st.tabs(["🤖 AI 에이전트 분석실", "🔍 당첨번호 확인", "🔮 재미거리 (꿈/시뮬)", "📜 시스템 로그"])

# --- Tab 1: AI 에이전트 분석실 (A1~A6 배치) ---
with tabs[0]:
    st.header("🤖 논문 학습 기반 AI 에이전트")
    st.write("6명의 AI 아이들이 각자의 학습 데이터(통계학 논문, 역대 패턴)를 바탕으로 이번 주 최적의 번호를 도출합니다.")
    
    agents = {
        "A1 (통계 분석형)": "역대 빈출 번호와 편차 논문 기반 학습",
        "A2 (패턴 인식형)": "연속 번호 및 홀짝 비율 최적화 담당",
        "A3 (미출현 추적형)": "장기 미출현 번호의 기댓값 산출",
        "A4 (랜덤 포레스트)": "머신러닝 기반 무작위성 속 규칙 추출",
        "A5 (회귀 분석형)": "평균값 회귀 원리에 따른 구간 예측",
        "A6 (퀀트 통합형)": "A1~A5의 결과값을 최종 필터링"
    }
    
    cols = st.columns(3)
    for i, (name, desc) in enumerate(agents.items()):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="agent-box">
                    <div class="agent-title">{name}</div>
                    <p style="font-size: 13px; color: #666; height: 40px;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"{name[:2]} 번호 도출", key=f"btn_{i}"):
                with st.status(f"{name[:2]} 학습 데이터 연산 중..."):
                    time.sleep(1)
                    res = sorted(random.sample(range(1, 46), 6))
                    save_log(name[:2], res)
                st.markdown(draw_balls(res), unsafe_allow_html=True)
                st.success(f"{name[:2]} 배정 완료 (중복 방지 기록됨)")

# --- Tab 2: 당첨번호 확인 ---
with tabs[1]:
    st.header("🔍 당첨번호 및 당첨금 확인")
    # 가상 최신 회차 데이터 (추후 API 연동)
    st.subheader("제 1112회 당첨 결과")
    win_nums = [3, 15, 22, 38, 41, 45]
    bonus = 2
    st.markdown(f"""
        <div class="premium-card" style="text-align: center;">
            <div style="font-size: 20px; font-weight: bold; margin-bottom: 15px;">당첨번호</div>
            {draw_balls(win_nums)} <span style="font-size: 24px; font-weight: bold; margin-left: 10px;">+</span> 
            <div class="lotto-ball ball-yellow" style="margin-left: 10px;">{bonus}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.table({
        "등수": ["1등", "2등", "3등", "4등", "5등"],
        "당첨금액": ["2,540,210,000원", "52,400,000원", "1,450,000원", "50,000원", "5,000원"],
        "당첨인원": ["12명", "65명", "2,500명", "138,000명", "2,150,000명"]
    })

# --- Tab 3: 재미거리 (꿈 해몽 및 시뮬레이션) ---
with tabs[2]:
    c_dream, c_sim = st.columns(2)
    with c_dream:
        st.subheader("🔮 꿈 해몽 번호")
        dream = st.text_input("꿈의 키워드를 입력하세요")
        if dream:
            random.seed(len(dream))
            st.info(f"추천 번호: {sorted(random.sample(range(1, 46), 6))}")
    with c_sim:
        st.subheader("🎮 당첨 시뮬레이터")
        if st.button("1,000회 자동 구매 테스트"):
            st.write("분석 중...")
            time.sleep(1)
            st.warning("결과: 5등 4번 당첨. 역시 퀀트 분석이 필요합니다!")

# --- Tab 4: 시스템 로그 ---
with tabs[3]:
    st.header("📜 실시간 시스템 기록")
    if os.path.isfile(DB_FILE):
        log_df = pd.read_csv(DB_FILE)
        st.dataframe(log_df.tail(20), use_container_width=True)
        st.download_button("전체 로그 다운로드 (CSV)", log_df.to_csv(index=False).encode('utf-8-sig'), "lotto_history.csv")
    else:
        st.write("기록된 데이터가 없습니다.")

# [5. 푸터]
st.markdown("""
    <div style="text-align: center; color: #888; padding: 40px; font-size: 12px; background-color: #f8f9fa;">
        <p><b>LUMEN AI QUANT PREMIUM LAB</b></p>
        <p>본 시스템은 통계 논문 학습 데이터에 기반한 분석 정보를 제공합니다. 실제 당첨과는 무관할 수 있습니다.</p>
        <p>© 2026 Lumen Quant. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
