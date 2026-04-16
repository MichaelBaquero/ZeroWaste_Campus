"""
Módulo: cleaning_data.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo centraliza y ejecuta el *pipeline completo de limpieza de datos*
    del proyecto ZeroWaste Campus. Integra todos los submódulos de la carpeta
    `Cleaning_data` en un flujo coherente y ordenado.

    El propósito principal es transformar el dataset bruto (extraído de Google Sheets o CSV)
    en un DataFrame limpio, estandarizado y listo para el análisis o visualización.

Dependencias:
    - pandas
    - re
    - unidecode
    - Cleaning_data.boolean_clean
    - Cleaning_data.dates_clean
    - Cleaning_data.Nums_clean
    - Cleaning_data.outliers_clean
    - Cleaning_data.str_clean

Funciones principales:
    - cleaner_data(df, save_intermediate=False):
        Aplica todas las etapas de limpieza de forma secuencial, asegurando coherencia entre tipos de datos,
        fechas, valores categóricos, numéricos y texto libre.

Flujo general del pipeline:
    1 Normaliza nombres de columnas.
    2 Limpia fechas, booleanos y numéricos.
    3 Rellena valores faltantes y maneja negativos.
    4 Detecta y corrige outliers.
    5 Corrige inconsistencias lógicas.
    6 Limpia y estandariza texto y categorías.
    7 (Opcional) Exporta los datos intermedios a CSV.
"""

import pandas as pd
import re
from unidecode import unidecode

# --- Importación de submódulos de limpieza ---
from Cleaning_data.dates_clean import clean_dates as date_cl
from Cleaning_data.boolean_clean import clean_booleans as bool_cl
from Cleaning_data.boolean_clean import corregir_inconsistencias as bool_corr
from Cleaning_data.Nums_clean import clean_integers as int_cl
from Cleaning_data.Nums_clean import clean_floats as float_cl
from Cleaning_data.Nums_clean import fill_missing_with_medians_and_keep_negatives as fmmn
from Cleaning_data.outliers_clean import handle_outliers as outlier_cl
from Cleaning_data.str_clean import clean_text
from Cleaning_data.str_clean import clean_categorical_options


# =====================================================
# FUNCIÓN PRINCIPAL: cleaner_data
# =====================================================
def cleaner_data(df, save_intermediate=False):
    """
    Aplica el pipeline completo de limpieza sobre un DataFrame de entrada.

    Descripción:
        Esta función orquesta la ejecución de todas las etapas de limpieza definidas
        en los submódulos de la carpeta `Cleaning_data`. Se encarga de asegurar que los datos
        sean coherentes, homogéneos y compatibles con los módulos de análisis y visualización
        del sistema ZeroWaste Campus.

    Pasos del proceso:
        1 **Normalización de nombres de columnas:**
            - Convierte todo a minúsculas.
            - Reemplaza espacios por guiones bajos.
            - Elimina tildes y caracteres especiales.
        
        2 **Limpieza de fechas:**
            - Convierte la columna `fecha_de_registro` a formato datetime estándar.
        
        3 **Limpieza de booleanos:**
            - Normaliza respuestas tipo "Sí/No" a valores True/False.
        
        4 **Limpieza de datos numéricos:**
            - Convierte valores enteros y decimales según sus columnas correspondientes.
            - Admite tanto punto (.) como coma (,) como separador decimal.
        
        5 **Relleno de faltantes y manejo de negativos:**
            - Sustituye valores nulos por la mediana de la columna.
            - Mantiene registros negativos en un DataFrame separado y los reincorpora.
        
        6 **Corrección de outliers:**
            - Detecta valores atípicos (fuera de 1.5 * IQR).
            - Sustituye outliers por la mediana de la columna.
        
        7 **Corrección de inconsistencias lógicas:**
            - Ajusta la relación entre `cantidad_aproximada_desperdiciada_kg`
              y `hubo_desperdicio_de_alimentos`.
        
        8 **Limpieza de categorías y texto libre:**
            - Corrige categorías fuera del conjunto válido (reemplaza por "otros").
            - Limpia texto libre en campos de observaciones.

        9 **Exportación opcional:**
            - Si `save_intermediate=True`, exporta el resultado como `export_final.csv`
              con formato estándar latinoamericano (separador `;`, decimal `,`).

    Parámetros:
        df (pd.DataFrame): DataFrame original sin limpiar.
        save_intermediate (bool, opcional): Si es True, guarda el DataFrame limpio como CSV.

    Retorna:
        pd.DataFrame: DataFrame completamente limpio y listo para análisis.
    """

    # --- 1️ Normalización de nombres de columnas ---
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_")
        .map(unidecode).str.replace(r"[^0-9a-zA-Z_]", "", regex=True)
    )

    # --- 2️ Definir columnas numéricas relevantes ---
    cols_enteros = [
        "numero_de_estudiantes_atendidos_hoy",
        "numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion"
    ]
    cols_floats = ["cantidad_aproximada_desperdiciada_kg"]

    # --- 3️ Pipeline de limpieza en orden lógico ---
    df = date_cl(df)                              # Fechas primero
    df = bool_cl(df)                              # Normalizar booleanos (Sí/No → True/False)
    df = float_cl(df, cols_floats)                # Limpiar floats
    df = int_cl(df, cols_enteros)                 # Limpiar enteros
    df = fmmn(df)                                 # Rellenar faltantes / manejar negativos
    df = outlier_cl(df)                           # Corregir outliers
    df = bool_corr(df)                            # Corregir inconsistencias lógicas
    df = clean_categorical_options(df)            # Corregir valores categóricos
    df = clean_text(df)                           # Limpieza de texto libre

    # --- 4️ Guardado opcional ---
    if save_intermediate:
        df.to_csv(
            "export_final.csv",
            sep=';', decimal=',', encoding='utf-8-sig', index=False
        )

    return df