import streamlit as st

st.set_page_config(page_title="운동 플래너", layout="wide")

# 스타일 설정
st.markdown("""
    <style>
    .stMultiSelect div div div div { font-size: 14px; }
    h3 { color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("운동 스케쥴")

# --- 운동 데이터 설정 ---
exercise_data = {
    "하체": ["BSS", "RDL", "Single RDL", "Hip thrust", "Goblet Squat", "Leg extension", "Reverse lunge", "Sumo Squat", "Smith machine", "Cable kick back", "Step up"],
    "상체": {
        "어깨": ["Lateral raises", "Front raises", "Upright rows", "Military press"],
        "등": ["Wide grip lat pull down", "Seated row", "Seated face pull", "Cable seated one arm pull", "Bent over barbell row", "Lat pull down", "Pull over"],
        "팔": ["Cable one arm biceps curl", "Dumbbell hammer curl"]
    },
    "복근": ["A", "B", "C", "D", "E"]
}

schedule = {
    "월요일": "하체", "화요일": "휴식", "수요일": "상체", "목요일": "복근", "금요일": "하체", "토요일": "상체", "일요일": "휴식"
}

# --- 사이드바: 운동 선택 ---
st.sidebar.header("운동 선택")
selected_plan = {}

for day, target in schedule.items():
    if target == "휴식":
        selected_plan[day] = ["휴식"]
    elif target == "상체":
        st.sidebar.subheader(f"{day}")
        shoulder = st.sidebar.multiselect(f"어깨", exercise_data["상체"]["어깨"], key=f"{day}_sh")
        back = st.sidebar.multiselect(f"등", exercise_data["상체"]["등"], key=f"{day}_bk")
        arms = st.sidebar.multiselect(f"팔", exercise_data["상체"]["팔"], key=f"{day}_ar")
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
        color = "#E74C3C" if target_part == "하체" else "#3498DB" if target_part == "상체" else "#27AE60" if target_part == "복근" else "#95A5A6"
        st.markdown(f"<p style='color:{color}; font-weight:bold;'>[{target_part}]</p>", unsafe_allow_html=True)

        if selected_plan[day_name]:
            for ex in selected_plan[day_name]:
                st.write(f"• {ex}")
        else:
            st.write("---")

#------------------------------------
import urllib
print("Password/Enpoint IP for localtunnel is:", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())

