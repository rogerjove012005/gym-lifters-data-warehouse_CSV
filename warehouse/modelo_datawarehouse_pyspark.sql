-- MODELO DE DATA WAREHOUSE - PYSPARK

-- Dimensión: Atletas
CREATE TABLE IF NOT EXISTS dim_athlete (
    id_athlete INTEGER PRIMARY KEY,
    athlete_id TEXT,
    name TEXT NOT NULL,
    gender TEXT,
    age REAL,
    country TEXT
);

-- Dimensión: Competencias
CREATE TABLE IF NOT EXISTS dim_competition (
    id_competition INTEGER PRIMARY KEY,
    competition TEXT NOT NULL,
    year INTEGER NOT NULL,
    category TEXT
);

-- Dimensión: Equipos
CREATE TABLE IF NOT EXISTS dim_team (
    id_team INTEGER PRIMARY KEY,
    team TEXT NOT NULL,
    coach TEXT
);


-- Tabla de Hechos: Levantamientos
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
    efficiency_ratio REAL,
    lift_difference REAL,
    performance_category TEXT,
    FOREIGN KEY (id_athlete) REFERENCES dim_athlete(id_athlete),
    FOREIGN KEY (id_competition) REFERENCES dim_competition(id_competition),
    FOREIGN KEY (id_team) REFERENCES dim_team(id_team)
);

CREATE INDEX IF NOT EXISTS idx_fact_athlete ON fact_lifting(id_athlete);
CREATE INDEX IF NOT EXISTS idx_fact_competition ON fact_lifting(id_competition);
CREATE INDEX IF NOT EXISTS idx_fact_team ON fact_lifting(id_team);
CREATE INDEX IF NOT EXISTS idx_athlete_country ON dim_athlete(country);
CREATE INDEX IF NOT EXISTS idx_competition_year ON dim_competition(year);

