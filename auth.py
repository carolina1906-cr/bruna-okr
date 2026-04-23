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
    authenticator.login(location="main")
    if st.session_state.get("authentication_status") is False:
        st.error("Usuario o contrasena incorrectos")
        st.stop()
    elif st.session_state.get("authentication_status") is None:
        st.stop()
    authenticator.logout(location="sidebar")
    st.sidebar.write(f"Hola, {st.session_state.get('name')}")
    try:
        if authenticator.reset_password(st.session_state.get("username"), location="sidebar"):
            with open("auth_config.yaml", "w") as file:
                yaml.dump(config, file, default_flow_style=False)
            st.sidebar.success("Contrasena actualizada correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
    return authenticator