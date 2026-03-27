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
st.set_page_config(page_title="Lumen Quant Master v11.7", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #ffffff; color: #333; }
    
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #1e3d1e; 
        padding: 15px 50px; color: white; display: flex; justify-content: space-between;
        align-items: center; z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-container { margin-top: 100px; }
    .premium-card {
        background-color: #ffffff; border-radius: 20px; padding: 30px;
        border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .agent-room {
        background-color: #f8fcf8; border-radius: 20px; padding: 40px;
        border: 2px solid #e1eee1; text-align: center; margin: 20px 0;
    }
    .ball {
        width: 45px; height: 45px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 18px; color: white; margin: 5px; border: 2px solid #fff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    
    /* 카카오톡 노란색 버튼 커스텀 스타일 */
    .kakao-send-btn {
        display: block; width: 100%; padding: 15px; background-color: #FEE500;
        color: #191919 !important; text-align: center; text-decoration: none; font-weight: bold;
        border-radius: 25px; font-size: 18px; margin-top: 20px; border: none;
    }
    .kakao-send-btn:hover { background-color: #fada00; }
    </style>
""", unsafe_allow_html=True)

# [2. 데이터 엔진: 네이버 실시간 크롤링]
@st.cache_data(ttl=3600)
def fetch_lotto_data(drw_no=None):
    try:
        url = f"https://search.naver.com/search.naver?query={drw_no}회+로또" if drw_no else "https://search.naver.com/search.naver?query=로또+당첨번호"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
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

# [3. 상단 내비게이션]
st.markdown("""
    <div class="nav-bar">
        <div style="font-size: 22px; font-weight: bold; letter-spacing: 1px;">💎 LUMEN QUANT MASTER</div>
        <div style="cursor: pointer; font-weight: bold; border: 1px solid white; padding: 5px 15px; border-radius: 20px;" onclick="window.location.reload()">🏠 HOME</div>
    </div>
    <div class="main-container"></div>
""", unsafe_allow_html=True)

# [4. 데이터 영구 기록]
DB_FILE = "lotto_master_db.csv"
def save_to_db(agent, nums):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[now, agent, str(nums)]], columns=['Time', 'Agent', 'Numbers'])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else: df.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

# [5. 메인 탭]
tabs = st.tabs(["🤖 AI 에이전트 룸", "📜 전회차 히스토리", "🔍 상세 조회", "🔮 수동 검증"])

# --- Tab 1: AI 룸 & 확실한 카카오톡 전송 ---
with tabs[0]:
    if 'current_room' not in st.session_state: st.session_state.current_room = "Main"
    agents = ["A1 (통계분석)", "A2 (패턴매칭)", "A3 (인사이트)", "A4 (퀀트밸런스)", "A5 (시뮬레이션)", "A6 (최종가디언)"]

    if st.session_state.current_room == "Main":
        st.subheader("🤖 전용 AI 에이전트 선택")
        cols = st.columns(3)
        for i, name in enumerate(agents):
            with cols[i % 3]:
                if st.button(f"{name.split(' ')[0]} 입장", key=f"enter_{i}"):
                    st.session_state.current_room = name
                    st.rerun()
    else:
        st.markdown(f"<div class='agent-room'><h2>🧪 {st.session_state.current_room} 연구실</h2></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("🚪 로비로 나가기"): 
                st.session_state.current_room = "Main"
                st.rerun()
        with c2:
            if st.button("🔥 독점 번호 추출"):
                res = sorted(random.sample(range(1, 46), 6))
                save_to_db(st.session_state.current_room, res)
                st.session_state.last_res = res
                st.markdown(get_ball_ui(res), unsafe_allow_html=True)
                
                # [수정된 카카오톡 공유 방식]
                share_text = f"🛡️ 루멘퀀트 배정번호: {res}"
                # 별도의 앱키 없이 모바일 시스템 공유 기능을 활용하는 가장 안정적인 링크
                whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}" # 대안
                sms_url = f"sms:?body={urllib.parse.quote(share_text)}" # 문자 대안
                
                # 카톡으로 바로 보내기 버튼 (URL 복사 방식 병행)
                st.markdown(f"""
                    <a href="https://t.me/share/url?url=LumenQuant&text={urllib.parse.quote(share_text)}" target="_blank" class="kakao-send-btn" style="background-color: #0088cc; color: white !important;">💬 텔레그램으로 번호 보내기</a>
                    <a href="https://www.facebook.com/sharer/sharer.php?u=LumenQuant&quote={urllib.parse.quote(share_text)}" target="_blank" class="kakao-send-btn" style="background-color: #4267B2; color: white !important;">💬 페이스북으로 번호 보내기</a>
                    <div style="background-color: #FEE500; padding: 15px; border-radius: 25px; text-align: center; margin-top: 10px; color: #191919; font-weight: bold; cursor: pointer;" onclick="navigator.clipboard.writeText('{share_text}'); alert('번호가 복사되었습니다! 카카오톡에 붙여넣기 하세요.');">
                        💬 번호 복사해서 카톡에 붙여넣기
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()

# --- Tab 2: 전회차 히스토리 ---
with tabs[1]:
    latest_info = fetch_lotto_data()
    st.header(f"📜 전회차 히스토리 (1회 ~ {latest_info['최신']}회)")
    history_list = [{"회차": i, "상태": "연산 완료"} for i in range(latest_info['최신'], 0, -1)]
    st.dataframe(pd.DataFrame(history_list), use_container_width=True, height=500)

# --- Tab 3: 상세 조회 ---
with tabs[2]:
    search_no = st.number_input("조회 회차", min_value=1, max_value=latest_info['최신'], value=latest_info['최신'])
    if st.button("조회 실행"):
        old = fetch_lotto_data(search_no)
        st.markdown(f"<div class='premium-card' style='text-align:center;'>{get_ball_ui(old['번호'])}</div>", unsafe_allow_html=True)

# --- Tab 4: 수동 검증 ---
with tabs[3]:
    latest_no = latest_info['최신']
    target_round = st.selectbox("확인 회차", [latest_no, latest_no - 1])
    user_nums = st.multiselect("보유 번호", list(range(1, 46)), max_selections=6)
    if len(user_nums) == 6 and st.button("확인"):
        win_data = fetch_lotto_data(target_round)
        match = len(set(win_data['번호']) & set(user_nums))
        st.markdown(f"<div class='premium-card' style='text-align:center;'><h3>일치: {match}개</h3></div>", unsafe_allow_html=True)
