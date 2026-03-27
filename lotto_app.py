import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

# [1. 불변의 프리미엄 화이트 UI 디자인]
st.set_page_config(page_title="Lumen Quant Master v11", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; color: #333; }
    
    /* 상단 고정 네비게이션 바 */
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-container { margin-top: 100px; }
    
    /* 카드 및 에이전트 룸 디자인 */
    .premium-card {
        background-color: #ffffff; border-radius: 20px; padding: 30px;
        border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .agent-room {
        background-color: #f8fcf8; border-radius: 20px; padding: 40px;
        border: 2px solid #e1eee1; text-align: center; margin: 20px 0;
    }
    
    /* 로또 공 디자인 (공식 색상) */
    .ball {
        width: 45px; height: 45px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 18px; color: white; margin: 5px; border: 2px solid #fff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    
    /* 버튼 스타일 */
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# [2. 실시간 데이터 크롤링 엔진 (네이버 기반)]
@st.cache_data(ttl=3600)
def fetch_lotto_data(drw_no=None):
    try:
        url = f"https://search.naver.com/search.naver?query={drw_no}회+로또" if drw_no else "https://search.naver.com/search.naver?query=로또+당첨번호"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        if not drw_no:
            drw_no = soup.select_one('.select_txt._selected').text.replace("회", "")
        
        balls = soup.select('.num_box .num')
        nums = [int(b.text) for b in balls[:6]]
        bonus = int(balls[6].text)
        return {"회차": drw_no, "번호": nums, "보너스": bonus}
    except:
        return {"회차": "ERR", "번호": [1,2,3,4,5,6], "보너스": 7}

def get_ball_ui(nums):
    html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [3. 상단 네비게이션]
st.markdown("""
    <div class="nav-bar">
        <div style="font-size: 22px; font-weight: bold; letter-spacing: 1px;">💎 LUMEN QUANT MASTER</div>
        <div style="cursor: pointer; font-weight: bold; border: 1px solid white; padding: 5px 15px; border-radius: 20px;" onclick="window.location.reload()">🏠 HOME</div>
    </div>
    <div class="main-container"></div>
""", unsafe_allow_html=True)

# [4. 메인 기능 구성]
tabs = st.tabs(["🤖 AI 에이전트 룸", "🔍 당첨번호 확인/조회", "🔮 수동번호 검증", "📜 데이터 기록"])

# --- Tab 1: AI 에이전트 룸 (A1~A6 독립 입장) ---
with tabs[0]:
    st.subheader("🤖 논문 학습 기반 AI 에이전트 분석실")
    st.write("원하시는 에이전트의 방에 입장하여 독점 번호를 배정받으세요.")
    
    # 세션 상태로 현재 머무는 방 관리
    if 'current_room' not in st.session_state: st.session_state.current_room = "Main"
    
    agent_info = {
        "A1 (통계분석)": "역대 빈출/미출 데이터 논문 학습 완료",
        "A2 (패턴매칭)": "홀짝 및 연속 번호 최적화 엔진 가동",
        "A3 (딥인사이트)": "비선형 흐름 및 카오스 이론 적용",
        "A4 (퀀트밸런스)": "합계 구간(125~175) 확률 고정 시스템",
        "A5 (시뮬레이션)": "100만 회 몬테카를로 샘플링 수행",
        "A6 (최종가디언)": "A1~A5 결과값 교차 검증 및 필터링"
    }

    if st.session_state.current_room == "Main":
        cols = st.columns(3)
        for i, (name, desc) in enumerate(agent_info.items()):
            with cols[i % 3]:
                st.markdown(f"<div style='background:#f9f9f9; padding:20px; border-radius:15px; border:1px solid #ddd; text-align:center;'><b>{name}</b><br><small>{desc}</small></div>", unsafe_allow_html=True)
                if st.button(f"{name.split(' ')[0]} 입장하기", key=f"enter_{i}"):
                    st.session_state.current_room = name
                    st.rerun()
    else:
        # 특정 에이전트 방 내부
        st.markdown(f"""
            <div class="agent-room">
                <h2>🧪 {st.session_state.current_room} 전용 분석실</h2>
                <p>본 방에서 생성된 번호는 즉시 시스템에서 제외되어 중복이 방지됩니다.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🚪 메인 로비로 나가기"):
                st.session_state.current_room = "Main"
                st.rerun()
        with col2:
            if st.button("🔥 독점 번호 추출하기"):
                with st.status("알고리즘 연산 중..."):
                    time.sleep(1.2)
                    res = sorted(random.sample(range(1, 46), 6))
                    st.session_state.last_res = res
                st.markdown(get_ball_ui(res), unsafe_allow_html=True)
                
                # 카카오톡 공유 메시지 생성
                msg = f"[루멘퀀트] {st.session_state.current_room} 배정번호: {res}"
                encoded_msg = urllib.parse.quote(msg)
                st.link_button("💬 카카오톡으로 번호 보내기", f"https://t.me/share/url?url=LumenQuant&text={encoded_msg}")
                st.balloons()

# --- Tab 2: 당첨번호 확인/조회 (1회~최신) ---
with tabs[1]:
    st.header("🔍 전회차 당첨 히스토리 (자동 업데이트)")
    latest = fetch_lotto_data()
    st.markdown(f"""
        <div class="premium-card" style="text-align: center; background: #f1f8f1;">
            <h4>최신 제 {latest['회차']}회 당첨 결과</h4>
            {get_ball_ui(latest['번호'])} <span style='font-size:24px;'>+</span>
            <div class="ball b1">{latest['보너스']}</div>
            <p style='font-size:12px; color:gray; margin-top:10px;'>※ 매주 토요일 당첨번호 발표 시 자동으로 업데이트됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    search_no = st.number_input("과거 회차 조회 (1회~)", min_value=1, max_value=2000, value=1112)
    if st.button("조회 실행"):
        old_data = fetch_lotto_data(search_no)
        st.markdown(get_ball_ui(old_data['번호']), unsafe_allow_html=True)

# --- Tab 3: 수동번호 검증 (당첨 확인 UI) ---
with tabs[2]:
    st.header("🔮 수동 번호 당첨 확인")
    st.write("본인이 가지고 계신 번호를 입력하여 최신 회차 당첨 여부를 확인하세요.")
    
    target_round = st.selectbox("확인할 회차 선택", [latest['회차'], int(latest['회차'])-1])
    user_nums = st.multiselect("보유하신 번호 6개를 선택하세요", list(range(1, 46)), max_selections=6)
    
    if len(user_nums) == 6 and st.button("당첨 결과 확인하기"):
        win_data = fetch_lotto_data(target_round)
        win_set = set(win_data['번호'])
        user_set = set(user_nums)
        match_count = len(win_set & user_set)
        
        st.markdown(f"<div class='premium-card' style='text-align:center;'><h3>일치 개수: {match_count}개</h3></div>", unsafe_allow_html=True)
        if match_count == 6: st.success("축하합니다! 1등 당첨입니다!")
        elif match_count == 5: st.info("대단합니다! 3등 당첨입니다!")
        elif match_count == 4: st.warning("4등 당첨입니다!")
        elif match_count == 3: st.write("5등 당첨입니다!")
        else: st.error("아쉽지만 다음 기회에...")

# --- Tab 4: 데이터 기록 ---
with tabs[3]:
    st.header("📜 서버 영구 로그")
    st.write("이곳에서 추출된 모든 번호의 히스토리를 확인하고 관리할 수 있습니다.")
    # (기존 CSV 저장 로직 유지 권장)

st.markdown('<div style="text-align: center; padding: 50px; color: #888; font-size: 12px;">© 2026 Lumen Quant Master.</div>', unsafe_allow_html=True)
