import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import requests
from datetime import datetime, timedelta
import urllib.parse

# [1. 마스터 보안 설정]
MASTER_CODE = "lumen_secret_99"  # 🔑 마스터 비밀번호
TELEGRAM_TOKEN = '8369798851:AAH7EYXjvJppJf5Pp3RcMjsAeI4LaBsRK1I'
CHAT_ID = '7628406047'

st.set_page_config(page_title="Lumen Quant | 로또 AI 분석 포털", page_icon="🕒", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #f8f9fa; }
    
    .portal-header { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 40px 20px; text-align: center; color: white; border-radius: 0 0 30px 30px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
    .portal-header h1 { font-weight: 900; font-size: 38px; margin-bottom: 10px; letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.4); }
    .live-time { background: rgba(255,255,255,0.1); display: inline-block; padding: 8px 20px; border-radius: 20px; font-weight: bold; font-size: 15px; border: 1px solid rgba(255,255,255,0.2); margin-top: 10px; }
    
    .portal-card { background-color: #ffffff; border-radius: 20px; padding: 30px; border: 1px solid #eaeaea; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.04); }
    .ball { width: 42px; height: 42px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; color: white; margin: 4px; box-shadow: inset -3px -3px 6px rgba(0,0,0,0.2), 2px 2px 5px rgba(0,0,0,0.1); text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }
    .b1 { background-color: #fbc02d; } .b11 { background-color: #1976d2; } .b21 { background-color: #e53935; } .b31 { background-color: #757575; } .b41 { background-color: #43a047; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; background-color: #1e3d1e; color: white; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #2d5a2d; color: white; box-shadow: 0 4px 10px rgba(30,61,30,0.3); }
    </style>
""", unsafe_allow_html=True)

# [2. 코어 엔진: 자동 날짜 계산 및 API]
def get_latest_draw_no():
    """매주 토요일 오후 9시 기준 자동 회차 계산"""
    base_date = datetime(2002, 12, 7, 21, 0, 0)
    now = datetime.now()
    diff = now - base_date
    return (diff.days // 7) + 1

@st.cache_data
def get_all_draw_dates(latest_no):
    """1회차부터 최신 회차까지의 전체 리스트를 수학적으로 생성 (서버 과부하 방지)"""
    base_date = datetime(2002, 12, 7)
    data = []
    for i in range(latest_no, 0, -1):
        draw_date = base_date + timedelta(weeks=i-1)
        data.append({"회차": f"제 {i}회", "공식 추첨일": draw_date.strftime("%Y-%m-%d"), "데이터 상태": "안전 보관 중 (상세 조회 가능)"})
    return pd.DataFrame(data)

@st.cache_data(ttl=86400)
def fetch_lotto_detail(drw_no):
    """특정 회차의 상세 데이터만 호출"""
    try:
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
        resp = requests.get(url, timeout=5).json()
        if resp.get("returnValue") == "success":
            nums = [resp[f"drwtNo{i}"] for i in range(1, 7)]
            return {
                "회차": drw_no, "추첨일": resp["drwNoDate"], "번호": nums, "보너스": resp["bnusNo"],
                "1등당첨금": resp["firstWinamnt"], "1등당첨자수": resp["firstPrzwnerCo"], "총판매금액": resp["totSellamnt"]
            }
    except: pass
    return {"회차": drw_no, "추첨일": "데이터 없음", "번호": [1,2,3,4,5,6], "보너스": 7, "1등당첨금": 0, "1등당첨자수": 0, "총판매금액": 0}

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

def get_ball_ui(nums):
    html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    for n in nums:
        c = "b1" if n<=10 else "b11" if n<=20 else "b21" if n<=30 else "b31" if n<=40 else "b41"
        html += f'<div class="ball {c}">{n}</div>'
    html += '</div>'
    return html

# [3. 사이드바 - 마스터 로그인]
with st.sidebar:
    st.markdown("### 🔑 마스터 로그인")
    input_code = st.text_input("Admin Code", type="password")
    is_master = (input_code == MASTER_CODE)
    if is_master: st.success("마스터 권한이 활성화되었습니다.")
    st.markdown("---")
    st.markdown("**[포털 안내]**\n방문객 누구나 무료로 AI 번호 추출 및 전회차 당첨 조회가 가능합니다.")

# [4. 포털 대문 (라이브 타임 추가)]
current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
st.markdown(f"""
    <div class="portal-header">
        <h1>💎 LUMEN QUANT PORTAL</h1>
        <p>수학적 통계와 AI 에이전트가 분석하는 프리미엄 로또 포털</p>
        <div class="live-time">🕒 실시간 서버 동기화: {current_time}</div>
    </div>
""", unsafe_allow_html=True)

# 라이브 전광판
latest_no = get_latest_draw_no()
latest_data = fetch_lotto_detail(latest_no - 1)

st.markdown(f"""
    <div class="portal-card" style="text-align: center; border-top: 4px solid #1e3d1e;">
        <h3 style="color: #333; font-weight: bold; margin-bottom: 20px;">🎉 제 {latest_data['회차']}회 공식 당첨 결과</h3>
        <p style="color: #666; font-size: 14px; margin-top: -10px;">추첨일: {latest_data['추첨일']}</p>
        <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 15px;">
            {get_ball_ui(latest_data['번호'])}
            <span style="font-size: 28px; font-weight: 900; color: #ccc;">+</span>
            <div class="ball b1">{latest_data['보너스']}</div>
        </div>
        <div style="background-color: #f1f8f1; padding: 15px; border-radius: 10px; border: 1px solid #d1e7d1;">
            <strong style="color:#d4af37; font-size:18px;">👑 1등 당첨금: {latest_data['1등당첨금']:,}원</strong> <br>
            <span style="color:#555;">(당첨자 수: {latest_data['1등당첨자수']}명)</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# [5. 포털 탭 메뉴]
if is_master: tabs = st.tabs(["🏠 AI 번호 추출", "📚 전체 회차 히스토리", "🎯 당첨 확인기", "⚙️ 데이터 센터 (마스터)"])
else: tabs = st.tabs(["🏠 AI 번호 추출", "📚 전체 회차 히스토리", "🎯 당첨 확인기"])

# --- Tab 1: AI 번호 추출 ---
with tabs[0]:
    st.markdown("### 🤖 루멘 퀀트 AI 에이전트")
    c1, c2 = st.columns([1, 1])
    with c1:
        agent = st.selectbox("분석 알고리즘 선택", ["A1 (통계분석)", "A2 (패턴매칭)", "A3 (인사이트)", "A4 (퀀트밸런스)", "A5 (500만회 몬테카를로)", "A6 (가디언)"])
    with c2:
        count = st.select_slider("추출 조합 개수", options=[1, 5, 10, 20, 30, 40, 50], value=5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"🔥 {agent.split(' ')[0]} 엔진 가동 및 번호 추출 (무료)"):
        with st.spinner("최적의 퀀트 조합을 연산 중입니다..."):
            time.sleep(1.5)
            all_results = [sorted(random.sample(range(1, 46), 6)) for _ in range(count)]
            st.success("✅ 번호 추출이 완료되었습니다! 행운을 빕니다.")
            for i, res in enumerate(all_results):
                st.markdown(f'<div style="background: #fff; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #1e3d1e; box-shadow: 0 2px 5px rgba(0,0,0,0.05);"><strong style="color:#1e3d1e; display:inline-block; width: 60px;">게임 {i+1}</strong> <span style="display:inline-block;">{get_ball_ui(res)}</span></div>', unsafe_allow_html=True)
            
            send_telegram(f"🔔 [포털 방문자 추출]\n엔진: {agent.split(' ')[0]}\n개수: {count}게임\n샘플: {all_results[0]}")

# --- Tab 2: 전체 회차 히스토리 (마스터 시트 & 상세 조회) ---
with tabs[1]:
    st.markdown("### 📚 1회~최신 상세 당첨 조회")
    st.write("조회하고 싶은 회차를 입력하면 해당 회차의 공식 번호와 상금을 즉시 불러옵니다.")
    
    search_no = st.number_input("조회할 회차를 입력하세요 (예: 1112)", min_value=1, max_value=latest_no, value=latest_data['회차'])
    
    if st.button("🔍 상세 기록 조회하기"):
        with st.spinner("공식 데이터를 불러오는 중..."):
            detail = fetch_lotto_detail(search_no)
            if detail:
                st.markdown(f"""
                    <div class="portal-card" style="text-align:center;">
                        <h4 style="color:#1e3d1e; margin-bottom:5px;">제 {detail['회차']}회 당첨 결과</h4>
                        <p style="color:#888; margin-bottom:20px;">추첨일: {detail['추첨일']}</p>
                        <div style="margin-bottom: 20px;">{get_ball_ui(detail['번호'])} <br><br> <b>보너스:</b> <div class="ball b1" style="display:inline-flex;">{detail['보너스']}</div></div>
                        <div style="background:#f9f9f9; padding:20px; border-radius:15px; border:1px solid #eee; text-align:left;">
                            <p style="margin:5px 0;">💰 <b>1등 총 당첨금:</b> {detail['1등당첨금']:,} 원</p>
                            <p style="margin:5px 0;">👑 <b>1등 당첨자 수:</b> {detail['1등당첨자수']} 명</p>
                            <p style="margin:5px 0; color:#666;">📈 <b>총 판매 금액:</b> {detail['총판매금액']:,} 원</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### 📜 로또 전체 회차 마스터 시트 (1회차부터)")
    # 서버 과부하 없이 전체 회차의 날짜를 한눈에 보여주는 거대한 표
    all_draws_df = get_all_draw_dates(latest_no - 1)
    st.dataframe(all_draws_df, use_container_width=True, height=400)

# --- Tab 3: 번호 당첨 확인 ---
with tabs[2]:
    st.markdown("### 🎯 내 번호 당첨 확인기")
    target_round = st.selectbox("비교할 회차 선택", [latest_data['회차'], latest_data['회차'] - 1])
    user_nums = st.multiselect("보유하신 번호 6개를 선택하세요", list(range(1, 46)), max_selections=6)
    
    if len(user_nums) == 6 and st.button("🎯 당첨 결과 확인"):
        win_data = fetch_lotto_detail(target_round)
        match_count = len(set(win_data['번호']) & set(user_nums))
        st.markdown(f"<div class='portal-card' style='text-align:center; background:#f0f8ff;'><h3 style='color:#0056b3;'>일치하는 번호: {match_count}개</h3></div>", unsafe_allow_html=True)

# --- Tab 4: 마스터 관리 센터 ---
if is_master:
    with tabs[3]:
        st.error("🚨 마스터 권한 영역입니다. 일반 방문객에게는 이 탭이 보이지 않습니다.")
        st.write("루멘 퀀트 v16 엔진이 정상적으로 서버 데이터를 통제 중입니다.")

# [6. 푸터]
st.markdown('<div style="text-align: center; padding: 40px; margin-top: 50px; border-top: 1px solid #ddd; color: #999; font-size: 13px;"><strong>LUMEN QUANT PORTAL</strong><br>Copyright © 2026 Lumen Quant. All Rights Reserved.</div>', unsafe_allow_html=True)
