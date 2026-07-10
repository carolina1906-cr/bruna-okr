import streamlit as st
from auth import check_login
from db import get_departments, get_key_results, get_monthly_values, get_setting, get_meta_progresiva
from calculations import calcular_avance, semaforo
from config import get_supabase
from constants import MESES

check_login()

st.set_page_config(page_title="Seguimiento OKR", layout="wide")
st.title("Seguimiento OKR")
st.caption("Vision acumulada del ano — revision ejecutiva por area")

with st.expander("Como se calcula el avance acumulado?"):
    st.markdown("""
| Tipo de KR | Como se calcula el acumulado |
|---|---|
| **Acumulado anual** | Suma de todos los meses registrados hasta el mes seleccionado vs meta anual |
| **Mensual puntual** | Promedio de los meses con dato registrado vs meta |
| **Meta progresiva** | Avance del ultimo mes con dato vs la meta esperada de ese mes |
| **Completado / No** | 1 = 100%, 0 = 0% |

> **Importante:** Para KRs de tipo mensual puntual, el % se calcula solo sobre los meses que tienen dato registrado.
> Si hay meses sin registro, el sistema lo indica para que pueda evaluar si el resultado es representativo.
""")

PREGUNTAS = {
    "critico": "Que esta bloqueando este resultado y que necesitan para desbloquearlo?",
    "en_riesgo": "Que acciones concretas tienen para los proximos 30 dias?",
    "en_meta": "Que los esta llevando a este resultado? Como lo sostienen?",
    "sobre_meta": "Excelente resultado. Que los llevo aqui y como replicarlo?",
    "sin_dato": "Por que no hay datos registrados aun? Cuando estaran disponibles?",
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

def calcular_acumulado_seguimiento(kr, vals, mes_hasta, year_sel, supabase):
    tipo = kr["measurement_type"]
    delta = kr["delta"]
    base = kr.get("base") or 0

    def pct_simple(valor, meta, delta, base):
        if valor is None or meta is None:
            return None
        if delta == "Reducir":
            rango = base - meta
            if rango == 0:
                return None
            return round(((base - valor) / rango) * 100, 1)
        else:
            if meta == 0:
                return None
            return round((valor / meta) * 100, 1)

    # Verificar si tiene metas progresivas
    metas_prog = supabase.table("kr_metas_progresivas").select("*").eq("kr_id", kr["id"]).eq("year", year_sel).lte("month", mes_hasta).order("month").execute()

    if metas_prog.data:
        # Usar ultima meta progresiva disponible hasta el mes seleccionado
        ultima = metas_prog.data[-1]
        mes_meta = ultima["month"]
        meta_prog = ultima["meta_mes"]
        v = vals.get(mes_meta)
        if v is None:
            return None, 0, mes_hasta
        pct = pct_simple(v, meta_prog, delta, base)
        return pct, 1, mes_hasta

    meta = kr["goal"]

    if tipo == "completado":
        v = vals.get(mes_hasta)
        if v is None:
            return None, 0, 0
        pct = 100.0 if v >= 1 else 0.0
        return pct, 1, 1

    elif tipo == "acumulado_anual":
        valores = [(m, vals.get(m)) for m in range(1, mes_hasta + 1) if vals.get(m) is not None]
        if not valores:
            return None, 0, mes_hasta
        acum = sum(v for _, v in valores)
        return pct_simple(acum, meta, delta, base), len(valores), mes_hasta

    elif tipo == "mensual_puntual":
        valores = [(m, vals.get(m)) for m in range(1, mes_hasta + 1) if vals.get(m) is not None]
        if not valores:
            return None, 0, mes_hasta
        promedio = sum(v for _, v in valores) / len(valores)
        return pct_simple(promedio, meta, delta, base), len(valores), mes_hasta

    elif tipo == "fechas_fijas":
        meses_con_valor = [m for m in range(1, mes_hasta + 1) if vals.get(m) is not None]
        if not meses_con_valor:
            return None, 0, mes_hasta
        v = vals.get(max(meses_con_valor))
        return pct_simple(v, meta, delta, base), len(meses_con_valor), mes_hasta

    return None, 0, mes_hasta

puede_editar = st.session_state.get("username") in ("culloa", "abrunadobles")

year_activo = int(get_setting("active_year", 2026))

col1, col2 = st.columns([2, 2])
with col1:
    mes_hasta = st.selectbox(
        "Ver avance hasta:",
        options=list(range(1, 13)),
        format_func=lambda m: MESES[m-1],
        index=int(get_setting("active_month", 1)) - 1
    )
with col2:
    year_sel = st.number_input("Ano:", min_value=2024, max_value=2030, value=year_activo)

mes_anterior = mes_hasta - 1
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
            pct_show, meses_con_dato, total_meses = calcular_acumulado_seguimiento(kr, vals, mes_hasta, year_sel, supabase)
            estado = semaforo(pct_show)

            seg_actual = supabase.table("seguimiento_okr").select("*").eq("kr_id", kr["id"]).eq("year", year_sel).eq("month", mes_hasta).execute()
            seg_anterior = supabase.table("seguimiento_okr").select("*").eq("kr_id", kr["id"]).eq("year", year_anterior).eq("month", mes_anterior).execute()

            compromiso_anterior = seg_anterior.data[0]["compromiso_nuevo"] if seg_anterior.data else None
            cumplio_actual = seg_actual.data[0]["cumplio_compromiso"] if seg_actual.data else ""
            compromiso_actual = seg_actual.data[0]["compromiso_nuevo"] if seg_actual.data else ""

            color = ESTADO_COLOR.get(estado, "#999")
            pct_txt = f"{pct_show:.1f}%" if pct_show is not None else "Sin dato"
            estado_txt = ESTADO_LABEL.get(estado, "Sin dato")

            meses_registrados = [MESES[m-1] for m in range(1, mes_hasta + 1) if vals.get(m) is not None]
            meses_faltantes = total_meses - meses_con_dato

            alerta_datos = ""
            if kr["measurement_type"] == "mensual_puntual" and meses_faltantes > 0:
                alerta_datos = f'<div style="font-size:11px;color:#BA7517;margin-top:4px;">⚠️ {meses_con_dato} de {total_meses} meses registrados ({", ".join(meses_registrados)}). Faltan {meses_faltantes} meses.</div>'

            delta_badge = f'<span style="font-size:10px;background:#e8eaf6;color:#1A2744;padding:1px 6px;border-radius:4px;font-weight:600;margin-right:6px;">{kr["delta"]}</span>'

            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding: 10px 14px; margin-bottom: 8px; background: #f8f9fa; border-radius: 0 8px 8px 0;">
                <div style="font-size:14px; font-weight:600; color:#1A2744; margin-bottom:4px;">{delta_badge}{kr['name']}</div>
                <div style="font-size:12px; color:#888;">Meta: {kr['goal']} {kr['unit']} | Base: {kr['base']} | Ene - {MESES[mes_hasta-1]}</div>
                <div style="font-size:22px; font-weight:700; color:{color}; margin-top:4px;">{pct_txt} <span style="font-size:12px; font-weight:400; color:{color};">({estado_txt})</span></div>
                {alerta_datos}
            </div>
            """, unsafe_allow_html=True)

            if compromiso_anterior:
                st.markdown(f"**Compromiso de {MESES[mes_anterior-1]} {year_anterior}:**")
                st.info(compromiso_anterior)
                if cumplio_actual:
                    st.markdown("**Seguimiento:**")
                    st.success(cumplio_actual)

            if compromiso_actual and not puede_editar:
                st.markdown(f"**Compromiso registrado:**")
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
                        f"Compromiso para {MESES[mes_hasta-1]}:",
                        value=compromiso_actual or "",
                        key=f"compromiso_{dept['code']}_{kr['id']}",
                        height=80
                    )
                if st.button("Guardar", key=f"guardar_{dept['code']}_{kr['id']}"):
                    data = {
                        "kr_id": kr["id"],
                        "year": year_sel,
                        "month": mes_hasta,
                        "cumplio_compromiso": nuevo_cumplio,
                        "compromiso_nuevo": nuevo_compromiso,
                        "updated_by": st.session_state.get("username"),
                    }
                    supabase.table("seguimiento_okr").upsert(data, on_conflict="kr_id,year,month").execute()
                    st.success("Guardado.")
                    st.rerun()

            st.divider()