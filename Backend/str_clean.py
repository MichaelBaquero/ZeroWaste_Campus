"""
Módulo: str_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene las funciones para la limpieza y normalización
    de columnas de texto dentro del dataset. Se encarga de:
      - Estandarizar categorías predefinidas (tipo de alimento, motivo de
        desperdicio, destino del excedente), incluyendo columnas de
        selección múltiple (respuestas separadas por coma).
      - Limpiar texto libre en campos de observaciones o comentarios.

Dependencias:
    - pandas
    - re
    - unidecode
    - config (CATEGORIAS_VALIDAS, COLUMNAS_MULTISELECCION)

Funciones principales:
    - clean_categorical_options(df): Normaliza valores categóricos conocidos,
      con soporte para columnas de selección única y múltiple.
    - clean_text(df, col_text): Limpia texto libre, eliminando caracteres
      especiales y normalizando formato.
"""

import pandas as pd
import re
from unidecode import unidecode
from config import CATEGORIAS_VALIDAS, COLUMNAS_MULTISELECCION


def _normalizar(valor) -> str:
    """Convierte un valor a texto, minúsculas, sin espacios y sin tildes."""
    return unidecode(str(valor).strip().lower())


# =====================================================
# FUNCIÓN: clean_categorical_options
# =====================================================
def clean_categorical_options(df):
    """
    Normaliza las categorías predefinidas en columnas específicas del DataFrame.

    Objetivo:
        Garantizar que los valores dentro de columnas categóricas críticas
        coincidan con un conjunto de opciones válidas, sin importar tildes,
        mayúsculas o espacios. Si un valor no coincide, se asigna "otros".

    Columnas procesadas:
        Definidas dinámicamente en `config.CATEGORIAS_VALIDAS`.

    Columnas de selección múltiple:
        Las columnas listadas en `config.COLUMNAS_MULTISELECCION` (por
        ejemplo, "tipos_de_alimentos_mas_desperdiciados") pueden contener
        varias respuestas separadas por coma en una sola celda. Cada
        respuesta se evalúa por separado contra la lista de opciones
        válidas; las opciones reconocidas se conservan y las no
        reconocidas se descartan. Si ninguna opción de la celda es
        válida, el valor final es "otros".

    Columnas de selección única:
        Se comparan directamente contra la lista de opciones válidas;
        si no coinciden, se asigna "otros".

    Parámetros:
        df (pd.DataFrame): DataFrame con las columnas categóricas.

    Retorna:
        pd.DataFrame: DataFrame con categorías normalizadas.
    """
    for col, validos in CATEGORIAS_VALIDAS.items():
        if col not in df.columns:
            continue

        validos_normalizados = {_normalizar(v) for v in validos}

        if col in COLUMNAS_MULTISELECCION:
            opciones_ordenadas = sorted(validos_normalizados, key=len, reverse=True)
            def limpiar_celda_multiseleccion(valor):
                texto = _normalizar(valor)
                encontrados = []
                for opcion in opciones_ordenadas:
                    if opcion in texto:
                        encontrados.append(opcion)
                        texto = texto.replace(opcion, "", 1)
                return ", ".join(encontrados) if encontrados else "otros"

            df[col] = df[col].map(limpiar_celda_multiseleccion)
        else:
            df[col] = df[col].map(
                lambda x: _normalizar(x) if _normalizar(x) in validos_normalizados else "otros"
            )

    return df


# =====================================================
# FUNCIÓN: clean_text
# =====================================================
def clean_text(df, col_text="comentarios_o_notas_del_dia"):
    """
    Limpia y estandariza el contenido textual de una columna de texto libre.

    Objetivo:
        Asegurar que los campos de texto libre (como comentarios o notas)
        estén libres de caracteres especiales, tildes y espacios extra,
        conservando solo letras, números y espacios.

    Pasos:
        1 Convierte el texto a string y elimina espacios iniciales/finales.
        2 Transforma a minúsculas y remueve acentos (usando unidecode).
        3 Elimina caracteres no alfanuméricos (usando expresiones regulares).
        4 Reemplaza valores vacíos o "nan" por "desconocido".

    Parámetros:
        df (pd.DataFrame): DataFrame con la columna de texto a limpiar.
        col_text (str): Nombre de la columna a procesar (por defecto: "comentarios_o_notas_del_dia").

    Retorna:
        pd.DataFrame: DataFrame con la columna de texto limpia y estandarizada.
    """
    if col_text in df.columns:
        df[col_text] = (
            df[col_text]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(lambda x: re.sub(r"[^a-zA-Z0-9\s]", "", unidecode(x)))
            .replace({"": "desconocido", "nan": "desconocido"})
        )

    return df