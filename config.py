import os
import streamlit as st
from supabase import create_client, Client

def get_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    except Exception:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_KEY", "")
    if not url or not key:
        st.error("Faltan credenciales de Supabase. Configura .streamlit/secrets.toml")
        st.stop()
    return create_client(url, key)
