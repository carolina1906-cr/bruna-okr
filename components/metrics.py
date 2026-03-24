import streamlit as st

def metric_cards(total, en_meta, en_riesgo, critico, sin_dato, promedio):
    cols = st.columns(5)
    with cols[0]:
        st.metric("Total KRs", total)
    with cols[1]:
        st.metric("En meta", en_meta, delta=None)
    with cols[2]:
        st.metric("En riesgo", en_riesgo)
    with cols[3]:
        st.metric("Critico", critico)
    with cols[4]:
        prom = f"{promedio:.1f}%" if promedio is not None else "—"
        st.metric("Promedio org.", prom)
