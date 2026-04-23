import streamlit as st
st.set_page_config(page_title="Guia de uso", layout="wide")
st.markdown("""
<style>
div[data-testid="stPageLink-NavLink"] p { font-size: 0px; }
div[data-testid="stPageLink-NavLink"] { text-align: center; }
</style>
""", unsafe_allow_html=True)
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
st.title("📖 Guía de uso — OKR Tracker Bruna Group")
st.markdown("Bienvenido al sistema de seguimiento de OKRs de Bruna Group 2026.")
st.divider()
st.header("¿Qué es esta plataforma?")
st.markdown("""
El OKR Tracker centraliza el avance de los **27 Resultados Clave (KRs)** de los **7 departamentos** de Bruna Group.
Su propósito es simple: que cada líder tenga visibilidad clara de cómo va su área, y que la alta dirección pueda ver el pulso organizacional de un vistazo.
> *No re