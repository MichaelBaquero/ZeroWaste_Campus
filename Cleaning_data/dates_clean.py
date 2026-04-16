"""
Módulo: dates_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene funciones dedicadas a la normalización y limpieza de
    columnas de tipo fecha en el conjunto de datos. Su objetivo es garantizar
    que las fechas estén en un formato estándar (datetime64) para permitir un
    manejo correcto en análisis, filtrado y visualización.

Dependencias:
    - pandas

Funciones principales:
    - clean_dates(df, col_fecha="fecha_de_registro"):
        Convierte la columna de fecha indicada al tipo datetime, manejando
        errores de conversión y asegurando compatibilidad con diferentes
        formatos de entrada.
"""

import pandas as pd

# =====================================================
# FUNCIÓN: clean_dates
# =====================================================
def clean_dates(df, col_fecha="fecha_de_registro"):
    """
    Limpia y normaliza una columna de fechas dentro de un DataFrame.

    Parámetros:
        df (pd.DataFrame): DataFrame que contiene los datos originales.
        col_fecha (str): Nombre de la columna de fecha a procesar.
                         Por defecto: 'fecha_de_registro'.

    Proceso:
        - Verifica que la columna exista en el DataFrame.
        - Convierte los valores a tipo datetime con el parámetro `dayfirst=True`
          para asegurar compatibilidad con el formato latinoamericano (dd/mm/yyyy).
        - Utiliza `errors="coerce"` para asignar NaT a valores no convertibles.

    Retorna:
        pd.DataFrame: DataFrame con la columna de fechas convertida a formato datetime.
    """
    if col_fecha in df.columns:
        df[col_fecha] = pd.to_datetime(df[col_fecha], dayfirst=True, errors="coerce")
    return df