-- ============================================
-- MODELO DE DATA WAREHOUSE - PANDAS
-- ============================================
-- Este archivo contiene las definiciones DDL (Data Definition Language)
-- para el Data Warehouse creado con Pandas.
-- Base de datos: warehouse_pandas.db
-- ============================================

-- ============================================
-- TABLAS DE DIMENSIONES
-- ============================================

-- Dimensión: Atletas
-- Contiene información única de cada atleta
CREATE TABLE IF NOT EXISTS dim_athlete (
    id_athlete INTEGER PRIMARY KEY,
    athlete_id TEXT,
    name TEXT NOT NULL,
    gender TEXT,
    age REAL,
    country TEXT
);

-- Dimensión: Competencias
-- Contiene información de las competencias
CREATE TABLE IF NOT EXISTS dim_competition (
    id_competition INTEGER PRIMARY KEY,
    competition TEXT NOT NULL,
    year INTEGER NOT NULL,
    category TEXT
);

-- Dimensión: Equipos
-- Contiene información de equipos y coaches
CREATE TABLE IF NOT EXISTS dim_team (
    id_team INTEGER PRIMARY KEY,
    team TEXT NOT NULL,
    coach TEXT
);

-- ============================================
-- TABLA DE HECHOS
-- ============================================

-- Tabla de Hechos: Levantamientos
-- Contiene las métricas de levantamiento relacionadas con las dimensiones
CREATE TABLE IF NOT EXISTS fact_lifting (
    id_fact INTEGER PRIMARY KEY AUTOINCREMENT,
    id_athlete INTEGER NOT NULL,
    id_competition INTEGER NOT NULL,
    id_team INTEGER NOT NULL,
    snatch_kg REAL,
    clean_and_jerk_kg REAL,
    total_kg REAL,
    body_weight_kg REAL,
    event_rank REAL,
    medal TEXT,
    record_status TEXT,
    lifting_style TEXT,
    FOREIGN KEY (id_athlete) REFERENCES dim_athlete(id_athlete),
    FOREIGN KEY (id_competition) REFERENCES dim_competition(id_competition),
    FOREIGN KEY (id_team) REFERENCES dim_team(id_team)
);

-- ============================================
-- ÍNDICES PARA MEJORAR RENDIMIENTO
-- ============================================

CREATE INDEX IF NOT EXISTS idx_fact_athlete ON fact_lifting(id_athlete);
CREATE INDEX IF NOT EXISTS idx_fact_competition ON fact_lifting(id_competition);
CREATE INDEX IF NOT EXISTS idx_fact_team ON fact_lifting(id_team);
CREATE INDEX IF NOT EXISTS idx_athlete_country ON dim_athlete(country);
CREATE INDEX IF NOT EXISTS idx_competition_year ON dim_competition(year);

-- ============================================
-- COMENTARIOS SOBRE EL MODELO
-- ============================================
-- Modelo Dimensional: Esquema en Estrella
-- 
-- Estructura:
--   - 1 Tabla de Hechos: fact_lifting
--   - 3 Tablas de Dimensiones: dim_athlete, dim_competition, dim_team
-- 
-- Relaciones:
--   - fact_lifting.id_athlete -> dim_athlete.id_athlete
--   - fact_lifting.id_competition -> dim_competition.id_competition
--   - fact_lifting.id_team -> dim_team.id_team
-- 
-- Métricas en fact_lifting:
--   - snatch_kg: Peso levantado en snatch (kg)
--   - clean_and_jerk_kg: Peso levantado en clean and jerk (kg)
--   - total_kg: Total levantado (kg)
--   - body_weight_kg: Peso corporal del atleta (kg)
--   - event_rank: Posición en la competencia
--   - medal: Medalla obtenida (Gold, Silver, Bronze)
--   - record_status: Estado del récord (World Record, National Record, Personal Best)
--   - lifting_style: Estilo de levantamiento (Olympic, Powerlifting, CrossFit, Functional)
-- ============================================

