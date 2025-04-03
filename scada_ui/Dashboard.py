# scada_ui/app.py
import streamlit as st
from process_sim.interfaces.mqtt_interface import publish_mqtt
from scada_ui.utils.modbus_client import read_modbus_register

st.set_page_config(
    page_title="SCADA UI",
    layout="wide",
)


st.title("📊 Dashboard")

st.header("📡 MQTT & Modbus Queries")

# MQTT Command
mqtt_topic = st.text_input("MQTT Topic")
mqtt_payload = st.text_input("MQTT Payload")
if st.button("Send MQTT"):
    publish_mqtt(mqtt_topic, mqtt_payload)
    st.success("MQTT message sent.")

# Modbus Read
col1, col2 = st.columns(2)
with col1:
    modbus_ip = st.text_input("Modbus IP", value="localhost")
    modbus_port = st.number_input("Modbus Port", value=5200, step=1)
    modbus_address = st.number_input("Register Address", value=0, step=1)
    if st.button("Read Modbus Register"):
        value = read_modbus_register(modbus_ip, modbus_port, modbus_address)
        st.write("Register Value:", value)