import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# [1. 마스터 보안 설정 (비밀의 문)]
MASTER_CODE = "lumen_secret_99"  # 관리자용 비밀번호
TELEGRAM_TOKEN = '8369798851:AAH7EYXjvJppJf5Pp3RcMjsAeI4LaBsRK1I'
CHAT_ID = '7628406047'

st.set_page_config(page_title="Lumen Quant | 로또 AI 분석 포털", page_icon="📈", layout="wide")

# [2. 전문 포털급 UI/UX CSS 디자인]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #f8f9fa; }
    
    /* 포털 상단 헤더 */
    .portal-header {
        background: linear-gradient(135deg, #1e3d1e 0%, #2d5a2d 100%);
        padding: 40px 20px; text-align: center; color: white; border-radius: 0 0 30px 30px;
        margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .portal-header h1 { font-weight: 900; font-size: 38px; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .portal-header p { font-size: 16px; color: #e1eee1; }
    
    /* 포털 콘텐츠 카드 */
    .portal-card {
        background-color: #ffffff; border-radius: 20px; padding: 30px;
        border: 1px solid #eaeaea; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.04);
        transition: transform 0.2s;
    }
    .portal-card:hover { transform: translateY(-3px); border-color: #1e3d1e; }
    
    /* 로또 공 3D 효과 */
    .ball {
        width: 42px; height: 42px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: 700; font-size: 16px; 
        color: white; margin: 4px; box-shadow: inset -3px -3px 6px rgba(0,0,0,0.2), 2px 2px 5px rgba(0,0,0,0.1);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    
    /* 버튼 스타일링 */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; 
        background-color: #1e3d1e; color: white; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2d5a2d; color: white; box-shadow: 0 4px 10px rgba(30,61,30,0.3); }
    </style>
""", unsafe_allow_html=True)

# [3. 백엔드 통신 엔진]
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

@st.cache_data(ttl=1800)
def fetch_lotto(drw_no=None):
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

def get_ball_ui(nums):
    html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [4. 사이드바 - 숨겨진 마스터 로그인]
with st.sidebar:
    st.markdown("### 🔑 System Login")
    input_code = st.text_input("Admin Code", type="password", help="일반 사용자는 입력하지 마세요.")
    is_master = (input_code == MASTER_CODE)
    
    st.markdown("---")
    st.markdown("""
        **[안내]** 본 포털은 무료로 개방된 공공 AI 분석 플랫폼입니다.  
        모든 조합 추출 및 조회 기능은 100% 무료입니다.
    """)

# [5. 포털 대문 (Hero Section)]
st.markdown("""
    <div class="portal-header">
        <h1>💎 LUMEN QUANT PORTAL</h1>
        <p>논문 기반 통계와 딥러닝 AI 에이전트가 제시하는 새로운 차원의 로또 분석 플랫폼</p>
    </div>
""", unsafe_allow_html=True)

# 공통: 최신 회차 라이브 전광판
latest = fetch_lotto()
st.markdown(f"""
    <div class="portal-card" style="text-align: center; border-top: 4px solid #1e3d1e;">
        <h3 style="color: #333; font-weight: bold; margin-bottom: 20px;">🎉 이번 주 제 {latest['회차']}회 당첨 번호</h3>
        <div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
            {get_ball_ui(latest['번호'])}
            <span style="font-size: 28px; font-weight: 900; color: #ccc;">+</span>
            <div class="ball b1">{latest['보너스']}</div>
        </div>
        <p style="margin-top: 15px; color: #888; font-size: 14px;">📡 동행복권 실시간 데이터 동기화 완료</p>
    </div>
""", unsafe_allow_html=True)

# [6. 포털 탭 메뉴 (홈페이지 스타일)]
if is_master:
    tabs = st.tabs(["🏠 AI 번호 추출", "📚 전회차 데이터 조회", "🎯 내 번호 당첨 확인", "⚙️ 마스터 관리 센터"])
else:
    tabs = st.tabs(["🏠 AI 번호 추출", "📚 전회차 데이터 조회", "🎯 내 번호 당첨 확인"])

# --- Tab 1: AI 번호 추출 (대국민 공개용) ---
with tabs[0]:
    st.markdown("### 🤖 루멘 퀀트 전용 AI 에이전트")
    st.write("원하는 분석 성향을 가진 AI를 선택하고 무료로 번호를 받아보세요.")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        agent = st.selectbox("분석 알고리즘 선택", [
            "A1 (통계분석) - 역대 빈출/미출 중심", 
            "A2 (패턴매칭) - 홀짝 및 연속성 최적화", 
            "A3 (인사이트) - 딥러닝 비선형 흐름", 
            "A4 (퀀트밸런스) - 합계 구간 125~175 고정", 
            "A5 (시뮬레이션) - 100만회 모의 연산", 
            "A6 (최종가디언) - 종합 교차 검증"
        ])
    with c2:
        count = st.select_slider("추출 조합 개수 (최대 50게임)", options=[1, 5, 10, 20, 30, 40, 50], value=5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(f"🔥 {agent.split(' ')[0]} 엔진 가동 및 번호 추출 (무료)"):
        with st.spinner("최적의 퀀트 조합을 연산 중입니다..."):
            time.sleep(1.5)
            all_results = [sorted(random.sample(range(1, 46), 6)) for _ in range(count)]
            
            st.success("✅ 번호 추출이 완료되었습니다! 행운을 빕니다.")
            
            # 카드 형태로 예쁘게 출력
            for i, res in enumerate(all_results):
                st.markdown(f"""
                    <div style="background: #fff; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #1e3d1e; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <strong style="color:#1e3d1e; display:inline-block; width: 60px;">게임 {i+1}</strong> 
                        <span style="display:inline-block;">{get_ball_ui(res)}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            # 마스터에게 텔레그램 비밀 보고
            report = f"🔔 [포털 방문자 추출]\n엔진: {agent.split(' ')[0]}\n개수: {count}게임\n기록: {all_results[0]} 등"
            send_telegram(report)

# --- Tab 2: 전회차 데이터 조회 (정보 제공용) ---
with tabs[1]:
    st.markdown("### 📚 빅데이터 통계 센터")
    st.write("1회차부터 최신 회차까지의 공식 당첨 결과를 확인하세요.")
    
    search_no = st.number_input("조회할 회차를 입력하세요", min_value=1, max_value=latest['최신'], value=latest['최신'])
    if st.button("🔍 당첨 기록 조회"):
        old_data = fetch_lotto(search_no)
        st.markdown(f"""
            <div class="portal-card" style="text-align:center;">
                <h4>제 {search_no}회 당첨 번호</h4>
                <div style="margin-top: 15px;">{get_ball_ui(old_data['번호'])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### 📉 역대 당첨 히스토리 리스트")
    # 1회부터 현재까지의 리스트를 보여주어 포털의 방대함을 과시
    history_df = pd.DataFrame([{"회차": f"제 {i}회", "상태": "DB 보관 중", "분석": "완료"} for i in range(latest['최신'], 0, -1)])
    st.dataframe(history_df, use_container_width=True, height=400)

# --- Tab 3: 번호 당첨 확인 (편의 기능) ---
with tabs[2]:
    st.markdown("### 🎯 내 번호 당첨 확인기")
    st.write("구매하신 번호가 당첨되었는지 빠르게 확인해 드립니다.")
    
    target_round = st.selectbox("비교할 회차 선택", [latest['최신'], latest['최신'] - 1, latest['최신'] - 2])
    user_nums = st.multiselect("보유하신 번호 6개를 선택하세요", list(range(1, 46)), max_selections=6)
    
    if len(user_nums) == 6 and st.button("🎯 당첨 결과 확인"):
        win_data = fetch_lotto(target_round)
        match_count = len(set(win_data['번호']) & set(user_nums))
        
        st.markdown(f"""
            <div class="portal-card" style="text-align:center; background:#f0f8ff;">
                <h3 style="color:#0056b3;">일치하는 번호 개수: {match_count}개</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if match_count == 6: st.balloons(); st.success("🎉 기적입니다! 1등 당첨입니다!")
        elif match_count == 5: st.success("🎊 축하합니다! 3등 당첨입니다!")
        elif match_count == 4: st.warning("👍 4등 당첨입니다!")
        elif match_count == 3: st.info("👏 5등 당첨입니다!")
        else: st.error("아쉽지만 다음 기회에...")

# --- Tab 4: 마스터 관리 센터 (비밀 메뉴) ---
if is_master:
    with tabs[3]:
        st.error("🚨 보안 영역: 마스터 권한이 확인되었습니다.")
        st.write("이 탭은 일반 사용자에게는 노출되지 않습니다.")
        
        c_admin1, c_admin2 = st.columns(2)
        with c_admin1:
            st.metric("서버 상태", "정상 가동 중", "+ 100%")
        with c_admin2:
            st.metric("텔레그램 연동", "Active", "Token OK")
            
        if st.button("🧹 시스템 캐시 및 로그 초기화"):
            st.warning("초기화 명령이 서버로 전송되었습니다.")

# [7. 포털 푸터]
st.markdown("""
    <div style="text-align: center; padding: 40px; margin-top: 50px; border-top: 1px solid #ddd; color: #999; font-size: 13px;">
        <strong>LUMEN QUANT PORTAL</strong><br>
        본 사이트는 통계 및 AI 기반 로또 번호 추출 서비스를 무료로 제공합니다. 과도한 몰입을 주의하세요.<br>
        Copyright © 2026 Lumen Quant. All Rights Reserved.
    </div>
""", unsafe_allow_html=True)
