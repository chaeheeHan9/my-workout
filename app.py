import streamlit as st

st.set_page_config(page_title="🏋️ Planner", layout="wide")

# --- 세션 상태 초기화 ---
# multiselect의 선택값들을 개별적으로 저장하기 위해 session_state를 위젯 키와 연결합니다.
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True

# --- 리셋 함수 (에러 수정) ---
def reset_plan():
    # 모든 위젯 키에 해당하는 값을 비웁니다.
    for key in st.session_state.keys():
        if any(day in key for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            st.session_state[key] = []
    # st.rerun()은 콜백 함수(on_click) 내에서 호출해도 되지만, 
    # 최신 버전에서는 자동으로 새로고침되므로 생략하거나 아래처럼 별도로 처리합니다.

# 스타일 설정
st.markdown("""
    <style>
    .stMultiSelect div div div div { font-size: 14px; }
    h3 { color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Schedule")

# --- 운동 데이터 설정 ---
exercise_data = {
    "Lower Body": ["BSS", "RDL", "Single RDL", "Hip thrust", "Goblet Squat", "Leg extension", "Reverse lunge", "Sumo Squat", "Smith machine", "Cable kick back", "Step up"],
    "Upper Body": {
        "Shoulders": ["Lateral raises", "Front raises", "Upright rows", "Military press"],
        "Back": ["Wide grip lat pull down", "Seated row", "Seated face pull", "Cable seated one arm pull", "Bent over barbell row", "Lat pull down", "Pull over"],
        "Arms": ["Cable one arm biceps curl", "Dumbbell hammer curl"]
    },
    "Abs": ["A", "B", "C", "D", "E"]
}

schedule = {
    "Mon": "Lower Body", "Tue": "Break", "Wed": "Upper Body", "Thu": "Abs", "Fri": "Lower Body", "Sat": "Upper Body", "Sun": "Break"
}

# --- 사이드바: 운동 선택 ---
st.sidebar.header("Choose your exercise")
selected_plan = {}

for day, target in schedule.items():
    if target == "Break":
        selected_plan[day] = []
    elif target == "Upper Body":
        st.sidebar.subheader(f"{day}")
        # default 인자에 session_state를 연결하여 새로고침 시에도 유지되게 합니다.
        shoulder = st.sidebar.multiselect(f"Shoulders", exercise_data["Upper Body"]["Shoulders"], key=f"{day}_sh")
        back = st.sidebar.multiselect(f"Back", exercise_data["Upper Body"]["Back"], key=f"{day}_bk")
        arms = st.sidebar.multiselect(f"Arms", exercise_data["Upper Body"]["Arms"], key=f"{day}_ar")
        selected_plan[day] = shoulder + back + arms
    else:
        st.sidebar.subheader(f"{day}")
        selected_plan[day] = st.sidebar.multiselect(f"{target}", exercise_data[target], key=day)

# --- 메인 화면: 7일 캘린더 ---
cols = st.columns(7)
days = list(schedule.keys())

for i, col in enumerate(cols):
    day_name = days[i]
    with col:
        target_part = schedule[day_name]
        st.markdown(f"### {day_name}")
        color = "#CF3275" if target_part == "Lower Body" else "#32CF3C" if target_part == "Upper Body" else "#32C5CF" if target_part == "Abs" else "#545454"
        st.markdown(f"<p style='color:{color}; font-weight:bold;'>[{target_part}]</p>", unsafe_allow_html=True)

        if selected_plan[day_name]:
            for ex in selected_plan[day_name]:
                st.write(f"• {ex}")
        else:
            st.write("")

# --- 하단 컨트롤 버튼 ---
st.sidebar.markdown("---")
# on_click에서 reset_plan을 호출하도록 유지하되 내부 에러가 없도록 수정되었습니다.
if st.sidebar.button("🗑️ Reset", on_click=reset_plan):
    st.sidebar.warning("Reset Complete")
