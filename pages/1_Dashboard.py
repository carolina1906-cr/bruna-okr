import streamlit as st
from db import get_departments, get_key_results, get_monthly_values, get_setting
from calculations import calcular_avance, semaforo
from components.semaforo import badge, color_pct
from components.metrics import metric_cards
from constants import MESES

st.set_page_config(page_title="Dashboard OKR", layout="wide")
st.title("📊 Dashboard — Todos los KRs")

mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))
st.caption(f"Mes activo: {MESES[mes_activo-1]} {year_activo}")

departments = get_departments()
all_krs = get_key_results()

total = 0
en_meta_n = en_riesgo_n = critico_n = sin_dato_n = 0
promedios = []

for dept in departments:
    krs = [k for k in all_krs if k["department_code"] == dept["code"]]
    if not krs:
        continue

    st.subheader(f"{dept['name']}")

    rows = []
    dept_pcts = []
    for kr in krs:
        vals = get_monthly_values(kr["id"], year_activo)
        pct_m, pct_a = calcular_avance(kr, vals, mes_activo)
        estado = semaforo(pct_m)
        total += 1
        if estado == "en_meta" or estado == "sobre_meta":
            en_meta_n += 1
        elif estado == "en_riesgo":
            en_riesgo_n += 1
        elif estado == "critico":
            critico_n += 1
        else:
            sin_dato_n += 1
        if pct_m is not None:
            dept_pcts.append(pct_m)
            promedios.append(pct_m)
        rows.append({
            "KR": f"{kr['name']} ({kr['delta']})",
            "Unidad": kr["unit"],
            "Meta": kr["goal"],
            "% Mes": f"{pct_m:.1f}%" if pct_m is not None else "—",
            "% Acum.": f"{pct_a:.1f}%" if pct_a is not None else "—",
            "Estado": badge(estado),
        })

    import pandas as pd
    df = pd.DataFrame(rows)
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    if dept_pcts:
        prom_dept = sum(dept_pcts) / len(dept_pcts)
        st.caption(f"Promedio area: {prom_dept:.1f}%")
    st.divider()

st.subheader("Resumen organizacional")
prom_org = sum(promedios) / len(promedios) if promedios else None
metric_cards(total, en_meta_n, en_riesgo_n, critico_n, sin_dato_n, prom_org)
