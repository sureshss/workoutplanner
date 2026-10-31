import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000/plan"
st.title("Workout planner")

goal = st.selectbox(
    "Fitness goal",
    ["Build muscle", "Lose fat", "General fitness", "Improve endurance"],
)
level = st.selectbox("Experience level", ["Beginner", "Intermediate", "Advanced"])
days = st.slider("Days available per week", min_value=1, max_value=7, value=3)
equipment = st.selectbox(
    "Equipment access",
    ["No equipment", "Home dumbbells", "Full gym"]
)
limitations = st.text_area(
    "Injuries or limitations (optional)",
    placeholder="e.g. bad knees, no overhead pressing",
)

if st.button("Create plan"):
    payload = { 
            "goal":goal,       
            "level": level,
            "days": days,
            "equipment": equipment,
            "limitations": limitations.strip() or None,
        }
    response = httpx.post(API_URL, json=payload, timeout=30)
    
    if response.is_success:
        st.dataframe(response.json(), hide_index=True)
   


