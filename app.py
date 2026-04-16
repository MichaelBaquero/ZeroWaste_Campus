"""
Módulo: app.py
---------------
Archivo principal de ejecución del dashboard interactivo ZeroWaste Campus.
Este módulo inicializa la aplicación de Streamlit, configura la interfaz base y
coordina el flujo general de carga, limpieza y visualización de los datos.

Responsabilidades:
-------------------
1. Configurar los parámetros iniciales de la página (título, ícono y diseño).
2. Cargar los datos desde la fuente (Google Sheets) y aplicar limpieza estandarizada.
3. Ejecutar el dashboard visual principal con métricas, filtros y gráficos.
4. Mantener la eficiencia mediante caché de datos para evitar recargas innecesarias.

Librerías utilizadas:
---------------------
- streamlit: Framework principal para la interfaz y ejecución del dashboard.
- Data_connection.initial_read: Módulo encargado de la conexión y lectura de datos.
- Data_connection.cleaning_data: Módulo de procesamiento y limpieza de datos.
- Visual_page.dashboard: Módulo que genera la visualización interactiva del dashboard.
"""

import streamlit as st
from Data_connection.initial_read import initial_read as read_data
from Data_connection.cleaning_data import cleaner_data as clean_data
from Visual_page.dashboard import run_dashboard

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ZeroWaste Campus Dashboard",
    page_icon="🍽️",
    layout="wide"
)


@st.cache_data
def load_clean_data():
    """
    Carga los datos desde la fuente principal y aplica el proceso de limpieza.

    Este proceso se almacena en caché para evitar recargas innecesarias
    durante la sesión, optimizando el rendimiento de la aplicación.

    Flujo:
    -------
    1. Llama al método `initial_read()` para obtener los datos crudos desde Google Sheets.
    2. Aplica la función `cleaner_data()` para normalizar, validar y limpiar los datos.
    3. Retorna el DataFrame final, listo para visualización.

    Retorna:
        DataFrame: Datos completamente limpios y listos para análisis.
    """
    df = read_data()   # Lectura directa desde Google Sheets usando creds.json
    df = clean_data(df)
    return df


def main():
    """
    Punto de entrada principal de la aplicación Streamlit.

    Funciones:
    -----------
    - Muestra un mensaje lateral con instrucciones de navegación.
    - Carga los datos limpios mediante `load_clean_data()`.
    - Llama a `run_dashboard()` para renderizar el dashboard completo con métricas y gráficos.
    """
    st.sidebar.success("Usa los filtros para explorar los datos 🔍")

    # --- Cargar datos limpios ---
    df = load_clean_data()

    # --- Ejecutar dashboard principal ---
    run_dashboard(df, title="ZeroWaste Campus Dashboard")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    main()  # ✅ Solo una ejecución principal controlada