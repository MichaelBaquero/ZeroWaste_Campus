"""
Módulo: outliers_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene las funciones destinadas a la detección y corrección
    de valores atípicos (outliers) en los datos numéricos del proyecto.
    Los outliers pueden alterar significativamente las métricas y modelos
    estadísticos, por lo que se identifican y sustituyen por valores más
    representativos (como la mediana de la columna).

Dependencias:
    - pandas
    - numpy

Funciones principales:
    - handle_outliers(df): Detecta y corrige valores atípicos en columnas numéricas.

Criterio de detección:
    - Se utiliza el rango intercuartílico (IQR, por sus siglas en inglés):
        • Q1 = cuartil 25%
        • Q3 = cuartil 75%
        • IQR = Q3 - Q1
        • Límite inferior = Q1 - 1.5 * IQR
        • Límite superior = Q3 + 1.5 * IQR
    - Los valores fuera de este rango son marcados como outliers y reemplazados por la mediana.

Columnas consideradas:
    - Enteras:
        • numero_de_estudiantes_atendidos_hoy
        • numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion
    - Decimales:
        • cantidad_aproximada_desperdiciada_kg
"""

import pandas as pd

# =====================================================
# FUNCIÓN: handle_outliers
# =====================================================
def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta y corrige outliers solo en columnas numéricas relevantes.

    Detalles del proceso:
        1 Identifica columnas objetivo (enteras y decimales) que existan en el DataFrame.
        2 Calcula el rango intercuartílico (IQR) para cada columna.
        3 Determina los límites inferior y superior aceptables.
        4 Crea una columna auxiliar `nombre_columna_outlier` para marcar los registros anómalos.
        5 Sustituye los valores atípicos por la mediana de la columna correspondiente.
        6 Mantiene la compatibilidad de tipos de datos (Int64 o float).

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos numéricos a limpiar.

    Retorna:
        pd.DataFrame: DataFrame con outliers corregidos y marcados.
    """

    # --- 1. Definir columnas numéricas ---
    cols_enteros = [
        "numero_de_estudiantes_atendidos_hoy",
        "numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion"
    ]
    cols_floats = ["cantidad_aproximada_desperdiciada_kg"]

    # Filtrar solo columnas existentes en el DataFrame
    cols_target = [c for c in cols_enteros + cols_floats if c in df.columns]

    # --- 2. Detección y corrección de outliers ---
    for col in cols_target:
        # Cálculo de límites por IQR
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        # Columna bandera para registrar outliers detectados
        flag_col = f"{col}_outlier"
        df[flag_col] = False

        # Identificar filas con valores fuera del rango aceptado
        mask_outliers = (df[col] < lower) | (df[col] > upper)
        df.loc[mask_outliers, flag_col] = True

        # Calcular mediana (ignorando NaN)
        median = df[col].median(skipna=True)

        # --- 3. Sustitución de outliers ---
        if pd.api.types.is_integer_dtype(df[col]):
            # Asegurar compatibilidad con tipo Int64 nullable
            if df[col].dtype != "Int64":
                df[col] = df[col].astype("Int64")
            df.loc[mask_outliers, col] = int(median) if not pd.isna(median) else pd.NA
        else:
            # En columnas flotantes, asignar directamente la mediana
            df.loc[mask_outliers, col] = median

    return df