# ============================================================
# Dockerfile para Proyecto RA1 - Data Warehouse ETL
# ============================================================
# Este Dockerfile crea un contenedor con todas las dependencias
# necesarias para ejecutar los notebooks de Pandas y PySpark
# ============================================================

# Usar imagen base de Python con Jupyter
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Proyecto RA1"
LABEL description="Contenedor para ETL con Pandas y PySpark"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configurar JAVA_HOME para PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos (si existen) o instalar directamente
COPY requirements.txt* ./

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install \
    pandas==2.1.4 \
    numpy==1.24.3 \
    pyspark==3.5.0 \
    jupyter==1.0.0 \
    notebook==7.0.6 \
    sqlalchemy==2.0.23 \
    ipykernel==6.27.1

# Si existe requirements.txt, instalarlo también
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Crear directorios necesarios
RUN mkdir -p /app/data \
    /app/notebooks \
    /app/warehouse \
    /app/docs

# Copiar el contenido del proyecto
COPY . /app/

# Exponer puerto para Jupyter
EXPOSE 8888

# Comando por defecto: iniciar Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]

