import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from database import create_table, insert_data

st.set_page_config(
    page_title="Fire Detection Control Center",
    page_icon="🔥",
    layout="wide"
)

create_table()

# ---------- Custom Styling ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main {
    background: linear-gradient(135deg, #020617, #0f172a);
}

.dashboard-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #f8fafc;
}

.dashboard-subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

.card {
    background: rgba(30,41,59,0.85);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    text-align: center;
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
}

.card h1 {
    font-size: 42px;
}

.alert-box {
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: white;
}

.safe {
    background: linear-gradient(135deg,#15803d,#22c55e);
}

.warning {
    background: linear-gradient(135deg,#b45309,#f59e0b);
}

.danger {
    background: linear-gradient(135deg,#991b1b,#ef4444);
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("⚙ System Settings")
speed = st.sidebar.slider("Refresh Speed", 1, 5, 1)
gas_threshold = st.sidebar.slider("Gas Threshold", 500, 1000, 700)
temp_threshold = st.sidebar.slider("Temperature Threshold", 40, 100, 70)

# ---------- Header ----------
st.markdown('<div class="dashboard-title">🔥 Fire Detection Control Center</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">AI Powered Smart Monitoring Dashboard</div>', unsafe_allow_html=True)

# ---------- Functions ----------
def generate_data():
    gas = random.randint(100, 1000)
    temp = random.randint(20, 100)
    flame = random.choice(["YES", "NO"])
    return gas, temp, flame

def detect_status(gas, temp, flame):
    if gas > gas_threshold or temp > temp_threshold or flame == "YES":
        return "DANGER"
    elif gas > gas_threshold - 150:
        return "WARNING"
    return "SAFE"

placeholder = st.empty()
data = []

for i in range(50):

    gas, temp, flame = generate_data()
    status = detect_status(gas, temp, flame)

    timestamp = datetime.now().strftime("%H:%M:%S")

    insert_data(timestamp, gas, temp, flame, status)

    data.append({
        "Time": timestamp,
        "Gas": gas,
        "Temperature": temp,
        "Flame": flame,
        "Status": status
    })

    df = pd.DataFrame(data)

    with placeholder.container():

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="card">
                <h3>⛽ Gas Level</h3>
                <h1>{gas}</h1>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="card">
                <h3>🌡 Temperature</h3>
                <h1>{temp}°C</h1>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="card">
                <h3>🔥 Flame</h3>
                <h1>{flame}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        if status == "DANGER":
            st.markdown('<div class="alert-box danger">🚨 CRITICAL THREAT DETECTED</div>', unsafe_allow_html=True)
        elif status == "WARNING":
            st.markdown('<div class="alert-box warning">⚠ WARNING ZONE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box safe">✅ ALL SYSTEMS NORMAL</div>', unsafe_allow_html=True)

        st.write("")

        left, right = st.columns([2,1])

        with left:
            st.subheader("📈 Sensor Analytics")
            st.area_chart(df[["Gas", "Temperature"]])

        with right:
            st.subheader("📊 Status Overview")
            st.bar_chart(df["Status"].value_counts())

        st.subheader("📜 Event Logs")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)

        st.download_button(
            "⬇ Export Security Report",
            csv,
            "fire_report.csv",
            "text/csv",
            key=f"download_{i}"
        )

    time.sleep(speed)