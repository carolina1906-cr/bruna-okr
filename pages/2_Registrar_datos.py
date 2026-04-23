import streamlit as st
from db import get_departments, get_key_results, get_monthly_values, upsert_monthly_value, get_setting, set_setting
from calculations import calcular_avance, semaforo
from components.semaforo import badge
from constants import MESES
st.set_page_config(page_title="Registrar datos", layout="wide")
st.markdown("""
<style>
div[data-testid="stPageLink-NavLink"] p { font-size: 0px; }
div[data-testid="stPageLink-NavLink"] { text-align: center; }
</style>
""", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("app.py", label="🏠 Inicio", use_container_width=True)
with col2:
    st.page_link("pages/2_Registrar_datos.py", label="📋 Registrar datos", use_container_widt