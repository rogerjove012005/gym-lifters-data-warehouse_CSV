# Proyecto RA1 - Data Warehouse ETL para Datos de Levantamiento de Pesas

Este proyecto implementa un proceso completo de ETL (Extract, Transform, Load) para construir un data warehouse dimensional a partir de datos de competencias de levantamiento de pesas. El objetivo es transformar datos crudos en un modelo estructurado que permita realizar análisis y consultas eficientes.

## Descripción del Proyecto

El proyecto trabaja con un dataset de atletas de levantamiento de pesas que incluye información sobre competencias, resultados, equipos y métricas de rendimiento. A través de diferentes fases, los datos pasan por un proceso de limpieza, transformación y carga en un data warehouse basado en el modelo dimensional (esquema en estrella).

El flujo completo incluye:
- Limpieza y preparación de datos con Pandas
- Implementación de ETL con Pandas
- Implementación de ETL con PySpark
- Carga de datos en SQLite
- Modelado dimensional con tablas de hechos y dimensiones

## Fases del Proyecto

### Fase 1: Exploración y Limpieza de Datos

En esta primera fase, trabajamos con el dataset original `gym_lifters.csv` para entender su estructura y prepararlo para el procesamiento posterior. Las tareas principales incluyen:

- **Exploración inicial**: Análisis de la estructura del dataset, tipos de datos, valores nulos y duplicados
- **Limpieza de datos**: 
  - Estandarización de nombres de columnas a snake_case
  - Eliminación de duplicados
  - Tratamiento de valores nulos e inválidos
  - Conversión de tipos de datos
  - Limpieza de unidades en columnas numéricas (por ejemplo, extraer números de valores como "154kg")
- **Validación**: Verificación de la calidad de los datos después de la limpieza
- **Exportación**: Guardado del dataset limpio en `gym_lifters_clean.csv`

Esta fase es crucial porque establece la base de datos limpia que se utilizará en las siguientes etapas del proceso ETL.

### Fase 2: ETL con Pandas

En esta fase implementamos el proceso ETL completo usando Pandas. El objetivo es crear un modelo dimensional con tablas de dimensiones y una tabla de hechos.

**Extracción (E)**: Cargamos el dataset limpio generado en la Fase 1.

**Transformación (T)**: Creamos el modelo dimensional:
- **dim_athlete**: Tabla de dimensiones con información única de cada atleta (ID, nombre, género, edad, país)
- **dim_competition**: Tabla de dimensiones con información de competencias (ID, nombre de competencia, año, categoría)
- **dim_team**: Tabla de dimensiones con información de equipos y coaches (ID, equipo, coach)
- **fact_lifting**: Tabla de hechos que contiene las métricas de levantamiento (pesos, rankings, medallas) relacionadas con las dimensiones mediante claves foráneas

La transformación incluye la eliminación de duplicados, la generación de IDs únicos para cada dimensión, y la creación de relaciones mediante operaciones de merge (equivalente a JOIN en SQL).

**Carga (L)**: Utilizamos SQLAlchemy y el método `to_sql()` de Pandas para cargar todas las tablas en la base de datos SQLite `warehouse_pandas.db`.

### Fase 3: ETL con PySpark

Esta fase replica el proceso ETL pero utilizando PySpark, lo que nos permite trabajar con grandes volúmenes de datos de manera distribuida. Las transformaciones incluyen:

- **Filtrado avanzado**: Selección de registros válidos con condiciones específicas (años entre 2010-2025, total_kg > 0)
- **Creación de columnas derivadas**: 
  - `efficiency_ratio`: Ratio de eficiencia (total_kg / body_weight_kg)
  - `lift_difference`: Diferencia entre clean_and_jerk y snatch
  - `performance_category`: Categorización del rendimiento (Elite, Advanced, Intermediate, Beginner)
- **Agregaciones**: Cálculos de estadísticas por país y categoría
- **Joins complejos**: Relaciones entre tablas usando la API de Spark SQL

El resultado se carga en `warehouse_pyspark.db`, que incluye las mismas dimensiones pero con métricas adicionales en la tabla de hechos.

## Herramientas Utilizadas

- **Pandas 2.1.4**: Para manipulación y análisis de datos estructurados
- **NumPy 1.24.3**: Para operaciones numéricas y manejo de arrays
- **PySpark 3.5.0**: Para procesamiento distribuido de grandes volúmenes de datos
- **SQLAlchemy 2.0.23**: Para la conexión y carga de datos en SQLite
- **Jupyter Notebook 7.0.6**: Entorno interactivo para desarrollo y documentación
- **SQLite**: Base de datos relacional para almacenar el data warehouse
- **Docker**: Para containerización y despliegue del entorno de trabajo

## Estructura de Carpetas

```
Practica/
├── data/                          # Datos del proyecto
│   ├── gym_lifters.csv           # Dataset original
│   └── gym_lifters_clean.csv     # Dataset limpio (generado en Fase 1)
│
├── notebooks/                     # Notebooks de Jupyter
│   ├── 01_pandas.ipynb          # Fase 1: Limpieza + Fase 2: ETL con Pandas
│   └── 02_pyspark.ipynb         # Fase 3: ETL con PySpark
│
├── warehouse/                     # Data Warehouse (bases de datos SQLite)
│   ├── warehouse_pandas.db       # Base de datos generada con Pandas
│   ├── warehouse_pyspark.db     # Base de datos generada con PySpark
│   ├── modelo_datawarehouse_pandas.sql    # DDL del modelo Pandas
│   └── modelo_datawarehouse_pyspark.sql   # DDL del modelo PySpark
│
├── docs/                          # Documentación
│   ├── README.md                 # Este archivo
│   └── diagrama.png              # Diagrama del modelo dimensional
│
├── Dockerfile                     # Configuración del contenedor Docker
├── docker-compose.yml            # Orquestación de servicios Docker
└── requirements.txt              # Dependencias de Python
```

## Instrucciones de Ejecución

### Ejecución con Docker (Recomendado)

Esta es la forma más sencilla de ejecutar el proyecto, ya que todas las dependencias están preconfiguradas.

1. **Requisitos previos**: Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

2. **Construir y ejecutar el contenedor**:
   ```bash
   docker compose up --build
   ```

3. **Acceder a Jupyter Notebook**: Una vez que el contenedor esté en ejecución, abre tu navegador y ve a:
   ```
   http://localhost:8888
   ```

4. **Ejecutar los notebooks**: 
   - Abre `01_pandas.ipynb` y ejecuta todas las celdas en orden
   - Luego abre `02_pyspark.ipynb` y ejecuta todas las celdas

5. **Detener el contenedor**: Cuando termines, presiona `Ctrl+C` en la terminal o ejecuta:
   ```bash
   docker compose down
   ```

### Ejecución sin Docker

Si prefieres ejecutar el proyecto directamente en tu máquina local:

1. **Requisitos previos**:
   - Python 3.11 o superior
   - Java 11 (necesario para PySpark)

2. **Crear un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar Jupyter** (si no está incluido):
   ```bash
   pip install jupyter notebook
   ```

5. **Iniciar Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

6. **Ejecutar los notebooks** en el mismo orden que se mencionó anteriormente.

**Nota importante**: Asegúrate de que las rutas en los notebooks sean correctas según desde dónde ejecutes Jupyter. Si ejecutas desde la raíz del proyecto, las rutas deben ser `data/gym_lifters.csv`. Si ejecutas desde la carpeta `notebooks/`, usa `../data/gym_lifters.csv`.

## Explicación Breve de Cada ETL

### ETL con Pandas

El proceso ETL con Pandas es ideal para datasets de tamaño medio que caben en memoria. Utiliza operaciones de DataFrame nativas de Pandas:

- **Extracción**: Lectura directa del CSV con `pd.read_csv()`
- **Transformación**: 
  - Operaciones de filtrado y selección de columnas
  - Eliminación de duplicados con `drop_duplicates()`
  - Creación de relaciones mediante `merge()` (equivalente a JOIN)
  - Generación de IDs secuenciales con `reset_index()`
- **Carga**: Uso de `to_sql()` de Pandas con SQLAlchemy para insertar datos en SQLite

**Ventajas**: Sintaxis simple, fácil de depurar, ideal para prototipado rápido.

### ETL con PySpark

El proceso ETL con PySpark está diseñado para manejar grandes volúmenes de datos de manera distribuida:

- **Extracción**: Lectura del CSV con `spark.read.csv()` que puede manejar archivos particionados
- **Transformación**:
  - Filtrado con `filter()` y expresiones complejas
  - Creación de columnas derivadas con `withColumn()` y funciones condicionales
  - Agregaciones con `groupBy()` y funciones de agregación
  - Joins optimizados con la API de Spark SQL
  - Uso de ventanas (`Window`) para generar IDs secuenciales
- **Carga**: Conversión a Pandas con `toPandas()` y luego carga en SQLite (en producción, se usaría escritura directa a bases de datos distribuidas)

**Ventajas**: Escalabilidad, procesamiento paralelo, optimización automática de consultas.

## Cómo se Cargaron los Datos en SQLite

### Método con Pandas

Para el ETL con Pandas, utilizamos SQLAlchemy para crear una conexión a SQLite y luego el método `to_sql()` de Pandas:

```python
from sqlalchemy import create_engine

# Crear conexión
engine = create_engine('sqlite:///warehouse/warehouse_pandas.db')

# Cargar cada tabla
dim_athlete.to_sql('dim_athlete', con=engine, if_exists='replace', index=False)
dim_competition.to_sql('dim_competition', con=engine, if_exists='replace', index=False)
dim_team.to_sql('dim_team', con=engine, if_exists='replace', index=False)
fact_lifting.to_sql('fact_lifting', con=engine, if_exists='replace', index=False)
```

El parámetro `if_exists='replace'` asegura que si la tabla ya existe, se reemplaza completamente. `index=False` evita que el índice del DataFrame se guarde como columna adicional.

### Método con PySpark

Para PySpark, el proceso es similar pero requiere una conversión intermedia:

```python
import sqlite3
import pandas as pd

# Crear conexión
conn = sqlite3.connect('warehouse/warehouse_pyspark.db')

# Convertir DataFrames de Spark a Pandas y cargar
dim_athlete_pd = dim_athlete.toPandas()
dim_athlete_pd.to_sql('dim_athlete', conn, if_exists='replace', index=False)

# Repetir para las demás tablas...
```

La conversión a Pandas es necesaria porque SQLite no tiene un conector nativo para PySpark. En un entorno de producción con grandes volúmenes de datos, se usarían sistemas como Hive, Delta Lake o escritura directa a bases de datos distribuidas.

## Diagrama del Modelo Dimensional

El modelo sigue un **esquema en estrella** (star schema), que es una de las estructuras más comunes en data warehousing:

```
                    fact_lifting
                  (Tabla de Hechos)
                         |
        +----------------+----------------+
        |                |                |
   dim_athlete    dim_competition    dim_team
  (Dimensión)      (Dimensión)      (Dimensión)
```

**Tabla de Hechos (fact_lifting)**:
- Contiene las métricas de levantamiento: `snatch_kg`, `clean_and_jerk_kg`, `total_kg`, `body_weight_kg`, `event_rank`, `medal`, `record_status`, `lifting_style`
- En la versión PySpark también incluye: `efficiency_ratio`, `lift_difference`, `performance_category`
- Se relaciona con las dimensiones mediante claves foráneas: `id_athlete`, `id_competition`, `id_team`

**Tablas de Dimensiones**:
- **dim_athlete**: Información descriptiva de los atletas (nombre, género, edad, país)
- **dim_competition**: Información de las competencias (nombre, año, categoría)
- **dim_team**: Información de equipos y coaches

Este diseño permite realizar consultas analíticas eficientes, ya que las dimensiones se almacenan una sola vez y se referencian desde la tabla de hechos, evitando redundancia y facilitando el mantenimiento.

Un diagrama visual más detallado se encuentra en `docs/diagrama.png`.

## Consultas y Queries de Ejemplo

Aquí tienes algunas consultas útiles que puedes ejecutar sobre el data warehouse:

### Consulta 1: Top 10 Atletas por Total Levantado

```sql
SELECT 
    a.name,
    a.country,
    a.gender,
    COUNT(f.id_athlete) as total_competitions,
    AVG(f.total_kg) as avg_total_kg,
    MAX(f.total_kg) as max_total_kg
FROM fact_lifting f
JOIN dim_athlete a ON f.id_athlete = a.id_athlete
GROUP BY a.id_athlete, a.name, a.country, a.gender
ORDER BY max_total_kg DESC
LIMIT 10;
```

### Consulta 2: Promedio de Total por País

```sql
SELECT 
    a.country,
    COUNT(DISTINCT a.id_athlete) as num_athletes,
    AVG(f.total_kg) as avg_total_kg,
    MAX(f.total_kg) as max_total_kg
FROM fact_lifting f
JOIN dim_athlete a ON f.id_athlete = a.id_athlete
GROUP BY a.country
ORDER BY avg_total_kg DESC
LIMIT 10;
```

### Consulta 3: Competencias con Más Participantes

```sql
SELECT 
    c.competition,
    c.year,
    c.category,
    COUNT(f.id_athlete) as num_participants,
    AVG(f.total_kg) as avg_total_kg
FROM fact_lifting f
JOIN dim_competition c ON f.id_competition = c.id_competition
GROUP BY c.id_competition, c.competition, c.year, c.category
ORDER BY num_participants DESC
LIMIT 10;
```

### Consulta 4: Equipos con Mejor Rendimiento

```sql
SELECT 
    t.team,
    t.coach,
    COUNT(DISTINCT f.id_athlete) as num_athletes,
    AVG(f.total_kg) as avg_total_kg,
    COUNT(CASE WHEN f.medal IS NOT NULL AND f.medal != '' THEN 1 END) as total_medals
FROM fact_lifting f
JOIN dim_team t ON f.id_team = t.id_team
GROUP BY t.id_team, t.team, t.coach
ORDER BY avg_total_kg DESC
LIMIT 10;
```

### Consulta 5: Evolución Temporal del Rendimiento

```sql
SELECT 
    c.year,
    COUNT(DISTINCT f.id_athlete) as num_athletes,
    AVG(f.total_kg) as avg_total_kg,
    MAX(f.total_kg) as max_total_kg
FROM fact_lifting f
JOIN dim_competition c ON f.id_competition = c.id_competition
WHERE c.year >= 2010
GROUP BY c.year
ORDER BY c.year;
```

### Consulta 6: Análisis de Medallas por País

```sql
SELECT 
    a.country,
    COUNT(CASE WHEN f.medal = 'gold' THEN 1 END) as gold_medals,
    COUNT(CASE WHEN f.medal = 'silver' THEN 1 END) as silver_medals,
    COUNT(CASE WHEN f.medal = 'bronze' THEN 1 END) as bronze_medals,
    COUNT(CASE WHEN f.medal IS NOT NULL AND f.medal != '' THEN 1 END) as total_medals
FROM fact_lifting f
JOIN dim_athlete a ON f.id_athlete = a.id_athlete
GROUP BY a.country
HAVING total_medals > 0
ORDER BY total_medals DESC;
```

Para ejecutar estas consultas, puedes usar cualquier cliente SQLite o ejecutarlas directamente desde Python:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('warehouse/warehouse_pandas.db')
result = pd.read_sql_query("TU_CONSULTA_AQUI", conn)
print(result)
conn.close()
```

## Conclusiones y Aprendizajes

Este proyecto ha sido una experiencia muy enriquecedora para entender el proceso completo de construcción de un data warehouse. Algunos de los aprendizajes más importantes:

**Sobre la Limpieza de Datos**: La fase de limpieza es fundamental y suele tomar más tiempo del esperado. Encontrar valores inconsistentes, manejar nulos de manera apropiada, y estandarizar formatos requiere mucha atención al detalle. Un dataset limpio es la base de todo el proceso posterior.

**Sobre el Modelado Dimensional**: El esquema en estrella es intuitivo y eficiente para análisis. Separar las dimensiones descriptivas de las métricas en la tabla de hechos no solo reduce redundancia, sino que también facilita el mantenimiento y las consultas analíticas.

**Sobre Pandas vs PySpark**: Cada herramienta tiene su lugar. Pandas es excelente para prototipado rápido y datasets que caben en memoria, con una sintaxis muy clara. PySpark, por otro lado, es indispensable cuando trabajas con grandes volúmenes de datos y necesitas procesamiento distribuido. La curva de aprendizaje de PySpark es más pronunciada, pero la capacidad de escalar es invaluable.

**Sobre el Proceso ETL**: La implementación de un ETL robusto requiere pensar en casos edge, manejo de errores, y validación de datos en cada paso. Los joins entre tablas deben hacerse con cuidado para no perder datos importantes, y es crucial verificar la integridad referencial.

**Sobre SQLite**: Aunque SQLite es perfecto para proyectos pequeños y medianos, tiene limitaciones en entornos de producción con alta concurrencia. Sin embargo, es una excelente opción para desarrollo, pruebas y proyectos académicos.

**Sobre Docker**: Containerizar el proyecto facilita enormemente la reproducibilidad y el despliegue. Evita problemas de "funciona en mi máquina" y permite que cualquier persona pueda ejecutar el proyecto con un solo comando.

En general, este proyecto ha sido una excelente introducción práctica a los conceptos de data warehousing, ETL, y procesamiento de datos a escala. La combinación de herramientas como Pandas, PySpark y SQLite proporciona una visión completa del ecosistema de procesamiento de datos moderno.

