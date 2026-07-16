"""
Módulo: theme_config.py
Descripción:
    Configuración visual del dashboard ZeroWaste Campus. Tema claro fijo
    (no hay alternancia claro/oscuro): los widgets nativos de Streamlit se
    fijan en modo claro vía .streamlit/config.toml, y este módulo aplica
    la paleta institucional sobre ese mismo modo para evitar conflictos
    entre el tema nativo y el CSS personalizado.
"""

import streamlit as st

PALETA_CLARA = {
    "background": "#FFFFFF",
    "card_bg": "#FAFAFA",
    "text_primary": "#212121",
    "text_secondary": "#424242",
    "primary": "#1B5E20",
    "primary_light": "#4CAF50",
    "secondary": "#FFC107",
    "alert": "#E65100",
    "border": "#E0E0E0",
    "plotly_template": "plotly_white",
}


def load_theme(mode: str = "light"):
    """
    Carga la configuración visual del dashboard.

    Args:
        mode (str): reservado para compatibilidad futura; actualmente
            solo existe la paleta clara y el parámetro se ignora.

    Retorna:
        tuple: (colors: dict, css: str)
    """
    c = PALETA_CLARA

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Roboto:wght@300;400;500&display=swap');

    html, body, [class*="css"], .stApp {{
        background-color: {c["background"]} !important;
        color: {c["text_primary"]} !important;
        font-family: 'Roboto', sans-serif !important;
    }}

    /* --- Ocultar elementos nativos de Streamlit --- */
    #MainMenu, header[data-testid="stHeader"], div[data-testid="stToolbar"],
    div[data-testid*="Toolbar"], footer, [data-testid="stStatusWidget"],
    [data-testid="stDecoration"], [data-testid="collapsedControl"] {{
        visibility: hidden !important;
        height: 0 !important;
        display: none !important;
    }}
    button[kind="icon"], [data-testid*="BaseButton-header"] {{
        visibility: hidden !important;
        display: none !important;
    }}
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    /* --- Encabezados --- */
    h1, h2, h3, h4, h5 {{
        font-family: 'Poppins', sans-serif !important;
        color: {c["primary"]} !important;
        font-weight: 600 !important;
    }}

    /* --- Tarjetas de KPI --- */
    .kpi-card {{
        background-color: {c["card_bg"]} !important;
        border: 1px solid {c["border"]} !important;
        border-left: 6px solid {c["primary"]} !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin-bottom: 15px !important;
        min-height: 110px;
    }}
    .kpi-card.alert {{
        border-left: 6px solid {c["alert"]} !important;
    }}
    .kpi-value {{
        font-size: 28px !important;
        font-weight: 600 !important;
        color: {c["primary"]} !important;
        font-family: 'Poppins', sans-serif !important;
    }}
    .kpi-card.alert .kpi-value {{
        color: {c["alert"]} !important;
    }}
    .kpi-label {{
        color: {c["text_secondary"]} !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}

    /* --- Expander --- */
    div[data-testid="stExpander"] {{
        background-color: {c["card_bg"]} !important;
        border: 1px solid {c["border"]} !important;
        border-radius: 8px !important;
    }}

    /* --- Tabla de datos --- */
    .stDataFrame, .stTable, div[data-testid="stDataFrame"] {{
        background-color: {c["card_bg"]} !important;
        color: {c["text_primary"]} !important;
        border-radius: 8px !important;
        border: 1px solid {c["border"]} !important;
    }}

    /* --- Espaciado general --- */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }}
    </style>
    """

    return c, css