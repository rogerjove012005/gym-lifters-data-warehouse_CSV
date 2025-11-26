"""
Tests unitarios para la carga en base de datos
"""
import pytest
import sqlite3
import pandas as pd
import os
from pathlib import Path
from sqlalchemy import create_engine


class TestDatabase:
    """Tests para la carga y validación de la base de datos"""
    
    @pytest.fixture
    def sample_dimensions(self):
        """Crea dimensiones de prueba"""
        dim_athlete = pd.DataFrame({
            'id_athlete': [1, 2, 3],
            'athlete_id': ['ath_1', 'ath_2', 'ath_3'],
            'name': ['John Doe', 'Jane Smith', 'Bob Wilson'],
            'gender': ['M', 'F', 'M'],
            'age': [25, 30, 35],
            'country': ['USA', 'Canada', 'Mexico']
        })
        
        dim_competition = pd.DataFrame({
            'id_competition': [1, 2],
            'competition': ['Comp1', 'Comp2'],
            'year': [2020, 2021],
            'category': ['M', 'F']
        })
        
        dim_team = pd.DataFrame({
            'id_team': [1, 2],
            'team': ['Team A', 'Team B'],
            'coach': ['Coach 1', 'Coach 2']
        })
        
        return dim_athlete, dim_competition, dim_team
    
    @pytest.fixture
    def sample_fact(self, sample_dimensions):
        """Crea tabla de hechos de prueba"""
        dim_athlete, dim_competition, dim_team = sample_dimensions
        
        fact_lifting = pd.DataFrame({
            'id_athlete': [1, 2, 1, 3],
            'id_competition': [1, 1, 2, 1],
            'id_team': [1, 2, 1, 2],
            'snatch_kg': [100, 120, 105, 110],
            'clean_and_jerk_kg': [130, 150, 135, 140],
            'total_kg': [230, 270, 240, 250],
            'body_weight_kg': [80, 70, 82, 85],
            'event_rank': [1, 2, 1, 3],
            'medal': ['gold', 'silver', 'gold', 'bronze'],
            'record_status': ['WR', None, None, None],
            'lifting_style': ['classic', 'classic', 'classic', 'classic']
        })
        
        return fact_lifting
    
    @pytest.fixture
    def test_db(self, sample_dimensions, sample_fact, tmp_path):
        """Crea una base de datos de prueba temporal"""
        db_path = tmp_path / "test_warehouse.db"
        
        if db_path.exists():
            os.remove(db_path)
        
        engine = create_engine(f'sqlite:///{db_path}')
        
        dim_athlete, dim_competition, dim_team = sample_dimensions
        
        dim_athlete.to_sql('dim_athlete', con=engine, if_exists='replace', index=False)
        dim_competition.to_sql('dim_competition', con=engine, if_exists='replace', index=False)
        dim_team.to_sql('dim_team', con=engine, if_exists='replace', index=False)
        sample_fact.to_sql('fact_lifting', con=engine, if_exists='replace', index=False)
        
        return str(db_path)
    
    def test_tables_exist(self, test_db):
        """Test: Verificar que todas las tablas existen"""
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['dim_athlete', 'dim_competition', 'dim_team', 'fact_lifting']
        for table in expected_tables:
            assert table in tables, f"Tabla {table} no existe en la base de datos"
        
        conn.close()
    
    def test_table_row_counts(self, test_db):
        """Test: Verificar conteo de filas en cada tabla"""
        conn = sqlite3.connect(test_db)
        
        expected_counts = {
            'dim_athlete': 3,
            'dim_competition': 2,
            'dim_team': 2,
            'fact_lifting': 4
        }
        
        for table, expected_count in expected_counts.items():
            count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn)['count'].iloc[0]
            assert count == expected_count, \
                f"Tabla {table} tiene {count} filas, se esperaban {expected_count}"
        
        conn.close()
    
    def test_foreign_key_integrity(self, test_db):
        """Test: Verificar integridad referencial"""
        conn = sqlite3.connect(test_db)
        
        # Verificar que todos los id_athlete en fact_lifting existen en dim_athlete
        query = """
        SELECT COUNT(*) as invalid
        FROM fact_lifting f
        LEFT JOIN dim_athlete a ON f.id_athlete = a.id_athlete
        WHERE a.id_athlete IS NULL
        """
        invalid_athletes = pd.read_sql_query(query, conn)['invalid'].iloc[0]
        assert invalid_athletes == 0, "Hay id_athlete inválidos en fact_lifting"
        
        # Verificar que todos los id_competition en fact_lifting existen en dim_competition
        query = """
        SELECT COUNT(*) as invalid
        FROM fact_lifting f
        LEFT JOIN dim_competition c ON f.id_competition = c.id_competition
        WHERE c.id_competition IS NULL
        """
        invalid_competitions = pd.read_sql_query(query, conn)['invalid'].iloc[0]
        assert invalid_competitions == 0, "Hay id_competition inválidos en fact_lifting"
        
        # Verificar que todos los id_team en fact_lifting existen en dim_team
        query = """
        SELECT COUNT(*) as invalid
        FROM fact_lifting f
        LEFT JOIN dim_team t ON f.id_team = t.id_team
        WHERE t.id_team IS NULL
        """
        invalid_teams = pd.read_sql_query(query, conn)['invalid'].iloc[0]
        assert invalid_teams == 0, "Hay id_team inválidos en fact_lifting"
        
        conn.close()
    
    def test_data_types(self, test_db):
        """Test: Verificar tipos de datos en las tablas"""
        conn = sqlite3.connect(test_db)
        
        # Verificar que id_athlete es numérico
        query = "SELECT id_athlete FROM dim_athlete LIMIT 1"
        result = pd.read_sql_query(query, conn)
        assert pd.api.types.is_numeric_dtype(result['id_athlete']), \
            "id_athlete no es numérico"
        
        # Verificar que total_kg es numérico
        query = "SELECT total_kg FROM fact_lifting LIMIT 1"
        result = pd.read_sql_query(query, conn)
        assert pd.api.types.is_numeric_dtype(result['total_kg']), \
            "total_kg no es numérico"
        
        conn.close()
    
    def test_star_schema_structure(self, test_db):
        """Test: Verificar estructura del star schema"""
        conn = sqlite3.connect(test_db)
        
        # Verificar que hay al menos una tabla de hechos
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'fact_%';")
        fact_tables = [row[0] for row in cursor.fetchall()]
        assert len(fact_tables) >= 1, "No se encontró tabla de hechos"
        
        # Verificar que hay al menos 2 tablas de dimensiones
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'dim_%';")
        dim_tables = [row[0] for row in cursor.fetchall()]
        assert len(dim_tables) >= 2, "No se encontraron suficientes tablas de dimensiones"
        
        conn.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

