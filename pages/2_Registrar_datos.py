import streamlit as st
from db import get_departments, get_key_results, get_monthly_values, upsert_monthly_value, get_setting, set_setting
from calculations import calcular_avance, semaforo
from components.semaforo import badge
from constants import MESES
from auth import check_login

check_login()

st.set_page_config(page_title="Registrar datos", layout="wide")
st.title("Registrar datos del mes")

mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))

departments = get_departments()
dept_names = {d["code"]: d["name"] for d in departments}

if "area_selected" not in st.session_state:
    st.session_state.area_selected = list(dept_names.keys())[0]

selected = st.selectbox(
    "Selecciona tu area:",
    options=[d["code"] for d in departments],
    format_func=lambda c: dept_names[c],
    index=[d["code"] for d in departments].index(st.session_state.area_selected)
    if st.session_state.area_selected in [d["code"] for d in departments] else 0
)
st.session_state.area_selected = selected

col1, col2 = st.columns([2, 2])
with col1:
    nuevo_mes = st.selectbox("Mes a registrar:", options=list(range(1, 13)),
                              format_func=lambda m: MESES[m-1], index=mes_activo-1)
with col2:
    nuevo_year = st.number_input("Año:", min_value=2024, max_value=2030, value=year_activo)

if nuevo_mes != mes_activo or nuevo_year != year_activo:
    set_setting("active_month", nuevo_mes)
    set_setting("active_year", nuevo_year)
    mes_activo = nuevo_mes
    year_activo = nuevo_year
    st.cache_data.clear()
    st.rerun()

st.divider()

krs = get_key_results(selected)
if not krs:
    st.warning("No hay KRs registrados para esta area.")
    st.stop()

dept = next((d for d in departments if d["code"] == selected), {})
if dept.get("objective"):
    st.caption(f"Objetivo: {dept['objective']}")

st.subheader(f"KRs - {dept_names[selected]} - {MESES[mes_activo-1]} {year_activo}")

def delta_label(delta):
    return f'<span style="font-size:10px;background:#e8eaf6;color:#1A2744;padding:1px 6px;border-radius:4px;font-weight:600;">{delta}</span>'

with st.form("ingreso_form"):
    nuevos_valores = {}
    for kr in krs:
        vals = get_monthly_values(kr["id"], year_activo)
        val_actual = vals.get(mes_activo)
        pct_m, _ = calcular_avance(kr, vals, mes_activo)
        estado = semaforo(pct_m)
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1: