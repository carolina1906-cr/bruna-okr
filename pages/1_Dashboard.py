import streamlit as st
import pandas as pd
from db import get_departments, get_key_results, get_monthly_values, get_setting
from calculations import calcular_avance, semaforo
from components.semaforo import badge, color_pct
from components.metrics import metric_cards
from constants import MESES

st.set_page_config(page_title="Dashboard OKR", layout="wide")

st.markdown("""
<style>
    .kr-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-left: 4px solid #dee2e6;
    }
    .kr-card.verde { border-left-color: #2DC653; }
    .kr-card.amarillo { border-left-color: #FFD600; }
    .kr-card.rojo { border-left-color: #E63946; }
    .kr-card.navy { border-left-color: #1A2744; }
    .kr-card.gris { border-left-color: #D0D4DF; }
    .kr-name { font-size: 14px; font-weight: 500; margin-bottom: 6px; }
    .kr-meta { font-size: 12px; color: #666; margin-bottom: 6px; }
    .kr-pct { font-size: 20px; font-weight: 700; }
    .dept-header { font-size: 16px; font-weight: 600; margin: 16px 0 8px 0; padding-bottom: 4px; border-bottom: 2px solid #e9ecef; }
    @media (max-width: 768px) {
        .kr-name { font-size: 13px; }
        .kr-pct { font-size: 18px; }
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard — Todos los KRs")

mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))
st.caption(f"Mes activo: {MESES[mes_activo-1]} {year_activo}")

departments = get_departments()
all_krs = get_key_results()

total = 0
en_meta_n = en_riesgo_n = critico_n = sin_dato_n = 0
promedios = []

COLOR_MAP = {
    "sobre_meta": "navy",
    "en_meta": "verde",
    "en_riesgo": "amarillo",
    "critico": "rojo",
    "sin_dato": "gris"
}

PCT_COLOR = {
    "sobre_meta": "#1A2744",
    "en_meta": "#2DC653",
    "en_riesgo": "#BA7517",
    "critico": "#E63946",
    "sin_dato": "#999"
}

DELTA_ICON = lambda d: '↑' if d in ['Aumentar','Expandir','Elevar','Lograr','Impulsar','Automatizar','Superar','Mantener/elevar'] else '↓' if d in ['Reducir','Disminuir'] else '✓'

for dept in departments:
    krs = [k for k in all_krs if k["department_code"] == dept["code"]]
    if not krs:
        continue

    dept_pcts = []
    kr_data = []
    for kr in krs:
        vals = get_monthly_values(kr["id"], year_activo)
        pct_m, pct_a = calcular_avance(kr, vals, mes_activo)
        estado = semaforo(pct_m)
        total += 1
        if estado in ("en_meta", "sobre_meta"):
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
        kr_data.append((kr, pct_m, pct_a, estado))

    prom_dept = round(sum(dept_pcts) / len(dept_pcts), 1) if dept_pcts else None
    prom_txt = f"{prom_dept}%" if prom_dept is not None else "Sin datos"

    st.markdown(f'<div class="dept-header">{dept["name"]} <span style="font-size:13px;color:#666;font-weight:400;">— {prom_txt} promedio</span></div>', unsafe_allow_html=True)

    for kr, pct_m, pct_a, estado in kr_data:
        color_class = COLOR_MAP.get(estado, "gris")
        pct_color = PCT_COLOR.get(estado, "#999")
        pct_txt = f"{pct_m:.1f}%" if pct_m is not None else "Sin dato"
        acum_txt = f"Acum: {pct_a:.1f}%" if pct_a is not None else ""
        icon = DELTA_ICON(kr["delta"])

        st.markdown(f"""
        <div class="kr-card {color_class}">
            <div class="kr-name">{icon} {kr['name']}</div>
            <div class="kr-meta">Meta: {kr['goal']} {kr['unit']} &nbsp;|&nbsp; Base: {kr['base']} &nbsp;{f'| {acum_txt}' if acum_txt else ''}</div>
            <div class="kr-pct" style="color:{pct_color};">{pct_txt}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.subheader("Resumen organizacional")
prom_org = round(sum(promedios) / len(promedios), 1) if promedios else None
metric_cards(total, en_meta_n, en_riesgo_n, critico_n, sin_dato_n, prom_org)
