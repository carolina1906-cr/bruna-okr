import streamlit as st
from auth import check_login
from db import get_departments, get_key_results, get_monthly_values, get_setting
from calculations import calcular_avance, semaforo
from config import get_supabase
from constants import MESES

check_login()

st.set_page_config(page_title="Seguimiento OKR", layout="wide")
st.title("Seguimiento OKR")
st.caption("Revision ejecutiva de avance y compromisos por area")

PREGUNTAS = {
    "critico": "Que esta bloqueando este resultado y que necesitan para desbloquearlo?",
    "en_riesgo": "Que acciones concretas tienen para los proximos 30 dias?",
    "en_meta": "Que los esta llevando a este resultado? Como lo sostienen?",
    "sobre_meta": "Excelente resultado. Que los llevo aqui y como replicarlo?",
    "sin_dato": "Por que no hay datos registrados? Cuando estaran disponibles?",
}

ESTADO_COLOR = {
    "critico": "#E63946",
    "en_riesgo": "#FFD600",
    "en_meta": "#2DC653",
    "sobre_meta": "#1A2744",
    "sin_dato": "#999",
}

ESTADO_LABEL = {
    "critico": "Critico",
    "en_riesgo": "En riesgo",
    "en_meta": "En meta",
    "sobre_meta": "Sobre meta",
    "sin_dato": "Sin dato",
}

puede_editar = st.session_state.get("username") in ("culloa", "abrunadobles")

year_activo = int(get_setting("active_year", 2026))

# Selector propio de esta pagina - no afecta el mes global del dashboard
col1, col2, col3 = st.columns([2, 2, 3])
with col1:
    mes_sel = st.selectbox("Mes a revisar:", options=list(range(1, 13)),
                           format_func=lambda m: MESES[m-1],
                           index=int(get_setting("active_month", 1)) - 1)
with col2:
    year_sel = st.number_input("Año:", min_value=2024, max_value=2030, value=year_activo)
with col3:
    modo = st.radio("Vista:", ["Acumulado año", "Mes puntual"], horizontal=True)

usar_acum = modo == "Acumulado año"

mes_anterior = mes_sel - 1
year_anterior = year_sel
if mes_anterior == 0:
    mes_anterior = 12
    year_anterior -= 1

supabase = get_supabase()
departments = get_departments()
all_krs = get_key_results()

st.divider()

tabs = st.tabs([d["name"] for d in departments])

for tab, dept in zip(tabs, departments):
    with tab:
        krs = [k for k in all_krs if k["department_code"] == dept["code"]]
        if not krs:
            st.caption("No hay KRs para esta area.")
            continue

        dept_obj = dept.get("objective", "")
        if dept_obj:
            st.caption(dept_obj)

        st.divider()

        for kr in krs:
            vals = get_monthly_values(kr["id"], year_sel)
            pct_m, pct_a = calcular_avance(kr, vals, mes_sel)
            pct_show = pct_a if usar_acum and pct_a is not None else pct_m
            estado = semaforo(pct_show)

            # Los compromisos siempre se guardan por mes puntual
            seg_actual = supabase.table("seguimiento_okr").select("*").eq("kr_id", kr["id"]).eq("year", year_sel).eq("month", mes_sel).execute()
            seg_anterior = supabase.table("seguimiento_okr").select("*").eq("kr_id", kr["id"]).eq("year", year_anterior).eq("month", mes_anterior).execute()

            compromiso_anterior = seg_anterior.data[0]["compromiso_nuevo"] if seg_anterior.data else None
            cumplio_actual = seg_actual.data[0]["cumplio_compromiso"] if seg_actual.data else ""
            compromiso_actual = seg_actual.data[0]["compromiso_nuevo"] if seg_actual.data else ""

            color = ESTADO_COLOR.get(estado, "#999")
            pct_txt = f"{pct_show:.1f}%" if pct_show is not None else "Sin dato"
            estado_txt = ESTADO_LABEL.get(estado, "Sin dato")
            vista_txt = "Acumulado" if usar_acum else MESES[mes_sel-1]

            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding: 10px 14px; margin-bottom: 8px; background: #f8f9fa; border-radius: 0 8px 8px 0;">
                <div style="font-size:14px; font-weight:600; color:#1A2744; margin-bottom:4px;">{kr['name']}</div>
                <div style="font-size:12px; color:#888;">Meta: {kr['goal']} {kr['unit']} | Base: {kr['base']} | Vista: {vista_txt}</div>
                <div style="font-size:22px; font-weight:700; color:{color}; margin-top:4px;">{pct_txt} <span style="font-size:12px; font-weight:400; color:{color};">({estado_txt})</span></div>
            </div>
            """, unsafe_allow_html=True)

            if compromiso_anterior:
                st.markdown(f"**Compromiso de {MESES[mes_anterior-1]} {year_anterior}:**")
                st.info(compromiso_anterior)
                if cumplio_actual:
                    st.markdown("**Seguimiento:**")
                    st.success(cumplio_actual)

            if compromiso_actual and not puede_editar:
                st.markdown(f"**Compromiso para {MESES[mes_sel-1]} {year_sel}:**")
                st.write(compromiso_actual)

            pregunta = PREGUNTAS.get(estado, "")
            st.markdown(f"*{pregunta}*")

            if puede_editar:
                col1, col2 = st.columns(2)
                with col1:
                    nuevo_cumplio = st.text_area(
                        "Seguimiento del compromiso anterior:",
                        value=cumplio_actual or "",
                        key=f"cumplio_{dept['code']}_{kr['id']}",
                        height=80
                    )
                with col2:
                    nuevo_compromiso = st.text_area(
                        f"Compromiso para {MESES[mes_sel-1]}:",
                        value=compromiso_actual or "",
                        key=f"compromiso_{dept['code']}_{kr['id']}",
                        height=80
                    )
                if st.button("Guardar", key=f"guardar_{dept['code']}_{kr['id']}"):
                    data = {
                        "kr_id": kr["id"],
                        "year": year_sel,
                        "month": mes_sel,
                        "cumplio_compromiso": nuevo_cumplio,
                        "compromiso_nuevo": nuevo_compromiso,
                        "updated_by": st.session_state.get("username"),
                    }
                    supabase.table("seguimiento_okr").upsert(data, on_conflict="kr_id,year,month").execute()
                    st.success("Guardado.")
                    st.rerun()

            st.divider()