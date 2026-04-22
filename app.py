import streamlit as st
from db import get_departments, get_key_results, get_monthly_values, get_setting
from calculations import calcular_avance, semaforo
from constants import MESES

st.set_page_config(
    page_title="OKR Tracker — Bruna Group",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main-title { font-size: 28px; font-weight: 700; color: #1A2744; margin-bottom: 4px; }
    .main-sub { font-size: 15px; color: #666; margin-bottom: 24px; }
    .summary-card { background: #f8f9fa; border-radius: 10px; padding: 16px 20px; text-align: center; margin-bottom: 8px; }
    .summary-num { font-size: 32px; font-weight: 700; }
    .summary-label { font-size: 13px; color: #666; margin-top: 4px; }
    .dept-btn { display: block; width: 100%; text-align: left; background: white; border: 1.5px solid #e9ecef; border-radius: 10px; padding: 14px 18px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
    .dept-btn:hover { border-color: #1A2744; background: #f0f4ff; }
    .dept-name { font-size: 15px; font-weight: 600; color: #1A2744; }
    .dept-obj { font-size: 12px; color: #888; margin-top: 3px; }
    .dept-pct { font-size: 18px; font-weight: 700; float: right; margin-top: -20px; }
    .section-title { font-size: 18px; font-weight: 600; color: #1A2744; margin: 24px 0 12px 0; }
    .rag-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
</style>
""", unsafe_allow_html=True)

mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))

st.markdown(f'<div class="main-title">📊 OKR Tracker — Bruna Group {year_activo}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-sub">Mes activo: {MESES[mes_activo-1]} {year_activo}</div>', unsafe_allow_html=True)

departments = get_departments()
all_krs = get_key_results()

total = en_meta = en_riesgo = critico = sin_dato = 0
promedios = []
dept_data = []

PCT_COLOR = {
    "sobre_meta": "#1A2744",
    "en_meta": "#2DC653",
    "en_riesgo": "#BA7517",
    "critico": "#E63946",
    "sin_dato": "#999"
}

RAG_COLOR = {
    "sobre_meta": "#1A2744",
    "en_meta": "#2DC653",
    "en_riesgo": "#FFD600",
    "critico": "#E63946",
    "sin_dato": "#D0D4DF"
}

for dept in departments:
    krs = [k for k in all_krs if k["department_code"] == dept["code"]]
    if not krs:
        continue
    dept_pcts = []
    dept_estados = []
    for kr in krs:
        vals = get_monthly_values(kr["id"], year_activo)
        pct_m, _ = calcular_avance(kr, vals, mes_activo)
        estado = semaforo(pct_m)
        total += 1
        if estado in ("en_meta", "sobre_meta"):
            en_meta += 1
        elif estado == "en_riesgo":
            en_riesgo += 1
        elif estado == "critico":
            critico += 1
        else:
            sin_dato += 1
        if pct_m is not None:
            dept_pcts.append(pct_m)
            promedios.append(pct_m)
        dept_estados.append(estado)
    prom = round(sum(dept_pcts) / len(dept_pcts), 1) if dept_pcts else None
    dept_data.append((dept, prom, dept_estados))

prom_org = round(sum(promedios) / len(promedios), 1) if promedios else None

# Resumen ejecutivo
st.markdown('<div class="section-title">Resumen organizacional</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    pct_txt = f"{prom_org}%" if prom_org else "—"
    color = "#1A2744" if prom_org and prom_org >= 70 else "#E63946" if prom_org and prom_org < 40 else "#BA7517"
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:{color};">{pct_txt}</div><div class="summary-label">Avance global</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#2DC653;">{en_meta}</div><div class="summary-label">En meta</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#BA7517;">{en_riesgo}</div><div class="summary-label">En riesgo</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#E63946;">{critico}</div><div class="summary-label">Crítico</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#999;">{sin_dato}</div><div class="summary-label">Sin dato</div></div>', unsafe_allow_html=True)

# Menu por area
st.markdown('<div class="section-title">Ver por área</div>', unsafe_allow_html=True)
st.caption("Selecciona un área para ver sus KRs en detalle")

cols = st.columns(2)
for i, (dept, prom, estados) in enumerate(dept_data):
    with cols[i % 2]:
        pct_txt = f"{prom}%" if prom is not None else "Sin datos"
        pct_color = "#2DC653" if prom and prom >= 70 else "#E63946" if prom and prom < 40 else "#BA7517" if prom else "#999"
        dots = "".join([f'<span class="rag-dot" style="background:{RAG_COLOR[e]};"></span>' for e in estados])
        if st.button(f"**{dept['name']}** — {pct_txt}", key=f"btn_{dept['code']}", use_container_width=True):
            st.switch_page("pages/2_Departamento.py")
        st.caption(dept.get("objective", "")[:80] + "..." if dept.get("objective") and len(dept.get("objective","")) > 80 else dept.get("objective",""))

st.divider()
st.markdown("""
**Navegación:**
- 📊 **Dashboard** — Vista completa de todos los KRs con semáforo
- 📋 **Departamento** — Ingresar datos mensuales por área  
- ⚙️ **Control** — Cambiar mes activo
- 📥 **Exportar** — Descargar Excel
""")
