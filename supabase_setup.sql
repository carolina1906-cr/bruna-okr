-- ============================================================
-- Bruna Group OKR Tracker — Supabase Setup SQL
-- Ejecutar completo en SQL Editor de Supabase
-- ============================================================

-- 1. TABLA: departments
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    objective TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. TABLA: key_results
CREATE TABLE IF NOT EXISTS key_results (
    id SERIAL PRIMARY KEY,
    department_code TEXT NOT NULL REFERENCES departments(code),
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    base NUMERIC,
    goal NUMERIC NOT NULL,
    delta TEXT NOT NULL CHECK (delta IN ('Aumentar', 'Reducir', 'Completar')),
    measurement_type TEXT NOT NULL CHECK (measurement_type IN ('mensual_puntual', 'acumulado_anual', 'fechas_fijas', 'completado')),
    fixed_months INTEGER[],
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TABLA: monthly_values
CREATE TABLE IF NOT EXISTS monthly_values (
    id SERIAL PRIMARY KEY,
    key_result_id INTEGER NOT NULL REFERENCES key_results(id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    value NUMERIC,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(key_result_id, year, month)
);

-- 4. TABLA: app_settings
CREATE TABLE IF NOT EXISTS app_settings (
    id SERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- RLS: desactivado (acceso abierto con link privado)
-- ============================================================
ALTER TABLE departments DISABLE ROW LEVEL SECURITY;
ALTER TABLE key_results DISABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_values DISABLE ROW LEVEL SECURITY;
ALTER TABLE app_settings DISABLE ROW LEVEL SECURITY;

-- ============================================================
-- Configuracion inicial: mes activo = Enero 2026
-- ============================================================
INSERT INTO app_settings (key, value)
VALUES
    ('active_month', '1'),
    ('active_year', '2026')
ON CONFLICT (key) DO NOTHING;

-- ============================================================
-- DEPARTAMENTOS (9)
-- ============================================================
INSERT INTO departments (code, name, objective) VALUES
    ('BDU',   'BDU',              'Convertir desarrollos tecnicos a negocios rentables en LATAM'),
    ('FIN',   'Financiero',       'Fortalecer gestion del riesgo crediticio'),
    ('COMGL', 'Comercial Global', 'Crecimiento sostenible de ingresos'),
    ('SPU',   'SPU',              'Supply Chain confiable y operacion logistica optimizada'),
    ('NM',    'Nuevos Mercados',  'Operacion rentable en Peru'),
    ('TH',    'Talento Humano',   'Fortalecer cohesion de lideres'),
    ('OPS',   'Operaciones',      'Incrementar eficiencia operativa'),
    ('BITS',  'BITS',             'Estabilidad TI e innovacion con IA'),
    ('COMCR', 'Comercial CR',     'Crecimiento rentable con ejecucion comercial disciplinada')
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- KEY RESULTS (36)
-- ============================================================

-- BDU sin fixed_months (3 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('BDU', 'Ingresos generados por nuevos negocios BDU', 'USD', 0, 500000, 'Aumentar', 'acumulado_anual', 1),
    ('BDU', 'Numero de propuestas tecnico-comerciales enviadas', 'unidades', 0, 12, 'Aumentar', 'acumulado_anual', 2),
    ('BDU', 'Tasa de conversion de propuestas a contratos', '%', 0, 30, 'Aumentar', 'mensual_puntual', 3);

-- BDU con fixed_months (1 KR)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, fixed_months, sort_order) VALUES
    ('BDU', 'NPS interno de satisfaccion con BDU', 'puntos', 0, 70, 'Aumentar', 'fechas_fijas', '{6,12}', 4);

-- Financiero sin fixed_months (3 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('FIN', 'Indice de cartera vencida >90 dias', '%', 8, 4, 'Reducir', 'mensual_puntual', 1),
    ('FIN', 'Cobertura de provisiones sobre cartera vencida', '%', 60, 90, 'Aumentar', 'mensual_puntual', 2),
    ('FIN', 'Dias promedio de cobro (DSO)', 'dias', 75, 55, 'Reducir', 'mensual_puntual', 3);

-- Comercial Global sin fixed_months (3 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('COMGL', 'Ingresos totales Comercial Global', 'USD', 0, 3000000, 'Aumentar', 'acumulado_anual', 1),
    ('COMGL', 'Margen bruto promedio', '%', 18, 23, 'Aumentar', 'mensual_puntual', 2),
    ('COMGL', 'Numero de clientes activos nuevos', 'clientes', 0, 15, 'Aumentar', 'acumulado_anual', 3);

-- Comercial Global con fixed_months (2 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, fixed_months, sort_order) VALUES
    ('COMGL', 'Retencion de clientes top 20', '%', 85, 95, 'Aumentar', 'fechas_fijas', '{6,12}', 4),
    ('COMGL', 'Indice de satisfaccion de clientes (CSAT)', 'puntos', 72, 82, 'Aumentar', 'fechas_fijas', '{6,12}', 5);

-- SPU sin fixed_months (4 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('SPU', 'OTIF (On Time In Full)', '%', 78, 92, 'Aumentar', 'mensual_puntual', 1),
    ('SPU', 'Costo logistico como % de ventas', '%', 12, 9, 'Reducir', 'mensual_puntual', 2),
    ('SPU', 'Exactitud de inventario', '%', 88, 97, 'Aumentar', 'mensual_puntual', 3),
    ('SPU', 'Incidentes de calidad en despacho', 'incidentes', 15, 5, 'Reducir', 'mensual_puntual', 4);

-- Nuevos Mercados sin fixed_months (4 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('NM', 'Ingresos operacion Peru', 'USD', 0, 800000, 'Aumentar', 'acumulado_anual', 1),
    ('NM', 'EBITDA operacion Peru', 'USD', 0, 80000, 'Aumentar', 'acumulado_anual', 2),
    ('NM', 'Clientes activos en Peru', 'clientes', 0, 20, 'Aumentar', 'mensual_puntual', 3),
    ('NM', 'Licencias y permisos operativos obtenidos', 'completado', 0, 1, 'Completar', 'completado', 4);

-- Talento Humano con fixed_months (1 KR)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, fixed_months, sort_order) VALUES
    ('TH', 'Indice de cohesion de lideres (encuesta Bruna Axia)', 'puntos', 0, 80, 'Aumentar', 'fechas_fijas', '{6,12}', 1);

-- Operaciones sin fixed_months (5 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('OPS', 'Productividad por operador (unidades/hora)', 'unidades/hora', 42, 55, 'Aumentar', 'mensual_puntual', 1),
    ('OPS', 'Costo operativo por unidad procesada', 'USD', 2.8, 2.1, 'Reducir', 'mensual_puntual', 2),
    ('OPS', 'Tasa de error en procesamiento', '%', 4.5, 1.5, 'Reducir', 'mensual_puntual', 3),
    ('OPS', 'Tiempo de ciclo promedio (dias)', 'dias', 8, 5, 'Reducir', 'mensual_puntual', 4),
    ('OPS', 'Cumplimiento de SLAs internos', '%', 70, 90, 'Aumentar', 'mensual_puntual', 5);

-- BITS sin fixed_months (4 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('BITS', 'Disponibilidad de sistemas criticos (uptime)', '%', 96, 99.5, 'Aumentar', 'mensual_puntual', 1),
    ('BITS', 'Tiempo promedio de resolucion de incidentes (MTTR)', 'horas', 18, 6, 'Reducir', 'mensual_puntual', 2),
    ('BITS', 'Casos de uso de IA implementados en produccion', 'unidades', 0, 4, 'Aumentar', 'acumulado_anual', 3),
    ('BITS', 'Incidentes de seguridad criticos', 'incidentes', 3, 0, 'Reducir', 'mensual_puntual', 5);

-- BITS con fixed_months (1 KR)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, fixed_months, sort_order) VALUES
    ('BITS', 'Satisfaccion interna con soporte TI', 'puntos', 65, 82, 'Aumentar', 'fechas_fijas', '{6,12}', 4);

-- Comercial CR sin fixed_months (5 KRs)
INSERT INTO key_results (department_code, name, unit, base, goal, delta, measurement_type, sort_order) VALUES
    ('COMCR', 'Ingresos totales Comercial CR', 'USD', 0, 2500000, 'Aumentar', 'acumulado_anual', 1),
    ('COMCR', 'Margen bruto Comercial CR', '%', 20, 26, 'Aumentar', 'mensual_puntual', 2),
    ('COMCR', 'Visitas efectivas por vendedor por mes', 'visitas', 18, 28, 'Aumentar', 'mensual_puntual', 3),
    ('COMCR', 'Clientes nuevos activos CR', 'clientes', 0, 25, 'Aumentar', 'acumulado_anual', 4),
    ('COMCR', 'Tasa de cumplimiento de cuota por vendedor', '%', 65, 85, 'Aumentar', 'mensual_puntual', 5);

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================
