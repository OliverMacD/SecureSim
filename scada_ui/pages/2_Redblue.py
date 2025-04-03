# scada_ui/pages/4_Redblue.py

import streamlit as st

st.title("🔴🔵 Red/Blue Controls")

# Side-by-side layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛡️ Defenses")
    anomaly = st.checkbox("Anomaly Detection")
    auth = st.checkbox("Command Authentication")
    logging = st.checkbox("Logging & Auditing")

with col2:
    st.subheader("🧨 Attacks (Only one allowed)")
    attack = st.radio("Select Active Attack", options=["None", "Replay Attack", "False Data Injection", "Denial of Service"])

st.markdown("---")
st.subheader("📦 Device Status")

# Simulated Data Table
st.markdown("### 🌀 Pumps")
st.dataframe({
    "Pump": ["pump1", "pump2"],
    "State": ["ON", "OFF"],
    "Flow Rate": [60, 0]
})

st.markdown("### 🛢 Tanks")
st.dataframe({
    "Tank": ["tank1", "tank2"],
    "Max Volume": [1000, 500],
    "Current Volume": [850, 200]
})

st.markdown("---")
st.info("📶 Total network traffic: 23.6 kbps (simulated)")
