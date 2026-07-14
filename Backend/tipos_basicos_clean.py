import pandas as pd
import re
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
        - Mapea los valores 'si' → True y 'no' → False.
        - Retorna el DataFrame con la columna normalizada.

    Retorna:
        pd.DataFrame: DataFrame con la columna booleana limpia.
    """
    if col_bool in df.columns:
        df[col_bool] = (
            df[col_bool]
            .astype(str).str.strip().str.lower()
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
        - Si la cantidad es NaN y el booleano también, se asume 0.

    Además:
        - Se estandarizan valores textuales y booleanos (True/False, 'si', 'no')
          a formato numérico binario (1/0).

    Parámetros:
        df (pd.DataFrame): DataFrame con las columnas:
            - 'hubo_desperdicio_de_alimentos'
            - 'cantidad_aproximada_desperdiciada_kg'

    Retorna:
        pd.DataFrame: DataFrame con la columna booleana coherente y sin valores nulos.
    """
    # --- Normalización de la columna booleana ---
    df["hubo_desperdicio_de_alimentos"] = (
        df["hubo_desperdicio_de_alimentos"]
        .map({True: 1, False: 0, "si": 1, "sí": 1, "no": 0, "": 0, None: 0})
    )

    # --- Aplicación de reglas de coherencia ---
    df.loc[df["cantidad_aproximada_desperdiciada_kg"] > 0, "hubo_desperdicio_de_alimentos"] = 1
    df.loc[df["cantidad_aproximada_desperdiciada_kg"] == 0, "hubo_desperdicio_de_alimentos"] = 0

    # --- Reemplazo de valores faltantes ---
    df["hubo_desperdicio_de_alimentos"] = df["hubo_desperdicio_de_alimentos"].fillna(0).astype(int)

    return df