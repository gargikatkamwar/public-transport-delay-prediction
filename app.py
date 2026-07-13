import streamlit as st
import pandas as pd
import joblib

model = joblib.load("transit_delay_model.pkl")
columns = joblib.load("columns.pkl")

st.title("Public Transport Delay Predictor")
st.write("Predict expected delay based on route, time, and conditions")

route = st.selectbox("Route", [f"Route-{i}" for i in range(1,11)])
hour = st.slider("Hour of Day", 5, 22, 9)
day_of_week = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
weather = st.selectbox("Weather", ["Clear","Rain","Fog","Storm"])
traffic_level = st.slider("Traffic Level (1=Low, 10=High)", 1, 10, 5)

day_map = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}
day_num = day_map[day_of_week]
is_weekend = 1 if day_num >= 5 else 0
is_rush_hour = 1 if hour in [8,9,17,18,19] else 0

if st.button("Predict Delay"):
    input_df = pd.DataFrame([{
        "Hour": hour,
        "DayOfWeek": day_num,
        "IsWeekend": is_weekend,
        "IsRushHour": is_rush_hour,
        "TrafficLevel": traffic_level,
        f"Route_{route}": 1,
        f"Weather_{weather}": 1
    }]).reindex(columns=columns, fill_value=0)

    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Delay: {prediction:.1f} minutes")
