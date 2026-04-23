import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def check_login():
    with open("auth_config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )
    authenticator.login()
    if st.session_state.get("authentication_status") is False:
        st.error("Usuario o contrasena incorrectos")
        st.stop()
    elif st.session_state.get("authentication_status") is None:
        st.image("assets/logo.png", width=200)
        st.warning("Por favor ingresa tu usuario y contrasena")
        st.stop()
    authenticator.logout("Cerrar sesion", "sidebar")
    st.sidebar.write(f"Hola, {st.session_state.get('name')}")
    return authenticator