import streamlit as st
from db import get_setting
from constants import MESES
st.set_page_config(page_title="Exportar", layout="wide")
st.title("Exportar Excel")
mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))
st.info(f"Se exportara el reporte del mes activo: {MESES[mes_activo-1]} {year_activo}")
if st.button("Generar y descargar Excel"):
    try:
        from excel_export import generar_excel
        buffer = generar_excel(year_activo, mes_activo)
        st.download_button(
            label="Descargar Excel",
            data=buffer,
            file_name=f"OKR_Bruna_{year_activo}_{MESES[mes_activo-1]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error generando Excel: {e}")