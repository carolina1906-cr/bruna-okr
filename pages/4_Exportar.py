import streamlit as st
from db import get_setting
from constants import MESES
st.set_page_config(page_title="Exportar", layout="wide")
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
st.title("📥 Exportar Excel")
mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))
st.info(f"Se exportara el reporte del mes activo: **{MESES[mes_activo-1]} {year_activo}**")
if st.button("Generar y descargar Excel"):
    try:
        from excel_export import generar_excel
        buffer = generar_excel(year_activo, mes_activo)
        st.download_button(
            label="📥 Descargar Excel v9",
            data=buffer,
            file_name=f"OKR_Bruna_{year_activo}_{MESES[mes_activo-1]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error generando Excel: {e}")