import streamlit as st
from auth import check_login
from db import get_departments, get_key_results
from config import get_supabase
from constants import MESES

check_login()

st.set_page_config(page_title="Editar KRs", layout="wide")
st.title("Editar KRs")
st.caption("Cada lider puede actualizar la redaccion, linea base, meta, direccion y tipo de medicion de sus KRs.")

supabase = get_supabase()
username = st.session_state.get("username")
departments = get_departments()

ADMIN_USERS = ("culloa", "abrunadobles")

DELTA_OPCIONES = [
    "Aumentar", "Expandir", "Elevar", "Lograr", "Impulsar",
    "Automatizar", "Superar", "Mantener/elevar",
    "Reducir", "Disminuir",
    "Completar", "Construir", "Crear"
]

TIPO_OPCIONES = [
    "mensual_puntual",
    "acumulado_anual",
    "fechas_fijas",
    "completado"
]

TIPO_LABELS = {
    "mensual_puntual": "Mensual puntual — se mide cada mes vs meta",
    "acumulado_anual": "Acumulado anual — suma de meses vs meta anual",
    "fechas_fijas": "Fechas fijas — solo meses especificos",
    "completado": "Completado / No — binario 1 o 0"
}

if username in ADMIN_USERS:
    areas_editables = [d["code"] for d in departments]
else:
    user_result = supabase.table("users").select("area").eq("username", username).execute()
    if not user_result.data:
        st.error("No se encontro su area asignada.")
        st.stop()
    user_area = user_result.data[0]["area"]
    areas_editables = [user_area]

dept_names = {d["code"]: d["name"] for d in departments if d["code"] in areas_editables}

if not dept_names:
    st.warning("No tiene areas asignadas para editar.")
    st.stop()

if len(areas_editables) > 1:
    selected = st.selectbox("Selecciona el area:", options=list(dept_names.keys()),
                            format_func=lambda c: dept_names[c])
else:
    selected = areas_editables[0]
    st.subheader(dept_names[selected])

all_krs = get_key_results(selected)

if not all_krs:
    st.warning("No hay KRs para esta area.")
    st.stop()

st.divider()
st.markdown("**Edite los campos y presione Guardar en cada KR que modifique.**")
st.divider()

for kr in all_krs:
    with st.expander(f"{kr['name']}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            nuevo_nombre = st.text_input("Nombre del KR:", value=kr["name"], key=f"nombre_{kr['id']}")
        with col2:
            delta_index = DELTA_OPCIONES.index(kr["delta"]) if kr["delta"] in DELTA_OPCIONES else 0
            nuevo_delta = st.selectbox("Direccion:", options=DELTA_OPCIONES,
                                       index=delta_index, key=f"delta_{kr['id']}")

        col3, col4, col5 = st.columns(3)
        with col3:
            nueva_base = st.number_input("Linea base:", value=float(kr["base"] or 0), key=f"base_{kr['id']}")
        with col4:
            nueva_meta = st.number_input("Meta:", value=float(kr["goal"] or 0), key=f"meta_{kr['id']}")
        with col5:
            tipo_index = TIPO_OPCIONES.index(kr["measurement_type"]) if kr["measurement_type"] in TIPO_OPCIONES else 0
            nuevo_tipo = st.selectbox("Tipo de medicion:",
                                      options=TIPO_OPCIONES,
                                      format_func=lambda t: TIPO_LABELS[t],
                                      index=tipo_index,
                                      key=f"tipo_{kr['id']}")

        if st.button("Guardar cambios", key=f"save_{kr['id']}"):
            supabase.table("key_results").update({
                "name": nuevo_nombre,
                "base": nueva_base,
                "goal": nueva_meta,
                "delta": nuevo_delta,
                "measurement_type": nuevo_tipo,
            }).eq("id", kr["id"]).execute()
            st.success("KR actualizado correctamente.")
            st.cache_data.clear()
            st.rerun()

        st.divider()
        st.markdown("**Metas progresivas por mes** (opcional — solo si el KR tiene metas diferentes por mes)")

        metas_result = supabase.table("kr_metas_progresivas").select("*").eq("kr_id", kr["id"]).eq("year", 2026).order("month").execute()
        metas_existentes = {row["month"]: row["meta_mes"] for row in metas_result.data}

        meses_sel = st.multiselect(
            "Meses con meta progresiva:",
            options=list(range(1, 13)),
            default=list(metas_existentes.keys()),
            format_func=lambda m: MESES[m-1],
            key=f"meses_{kr['id']}"
        )

        nuevas_metas = {}
        if meses_sel:
            cols_metas = st.columns(len(meses_sel))
            for i, mes in enumerate(sorted(meses_sel)):
                with cols_metas[i]:
                    val = metas_existentes.get(mes, 0.0)
                    nuevas_metas[mes] = st.number_input(
                        MESES[mes-1],
                        value=float(val),
                        key=f"meta_prog_{kr['id']}_{mes}"
                    )

        if st.button("Guardar metas progresivas", key=f"save_prog_{kr['id']}"):
            supabase.table("kr_metas_progresivas").delete().eq("kr_id", kr["id"]).eq("year", 2026).execute()
            for mes, meta_val in nuevas_metas.items():
                supabase.table("kr_metas_progresivas").insert({
                    "kr_id": kr["id"],
                    "year": 2026,
                    "month": mes,
                    "meta_mes": meta_val
                }).execute()
            st.success("Metas progresivas guardadas.")
            st.rerun()