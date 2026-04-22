import streamlit as st
from db import get_setting, set_setting
from constants import MESES

st.set_page_config(page_title="Control", layout="wide")
st.title("⚙️ Control — Mes Activo")

mes_actual = int(get_setting("active_month", 1))
year_actual = int(get_setting("active_year", 2026))

st.subheader("Configurar mes activo")
col1, col2 = st.columns(2)
with col1:
    nuevo_mes = st.selectbox("Mes:", options=list(range(1, 13)),
                             format_func=lambda m: MESES[m-1],
                             index=mes_actual - 1)
with col2:
    nuevo_year = st.number_input("Año:", min_value=2024, max_value=2030, value=year_actual)

if st.button("Actualizar mes activo"):
    set_setting("active_month", nuevo_mes)
    set_setting("active_year", nuevo_year)
    st.success(f"Mes activo actualizado a {MESES[nuevo_mes-1]} {nuevo_year}")
    st.cache_data.clear()

st.divider()
st.subheader("Leyenda de semaforo")
st.markdown("""
| Color | Rango | Significado |
|---|---|---|
| 🟦 Navy | >100% | Sobre meta |
| 🟢 Verde | 70–100% | En meta |
| 🟡 Amarillo | 40–70% | En riesgo |
| 🔴 Rojo | <40% | Critico |
| ⚪ Gris | Sin dato | Sin datos ingresados |
""")

st.subheader("Tipos de medicion")
st.markdown("""
- **Mensual puntual**: Se mide cada mes independientemente
- **Acumulado anual**: Se suman todos los meses hasta el activo
- **Fechas fijas**: Solo se mide en meses especificos (Jun y Dic)
- **Completado/No**: Binario — 1 = completado, 0 = no completado
""")
