import streamlit as st
st.set_page_config(page_title="Guia de uso", layout="wide")
col1, col2, col3, col4 = st.columns(4)
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
    [data-testid="stPageLink-NavLink"] p { display: none; }
}
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

st.header("¿Qué es esta plataforma?")
st.markdown("""
El OKR Tracker centraliza el avance de los **31 Resultados Clave (KRs)** de los **8 departamentos** de Bruna Group.

Su propósito es simple: que cada líder tenga visibilidad clara de cómo va su área, y que la alta dirección pueda ver el pulso organizacional de un vistazo.

> *No reemplaza la conversación estratégica — la alimenta.*
""")

st.divider()

st.header("¿Cómo navegar?")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🏠 Inicio")
    st.markdown("""
- Resumen ejecutivo con el avance global de la empresa
- Semáforo por categoría (en meta, en riesgo, crítico)
- Botones por área para ver el detalle de cada departamento
- Selector de mes y modo de vista (mes activo o acumulado año)
""")

    st.subheader("📋 Registrar datos")
    st.markdown("""
- Selecciona tu área y el mes a registrar
- Ingresa el valor real de cada KR
- Guarda con el botón al final del formulario
- El semáforo se actualiza automáticamente
""")

with col2:
    st.subheader("📖 Guía de uso")
    st.markdown("""
- Encuentra aquí toda la información sobre cómo funciona la plataforma
- Leyenda del semáforo y tipos de medición
- Preguntas frecuentes
""")

    st.subheader("📥 Exportar")
    st.markdown("""
- Genera el reporte Excel con todos los KRs
- Incluye todas las áreas y meses ingresados
- Útil para presentaciones y archivo histórico
""")

st.divider()

st.header("🚦 Leyenda del semáforo")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div style="background:#1A2744;color:white;padding:10px;border-radius:8px;text-align:center;"><b>Sobre meta</b><br>>100%</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div style="background:#2DC653;color:white;padding:10px;border-radius:8px;text-align:center;"><b>En meta</b><br>70-100%</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div style="background:#FFD600;color:#1A2744;padding:10px;border-radius:8px;text-align:center;"><b>En riesgo</b><br>40-70%</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div style="background:#E63946;color:white;padding:10px;border-radius:8px;text-align:center;"><b>Crítico</b><br><40%</div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div style="background:#D0D4DF;color:#1A2744;padding:10px;border-radius:8px;text-align:center;"><b>Sin dato</b><br>Sin valor</div>', unsafe_allow_html=True)

st.divider()

st.header("📐 Tipos de medición")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
**↑ Mensual puntual**
Se mide cada mes de forma independiente. El valor ingresado se compara directamente contra la meta.
*Ejemplo: % OTIF del mes*

**↑ Acumulado anual**
Se suman todos los valores ingresados hasta el mes activo y se compara contra la meta anual.
*Ejemplo: Número de clientes nuevos en el año*
""")
with col2:
    st.markdown("""
**↑ Fechas fijas**
Solo se mide en meses específicos (generalmente Junio y Diciembre). En los otros meses no se espera valor.
*Ejemplo: Evaluación de equipo semestral*

**✓ Completado / No**
Binario: 1 = completado, 0 = no completado. Se usa para hitos o entregables.
*Ejemplo: Plan de incentivos propuesto*
""")

st.divider()

st.header("❓ Preguntas frecuentes")

with st.expander("¿Dónde se guardan los datos?"):
    st.markdown("En **Supabase**, una base de datos PostgreSQL en la nube con servidores seguros en AWS. Los datos no están en ninguna computadora local.")

with st.expander("¿Hay copias de seguridad?"):
    st.markdown("Sí. Supabase hace backups automáticos diarios. Adicionalmente, pueden exportar el Excel mensualmente como respaldo adicional.")

with st.expander("¿Es seguro?"):
    st.markdown("La plataforma usa credenciales de acceso y conexión cifrada. Actualmente el acceso es por link privado compartido con el equipo.")

with st.expander("¿Qué pasa si cambio un dato que ya guardé?"):
    st.markdown("Puedes volver a Registrar datos, seleccionar el mismo mes y área, cambiar el valor y guardar de nuevo. El sistema actualiza el valor, no duplica.")

with st.expander("¿Cómo se actualiza para el próximo año?"):
    st.markdown("Al iniciar un nuevo año, se exporta el Excel del año anterior como histórico, se cargan los nuevos KRs y se cambia el año activo desde Registrar datos.")
