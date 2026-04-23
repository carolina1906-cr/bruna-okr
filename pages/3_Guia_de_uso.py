import streamlit as st

if not st.session_state.get("authentication_status"):
    st.error("Debes iniciar sesion primero.")
    st.stop()

st.set_page_config(page_title="Guia de uso", layout="wide")
st.title("Guia de uso - OKR Tracker Bruna Group")
st.markdown("Bienvenido al sistema de seguimiento de OKRs de Bruna Group 2026.")
st.divider()
st.header("Que es esta plataforma?")
st.markdown("""
El OKR Tracker centraliza el avance de los **27 Resultados Clave (KRs)** de los **7 departamentos** de Bruna Group.
Su proposito es simple: que cada lider tenga visibilidad clara de como va su area, y que la alta direccion pueda ver el pulso organizacional de un vistazo.
""")
st.divider()
st.header("Como navegar?")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Inicio")
    st.markdown("""
- Resumen ejecutivo con el avance global de la empresa
- Semaforo por categoria (en meta, en riesgo, critico)
- Botones por area para ver el detalle de cada departamento
- Selector de mes y modo de vista (mes activo o acumulado año)
""")
    st.subheader("Registrar datos")
    st.markdown("""
- Selecciona tu area y el mes a registrar
- Ingresa el valor real de cada KR
- Guarda con el boton al final del formulario
- El semaforo se actualiza automaticamente
""")
with col2:
    st.subheader("Guia de uso")
    st.markdown("""
- Encuentra aqui toda la informacion sobre como funciona la plataforma
- Leyenda del semaforo y tipos de medicion
- Preguntas frecuentes
""")
    st.subheader("Exportar")
    st.markdown("""
- Genera el reporte Excel con todos los KRs
- Incluye todas las areas y meses ingresados
- Util para presentaciones y archivo historico
""")
st.divider()
st.header("Leyenda del semaforo")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div style="background:#1A2744;color:white;padding:10px;border-radius:8px;text-align:center;"><b>Sobre meta</b><br>>100%</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div style="background:#2DC653;color:white;padding:10px;border-radius:8px;text-align:center;"><b>En meta</b><br>70-100%</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div style="background:#FFD600;color:#1A2744;padding:10px;border-radius:8px;text-align:center;"><b>En riesgo</b><br>40-70%</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div style="background:#E63946;color:white;padding:10px;border-radius:8px;text-align:center;"><b>Critico</b><br><40%</div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div style="background:#D0D4DF;color:#1A2744;padding:10px;border-radius:8px;text-align:center;"><b>Sin dato</b><br>Sin valor</div>', unsafe_allow_html=True)
st.divider()
st.header("Preguntas frecuentes")
with st.expander("Donde se guardan los datos?"):
    st.markdown("En **Supabase**, una base de datos PostgreSQL en la nube con servidores seguros en AWS.")
with st.expander("Hay copias de seguridad?"):
    st.markdown("Si. Supabase hace backups automaticos diarios.")
with st.expander("Es seguro?"):
    st.markdown("La plataforma usa credenciales de acceso y conexion cifrada.")
with st.expander("Que pasa si cambio un dato que ya guarde?"):
    st.markdown("Puedes volver a Registrar datos, seleccionar el mismo mes y area, cambiar el valor y guardar de nuevo.")
with st.expander("Como se actualiza para el proximo año?"):
    st.markdown("Al iniciar un nuevo año, se exporta el Excel del año anterior como historico y se cargan los nuevos KRs.")