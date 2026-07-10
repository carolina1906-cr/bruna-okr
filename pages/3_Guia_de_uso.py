import streamlit as st
from auth import check_login
check_login()

st.set_page_config(page_title="Guia de uso", layout="wide")
st.title("Guia de uso - OKR Tracker Bruna Group")
st.markdown("Bienvenido al sistema de seguimiento de OKRs de Bruna Group 2026.")
st.divider()

st.header("Que es esta plataforma?")
st.markdown("""
El OKR Tracker centraliza el avance de los Resultados Clave (KRs) de los departamentos de Bruna Group.
Su proposito es que cada lider tenga visibilidad clara de como va su area, y que la alta direccion pueda ver el pulso organizacional de un vistazo.
""")
st.divider()

st.header("Como navegar?")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Inicio")
    st.markdown("""
- Resumen ejecutivo con el avance global de la empresa
- Semaforo por categoria (en meta, en riesgo, critico)
- Haga clic en cualquier area para ver el detalle de sus KRs
- Selector de mes y modo de vista (mes activo o acumulado ano)
- Al cambiar de mes o modo, el detalle se cierra automaticamente
""")
    st.subheader("Registrar datos")
    st.markdown("""
- Seleccione su area primero, luego el mes a registrar
- El area queda guardada al cambiar de mes
- Ingrese el valor real de cada KR
- Cada KR muestra la direccion esperada (Aumentar / Reducir / Completar)
- Guarde con el boton al final del formulario
""")
    st.subheader("Seguimiento OKR")
    st.markdown("""
- Herramienta de revision ejecutiva por area
- Muestra el avance acumulado del ano hasta el mes seleccionado
- Permite registrar compromisos por KR (solo Carolina y Antonio)
- Los compromisos del mes anterior se muestran automaticamente
- Todos los lideres pueden ver los compromisos registrados
""")
with col2:
    st.subheader("Editar KRs")
    st.markdown("""
- Cada lider puede editar los KRs de su propia area
- Campos editables: nombre, linea base, meta, direccion y tipo de medicion
- Tambien permite definir metas progresivas por mes para KRs en construccion
- Carolina y Antonio pueden editar cualquier area
""")
    st.subheader("Exportar")
    st.markdown("""
- Genera el reporte Excel con todos los KRs
- Incluye todas las areas y meses ingresados
- Util para presentaciones y archivo historico
""")
    st.subheader("Guia de uso")
    st.markdown("""
- Encuentra aqui toda la informacion sobre como funciona la plataforma
- Leyenda del semaforo y tipos de medicion
- Preguntas frecuentes
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

st.header("Tipos de medicion")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
**Mensual puntual**
Se mide cada mes de forma independiente. El valor ingresado se compara contra la meta del mes.
*Ejemplo: % OTIF del mes*

**Acumulado anual**
Se suman todos los valores ingresados hasta el mes activo y se compara contra la meta anual.
*Ejemplo: Numero de clientes nuevos en el ano*
""")
with col2:
    st.markdown("""
**Meta progresiva**
KRs en construccion con metas diferentes por mes. El sistema compara el avance contra la meta esperada de ese mes especifico.
*Ejemplo: Implementar proceso formal de credito — julio 20%, agosto 60%, setiembre 100%*

**Completado / No**
Binario: 1 = completado, 0 = no completado.
*Ejemplo: Plan de incentivos propuesto*
""")
st.divider()

st.header("Preguntas frecuentes")
with st.expander("Donde se guardan los datos?"):
    st.markdown("En **Supabase**, una base de datos PostgreSQL en la nube con servidores seguros en AWS. Los datos no estan en ninguna computadora local.")
with st.expander("Hay copias de seguridad?"):
    st.markdown("Si. Supabase hace backups automaticos diarios. Adicionalmente, pueden exportar el Excel mensualmente como respaldo adicional.")
with st.expander("Es seguro?"):
    st.markdown("La plataforma usa usuario y contrasena individual por persona, con conexion cifrada. Cada quien accede con sus propias credenciales.")
with st.expander("Que pasa si cambio un dato que ya guarde?"):
    st.markdown("Puede volver a Registrar datos, seleccionar el mismo mes y area, cambiar el valor y guardar de nuevo. El sistema actualiza el valor, no duplica.")
with st.expander("Olvide mi contrasena"):
    st.markdown("En la pantalla de inicio de sesion hay un boton 'Olvide mi contrasena'. Solo ingrese su usuario y una nueva contrasena.")
with st.expander("La app dice que no puede conectarse"):
    st.markdown("Supabase pausa los proyectos inactivos. Avise a Carolina para que reactive el proyecto desde el panel de Supabase. Se reactiva en menos de 2 minutos.")
with st.expander("Puedo editar el nombre o la meta de mi KR?"):
    st.markdown("Si. Vaya a **Editar KRs** en el menu lateral. Puede cambiar el nombre, linea base, meta, direccion y tipo de medicion de los KRs de su area.")
with st.expander("Como se actualiza para el proximo ano?"):
    st.markdown("Al iniciar un nuevo ano, se exporta el Excel del ano anterior como historico, se cargan los nuevos KRs y se cambia el ano activo.")