import streamlit as st
import bcrypt
from config import get_supabase

def check_login():
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
        st.session_state["username"] = None
        st.session_state["name"] = None

    if st.session_state["authentication_status"]:
        st.sidebar.write(f"Hola, {st.session_state['name']}")
        if st.sidebar.button("Cerrar sesion"):
            st.session_state["authentication_status"] = None
            st.session_state["username"] = None
            st.session_state["name"] = None
            st.rerun()
        cambiar_contrasena()
        return True

    st.image("assets/logo.png", width=200)
    st.title("OKR Tracker - Bruna Group")
    st.subheader("Inicio de sesion")
    username = st.text_input("Usuario")
    password = st.text_input("Contrasena", type="password")
    if st.button("Ingresar"):
        supabase = get_supabase()
        result = supabase.table("users").select("*").eq("username", username).execute()
        if result.data:
            user = result.data[0]
            stored = user["password"]
            st.write(f"Usuario encontrado: {user['name']}")
            st.write(f"Hash almacenado: {stored[:20]}...")
            try:
                match = bcrypt.checkpw(password.encode(), stored.encode())
                st.write(f"Contrasena correcta: {match}")
            except Exception as e:
                st.error(f"Error bcrypt: {e}")
        else:
            st.error("Usuario no encontrado en base de datos")
    st.stop()

def cambiar_contrasena():
    with st.sidebar.expander("Cambiar contrasena"):
        current = st.text_input("Contrasena actual", type="password", key="cp_current")
        new1 = st.text_input("Nueva contrasena", type="password", key="cp_new1")
        new2 = st.text_input("Repetir nueva contrasena", type="password", key="cp_new2")
        if st.button("Guardar", key="cp_save"):
            supabase = get_supabase()
            username = st.session_state["username"]
            result = supabase.table("users").select("password").eq("username", username).execute()
            if not result.data:
                st.error("Error al obtener usuario.")
                return
            stored = result.data[0]["password"]
            if not bcrypt.checkpw(current.encode(), stored.encode()):
                st.error("La contrasena actual es incorrecta.")
                return
            if new1 != new2:
                st.error("Las contrasenas nuevas no coinciden.")
                return
            if len(new1) < 6:
                st.error("La contrasena debe tener al menos 6 caracteres.")
                return
            new_hash = bcrypt.hashpw(new1.encode(), bcrypt.gensalt()).decode()
            supabase.table("users").update({"password": new_hash}).eq("username", username).execute()
            st.success("Contrasena actualizada correctamente.")