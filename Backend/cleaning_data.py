"""
Módulo: cleaning_data.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo centraliza y ejecuta el *pipeline completo de limpieza de datos*
    del proyecto ZeroWaste Campus. Integra los submódulos de limpieza ubicados
    en `Backend/` en un flujo coherente y ordenado.

    El propósito principal es transformar el dataset bruto (extraído de Google Sheets)
    en un DataFrame limpio, estandarizado y listo para el análisis o visualización.

Dependencias:
    - pandas
    - re
    - unidecode
    - Backend.tipos_basicos_clean
    - Backend.numeric_clean
    - Backend.str_clean

Funciones principales:
    - cleaner_data(df, save_intermediate=False):
        Aplica todas las etapas de limpieza de forma secuencial, asegurando
        coherencia entre tipos de datos, fechas, valores categóricos,
        numéricos y texto libre.

Flujo general del pipeline:
    1 Normaliza nombres de columnas.
    2 Limpia fechas y booleanos.
    3 Limpia valores numéricos (enteros y decimales).
    4 Trata negativos como inválidos e imputa faltantes (diferenciado por columna).
    5 Detecta outliers (corrige en conteos de estudiantes, solo marca en kg).
    6 Corrige inconsistencias lógicas entre el booleano y la cantidad en kg.
    7 Limpia y estandariza texto y categorías.
    8 (Opcional) Exporta los datos intermedios a CSV.
"""

import pandas as pd
import re
from unidecode import unidecode

# --- Importación de submódulos de limpieza ---
from Backend.tipos_basicos_clean import clean_dates as date_cl
from Backend.tipos_basicos_clean import clean_booleans as bool_cl
from Backend.tipos_basicos_clean import corregir_inconsistencias as bool_corr
from Backend.numeric_clean import clean_integers as int_cl
from Backend.numeric_clean import clean_floats as float_cl
from Backend.numeric_clean import handle_missing_values as fmmn
from Backend.numeric_clean import handle_outliers as outlier_cl
from Backend.str_clean import clean_text
from Backend.str_clean import clean_categorical_options


# =====================================================
# FUNCIÓN PRINCIPAL: cleaner_data
# =====================================================
def cleaner_data(df, save_intermediate=False):
    """
    Aplica el pipeline completo de limpieza sobre un DataFrame de entrada.

    Descripción:
        Esta función orquesta la ejecución de todas las etapas de limpieza
        definidas en los submódulos de `Backend/`. Se encarga de asegurar
        que los datos sean coherentes, homogéneos y compatibles con los
        módulos de análisis y visualización del sistema ZeroWaste Campus.

    Pasos del proceso:
        1 **Normalización de nombres de columnas:**
            - Convierte todo a minúsculas.
            - Reemplaza espacios por guiones bajos.
            - Elimina tildes y caracteres especiales.

        2 **Limpieza de fechas y booleanos:**
            - Convierte `fecha_de_registro` a formato datetime estándar.
            - Normaliza respuestas tipo "Sí/No" (con o sin tilde) a True/False.

        3 **Limpieza de datos numéricos:**
            - Convierte valores enteros y decimales según sus columnas correspondientes.
            - Admite tanto punto (.) como coma (,) como separador decimal.

        4 **Tratamiento de negativos e imputación de faltantes:**
            - Convierte valores negativos a NaN (se asumen errores de digitación).
            - Los conteos de estudiantes se imputan con la mediana.
            - `cantidad_aproximada_desperdiciada_kg` se deja como NaN si falta,
              sin inventar un valor en la métrica principal del proyecto.

        5 **Detección de outliers:**
            - Conteos de estudiantes: detecta y corrige por mediana.
            - Kg desperdiciado: el rango IQR se calcula solo sobre los días
              con desperdicio real; los valores fuera de rango se marcan en
              `cantidad_aproximada_desperdiciada_kg_outlier`, pero no se
              sobrescriben.

        6 **Corrección de inconsistencias lógicas:**
            - Ajusta la relación entre `cantidad_aproximada_desperdiciada_kg`
              y `hubo_desperdicio_de_alimentos`, sin forzar el booleano
              cuando la cantidad es desconocida.

        7 **Limpieza de categorías y texto libre:**
            - Corrige categorías fuera del conjunto válido (reemplaza por "otros").
            - Limpia texto libre en campos de observaciones.

        8 **Exportación opcional:**
            - Si `save_intermediate=True`, exporta el resultado como
              `export_final.csv` con formato estándar latinoamericano
              (separador `;`, decimal `,`).

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
    df = fmmn(df)                                 # Negativos → NaN, imputar (diferenciado por columna)
    df = outlier_cl(df)                           # Detectar outliers (corrige enteros, marca kg)
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