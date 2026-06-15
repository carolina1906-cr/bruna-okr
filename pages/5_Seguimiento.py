import streamlit as st
from auth import check_login
from db import get_departments, get_key_results, get_monthly_values, get_setting
from calculations import calcular_avance, semaforo
from config import get_supabase
from constants import MESES

check_login()

st.set_page_config(page_title="Seguimiento OKR", layout="wide")
st.title("Seguimiento OKR")
st.caption("Bitacora de revision mensual - registro de compromisos por area")

PREGUNTAS = {
    "critico": "Que esta bloqueando esto y que necesitan para desbloquearlo?",
    "en_riesgo": "Que acciones concretas tienen para los proximos 30 dias?",
    "en_meta": "Que los esta llevando a este resultado?",
    "sobre_meta": "Que los esta llevando a este resultado?",
    "sin_dato": "Por que no hay datos registrados este mes?",
}

ESTADO_LABEL = {
    "critico": "Critico",
    "en_riesgo": "En riesgo",
    "en_meta": "En meta",
    "sobre_meta": "Sobre meta",
    "sin_dato": "Sin dato",
}

ESTADO_COLOR = {
    "critico": "#E63946",
    "en_riesgo": "#BA7517",
    "en_meta": "#2DC653",
    "sobre_meta": "#1A2744",
    "sin_dato": "#999",
}

puede_editar = st.session_state.get("username") in ("culloa", "abrunadobles")

mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))

st.info(f"Mostrando seguimiento de: {MESES[mes_activo-1]} {year_activo}")

mes_anterior = mes_activo - 1
year_anterior = year_activo
if mes_anterior == 0:
    mes_anterior = 12
    year_anterior -= 1

supabase = get_supabase()
departments = get_departments()
all_krs = get_key_results()

dept_names = {d["code"]: d["name"] for d in departments}
selected_dept = st.selectbox("Selecciona el area:", options=[d["code"] for d in departments],
                              format_func=lambda c: dept_names[c])

krs = [k for k in all_krs if k["department_code"] == selected_dept]

if not krs:
    st.warning("No hay KRs para esta area.")
    st.stop()

for kr in krs:
    vals = get_monthly_values(kr["id"], year_activo)
    pct_m, pct_a = calcular_avance(kr, vals, mes_activo)
    estado = semaforo(pct_m)

    vals_ant = get_monthly_values(kr["id"], year_anterior)
    pct_m_ant, _ = calcular_avance(kr, vals_ant, mes_anterior)

    seg_actual = supabase.table("seguimiento_okr").select("*").eq("kr_id", kr["id"]).eq("year", year_activo).eq("month", mes_activo).execute()
    seg_anterior = supabase.table("seguimiento_okr").select("*").eq("kr_id", kr["id"]).eq("year", year_anterior).eq("month", mes_anterior).execute()

    compromiso_anterior = seg_anterior.data[0]["compromiso_nuevo"] if seg_anterior.data else None
    cumplio_actual = seg_actual.data[0]["cumplio_compromiso"] if seg_actual.data else ""
    compromiso_actual = seg_actual.data[0]["compromiso_nuevo"] if seg_actual.data else ""

    color = ESTADO_COLOR.get(estado, "#999")
    pct_txt = f"{pct_m:.1f}%" if pct_m is not None else "Sin dato"

    with st.expander(f"{kr['name']} -- {pct_txt} ({ESTADO_LABEL.get(estado, 'Sin dato')})"):
        st.markdown(f"<div style='border-left: 4px solid {color}; padding-left: 10px;'><b>Meta:</b> {kr['goal']} {kr['unit']} | <b>Avance actual:</b> {pct_txt}</div>", unsafe_allow_html=True)

        if compromiso_anterior:
            st.markdown(f"**Compromiso de {MESES[mes_anterior-1]} {year_anterior}:**")
            st.info(compromiso_anterior)

        st.markdown(f"**Pregunta sugerida:** {PREGUNTAS.get(estado, '')}")

        if puede_editar:
            nuevo_cumplio = st.text_area("Se cumplio el compromiso anterior? Comentario:", value=cumplio_actual or "", key=f"cumplio_{kr['id']}")
            nuevo_compromiso = st.text_area("Nuevo compromiso para el proximo mes:", value=compromiso_actual or "", key=f"compromiso_{kr['id']}")
            if st.button("Guardar", key=f"guardar_{kr['id']}"):
                data = {
                    "kr_id": kr["id"],
                    "year": year_activo,
                    "month": mes_activo,
                    "cumplio_compromiso": nuevo_cumplio,
                    "compromiso_nuevo": nuevo_compromiso,
                    "updated_by": st.session_state.get("username"),
                }
                supabase.table("seguimiento_okr").upsert(data, on_conflict="kr_id,year,month").execute()
                st.success("Guardado correctamente.")
                st.rerun()
        else:
            if cumplio_actual:
                st.markdown("**Cumplimiento del compromiso anterior:**")
                st.write(cumplio_actual)
            if compromiso_actual:
                st.markdown(f"**Compromiso para {MESES[mes_activo-1]} {year_activo}:**")
                st.write(compromiso_actual)
            if not cumplio_actual and not compromiso_actual:
                st.caption("Aun no hay seguimiento registrado para este mes.")