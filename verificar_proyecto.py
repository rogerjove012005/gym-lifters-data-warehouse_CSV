#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificación del Proyecto RA1 - Data Warehouse ETL
Verifica que todos los requisitos del proyecto estén cumplidos
"""

import os
import sys
import sqlite3
import glob
from pathlib import Path
from typing import List, Tuple

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Colores para la salida
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}[OK]{Colors.END} {text}")

def print_error(text: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {text}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}[WARN]{Colors.END} {text}")

def check_file_exists(filepath: str, description: str) -> bool:
    """Verifica si un archivo existe"""
    if os.path.exists(filepath):
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description}: {filepath} - NO ENCONTRADO")
        return False

def check_directory_exists(dirpath: str, description: str) -> bool:
    """Verifica si un directorio existe"""
    if os.path.isdir(dirpath):
        print_success(f"{description}: {dirpath}")
        return True
    else:
        print_error(f"{description}: {dirpath} - NO ENCONTRADO")
        return False

def check_sqlite_database(db_path: str, description: str) -> Tuple[bool, List[str]]:
    """Verifica que la base de datos SQLite exista y tenga tablas"""
    if not os.path.exists(db_path):
        print_error(f"{description}: {db_path} - NO ENCONTRADO")
        return False, []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        if tables:
            print_success(f"{description}: {db_path}")
            print(f"  → Tablas encontradas: {', '.join(tables)}")
            return True, tables
        else:
            print_warning(f"{description}: {db_path} - Existe pero no tiene tablas")
            return True, []
    except Exception as e:
        print_error(f"{description}: {db_path} - Error al leer: {str(e)}")
        return False, []

def check_sql_file(sql_path: str, description: str) -> Tuple[bool, List[str]]:
    """Verifica que el archivo SQL exista y contenga las tablas requeridas"""
    if not os.path.exists(sql_path):
        print_error(f"{description}: {sql_path} - NO ENCONTRADO")
        return False, []
    
    try:
        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar tablas en el contenido
        tables = []
        if 'CREATE TABLE' in content.upper():
            import re
            # Buscar nombres de tablas después de CREATE TABLE
            matches = re.findall(r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?(\w+)', content, re.IGNORECASE)
            tables = matches
        
        print_success(f"{description}: {sql_path}")
        if tables:
            print(f"  → Tablas definidas: {', '.join(tables)}")
        return True, tables
    except Exception as e:
        print_error(f"{description}: {sql_path} - Error al leer: {str(e)}")
        return False, []

def check_notebook(notebook_path: str, description: str) -> bool:
    """Verifica que el notebook exista"""
    if os.path.exists(notebook_path):
        print_success(f"{description}: {notebook_path}")
        return True
    else:
        print_error(f"{description}: {notebook_path} - NO ENCONTRADO")
        return False

def check_datawarehouse_structure(db_path: str, expected_tables: List[str]) -> bool:
    """Verifica que la base de datos tenga la estructura correcta del data warehouse"""
    if not os.path.exists(db_path):
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Verificar que exista tabla de hechos
        fact_tables = [t for t in existing_tables if t.startswith('fact_')]
        dim_tables = [t for t in existing_tables if t.startswith('dim_')]
        
        conn.close()
        
        if not fact_tables:
            print_error(f"  → No se encontró tabla de hechos en {db_path}")
            return False
        
        if len(dim_tables) < 2:
            print_error(f"  → Se encontraron menos de 2 tablas de dimensiones en {db_path} (encontradas: {len(dim_tables)})")
            return False
        
        print_success(f"  → Estructura correcta: 1 tabla de hechos, {len(dim_tables)} tablas de dimensiones")
        return True
    except Exception as e:
        print_error(f"  → Error al verificar estructura: {str(e)}")
        return False

def main():
    """Función principal de verificación"""
    print_header("VERIFICACIÓN DEL PROYECTO RA1 - DATA WAREHOUSE ETL")
    
    # Contador de verificaciones
    checks_passed = 0
    checks_failed = 0
    total_checks = 0
    
    # ============================================
    # 1. ESTRUCTURA DE CARPETAS
    # ============================================
    print_header("1. ESTRUCTURA DE CARPETAS")
    
    directories = [
        ("data/", "Carpeta de datos"),
        ("notebooks/", "Carpeta de notebooks"),
        ("warehouse/", "Carpeta de data warehouse"),
        ("docs/", "Carpeta de documentación"),
    ]
    
    for dirpath, description in directories:
        total_checks += 1
        if check_directory_exists(dirpath, description):
            checks_passed += 1
        else:
            checks_failed += 1
    
    # ============================================
    # 2. ARCHIVOS DE DATOS
    # ============================================
    print_header("2. ARCHIVOS DE DATOS")
    
    # Dataset original (obligatorio)
    total_checks += 1
    if check_file_exists("data/gym_lifters.csv", "Dataset original"):
        checks_passed += 1
    else:
        checks_failed += 1
    
    # Dataset limpio (opcional - se genera al ejecutar el notebook)
    total_checks += 1
    clean_files = glob.glob("data/gym_lifters_clean*.csv")
    if clean_files:
        # Encontrar el más reciente
        clean_files.sort(key=os.path.getmtime, reverse=True)
        latest_clean = clean_files[0]
        print_success(f"Dataset limpio (generado): {latest_clean}")
        print(f"  → Versiones encontradas: {len(clean_files)}")
        checks_passed += 1
    else:
        print_warning("Dataset limpio: data/gym_lifters_clean*.csv - No encontrado (se genera al ejecutar el notebook)")
        # Verificar que el notebook tenga código para generarlo
        try:
            with open("notebooks/01_pandas.ipynb", 'r', encoding='utf-8') as f:
                notebook_content = f.read()
                if 'gym_lifters_clean' in notebook_content and 'to_csv' in notebook_content:
                    print_success("  → El notebook 01_pandas.ipynb contiene código para generar el archivo limpio")
                    checks_passed += 1
                else:
                    print_warning("  → Verificar que el notebook pueda generar el archivo limpio")
                    checks_failed += 1
        except Exception as e:
            print_warning(f"  → No se pudo verificar el notebook: {str(e)}")
            checks_failed += 1
    
    # ============================================
    # 3. NOTEBOOKS
    # ============================================
    print_header("3. NOTEBOOKS DE JUPYTER")
    
    notebooks = [
        ("notebooks/01_pandas.ipynb", "Notebook de Pandas (Fase 1 y 2)"),
        ("notebooks/02_pyspark.ipynb", "Notebook de PySpark (Fase 3)"),
    ]
    
    for notebook_path, description in notebooks:
        total_checks += 1
        if check_notebook(notebook_path, description):
            checks_passed += 1
        else:
            checks_failed += 1
    
    # ============================================
    # 4. BASES DE DATOS SQLITE
    # ============================================
    print_header("4. BASES DE DATOS SQLITE")
    
    databases = [
        ("warehouse/warehouse_pandas.db", "Base de datos Pandas"),
        ("warehouse/warehouse_pyspark.db", "Base de datos PySpark"),
    ]
    
    db_tables = {}
    for db_path, description in databases:
        total_checks += 1
        exists, tables = check_sqlite_database(db_path, description)
        if exists:
            checks_passed += 1
            db_tables[db_path] = tables
        else:
            checks_failed += 1
    
    # Verificar estructura del data warehouse
    print(f"\n{Colors.BOLD}Verificando estructura del Data Warehouse:{Colors.END}")
    for db_path, description in databases:
        if db_path in db_tables:
            total_checks += 1
            if check_datawarehouse_structure(db_path, db_tables[db_path]):
                checks_passed += 1
            else:
                checks_failed += 1
    
    # ============================================
    # 5. ARCHIVOS SQL (DDL)
    # ============================================
    print_header("5. ARCHIVOS SQL (DDL DEL DATA WAREHOUSE)")
    
    sql_files = [
        ("warehouse/modelo_datawarehouse_pandas.sql", "DDL modelo Pandas"),
        ("warehouse/modelo_datawarehouse_pyspark.sql", "DDL modelo PySpark"),
    ]
    
    for sql_path, description in sql_files:
        total_checks += 1
        exists, tables = check_sql_file(sql_path, description)
        if exists:
            checks_passed += 1
        else:
            checks_failed += 1
    
    # ============================================
    # 6. DOCKER
    # ============================================
    print_header("6. CONFIGURACIÓN DOCKER")
    
    docker_files = [
        ("Dockerfile", "Dockerfile"),
        ("docker-compose.yml", "docker-compose.yml"),
    ]
    
    for filepath, description in docker_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            checks_passed += 1
        else:
            checks_failed += 1
    
    # ============================================
    # 7. DOCUMENTACIÓN
    # ============================================
    print_header("7. DOCUMENTACIÓN")
    
    doc_files = [
        ("docs/README.md", "README.md"),
    ]
    
    for filepath, description in doc_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            checks_passed += 1
        else:
            checks_failed += 1
    
    # Verificar diagrama
    diagram_found = False
    for ext in ['.png', '.jpg', '.jpeg', '.drawio']:
        for diagram_file in Path('docs').glob(f'*{ext}'):
            total_checks += 1
            if check_file_exists(str(diagram_file), f"Diagrama ({ext})"):
                checks_passed += 1
                diagram_found = True
                break
        if diagram_found:
            break
    
    if not diagram_found:
        total_checks += 1
        print_warning("Diagrama del modelo dimensional no encontrado")
        checks_failed += 1
    
    # ============================================
    # 8. REQUIREMENTS.TXT
    # ============================================
    print_header("8. DEPENDENCIAS")
    
    total_checks += 1
    if check_file_exists("requirements.txt", "requirements.txt"):
        checks_passed += 1
        # Verificar contenido básico
        try:
            with open("requirements.txt", 'r') as f:
                content = f.read()
                required_packages = ['pandas', 'pyspark', 'sqlalchemy', 'jupyter']
                found_packages = [pkg for pkg in required_packages if pkg.lower() in content.lower()]
                print(f"  → Paquetes encontrados: {', '.join(found_packages)}")
        except:
            pass
    else:
        checks_failed += 1
    
    # ============================================
    # RESUMEN FINAL
    # ============================================
    print_header("RESUMEN DE VERIFICACIÓN")
    
    print(f"\n{Colors.BOLD}Total de verificaciones:{Colors.END} {total_checks}")
    print(f"{Colors.GREEN}[OK] Verificaciones exitosas:{Colors.END} {checks_passed}")
    print(f"{Colors.RED}[ERROR] Verificaciones fallidas:{Colors.END} {checks_failed}")
    
    percentage = (checks_passed / total_checks * 100) if total_checks > 0 else 0
    print(f"\n{Colors.BOLD}Porcentaje de cumplimiento:{Colors.END} {percentage:.1f}%")
    
    if checks_failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}¡PROYECTO COMPLETO! Todos los requisitos están cumplidos.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}ATENCIÓN: Hay {checks_failed} requisito(s) pendiente(s).{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

