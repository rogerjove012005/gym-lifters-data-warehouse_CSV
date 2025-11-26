"""
Tests unitarios para la limpieza de datos
"""
import pytest
import pandas as pd
import numpy as np
import os
from pathlib import Path


class TestDataCleaning:
    """Tests para la fase de limpieza de datos"""
    
    @pytest.fixture
    def sample_raw_data(self):
        """Crea datos de prueba simulando el dataset crudo"""
        return pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith', '  BOB WILSON  ', '?', 'N/A'],
            'Country': ['USA', 'Canada', 'Mexico', 'Unknown', ''],
            'Age': ['25', '30', '?', '35', '40'],
            'Total Kg': ['200kg', '250', '300kg', '?', ''],
            'Year': [2020, 2021, '?', 2022, 2023],
            'Snatch Kg': ['100kg', '120', '150kg', '?', ''],
        })
    
    def test_remove_duplicates(self, sample_raw_data):
        """Test: Eliminación de duplicados"""
        df = sample_raw_data.copy()
        df_duplicated = pd.concat([df, df.iloc[[0]]], ignore_index=True)
        
        df_cleaned = df_duplicated.drop_duplicates()
        
        assert len(df_cleaned) == len(df), "No se eliminaron los duplicados correctamente"
    
    def test_column_name_normalization(self, sample_raw_data):
        """Test: Normalización de nombres de columnas a snake_case"""
        df = sample_raw_data.copy()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        assert 'total_kg' in df.columns, "Las columnas no se normalizaron correctamente"
        assert 'snatch_kg' in df.columns, "Las columnas no se normalizaron correctamente"
    
    def test_invalid_values_replacement(self, sample_raw_data):
        """Test: Reemplazo de valores inválidos por NaN"""
        df = sample_raw_data.copy()
        valores_invalidos = ['?', 'n/a', 'na', 'unknown', '-1', 'none']
        
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].replace(valores_invalidos, np.nan)
        
        assert df['Name'].isna().any(), "Los valores inválidos no se reemplazaron"
    
    def test_numeric_column_cleaning(self):
        """Test: Limpieza de columnas numéricas con unidades"""
        df = pd.DataFrame({
            'weight': ['100kg', '200', '150kg', '?', ''],
        })
        
        df['weight'] = df['weight'].astype(str).str.extract(r'(\d+\.?\d*)', expand=False)
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
        
        assert df['weight'].dtype in [np.float64, np.int64], "La columna no es numérica"
        assert df['weight'].iloc[0] == 100.0, "No se extrajo correctamente el número"
        assert df['weight'].iloc[1] == 200.0, "No se extrajo correctamente el número"
    
    def test_year_validation(self):
        """Test: Validación de años en rango válido"""
        df = pd.DataFrame({
            'year': [2020, 1800, 2030, 2021, 1900]
        })
        
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['year'] = df['year'].where((df['year'] >= 1900) & (df['year'] <= 2025), np.nan)
        
        assert df['year'].iloc[0] == 2020, "Año válido no se mantuvo"
        assert pd.isna(df['year'].iloc[1]), "Año inválido no se convirtió a NaN"
        assert pd.isna(df['year'].iloc[2]), "Año inválido no se convirtió a NaN"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

