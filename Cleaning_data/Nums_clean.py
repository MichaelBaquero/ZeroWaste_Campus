"""
Módulo: Nums_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene las funciones de limpieza y estandarización de
    columnas numéricas, tanto enteras como decimales.  
    Se encarga de:
        - Asegurar que los números sean válidos y tengan el tipo correcto.
        - Corregir errores de formato (coma vs punto decimal, separadores de miles).
        - Rellenar valores faltantes mediante la mediana.
        - Conservar valores negativos válidos y mantener la integridad de los datos.

Dependencias:
    - pandas
    - re
    - unidecode

Funciones principales:
    - clean_integers(df, cols_enteros): Limpia y convierte columnas enteras.
    - clean_floats(df, cols_floats): Normaliza valores decimales y corrige formatos.
    - fill_missing_with_medians_and_keep_negatives(df): Rellena faltantes con mediana y conserva negativos.
"""

import pandas as pd
import re
from unidecode import unidecode


# =====================================================
# FUNCIÓN: clean_integers
# =====================================================
def clean_integers(df, cols_enteros):
    """
    Limpia columnas numéricas enteras dentro de un DataFrame.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos.
        cols_enteros (list[str]): Lista de nombres de columnas que deben ser enteras.

    Proceso:
        - Convierte los valores a texto y elimina caracteres no numéricos.
        - Extrae solo los dígitos válidos (incluyendo signo negativo si existe).
        - Convierte el resultado a tipo entero con soporte para valores nulos (Int64).

    Retorna:
        pd.DataFrame: DataFrame con las columnas enteras normalizadas.
    """
    for col in cols_enteros:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.extract(r"^(-?\d+)")[0]  # Extrae dígitos con signo opcional
                .replace("", pd.NA)
                .pipe(pd.to_numeric, errors="coerce")
                .astype("Int64")
            )
    return df


# =====================================================
# FUNCIÓN: clean_floats
# =====================================================
def clean_floats(df, cols_floats):
    """
    Limpia y normaliza columnas numéricas con valores decimales (float).

    Características:
        - Corrige formatos con coma (,) o punto (.) como separador decimal.
        - Elimina puntos usados como separadores de miles.
        - Garantiza que los valores resultantes sean floats válidos.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos originales.
        cols_floats (list[str]): Lista de nombres de columnas con valores decimales.

    Retorna:
        pd.DataFrame: DataFrame con las columnas decimales corregidas.
    """
    for col in cols_floats:
        if col in df.columns:
            series = df[col].astype(str).str.strip()

            # Eliminar separadores de miles solo si están en formato tipo 1.234,56
            series = series.str.replace(r"(?<=\d)\.(?=\d{3}(,|$))", "", regex=True)

            # Convertir coma decimal a punto
            series = series.str.replace(",", ".", regex=False)

            # Mantener solo el número válido (con posible signo)
            series = series.str.extract(r"(-?\d+(?:\.\d+)?)")[0]

            # Convertir a numérico (float)
            df[col] = pd.to_numeric(series, errors="coerce")
    return df


# =====================================================
# FUNCIÓN: fill_missing_with_medians_and_keep_negatives
# =====================================================
def fill_missing_with_medians_and_keep_negatives(df):
    """
    Rellena valores faltantes con la mediana, preservando valores negativos válidos.

    Proceso detallado:
        1 Separa las filas con valores negativos (para conservarlos sin alteraciones).
        2 En el resto del DataFrame:
            - Reemplaza valores nulos (NaN) con la mediana de la columna.
            - Los enteros se redondean a valores Int64 válidos.
        3 Se reintroducen los registros negativos al conjunto final.
        4 Si existe la columna 'fecha_de_registro', ordena el resultado cronológicamente.

    Columnas procesadas:
        - Enteros:
            • numero_de_estudiantes_atendidos_hoy
            • numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion
        - Decimales:
            • cantidad_aproximada_desperdiciada_kg

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos ya numéricamente limpios.

    Retorna:
        pd.DataFrame: DataFrame final con faltantes imputados y negativos conservados.
    """
    cols_enteros = [ 
        "numero_de_estudiantes_atendidos_hoy",
        "numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion"
    ]
    cols_floats = ["cantidad_aproximada_desperdiciada_kg"]

    df = df.copy()

    # --- 1. Guardar negativos en un DataFrame aparte ---
    mask_negativos = pd.Series(False, index=df.index)
    for col in cols_enteros + cols_floats:
        if col in df.columns:
            mask_negativos |= df[col] < 0

    df_negativos = df[mask_negativos].copy()
    df_restantes = df[~mask_negativos].copy()

    # --- 2. Rellenar faltantes en df_restantes ---
    for col in cols_enteros:
        if col in df_restantes.columns:
            median = df_restantes[col].dropna().median()
            if not pd.isna(median):
                df_restantes[col] = df_restantes[col].fillna(int(round(median))).astype("Int64")

    for col in cols_floats:
        if col in df_restantes.columns:
            median = df_restantes[col].dropna().median()
            if not pd.isna(median):
                df_restantes[col] = df_restantes[col].fillna(float(median))

    # --- 3. Reincorporar los negativos ---
    df_final = pd.concat([df_restantes, df_negativos], axis=0)

    # --- 4. Ordenar por fecha si existe ---
    if "fecha_de_registro" in df_final.columns:
        df_final = df_final.sort_values(by="fecha_de_registro").reset_index(drop=True)
    else:
        df_final = df_final.reset_index(drop=True)

    return df_final