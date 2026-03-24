import streamlit as st

st.set_page_config(
    page_title="OKR Bruna Group",
    page_icon="favicon_bruna.png" if __import__("os").path.exists("favicon_bruna.png") else "📊",
    layout="wide"
)

st.title("📊 OKR Tracker — Bruna Group 2026")
st.markdown("""
Bienvenido al sistema de seguimiento de OKRs de Bruna Group.

Usa el menu de la izquierda para navegar:

- **Dashboard** — Vista consolidada de los 36 KRs con semaforo
- **Departamento** — Ingreso de datos por area
- **Control** — Configurar mes activo
- **Exportar** — Descargar Excel v9
""")

from db import get_setting
mes_activo = int(get_setting("active_month", 1))
year_activo = int(get_setting("active_year", 2026))
meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
st.info(f"Mes activo: **{meses[mes_activo-1]} {year_activo}**")
