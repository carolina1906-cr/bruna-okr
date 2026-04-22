import streamlit as st
from db import get_departments, get_key_results, get_monthly_values, upsert_monthly_value, get_setting, set_setting
from calculations import calcular_avance, semaforo
from components.semaforo import badge
from constants import MESES

st.set_page_config(page_title="Registrar datos", layout="wide")
st.title("📋 Registrar datos del mes")

# Selector de mes activo
mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))

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

departments = get_departments()
dept_names = {d["code"]: d["name"] for d in departments}
selected = st.selectbox("Selecciona tu área:", options=[d["code"] for d in departments],
                        format_func=lambda c: dept_names[c])

krs = get_key_results(selected)
if not krs:
    st.warning("No hay KRs registrados para esta área.")
    st.stop()

dept = next((d for d in departments if d["code"] == selected), {})
if dept.get("objective"):
    st.caption(f"Objetivo: {dept['objective']}")

st.subheader(f"KRs — {dept_names[selected]} — {MESES[mes_activo-1]} {year_activo}")

with st.form("ingreso_form"):
    nuevos_valores = {}
    for kr in krs:
        vals = get_monthly_values(kr["id"], year_activo)
        val_actual = vals.get(mes_activo)
        pct_m, _ = calcular_avance(kr, vals, mes_activo)
        estado = semaforo(pct_m)

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{kr['name']}** ({kr['unit']}) | Meta: {kr['goal']} | Base: {kr['base']}")
            st.markdown(badge(estado), unsafe_allow_html=True)
        with col2:
            nuevo = st.number_input(
                f"Valor {MESES[mes_activo-1]}",
                value=float(val_actual) if val_actual is not None else 0.0,
                key=f"kr_{kr['id']}"
            )
            nuevos_valores[kr["id"]] = nuevo
        with col3:
            pct_txt = f"{pct_m:.1f}%" if pct_m is not None else "—"
            st.metric("Avance", pct_txt)
        st.divider()

    submitted = st.form_submit_button("💾 Guardar datos del mes")
    if submitted:
        for kr_id, valor in nuevos_valores.items():
            upsert_monthly_value(kr_id, year_activo, mes_activo, valor)
        st.success(f"Datos de {MESES[mes_activo-1]} {year_activo} guardados correctamente.")
        st.cache_data.clear()
        st.rerun()
