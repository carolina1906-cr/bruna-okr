import streamlit as st
from db import get_departments, get_key_results, get_monthly_values, get_setting, set_setting
from calculations import calcular_avance, semaforo
from constants import MESES
st.set_page_config(
    page_title="Inicio — OKR Bruna Group",
    page_icon="📊",
    layout="wide"
)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("app.py", label="🏠 Inicio", use_container_width=True)
with col2:
    st.page_link("pages/2_Registrar_datos.py", label="📋 Registrar datos", use_container_width=True)
with col3:
    st.page_link("pages/3_Guia_de_uso.py", label="📖 Guía de uso", use_container_width=True)
with col4:
    st.page_link("pages/4_Exportar.py", label="📥 Exportar", use_container_width=True)
st.divider()

st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: 700; color: #1A2744; margin-bottom: 2px; }
    .summary-card { background: #f8f9fa; border-radius: 10px; padding: 14px 16px; text-align: center; }
    .summary-num { font-size: 28px; font-weight: 700; }
    .summary-label { font-size: 12px; color: #888; margin-top: 2px; }
    .section-title { font-size: 17px; font-weight: 600; color: #1A2744; margin: 20px 0 10px 0; }
    .kr-card { background: #f8f9fa; border-radius: 8px; padding: 12px 14px; margin-bottom: 6px; border-left: 4px solid #dee2e6; }
    .kr-card.verde { border-left-color: #2DC653; }
    .kr-card.amarillo { border-left-color: #FFD600; }
    .kr-card.rojo { border-left-color: #E63946; }
    .kr-card.navy { border-left-color: #1A2744; }
    .kr-card.gris { border-left-color: #D0D4DF; }
    .kr-name { font-size: 13px; font-weight: 500; margin-bottom: 4px; }
    .kr-meta { font-size: 11px; color: #888; margin-bottom: 4px; }
    .kr-pct { font-size: 18px; font-weight: 700; }
    .dept-obj { font-size: 12px; color: #666; font-style: italic; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

if "dept_selected" not in st.session_state:
    st.session_state.dept_selected = None

mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))

st.markdown('<div class="main-title">📊 OKR Tracker — Bruna Group</div>', unsafe_allow_html=True)

col_mes, col_year, col_modo = st.columns([2, 2, 3])
with col_mes:
    nuevo_mes = st.selectbox("Mes activo", options=list(range(1, 13)),
                              format_func=lambda m: MESES[m-1], index=mes_activo-1)
with col_year:
    nuevo_year = st.number_input("Año", min_value=2024, max_value=2030, value=year_activo)
with col_modo:
    modo = st.radio("Ver", ["Mes activo", "Acumulado año"], horizontal=True)

if nuevo_mes != mes_activo or nuevo_year != year_activo:
    set_setting("active_month", nuevo_mes)
    set_setting("active_year", nuevo_year)
    mes_activo = nuevo_mes
    year_activo = nuevo_year
    st.cache_data.clear()
    st.rerun()

usar_acum = modo == "Acumulado año"

departments = get_departments()
all_krs = get_key_results()

total = en_meta = en_riesgo = critico = sin_dato = 0
dept_promedios = []
dept_data = []

PCT_COLOR = {
    "sobre_meta": "#1A2744",
    "en_meta": "#2DC653",
    "en_riesgo": "#BA7517",
    "critico": "#E63946",
    "sin_dato": "#999"
}
COLOR_MAP = {
    "sobre_meta": "navy",
    "en_meta": "verde",
    "en_riesgo": "amarillo",
    "critico": "rojo",
    "sin_dato": "gris"
}
DELTA_ICON = lambda d: '↑' if d in ['Aumentar','Expandir','Elevar','Lograr','Impulsar','Automatizar','Superar','Mantener/elevar'] else '↓' if d in ['Reducir','Disminuir'] else '✓'

for dept in departments:
    krs = [k for k in all_krs if k["department_code"] == dept["code"]]
    if not krs:
        continue
    dept_pcts = []
    kr_list = []
    for kr in krs:
        vals = get_monthly_values(kr["id"], year_activo)
        pct_m, pct_a = calcular_avance(kr, vals, mes_activo)
        pct_show = pct_a if usar_acum and pct_a is not None else pct_m
        estado = semaforo(pct_show)
        total += 1
        if estado in ("en_meta", "sobre_meta"): en_meta += 1
        elif estado == "en_riesgo": en_riesgo += 1
        elif estado == "critico": critico += 1
        else: sin_dato += 1
        if pct_show is not None:
            dept_pcts.append(pct_show)
        kr_list.append((kr, pct_m, pct_a, pct_show, estado))
    prom = round(sum(dept_pcts) / len(dept_pcts), 1) if dept_pcts else None
    dept_promedios.append(prom if prom is not None else 0)
    dept_data.append((dept, prom, kr_list))

# Promedio global = promedio de promedios por área
prom_org = round(sum(dept_promedios) / len(dept_promedios), 1) if dept_promedios else None

# Resumen ejecutivo
st.markdown('<div class="section-title">Resumen organizacional</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
color_org = "#2DC653" if prom_org and prom_org >= 70 else "#E63946" if prom_org and prom_org < 40 else "#BA7517" if prom_org else "#999"
with c1:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:{color_org};">{prom_org if prom_org else "—"}%</div><div class="summary-label">Avance global</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#2DC653;">{en_meta}</div><div class="summary-label">En meta</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#BA7517;">{en_riesgo}</div><div class="summary-label">En riesgo</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#E63946;">{critico}</div><div class="summary-label">Crítico</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="summary-card"><div class="summary-num" style="color:#999;">{sin_dato}</div><div class="summary-label">Sin dato</div></div>', unsafe_allow_html=True)

# Menu por area
st.markdown('<div class="section-title">Ver por área</div>', unsafe_allow_html=True)

cols = st.columns(2)
for i, (dept, prom, kr_list) in enumerate(dept_data):
    with cols[i % 2]:
        pct_color = "#2DC653" if prom and prom >= 70 else "#E63946" if prom and prom < 40 else "#BA7517" if prom else "#999"
        pct_txt = f"{prom}%" if prom is not None else "Sin datos"
        obj_txt = dept.get("objective", "")
        if obj_txt and len(obj_txt) > 70:
            obj_txt = obj_txt[:70] + "..."
        label = f"**{dept['name']}** — {pct_txt}\n\n*{obj_txt}*"
        if st.button(label, key=f"btn_{dept['code']}", use_container_width=True):
            if st.session_state.dept_selected == dept["code"]:
                st.session_state.dept_selected = None
            else:
                st.session_state.dept_selected = dept["code"]
            st.rerun()

# Vista detalle por area
if st.session_state.dept_selected:
    selected = next((d for d in dept_data if d[0]["code"] == st.session_state.dept_selected), None)
    if selected:
        dept, prom, kr_list = selected
        st.divider()
        st.markdown(f'<div class="section-title">📋 {dept["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dept-obj">{dept.get("objective","")}</div>', unsafe_allow_html=True)

        for kr, pct_m, pct_a, pct_show, estado in kr_list:
            color_class = COLOR_MAP.get(estado, "gris")
            pct_color = PCT_COLOR.get(estado, "#999")
            pct_txt = f"{pct_show:.1f}%" if pct_show is not None else "Sin dato"
            acum_txt = f"Acum: {pct_a:.1f}%" if pct_a is not None else ""
            icon = DELTA_ICON(kr["delta"])
            st.markdown(f"""
            <div class="kr-card {color_class}">
                <div class="kr-name">{icon} {kr['name']}</div>
                <div class="kr-meta">Meta: {kr['goal']} {kr['unit']} &nbsp;|&nbsp; Base: {kr['base']} &nbsp;{f'| {acum_txt}' if acum_txt else ''}</div>
                <div class="kr-pct" style="color:{pct_color};">{pct_txt}</div>
            </div>
            """, unsafe_allow_html=True)
