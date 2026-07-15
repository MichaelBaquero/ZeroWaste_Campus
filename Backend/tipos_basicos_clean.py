"""
Módulo: tipos_basicos_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene las funciones de limpieza y normalización de
    columnas con tipos de datos básicos: fechas y booleanos. Resulta de
    la fusión de los antiguos módulos `dates_clean.py` y `boolean_clean.py`.

    Se encarga de:
        - Convertir la columna de fecha a tipo datetime estándar.
        - Normalizar respuestas textuales tipo "Sí/No" a valores booleanos.
        - Aplicar reglas de coherencia entre el booleano de desperdicio y
          la cantidad registrada en kg.

Dependencias:
    - pandas
    - unidecode

Funciones principales:
    - clean_dates(df, col_fecha): Convierte la columna de fecha a datetime.
    - clean_booleans(df, col_bool): Normaliza texto ("Sí"/"No", con o sin
      tilde) a valores booleanos (True/False).
    - corregir_inconsistencias(df): Ajusta la coherencia entre el booleano
      de desperdicio y la cantidad en kg.

Nota de diseño:
    Estas funciones asumen que se ejecutan dentro del pipeline orquestado
    por `cleaning_data.py`, el cual ya valida (en `initial_read.py`) que
    las columnas requeridas existan antes de normalizar sus nombres. Por
    eso `corregir_inconsistencias` no incluye una verificación adicional
    de existencia de columnas: sería redundante con esa validación previa.
"""

import pandas as pd
from unidecode import unidecode


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


# =====================================================
# FUNCIÓN: clean_booleans
# =====================================================
def clean_booleans(df, col_bool="hubo_desperdicio_de_alimentos"):
    """
    Limpia una columna booleana en el DataFrame, normalizando
    los valores textuales a booleanos (True/False).

    Parámetros:
        df (pd.DataFrame): DataFrame que contiene los datos originales.
        col_bool (str): Nombre de la columna booleana a limpiar. Por defecto,
                        se utiliza 'hubo_desperdicio_de_alimentos'.

    Proceso:
        - Convierte los valores a texto, elimina espacios y pasa a minúsculas.
        - Elimina tildes con unidecode (para que "Sí" y "Si" se traten igual).
        - Mapea los valores 'si' → True y 'no' → False.

    Retorna:
        pd.DataFrame: DataFrame con la columna booleana limpia.
    """
    if col_bool in df.columns:
        df[col_bool] = (
            df[col_bool]
            .astype(str).str.strip().str.lower()
            .map(unidecode)
            .map({"si": True, "no": False})
        )
    return df


# =====================================================
# FUNCIÓN: corregir_inconsistencias
# =====================================================
def corregir_inconsistencias(df):
    """
    Corrige inconsistencias entre la columna booleana de desperdicio
    y la cantidad aproximada desperdiciada, aplicando reglas lógicas.

    Reglas aplicadas:
        - Si 'cantidad_aproximada_desperdiciada_kg' > 0  ⇒  hubo_desperdicio = 1
        - Si 'cantidad_aproximada_desperdiciada_kg' == 0 ⇒  hubo_desperdicio = 0
        - Si la cantidad es NaN, no se fuerza ningún valor: se respeta la
          respuesta original de la persona (Sí/No), ya que no inventamos
          un dato de kg para tomar esa decisión.

    Parámetros:
        df (pd.DataFrame): DataFrame con las columnas:
            - 'hubo_desperdicio_de_alimentos'
            - 'cantidad_aproximada_desperdiciada_kg'
        Ambas columnas se asumen presentes (ver nota de diseño del módulo).

    Retorna:
        pd.DataFrame: DataFrame con la columna booleana coherente y sin valores nulos.
    """
    # --- Normalización de la columna booleana a formato numérico (1/0) ---
    df["hubo_desperdicio_de_alimentos"] = (
        df["hubo_desperdicio_de_alimentos"]
        .map({True: 1, False: 0})
    )

    # --- Aplicación de reglas de coherencia ---
    df.loc[df["cantidad_aproximada_desperdiciada_kg"] > 0, "hubo_desperdicio_de_alimentos"] = 1
    df.loc[df["cantidad_aproximada_desperdiciada_kg"] == 0, "hubo_desperdicio_de_alimentos"] = 0

    # --- Reemplazo de valores faltantes restantes ---
    df["hubo_desperdicio_de_alimentos"] = df["hubo_desperdicio_de_alimentos"].fillna(0).astype(int)

    return df