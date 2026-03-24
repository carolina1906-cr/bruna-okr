from constants import COLORES

LABELS = {
    "sobre_meta": "Sobre meta",
    "en_meta":    "En meta",
    "en_riesgo":  "En riesgo",
    "critico":    "Critico",
    "sin_dato":   "Sin dato",
}

TEXT_COLORS = {
    "sobre_meta": "#FFFFFF",
    "en_meta":    "#FFFFFF",
    "en_riesgo":  "#1A2744",
    "critico":    "#FFFFFF",
    "sin_dato":   "#1A2744",
}

def badge(estado):
    bg = COLORES.get(estado, "#D0D4DF")
    tc = TEXT_COLORS.get(estado, "#1A2744")
    label = LABELS.get(estado, estado)
    return f'<span style="background:{bg};color:{tc};padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">{label}</span>'

def color_pct(pct, estado):
    c = COLORES.get(estado, "#D0D4DF")
    texto = f"{pct:.1f}%" if pct is not None else "—"
    return f'<span style="color:{c};font-weight:600;">{texto}</span>'
