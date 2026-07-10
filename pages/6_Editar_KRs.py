import streamlit as st
from auth import check_login
from db import get_departments, get_key_results
from config import get_supabase

check_login()

st.set_page_config(page_title="Editar KRs", layout="wide")
st.title("Editar KRs")
st.caption("Cada lider puede actualizar la redaccion, linea base, meta y direccion de sus KRs.")

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

        col3, col4 = st.columns(2)
        with col3:
            nueva_base = st.number_input("Linea base:", value=float(kr["base"] or 0), key=f"base_{kr['id']}")
        with col4:
            nueva_meta = st.number_input("Meta:", value=float(kr["goal"] or 0), key=f"meta_{kr['id']}")

        if st.button("Guardar cambios", key=f"save_{kr['id']}"):
            supabase.table("key_results").update({
                "name": nuevo_nombre,
                "base": nueva_base,
                "goal": nueva_meta,
                "delta": nuevo_delta,
            }).eq("id", kr["id"]).execute()
            st.success("KR actualizado correctamente.")
            st.cache_data.clear()
            st.rerun()