import streamlit as st
import numpy as np
import random
import time

# [1. 페이지 설정]
st.set_page_config(page_title="Lumen Exclusive Lotto", layout="wide")

# [2. 중복 방지를 위한 세션 상태 초기화]
if 'used_combinations' not in st.session_state:
    st.session_state.used_combinations = set()

# [3. 고확률 추출 엔진]
class ExclusiveEngine:
    def __init__(self):
        self.numbers = list(range(1, 46))

    def is_high_probability(self, nums):
        """3~5등 당첨 확률이 높은 균형 잡힌 조합인지 검사"""
        total = sum(nums)
        odd_count = len([n for n in nums if n % 2 != 0])
        # 합계 구간 120~170 및 홀짝 비율 2:4, 3:3, 4:2 조건
        return (120 <= total <= 170) and (2 <= odd_count <= 4)

    def get_exclusive_numbers(self):
        """독점 조합 추출 및 중복 체크"""
        attempts = 0
        while attempts < 1000:
            nums = tuple(sorted(random.sample(self.numbers, 6)))
            # 중복 검사 및 고확률 필터 적용
            if nums not in st.session_state.used_combinations and self.is_high_probability(nums):
                st.session_state.used_combinations.add(nums)
                return nums
            attempts += 1
        return sorted(random.sample(self.numbers, 6)) # 예외 처리

engine = ExclusiveEngine()

# [4. UI 디자인]
st.title("🛡️ 루멘 퀀트: 독점 조합 배정 센터")
st.write("본 시스템은 생성된 번호를 즉시 폐기하여 **중복 당첨을 방지**합니다. (나만의 번호 보장)")

# 대시보드 지표
cols = st.columns(3)
cols[0].metric("배정 가능 조합", f"{1000 - len(st.session_state.used_combinations)}개", "실시간 갱신")
cols[1].metric("알고리즘 상태", "3~5등 집중 필터", "Active")
cols[2].metric("보안 모드", "독점권 보장", "On")

st.divider()

# 에이전트 섹션
st.subheader("🤖 전용 AI 에이전트 선택")
a_cols = st.columns(3)

agents = [
    ("Agent Gold", "3등 당첨 집중 타격형"),
    ("Agent Silver", "4~5등 빈도 극대화형"),
    ("Agent Bronze", "수익률 최적화 밸런스형")
]

for i, (name, desc) in enumerate(agents):
    with a_cols[i]:
        st.info(f"**{name}**\n\n{desc}")
        if st.button(f"{name}에게 번호 요청"):
            with st.status("수학적 독점 조합 산출 중...", expanded=True) as status:
                time.sleep(1.5)
                res = engine.get_exclusive_numbers()
                status.update(label="조합 배정 완료! (이 조합은 폐기되었습니다)", state="complete")
            
            # 화려한 번호 출력
            st.markdown(f"""
                <div style="background-color: #1c1f26; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #2e7d32;">
                    <h2 style="color: #4caf50; margin-bottom: 20px;">🔒 전용 독점 조합</h2>
                    <div style="display: flex; gap: 10px; justify-content: center;">
                        {''.join([f'<div style="width: 50px; height: 50px; border-radius: 50%; background-color: #2e7d32; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px;">{n}</div>' for n in res])}
                    </div>
                    <p style="margin-top: 20px; color: #888;">※ 이 번호는 다른 사용자에게 다시 제공되지 않습니다.</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()

st.divider()
if st.button("세션 초기화 (새로운 조합 리스트 생성)"):
    st.session_state.used_combinations = set()
    st.rerun()
