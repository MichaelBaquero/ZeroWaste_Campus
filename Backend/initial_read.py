"""
Módulo: initial_read.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo gestiona la conexión y lectura directa de datos desde Google Sheets,
    convirtiendo los registros en un DataFrame de pandas para su posterior limpieza y análisis.

    Es el primer paso del pipeline de datos del proyecto ZeroWaste Campus, 
    y se encarga de garantizar que la información proveniente del formulario
    (respuestas del Google Form) llegue correctamente estructurada y sin
    errores de formato numérico o de codificación.

Dependencias:
    - os (para rutas del sistema)
    - pandas (estructura tabular)
    - gspread (API de Google Sheets)
    - oauth2client.service_account (autenticación segura)

Funciones principales:
    - initial_read(sheet_id, creds_file) → No se deja creds_file por seguridad
        Autentica con Google Sheets, descarga los datos crudos y los
        convierte en un DataFrame estandarizado.

Puntos clave de esta versión:
    - Lectura en modo texto plano (`get_all_values`), evitando
      errores en decimales por el formato regional (coma/punto).
    - Verificación automática de columnas requeridas.
    - Eliminación de la columna redundante “Marca temporal”.
"""

import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# =====================================================
# FUNCIÓN PRINCIPAL: initial_read
# =====================================================
def initial_read(
    sheet_id: str = "1haRa4usWKwNJils1-XddO1WFLYsObIoPkbbcVNZFzTg",
    creds_file=os.path.join(os.path.dirname(__file__), "creds.json")
) -> pd.DataFrame:
    """
    Lee la hoja de cálculo de Google Sheets y retorna su contenido en un DataFrame de pandas.

    Descripción general:
        Esta función se encarga de autenticar de forma segura con Google Sheets
        mediante credenciales de servicio (archivo JSON), acceder a la hoja especificada
        por su ID, y cargar todos los registros en un DataFrame limpio.

        Los datos se leen como texto plano para evitar interpretaciones automáticas
        incorrectas de comas o puntos decimales que podrían alterar valores numéricos.
        Luego, se verifica la existencia de las columnas esperadas según la estructura
        del formulario ZeroWaste Campus.

    Pasos del proceso:
        1 Autenticación con Google Sheets mediante `creds.json`.
        2 Lectura completa de la hoja con `get_all_values()`.
        3 Conversión a DataFrame usando la primera fila como encabezados.
        4 Verificación de columnas obligatorias.
        5 Eliminación de la columna redundante `Marca temporal`.

    Args:
        sheet_id (str):
            ID único de la hoja de cálculo de Google Sheets.
            (Por defecto, la hoja oficial de ZeroWaste Campus)
        
        creds_file (str, opcional):
            Ruta al archivo de credenciales `creds.json`.
            Se construye automáticamente desde el directorio actual si no se especifica.

    Returns:
        pd.DataFrame:
            DataFrame con el contenido completo del Google Sheet,
            con texto plano en todas las columnas, listo para limpieza posterior.

    Raises:
        RuntimeError:
            Si ocurre un error durante la autenticación o lectura.
        ValueError:
            Si alguna columna obligatoria no está presente en la hoja.
    """

    # --- Definición de columnas requeridas ---
    required_columns = [
        "Marca temporal",
        "Fecha de registro",
        "Número de estudiantes atendidos hoy",
        "Número de estudiantes ausentes en el servicio de alimentación",
        "¿Hubo desperdicio de alimentos?",
        "Tipos de alimentos más desperdiciados",
        "Cantidad aproximada desperdiciada (Kg)",
        "Principal motivo de desperdicio",
        "¿Qué se hizo con el excedente?",
        "Comentarios o notas del día"
    ]

    # --- Permisos mínimos requeridos (solo lectura) ---
    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    try:
        # 1️ Construir ruta absoluta al archivo de credenciales
        creds_path = os.path.join(os.path.dirname(__file__), "..", creds_file)
        creds_path = os.path.abspath(creds_path)

        # 2️ Autenticación segura
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)

        # 3️ Lectura cruda desde Google Sheets
        sheet = client.open_by_key(sheet_id).sheet1
        raw_values = sheet.get_all_values()  # Devuelve lista de listas (texto plano)
        df = pd.DataFrame(raw_values[1:], columns=raw_values[0])  # Primera fila = encabezados

        # 4️ Verificar columnas obligatorias
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Faltan las siguientes columnas obligatorias en la hoja: {missing_cols}")

        # 5️ Eliminar columna redundante
        if "Marca temporal" in df.columns:
            df = df.drop(columns=["Marca temporal"])

        return df

    except Exception as e:
        raise RuntimeError(f"Error al leer la hoja de Google Sheets: {e}")