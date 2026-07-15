"""
Módulo: numeric_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene las funciones de limpieza, imputación y detección
    de valores atípicos para las columnas numéricas del proyecto (enteras y
    decimales). Resulta de la fusión de los antiguos módulos `Nums_clean.py`
    y `outliers_clean.py`.

    Se encarga de:
        - Convertir texto plano a valores numéricos válidos (enteros y floats).
        - Corregir errores de formato (coma vs punto decimal, separadores de miles).
        - Tratar valores negativos como inválidos (error de digitación),
          convirtiéndolos a valor faltante.
        - Imputar valores faltantes de forma diferenciada según la columna:
          los conteos de estudiantes se rellenan con la mediana; el
          desperdicio en kg se deja como valor faltante (NaN) para no
          inventar datos en la métrica principal del proyecto.
        - Detectar valores atípicos (outliers) vía rango intercuartílico (IQR),
          con una corrección diferenciada según el tipo de columna.

Dependencias:
    - pandas

Funciones principales:
    - clean_integers(df, cols_enteros): Limpia y convierte columnas enteras.
    - clean_floats(df, cols_floats): Normaliza valores decimales y corrige formatos.
    - handle_missing_values(df): Trata negativos como inválidos e imputa faltantes.
    - handle_outliers(df): Detecta outliers y los corrige o los conserva según la columna.

Nota de diseño (decisión tomada en conjunto con el equipo del proyecto):
    - `cantidad_aproximada_desperdiciada_kg` NUNCA se rellena automáticamente
      ni se sobreescribe por ser outlier. Un valor extremo en desperdicio de
      alimentos suele ser un evento real (ej. catering institucional), no un
      error — corregirlo silenciosamente destruiría información valiosa.
      Los cálculos del dashboard (`.sum()`, `.mean()`, `.groupby()`) ignoran
      los NaN de forma nativa, así que dejarlos sin rellenar no rompe nada.
    - Los conteos de estudiantes sí se imputan y corrigen automáticamente,
      ya que un valor absurdo ahí es mucho más probablemente un error de
      digitación que un evento real.
"""

import pandas as pd


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
# FUNCIÓN: handle_missing_values
# =====================================================
def handle_missing_values(df):
    """
    Trata valores negativos como inválidos e imputa faltantes de forma
    diferenciada según el tipo de columna.

    Proceso detallado:
        1 Convierte cualquier valor negativo (en enteros y en kg) a NaN —
          se asume que un negativo es un error de digitación, no un dato real.
        2 Conteos de estudiantes (enteros): los NaN se rellenan con la
          mediana de la columna.
        3 Desperdicio en kg (float): los NaN se dejan tal cual, sin rellenar.
          Los cálculos posteriores (.sum(), .mean()) los ignoran de forma
          nativa, así que no es necesario inventar un valor.
        4 Ordena el resultado por fecha si la columna existe.

    Columnas procesadas:
        - Enteros (se imputan con mediana):
            • numero_de_estudiantes_atendidos_hoy
            • numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion
        - Decimales (se dejan como NaN si faltan):
            • cantidad_aproximada_desperdiciada_kg

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos ya numéricamente limpios.

    Retorna:
        pd.DataFrame: DataFrame con negativos tratados como faltantes y
        conteos de estudiantes imputados.
    """
    cols_enteros = [
        "numero_de_estudiantes_atendidos_hoy",
        "numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion"
    ]
    cols_floats = ["cantidad_aproximada_desperdiciada_kg"]

    df = df.copy()

    # --- 1. Convertir negativos a NaN (en todas las columnas numéricas) ---
    for col in cols_enteros + cols_floats:
        if col in df.columns:
            df.loc[df[col] < 0, col] = pd.NA

    # --- 2. Imputar solo los conteos de estudiantes con la mediana ---
    for col in cols_enteros:
        if col in df.columns:
            median = df[col].dropna().median()
            if not pd.isna(median):
                df[col] = df[col].fillna(int(round(median))).astype("Int64")

    # --- 3. cols_floats (kg) se deja sin rellenar, a propósito ---

    # --- 4. Ordenar por fecha si existe ---
    if "fecha_de_registro" in df.columns:
        df = df.sort_values(by="fecha_de_registro").reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

    return df


# =====================================================
# FUNCIÓN: handle_outliers
# =====================================================
def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta valores atípicos (outliers) vía rango intercuartílico (IQR),
    con una corrección diferenciada según el tipo de columna.

    Criterio de detección (igual para todas las columnas):
        - Q1 = cuartil 25%, Q3 = cuartil 75%, IQR = Q3 - Q1
        - Límite inferior = Q1 - 1.5 * IQR
        - Límite superior = Q3 + 1.5 * IQR

    Comportamiento según columna:
        - Conteos de estudiantes (enteros):
            El IQR se calcula sobre toda la columna, y los valores fuera de
            rango se sustituyen automáticamente por la mediana — un valor
            absurdo aquí es más probablemente un error de digitación.

        - Desperdicio en kg (float):
            El IQR se calcula SOLO sobre los días donde sí hubo desperdicio
            real (`hubo_desperdicio_de_alimentos == True`), ignorando los
            días en cero. Esto evita que el rango quede aplastado contra
            cero y que un desperdicio real y modesto se marque como atípico
            solo por compararse contra muchos ceros legítimos.
            Los valores fuera de rango se MARCAN en una columna booleana
            auxiliar (`cantidad_aproximada_desperdiciada_kg_outlier`), pero
            el valor original NO se sobreescribe — un desperdicio inusualmente
            alto suele ser un evento real (ej. catering institucional) y no
            un error, así que se conserva para que el usuario pueda revisarlo.
            Esta columna auxiliar se usa en el dashboard para mostrar una
            tarjeta con el conteo de días atípicos.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos numéricos a limpiar.

    Retorna:
        pd.DataFrame: DataFrame con outliers corregidos (enteros) y
        marcados sin corregir (kg).
    """
    cols_enteros = [
        "numero_de_estudiantes_atendidos_hoy",
        "numero_de_estudiantes_ausentes_en_el_servicio_de_alimentacion"
    ]
    col_kg = "cantidad_aproximada_desperdiciada_kg"
    col_hubo_desperdicio = "hubo_desperdicio_de_alimentos"

    # --- 1. Conteos de estudiantes: detectar y corregir (comportamiento original) ---
    for col in [c for c in cols_enteros if c in df.columns]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        mask_outliers = (df[col] < lower) | (df[col] > upper)
        median = df[col].median(skipna=True)

        if df[col].dtype != "Int64":
            df[col] = df[col].astype("Int64")
        df.loc[mask_outliers, col] = int(median) if not pd.isna(median) else pd.NA

    # --- 2. Desperdicio en kg: detectar sobre el subconjunto con desperdicio real, sin corregir ---
    if col_kg in df.columns:
        if col_hubo_desperdicio in df.columns:
            subset = df.loc[df[col_hubo_desperdicio] == True, col_kg]
        else:
            # Salvaguarda si la columna booleana no está disponible en este punto del pipeline
            subset = df.loc[df[col_kg] > 0, col_kg]

        flag_col = f"{col_kg}_outlier"
        df[flag_col] = False

        if not subset.empty:
            q1 = subset.quantile(0.25)
            q3 = subset.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            mask_outliers = (df[col_kg] < lower) | (df[col_kg] > upper)
            df.loc[mask_outliers, flag_col] = True

    return df