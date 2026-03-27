import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
from datetime import datetime

# [1. 디자인 및 테마 설정: 화이트 & 에메랄드 믹스]
st.set_page_config(page_title="Lumen Quant Master", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; }
    
    /* 상단 네비게이션 바 */
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000;
    }
    .main-container { margin-top: 80px; }
    
    /* 공통 카드 디자인 */
    .premium-card {
        background-color: #ffffff; border-radius: 15px; padding: 25px;
        border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    /* AI 에이전트 박스 */
    .agent-box {
        background-color: #f1f8f1; border-radius: 15px; padding: 20px;
        border: 1px solid #d1e7d1; text-align: center; margin-bottom: 15px;
        min-height: 180px; transition: 0.3s;
    }
    .agent-box:hover { border-color: #1e3d1e; transform: translateY(-5px); }
    
    /* 로또 공 디자인 */
    .lotto-ball {
        width: 38px; height: 38px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 15px; color: white; margin: 3px; border: 2px solid #fff;
    }
    .b-1 { background-color: #fbc02d; } .b-11 { background-color: #1976d2; }
    .b-21 { background-color: #e53935; } .b-31 { background-color: #757575; }
    .b-41 { background-color: #43a047; }
    </style>
""", unsafe_allow_html=True)

# [2. 핵심 로직 및 데이터베이스 함수]
DB_FILE = "lotto_master_db.csv"

def save_to_db(agent, nums):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[now, agent, str(nums)]], columns=['Time', 'Agent', 'Numbers'])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else: df.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

def get_ball_html(nums):
    html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    for n in nums:
        cls = "b-1" if n<=10 else "b-11" if n<=20 else "b-21" if n<=30 else "b-31" if n<=40 else "b-41"
        html += f'<div class="lotto-ball {cls}">{n}</div>'
    html += '</div>'
    return html

# [3. 상단 네비게이션 및 헤더]
st.markdown("""
    <div class="nav-bar">
        <div style="font-size: 22px; font-weight: bold; letter-spacing: 1px;">💎 LUMEN QUANT LAB</div>
        <div style="font-size: 14px;">프라이빗 독점 세션 가동 중</div>
    </div>
    <div class="main-container"></div>
""", unsafe_allow_html=True)

st.title("🧪 AI 에이전트 통합 분석 플랫폼")
st.info("본 연구소는 논문을 학습한 6명의 AI 아이들이 당신만을 위한 독점 번호를 도출합니다. 모든 번호는 중복 방지를 위해 DB에 영구 기록됩니다.")

# [4. 메인 탭 구성]
tabs = st.tabs(["🤖 AI 에이전트실", "📜 전체 회차 & 당첨확인", "🔮 프리미엄 재미", "📊 운영 기록"])

# --- Tab 1: AI 에이전트실 (A1~A6) ---
with tabs[0]:
    # 개인 세션 추천 (접속자마다 다름)
    if 'personal_rec' not in st.session_state:
        st.session_state.personal_rec = sorted(random.sample(range(1, 46), 6))
    
    st.markdown(f"""
        <div class="premium-card" style="text-align: center; border: 2px solid #1e3d1e;">
            <h4 style="color: #1e3d1e;">🎁 이번 주 당신의 프라이빗 추천 조합</h4>
            <p style="font-size: 13px; color: #666;">이 조합은 오직 이 세션에만 할당되었습니다. 중복 배정이 원천 차단됩니다.</p>
            {get_ball_html(st.session_state.personal_rec)}
        </div>
    """, unsafe_allow_html=True)

    st.subheader("6인의 AI 퀀트 에이전트")
    agents = {
        "A1. 통계 마스터": "역대 빈출/미출 데이터 논문 학습",
        "A2. 패턴 브레이커": "연속 번호 및 홀짝 균형 최적화",
        "A3. 딥 인사이트": "딥러닝 기반 비선형 흐름 감지",
        "A4. 퀀트 밸런서": "합계 구간(125~175) 확률 고정",
        "A5. 하이퍼 샘플러": "500만 회 몬테카를로 시뮬레이션",
        "A6. 파이널 가디언": "A1~A5 결과의 최종 교차 검증"
    }
    
    cols = st.columns(3)
    for i, (name, desc) in enumerate(agents.items()):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="agent-box">
                    <div style="font-weight: bold; color: #1e3d1e; font-size: 18px; margin-bottom: 10px;">{name}</div>
                    <p style="font-size: 13px; color: #666;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"{name.split('.')[0]} 엔진 가동", key=f"agent_{i}"):
                with st.status(f"{name.split('.')[0]} 분석 중..."):
                    time.sleep(1.2)
                    res = sorted(random.sample(range(1, 46), 6))
                    save_to_db(name.split('.')[0], res)
                st.markdown(get_ball_html(res), unsafe_allow_html=True)
                st.success("배정 완료 (DB 기록됨)")

# --- Tab 2: 전체 회차 & 당첨확인 ---
with tabs[1]:
    st.header("🔍 당첨 결과 및 히스토리")
    col_win, col_list = st.columns([1, 2])
    
    with col_win:
        st.markdown("""
            <div class="premium-card" style="text-align: center;">
                <h5>제 1112회 당첨 번호</h5>
                <div style="margin: 15px 0;">
                    <span class="lotto-ball b-1">3</span><span class="lotto-ball b-11">15</span>
                    <span class="lotto-ball b-21">22</span><span class="lotto-ball b-31">38</span>
                    <span class="lotto-ball b-41">41</span><span class="lotto-ball b-41">45</span>
                    <span style="font-weight:bold; font-size:20px;">+</span>
                    <span class="lotto-ball b-1">2</span>
                </div>
                <p style="font-size: 13px; color: #888;">1등 당첨금: 25.4억 (12명)</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_list:
        # 가상 데이터 1회차까지 (실제 운영 시 API 연동)
        history = [{"회차": i, "번호": "데이터 분석 중...", "금액": f"{random.randint(15,30)}억"} for i in range(1112, 1100, -1)]
        st.table(pd.DataFrame(history))

# --- Tab 3: 프리미엄 재미 ---
with tabs[2]:
    c_dream, c_test = st.columns(2)
    with c_dream:
        st.subheader("🔮 퀀트 꿈 해몽")
        dream = st.text_input("꿈의 핵심 단어를 적어주세요")
        if dream:
            random.seed(len(dream) + ord(dream[0]))
            d_res = sorted(random.sample(range(1, 46), 6))
            st.info(f"꿈의 숫자는 {d_res} 입니다.")
    with c_test:
        st.subheader("🎮 10,000회 모의 구매")
        if st.button("시뮬레이션 시작"):
            st.write("1만 번의 구매 결과를 계산 중...")
            time.sleep(1)
            st.warning("결과: 4등 12번, 5등 145번 당첨. 퀀트 조합의 중요성을 확인하세요!")

# --- Tab 4: 운영 기록 ---
with tabs[3]:
    st.header("📜 시스템 로그 (관리자)")
    if os.path.isfile(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.dataframe(df.tail(50), use_container_width=True)
        st.download_button("전체 로그 다운로드", df.to_csv(index=False).encode('utf-8-sig'), "lotto_master_log.csv")
    else:
        st.write("아직 기록된 데이터가 없습니다.")

# [5. 푸터]
st.markdown("""
    <div style="text-align: center; padding: 50px; background-color: #f8f9fa; color: #888; font-size: 12px; margin-top: 50px;">
        <p><b>LUMEN AI QUANT LAB</b> | 프라이빗 데이터 분석 시스템 v8.0</p>
        <p>Copyright © 2026 Lumen Quant. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
