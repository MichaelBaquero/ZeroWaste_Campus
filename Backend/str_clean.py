"""
Módulo: str_clean.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo contiene las funciones para la limpieza y normalización
    de columnas de texto dentro del dataset. Se encarga de:
      - Estandarizar categorías predefinidas (por ejemplo: tipo de alimento, motivo de desperdicio)
      - Limpiar texto libre en campos de observaciones o comentarios

    El propósito es garantizar que las columnas de texto tengan valores coherentes,
    homogéneos y libres de caracteres no deseados, mejorando así la calidad de los datos
    para análisis descriptivos y visualizaciones.

Dependencias:
    - pandas
    - re
    - unidecode (para eliminar acentos y caracteres especiales)

Funciones principales:
    - clean_categorical_options(df): Normaliza valores categóricos conocidos, asignando "otros" a los no válidos.
    - clean_text(df, col_text): Limpia texto libre, eliminando caracteres especiales y normalizando formato.
"""

import pandas as pd
import re
from unidecode import unidecode


# =====================================================
# FUNCIÓN: clean_categorical_options
# =====================================================
def clean_categorical_options(df):
    """
    Normaliza las categorías predefinidas en columnas específicas del DataFrame.
    
    Objetivo:
        Garantizar que los valores dentro de columnas categóricas críticas coincidan
        con un conjunto de opciones válidas. Si no coinciden, se asigna "otros".

    Columnas procesadas:
        - tipos_de_alimentos_mas_desperdiciados
        - principal_motivo_de_desperdicio
        - que_se_hizo_con_el_excedente

    Mecanismo:
        1 Convierte el texto a minúsculas y elimina espacios.
        2 Verifica si el valor pertenece a la lista de opciones válidas.
        3 Si no pertenece, reemplaza el valor por "otros".

    Parámetros:
        df (pd.DataFrame): DataFrame con las columnas categóricas.

    Retorna:
        pd.DataFrame: DataFrame con categorías normalizadas.
    """
    options_dict = {
        "tipos_de_alimentos_mas_desperdiciados": [
            "frutas",
            "verduras / ensaladas",
            "proteina (carne, pollo, pescado, huevo)",
            "cereales / harinas (arroz, pasta, pan)"
        ],
        "principal_motivo_de_desperdicio": [
            "porciones muy grandes",
            "baja aceptacion / sabor",
            "excedente en cocina (sobro sin servir)",
            "tiempo insuficiente para comer"
        ],
        "que_se_hizo_con_el_excedente": [
            "se desecho totalmente",
            "se almaceno para consumo posterior",
            "se distribuyo / dono (ej banco de alimentos, personal de apoyo)"
        ]
    }

    for col, validos in options_dict.items():
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map(lambda x: x if x in validos else "otros")
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