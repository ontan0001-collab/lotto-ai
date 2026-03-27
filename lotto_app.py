import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

# [1. 프리미엄 화이트 UI & 카카오톡 전용 스크립트]
st.set_page_config(page_title="Lumen Quant Master v11.8", page_icon="💎", layout="wide")

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
        background-color: #ffffff; border-radius: 20px; padding: 25px;
        border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .ball {
        width: 35px; height: 35px; border-radius: 50%; display: inline-flex; 
        align-items: center; justify-content: center; font-weight: bold; 
        font-size: 14px; color: white; margin: 3px; border: 1px solid #fff;
    }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; }
    .b21 { background-color: #e53935; } .b31 { background-color: #757575; }
    .b41 { background-color: #43a047; }
    
    .kakao-link-btn {
        display: block; width: 100%; padding: 15px; background-color: #FEE500;
        color: #191919 !important; text-align: center; text-decoration: none; font-weight: bold;
        border-radius: 25px; font-size: 16px; margin-top: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# [2. 데이터 엔진]
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

def get_ball_html(nums):
    html = '<div style="display: flex; justify-content: start; flex-wrap: wrap;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [3. 상단 내비게이션]
st.markdown('<div class="nav-bar"><div style="font-size: 22px; font-weight: bold;">💎 LUMEN QUANT MASTER</div></div><div class="main-container"></div>', unsafe_allow_html=True)

# [4. 데이터 기록]
DB_FILE = "lotto_master_db.csv"
def save_to_db(agent, nums_list):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [[now, agent, str(nums)] for nums in nums_list]
    df = pd.DataFrame(data, columns=['Time', 'Agent', 'Numbers'])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False, mode='w', encoding='utf-8-sig')
    else: df.to_csv(DB_FILE, index=False, mode='a', header=False, encoding='utf-8-sig')

# [5. 메인 기능]
tabs = st.tabs(["🤖 AI 에이전트 룸", "📜 전회차 히스토리", "🔍 상세 조회"])

with tabs[0]:
    if 'current_room' not in st.session_state: st.session_state.current_room = "Main"
    agents = ["A1 (통계분석)", "A2 (패턴매칭)", "A3 (인사이트)", "A4 (퀀트밸런스)", "A5 (시뮬레이션)", "A6 (최종가디언)"]

    if st.session_state.current_room == "Main":
        st.subheader("🤖 연구실 선택")
        cols = st.columns(3)
        for i, name in enumerate(agents):
            with cols[i % 3]:
                if st.button(f"{name.split(' ')[0]} 입장"):
                    st.session_state.current_room = name
                    st.rerun()
    else:
        st.markdown(f"<div class='agent-room'><h3>🧪 {st.session_state.current_room} 연구실</h3></div>", unsafe_allow_html=True)
        
        # 조합 개수 선택 (10개 단위 요청 반영)
        count_option = st.select_slider("추출할 조합 개수를 선택하세요", options=[1, 10, 20, 30, 40, 50], value=10)
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("🚪 로비로 나가기"): 
                st.session_state.current_room = "Main"
                st.rerun()
        with c2:
            if st.button(f"🔥 {count_option}개 조합 동시 추출"):
                all_res = [sorted(random.sample(range(1, 46), 6)) for _ in range(count_option)]
                save_to_db(st.session_state.current_room, all_res)
                
                # 결과 출력
                msg_content = f"[{st.session_state.current_room} 추천번호]\n"
                for idx, res in enumerate(all_res):
                    st.markdown(f"**조합 {idx+1}**")
                    st.markdown(get_ball_html(res), unsafe_allow_html=True)
                    msg_content += f"{idx+1}세트: {', '.join(map(str, res))}\n"
                
                # [카카오톡 전송 최종 해결책]
                encoded_msg = urllib.parse.quote(msg_content)
                # 모바일 인텐트 방식: 설치된 카카오톡 앱을 직접 호출 (API 키 불필요)
                kakao_intent = f"kakaolink://send?text={encoded_msg}"
                
                st.markdown(f"""
                    <div style="margin-top:20px; padding:15px; background:#fffbe6; border:1px solid #ffe58f; border-radius:15px;">
                        <p style="margin-bottom:10px; font-weight:bold;">📲 카카오톡 전송 방법 (선택)</p>
                        <a href="kakaotalk://send?text={encoded_msg}" class="kakao-link-btn">1. 카카오톡 앱으로 바로 보내기</a>
                        <div class="kakao-link-btn" style="background:#eeeeee;" onclick="navigator.clipboard.writeText('{msg_content}'); alert('번호가 복사되었습니다! 카톡창에 붙여넣으세요.');">2. 전체 번호 복사하기</div>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()

with tabs[1]:
    latest_info = fetch_lotto_data()
    st.header(f"📜 전회차 히스토리 (1회 ~ {latest_info['최신']}회)")
    history_list = [{"회차": i, "분석상태": "완료"} for i in range(latest_info['최신'], 0, -1)]
    st.dataframe(pd.DataFrame(history_list), use_container_width=True, height=400)

with tabs[2]:
    search_no = st.number_input("조회 회차", min_value=1, max_value=latest_info['최신'], value=latest_info['최신'])
    if st.button("조회"):
        old = fetch_lotto_data(search_no)
        st.markdown(f"<div class='premium-card' style='text-align:center;'><h4>제 {search_no}회</h4>{get_ball_html(old['번호'])}</div>", unsafe_allow_html=True)
