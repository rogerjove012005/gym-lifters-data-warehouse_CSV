# 🏋️ Weightlifting Data Warehouse ETL Pipeline

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-green.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive ETL (Extract, Transform, Load) pipeline for building a dimensional data warehouse from weightlifting competition data. This project transforms raw competition data into a structured star schema model optimized for analytical queries and business intelligence.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Docker Installation (Recommended)](#docker-installation-recommended)
  - [Local Installation](#local-installation)
- [Usage](#usage)
- [Data Model](#data-model)
- [Example Queries](#example-queries)
- [Project Phases](#project-phases)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a complete data warehousing solution for weightlifting competition data. It processes raw CSV data through multiple ETL pipelines using both Pandas (for medium-scale data) and PySpark (for distributed processing), ultimately loading the transformed data into a SQLite-based dimensional data warehouse following the star schema pattern.

### Key Objectives

- **Data Quality**: Comprehensive data cleaning and validation
- **Scalability**: Support for both single-machine (Pandas) and distributed (PySpark) processing
- **Analytics-Ready**: Dimensional model optimized for analytical queries
- **Reproducibility**: Containerized environment for consistent execution

## ✨ Features

- 🔄 **Multi-Stage ETL Pipeline**: Data extraction, transformation, and loading with validation
- 📊 **Dimensional Modeling**: Star schema with fact and dimension tables
- 🐼 **Dual Processing Engines**: Pandas for in-memory processing, PySpark for distributed computing
- 🐳 **Dockerized Environment**: One-command setup and execution
- 📈 **Analytical Queries**: Pre-built SQL examples for common analytics
- ✅ **Data Validation**: Built-in data quality checks and integrity validation
- 📝 **Comprehensive Documentation**: Detailed documentation and code examples

## 🏗️ Architecture

The project follows a three-phase ETL architecture:

```
Raw Data (CSV) → Data Cleaning → ETL Processing → Dimensional Warehouse (SQLite)
     ↓                ↓                ↓                      ↓
gym_lifters.csv  Clean Dataset   Pandas/PySpark      Star Schema DB
```

### Data Flow

1. **Extract**: Load raw competition data from CSV files
2. **Transform**: 
   - Clean and standardize data
   - Create dimensional model (dimensions + facts)
   - Generate derived metrics and aggregations
3. **Load**: Persist transformed data into SQLite warehouse

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Data Processing** | Pandas | 2.1.4 | In-memory data manipulation |
| **Distributed Processing** | PySpark | 3.5.0 | Large-scale data processing |
| **Database** | SQLite | Latest | Data warehouse storage |
| **ORM** | SQLAlchemy | 2.0.23 | Database connectivity |
| **Notebooks** | Jupyter | 7.0.6 | Interactive development |
| **Containerization** | Docker | Latest | Environment management |
| **Language** | Python | 3.11+ | Core programming language |

## 📁 Project Structure

```
gym-lifters-data-warehouse_CSV/
├── data/                          # Data files
│   ├── gym_lifters.csv           # Raw dataset
│   └── gym_lifters_clean*.csv    # Cleaned datasets (generated)
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_pandas.ipynb          # Phase 1 & 2: Cleaning + Pandas ETL
│   └── 02_pyspark.ipynb         # Phase 3: PySpark ETL
│
├── warehouse/                     # Data warehouse
│   ├── warehouse_pandas.db      # Pandas-generated database
│   ├── warehouse_pyspark.db    # PySpark-generated database
│   ├── modelo_datawarehouse_pandas.sql    # DDL schema (Pandas)
│   └── modelo_datawarehouse_pyspark.sql   # DDL schema (PySpark)
│
├── docs/                          # Documentation
│   ├── README.md                # This file
│   └── diagrama_flujo.*         # Architecture diagrams
│
├── Dockerfile                     # Docker image configuration
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
└── verificar_proyecto.py         # Project verification script
```

## 🚀 Getting Started

### Prerequisites

- **Docker** (recommended): Docker Desktop or Docker Engine
- **OR Local Setup**:
  - Python 3.11 or higher
  - Java 11+ (required for PySpark)
  - pip package manager

### Docker Installation (Recommended)

The easiest way to run this project is using Docker, which handles all dependencies automatically.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/gym-lifters-data-warehouse_CSV.git
   cd gym-lifters-data-warehouse_CSV
   ```

2. **Build and start the container**:
   ```bash
   docker compose up --build
   ```

3. **Access Jupyter Notebook**:
   - Open your browser and navigate to: `http://localhost:8888`
   - The Jupyter interface will be available without authentication

4. **Execute the notebooks**:
   - Open `notebooks/01_pandas.ipynb` and run all cells sequentially
   - Then open `notebooks/02_pyspark.ipynb` and execute all cells

5. **Stop the container**:
   ```bash
   docker compose down
   ```

### Local Installation

If you prefer to run the project locally without Docker:

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

4. **Execute notebooks** in the same order as described above.

> **Note**: Ensure file paths in notebooks match your execution context. If running from project root, use `data/gym_lifters.csv`. If running from `notebooks/`, use `../data/gym_lifters.csv`.

## 💻 Usage

### Running the ETL Pipeline

1. **Data Cleaning Phase** (Notebook 01):
   - Loads raw data from `data/gym_lifters.csv`
   - Performs data cleaning and standardization
   - Exports cleaned data to `data/gym_lifters_clean.csv`

2. **Pandas ETL Phase** (Notebook 01):
   - Creates dimensional model using Pandas
   - Generates dimension tables: `dim_athlete`, `dim_competition`, `dim_team`
   - Creates fact table: `fact_lifting`
   - Loads data into `warehouse/warehouse_pandas.db`

3. **PySpark ETL Phase** (Notebook 02):
   - Replicates ETL process using PySpark
   - Adds derived metrics: `efficiency_ratio`, `lift_difference`, `performance_category`
   - Loads data into `warehouse/warehouse_pyspark.db`

### Verifying the Project

Run the verification script to check project completeness:

```bash
python verificar_proyecto.py
```

## 📊 Data Model

The data warehouse follows a **star schema** design pattern:

```
                    fact_lifting
                  (Fact Table)
                         |
        +----------------+----------------+
        |                |                |
   dim_athlete    dim_competition    dim_team
  (Dimension)      (Dimension)      (Dimension)
```

### Fact Table: `fact_lifting`

Contains measurable lifting metrics:
- **Basic Metrics**: `snatch_kg`, `clean_and_jerk_kg`, `total_kg`, `body_weight_kg`
- **Competition Data**: `event_rank`, `medal`, `record_status`, `lifting_style`
- **Derived Metrics** (PySpark version): `efficiency_ratio`, `lift_difference`, `performance_category`
- **Foreign Keys**: `id_athlete`, `id_competition`, `id_team`

### Dimension Tables

- **`dim_athlete`**: Athlete descriptive information (name, gender, age, country)
- **`dim_competition`**: Competition details (name, year, category)
- **`dim_team`**: Team and coach information

This design enables efficient analytical queries by storing descriptive data once and referencing it from the fact table, reducing redundancy and improving maintainability.

## 📝 Example Queries

### Top 10 Athletes by Total Weight Lifted

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

### Average Performance by Country

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

### Competitions with Most Participants

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

### Executing Queries from Python

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('warehouse/warehouse_pandas.db')
result = pd.read_sql_query("""
    SELECT country, AVG(total_kg) as avg_total
    FROM fact_lifting f
    JOIN dim_athlete a ON f.id_athlete = a.id_athlete
    GROUP BY country
    ORDER BY avg_total DESC
""", conn)
print(result)
conn.close()
```

## 🔄 Project Phases

### Phase 1: Data Exploration and Cleaning

**Objective**: Prepare raw data for ETL processing

**Activities**:
- Dataset structure analysis
- Data type validation
- Null value and duplicate detection
- Column name standardization (snake_case)
- Data type conversion
- Unit extraction from numeric columns (e.g., "154kg" → 154)
- Export cleaned dataset

**Output**: `data/gym_lifters_clean.csv`

### Phase 2: Pandas ETL

**Objective**: Build dimensional warehouse using Pandas

**Process**:
- **Extract**: Load cleaned dataset
- **Transform**: 
  - Create dimension tables (`dim_athlete`, `dim_competition`, `dim_team`)
  - Create fact table (`fact_lifting`)
  - Generate unique IDs and establish relationships
- **Load**: Persist to SQLite using SQLAlchemy

**Output**: `warehouse/warehouse_pandas.db`

### Phase 3: PySpark ETL

**Objective**: Replicate ETL with distributed processing capabilities

**Enhancements**:
- Advanced filtering (year ranges, weight thresholds)
- Derived metrics calculation:
  - `efficiency_ratio`: Performance efficiency metric
  - `lift_difference`: Snatch vs Clean & Jerk comparison
  - `performance_category`: Athlete classification (Elite/Advanced/Intermediate/Beginner)
- Complex aggregations and window functions
- Optimized joins using Spark SQL

**Output**: `warehouse/warehouse_pyspark.db`

## 🔧 Technical Details

### ETL Implementation Comparison

| Aspect | Pandas | PySpark |
|--------|--------|---------|
| **Use Case** | Medium datasets (fits in memory) | Large-scale distributed processing |
| **Syntax** | Simple, intuitive | More complex, SQL-like |
| **Performance** | Fast for in-memory operations | Optimized for distributed computing |
| **Scalability** | Limited by RAM | Horizontally scalable |
| **Best For** | Prototyping, small-medium data | Production, big data scenarios |

### Data Loading Methods

**Pandas Approach**:
```python
from sqlalchemy import create_engine

engine = create_engine('sqlite:///warehouse/warehouse_pandas.db')
df.to_sql('table_name', con=engine, if_exists='replace', index=False)
```

**PySpark Approach**:
```python
# Convert Spark DataFrame to Pandas for SQLite compatibility
df_pandas = spark_df.toPandas()
df_pandas.to_sql('table_name', conn, if_exists='replace', index=False)
```

> **Note**: In production environments, PySpark would write directly to distributed storage systems (Hive, Delta Lake, etc.) rather than converting to Pandas.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Weightlifting competition data providers
- Open-source community for excellent tools and libraries
- Contributors and reviewers

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub or contact the project maintainers.

---

**Built with ❤️ for data engineering and analytics**
