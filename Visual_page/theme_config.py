"""
Módulo: theme_config.py
Define la configuración visual del dashboard de Streamlit para ZeroWaste Campus.
Forza el uso de un tema claro, establece la paleta de colores institucionales y
aplica un estilo visual coherente en todos los componentes del dashboard.

Responsabilidades:
-------------------
1. Configurar colores, fuentes y estilos base para el tema claro.
2. Ocultar los elementos no deseados de la interfaz nativa de Streamlit (menú, footer, toolbar).
3. Aplicar estilos CSS personalizados a tarjetas KPI, tablas, gráficos, botones y sidebar.
4. Retornar la configuración del tema junto con la hoja de estilo CSS para su carga dinámica.

Librerías utilizadas:
---------------------
- streamlit: para integración del tema dentro del entorno del dashboard.
"""

import streamlit as st

def load_theme():
    """
    Carga la configuración visual del dashboard en modo claro.

    Retorna:
        tuple:
            - theme (dict): Diccionario con la definición de colores y tipografías.
            - css (str): Cadena de estilos CSS personalizada que se inyecta en la aplicación.

    Detalles:
    ----------
    - Se fuerza el modo claro (fondo blanco, texto oscuro).
    - Se aplican colores institucionales:
        * Verde oscuro (#1B5E20): Color principal.
        * Verde claro (#4CAF50): Acento secundario.
        * Amarillo (#FFC107): Indicadores visuales.
    - Oculta los menús, barras superiores e íconos de Streamlit para lograr
      una apariencia limpia y profesional.
    - Define el estilo visual de componentes clave: KPI cards, tablas, botones, sidebar y footer.
    """

    theme = {
        "colors": {
            "primary": "#1B5E20",        # Verde institucional oscuro
            "primary_light": "#4CAF50",  # Verde brillante
            "secondary": "#FFC107",      # Amarillo visible
            "background": "#FFFFFF",     # Fondo blanco
            "sidebar_bg": "#F1F8E9",     # Verde muy claro para diferenciar el sidebar
            "card_bg": "#FAFAFA",        # Fondo de tarjetas
            "text_primary": "#212121",   # Negro suave
            "text_secondary": "#424242", # Gris oscuro
            "accent": "#388E3C",         # Verde intermedio
        },
        "fonts": {
            "heading": "'Poppins', sans-serif",
            "body": "'Roboto', sans-serif",
        }
    }

    css = """
    <style>
    /* --- Tipografías principales --- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Roboto:wght@300;400;500&display=swap');

    /* --- Forzar modo claro y tipografía base --- */
    html, body, [class*="css"] {
        background-color: #FFFFFF !important;
        color: #212121 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    /* --- Ocultar elementos nativos de Streamlit --- */
    header[data-testid="stHeader"], div[data-testid="stToolbar"], footer, 
    [data-testid="stStatusWidget"], [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0 !important;
        display: none !important;
    }
    button[kind="icon"], [data-testid="stBaseButton-header"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* --- Sidebar --- */
    section[data-testid="stSidebar"] {
        background-color: #F1F8E9 !important;
        color: #212121 !important;
        border-right: 1px solid #C8E6C9 !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #1B5E20 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }

    /* --- Encabezados principales --- */
    h1, h2, h3, h4, h5 {
        font-family: 'Poppins', sans-serif !important;
        color: #1B5E20 !important;
        font-weight: 600 !important;
    }

    /* --- Tarjetas de KPI --- */
    .kpi-card {
        background-color: #FAFAFA !important;
        border-left: 6px solid #1B5E20 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }
    .kpi-value {
        font-size: 30px !important;
        font-weight: 600 !important;
        color: #1B5E20 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .kpi-label {
        color: #424242 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }

    /* --- Tablas y DataFrames --- */
    .stDataFrame, .stTable {
        background-color: #FFFFFF !important;
        color: #212121 !important;
        border-radius: 8px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* --- Gráficos --- */
    .chart-container {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px !important;
    }

    /* --- Botones --- */
    .stButton>button {
        background-color: #1B5E20 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        background-color: #388E3C !important;
        transform: translateY(-2px);
    }

    /* --- Footer --- */
    .footer {
        border-top: 2px solid #1B5E20 !important;
        padding: 15px 0 !important;
        text-align: center !important;
        color: #424242 !important;
        font-size: 14px !important;
        font-family: 'Roboto', sans-serif !important;
        margin-top: 40px !important;
    }

    /* --- Espaciado general del layout --- */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }
    </style>
    """

    return theme, css