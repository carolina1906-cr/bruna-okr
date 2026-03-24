def calcular_avance(kr, valores_mes, mes_activo):
    tipo = kr["measurement_type"]
    delta = kr["delta"]
    meta = kr["goal"]
    base = kr.get("base") or 0

    def pct_simple(valor, meta, delta, base):
        if valor is None or meta is None:
            return None
        if delta == "Reducir":
            rango = base - meta
            if rango == 0:
                return None
            return round(((base - valor) / rango) * 100, 1)
        else:
            if meta == 0:
                return None
            return round((valor / meta) * 100, 1)

    if tipo == "completado":
        v = valores_mes.get(mes_activo)
        if v is None:
            return None, None
        pct = 100.0 if v >= 1 else 0.0
        return pct, pct

    elif tipo == "mensual_puntual":
        v = valores_mes.get(mes_activo)
        pct = pct_simple(v, meta, delta, base)
        return pct, pct

    elif tipo == "acumulado_anual":
        v = valores_mes.get(mes_activo)
        pct_m = pct_simple(v, meta, delta, base)
        vals = [valores_mes.get(m) for m in range(1, mes_activo + 1) if valores_mes.get(m) is not None]
        if not vals:
            return pct_m, None
        acum = sum(vals)
        pct_a = pct_simple(acum, meta, delta, base)
        return pct_m, pct_a

    elif tipo == "fechas_fijas":
        meses_con_valor = [m for m in range(1, mes_activo + 1) if valores_mes.get(m) is not None]
        if not meses_con_valor:
            return None, None
        ultimo_mes = max(meses_con_valor)
        v = valores_mes.get(ultimo_mes)
        pct = pct_simple(v, meta, delta, base)
        return pct, pct

    return None, None


def semaforo(pct):
    if pct is None:
        return "sin_dato"
    if pct > 100:
        return "sobre_meta"
    if pct >= 70:
        return "en_meta"
    if pct >= 40:
        return "en_riesgo"
    return "critico"

    if tipo == "completado":
        v = valores_mes.get(mes_activo)
        if v is None:
            return None, None
        pct = 100.0 if v >= 1 else 0.0
        return pct, pct

    elif tipo == "mensual_puntual":
        v = valores_mes.get(mes_activo)
        pct = pct_simple(v, meta, delta, base)
        return pct, pct

    elif tipo == "acumulado_anual":
        v = valores_mes.get(mes_activo)
        pct_m = pct_simple(v, meta, delta, base)
        vals = [valores_mes.get(m) for m in range(1, mes_activo + 1) if valores_mes.get(m) is not None]
        if not vals:
            return pct_m, None
        acum = sum(vals)
        pct_a = pct_simple(acum, meta, delta, base)
        return pct_m, pct_a

    elif tipo == "fechas_fijas":
        fixed = kr.get("fixed_months") or []
        meses_disponibles = [m for m in fixed if m <= mes_activo]
        if not meses_disponibles:
            return None, None
        ultimo_mes = max(meses_disponibles)
        v = valores_mes.get(ultimo_mes)
        pct = pct_simple(v, meta, delta, base)
        return pct, pct

    return None, None


def semaforo(pct):
    if pct is None:
        return "sin_dato"
    if pct > 100:
        return "sobre_meta"
    if pct >= 70:
        return "en_meta"
    if pct >= 40:
        return "en_riesgo"
    return "critico"
