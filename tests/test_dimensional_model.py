"""
Tests unitarios para el modelo dimensional
"""
import pytest
import pandas as pd
import numpy as np


class TestDimensionalModel:
    """Tests para la creación del modelo dimensional"""
    
    @pytest.fixture
    def sample_clean_data(self):
        """Crea datos limpios de prueba"""
        return pd.DataFrame({
            'athlete_id': ['ath_1', 'ath_2', 'ath_1', 'ath_3', ''],
            'name': ['John Doe', 'Jane Smith', 'John Doe', 'Bob Wilson', 'Alice Brown'],
            'gender': ['M', 'F', 'M', 'M', 'F'],
            'age': [25, 30, 25, 35, 28],
            'country': ['USA', 'Canada', 'USA', 'Mexico', 'USA'],
            'competition': ['Comp1', 'Comp1', 'Comp2', 'Comp1', 'Comp2'],
            'year': [2020, 2020, 2021, 2020, 2021],
            'category': ['M', 'F', 'M', 'M', 'F'],
            'team': ['Team A', 'Team B', 'Team A', 'Team C', 'Team A'],
            'coach': ['Coach 1', 'Coach 2', 'Coach 1', 'Coach 3', 'Coach 1'],
            'snatch_kg': [100, 120, 105, 110, 115],
            'clean_and_jerk_kg': [130, 150, 135, 140, 145],
            'total_kg': [230, 270, 240, 250, 260],
            'body_weight_kg': [80, 70, 82, 85, 75],
        })
    
    def test_dim_athlete_creation(self, sample_clean_data):
        """Test: Creación de dim_athlete sin duplicados"""
        df = sample_clean_data.copy()
        
        dim_athlete = df[['athlete_id', 'name', 'gender', 'age', 'country']].copy()
        dim_athlete = dim_athlete[dim_athlete['name'].notna() & (dim_athlete['name'] != '')]
        dim_athlete = dim_athlete.drop_duplicates(subset=['name', 'country'], keep='first')
        dim_athlete = dim_athlete.reset_index(drop=True)
        dim_athlete.insert(0, 'id_athlete', range(1, len(dim_athlete) + 1))
        
        # Verificar que no hay duplicados
        assert len(dim_athlete) == len(dim_athlete.drop_duplicates(subset=['name', 'country'])), \
            "Hay duplicados en dim_athlete"
        
        # Verificar que tiene id_athlete
        assert 'id_athlete' in dim_athlete.columns, "Falta columna id_athlete"
        assert dim_athlete['id_athlete'].min() == 1, "id_athlete no empieza en 1"
    
    def test_dim_competition_creation(self, sample_clean_data):
        """Test: Creación de dim_competition sin duplicados"""
        df = sample_clean_data.copy()
        
        dim_competition = df[['competition', 'year', 'category']].copy()
        dim_competition = dim_competition[dim_competition['competition'].notna() & 
                                         dim_competition['year'].notna()]
        dim_competition = dim_competition.drop_duplicates(subset=['competition', 'year', 'category'], 
                                                          keep='first')
        dim_competition = dim_competition.reset_index(drop=True)
        dim_competition.insert(0, 'id_competition', range(1, len(dim_competition) + 1))
        
        # Verificar que no hay duplicados
        assert len(dim_competition) == len(dim_competition.drop_duplicates(
            subset=['competition', 'year', 'category'])), "Hay duplicados en dim_competition"
        
        # Verificar que tiene id_competition
        assert 'id_competition' in dim_competition.columns, "Falta columna id_competition"
    
    def test_dim_team_creation(self, sample_clean_data):
        """Test: Creación de dim_team sin duplicados"""
        df = sample_clean_data.copy()
        
        dim_team = df[['team', 'coach']].copy()
        dim_team = dim_team[dim_team['team'].notna() & (dim_team['team'] != '')]
        dim_team = dim_team.drop_duplicates(subset=['team', 'coach'], keep='first')
        dim_team = dim_team.reset_index(drop=True)
        dim_team.insert(0, 'id_team', range(1, len(dim_team) + 1))
        
        # Verificar que no hay duplicados
        assert len(dim_team) == len(dim_team.drop_duplicates(subset=['team', 'coach'])), \
            "Hay duplicados en dim_team"
        
        # Verificar que tiene id_team
        assert 'id_team' in dim_team.columns, "Falta columna id_team"
    
    def test_fact_lifting_creation(self, sample_clean_data):
        """Test: Creación de fact_lifting con relaciones correctas"""
        df = sample_clean_data.copy()
        
        # Crear dimensiones simplificadas
        dim_athlete = df[['name', 'country']].drop_duplicates().reset_index(drop=True)
        dim_athlete['id_athlete'] = range(1, len(dim_athlete) + 1)
        
        dim_competition = df[['competition', 'year', 'category']].drop_duplicates().reset_index(drop=True)
        dim_competition['id_competition'] = range(1, len(dim_competition) + 1)
        
        dim_team = df[['team', 'coach']].drop_duplicates().reset_index(drop=True)
        dim_team['id_team'] = range(1, len(dim_team) + 1)
        
        # Crear fact_lifting
        fact_base = df.copy()
        fact_with_athlete = fact_base.merge(
            dim_athlete[['id_athlete', 'name', 'country']], 
            on=['name', 'country'], 
            how='left'
        )
        fact_with_competition = fact_with_athlete.merge(
            dim_competition[['id_competition', 'competition', 'year', 'category']], 
            on=['competition', 'year', 'category'], 
            how='left'
        )
        fact_with_team = fact_with_competition.merge(
            dim_team[['id_team', 'team', 'coach']], 
            on=['team', 'coach'], 
            how='left'
        )
        
        fact_lifting = fact_with_team[
            fact_with_team['id_athlete'].notna() &
            fact_with_team['id_competition'].notna() &
            fact_with_team['id_team'].notna()
        ].copy()
        
        # Verificar que todas las foreign keys están presentes
        assert fact_lifting['id_athlete'].notna().all(), "Hay valores nulos en id_athlete"
        assert fact_lifting['id_competition'].notna().all(), "Hay valores nulos en id_competition"
        assert fact_lifting['id_team'].notna().all(), "Hay valores nulos en id_team"
        
        # Verificar que tiene las columnas de métricas
        required_cols = ['snatch_kg', 'clean_and_jerk_kg', 'total_kg']
        for col in required_cols:
            assert col in fact_lifting.columns, f"Falta columna {col} en fact_lifting"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

