"""
Módulo: components.py
Autor: Equipo ZeroWaste Campus
Descripción:
    Este módulo define los componentes visuales reutilizables del dashboard de Streamlit,
    proporcionando consistencia estética y modularidad en la interfaz de usuario.

    Contiene tres secciones principales:
        1 Encabezado (header_section)
        2 Tarjetas KPI (kpi_card)
        3 Pie de página (footer)

    Estos elementos son llamados directamente desde el módulo `dashboard.py`
    y pueden ser reutilizados en otras interfaces o versiones del proyecto.

Dependencias:
    - os → para verificar la existencia de rutas de imagen (logo)
    - streamlit → para la renderización interactiva y los elementos visuales

Funciones principales:
    - header_section(): Renderiza el encabezado con logo y título principal.
    - kpi_card(): Crea una tarjeta de indicador clave de desempeño (KPI).
    - footer(): Muestra un pie de página unificado para todas las páginas.

Importancia:
    Este módulo separa la capa visual (presentación) de la lógica de negocio
    (procesamiento de datos), manteniendo un código más limpio, escalable
    y fácil de mantener.
"""

import os
import streamlit as st


# =====================================================
# ENCABEZADO PRINCIPAL
# =====================================================
def header_section(logo_path="Visual_page/assets/logo_wzc.png"):
    """
    Renderiza el encabezado principal del dashboard con el logo y título del proyecto.

    Este encabezado se muestra en la parte superior del dashboard e incluye:
        - El logo institucional (ajustable por tamaño o ruta)
        - El título principal "Zero Waste Campus"
        - Un subtítulo descriptivo del propósito de la plataforma

    Args:
        logo_path (str): Ruta del logo institucional (por defecto: 'Visual_page/assets/logo_wzc.png').

    Notas:
        - Si el archivo del logo no existe, se muestra un cuadro verde con las siglas "ZWC".
        - El ancho del logo puede ajustarse con la variable `logo_width_px` para escalar su tamaño.
        - El diseño utiliza columnas de Streamlit para alinear el logo y el texto lateralmente.
    """
    logo_width_px = 1000  # Ancho del logo en píxeles (ajustable)

    # Columnas: [logo] [espacio] [título]
    col_logo, col_space, col_title = st.columns([1, 0.2, 6])

    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=logo_width_px)
        else:
            # Placeholder si no hay logo disponible
            st.markdown("""
                <div style="width:90px; height:90px; background:#4CAF50;
                            border-radius:10px; display:flex; align-items:center;
                            justify-content:center; color:white; font-weight:bold; font-size:24px;">
                    ZWC
                </div>
            """, unsafe_allow_html=True)

    # Columna de título alineada visualmente
    with col_space:
        st.write("")

    with col_title:
        st.markdown(
            "<h1 style='color:#1B5E20; margin:0; line-height:1; font-size:48px; font-family: Poppins, sans-serif;'>Zero Waste Campus</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='color:#666666; margin-top:6px; margin-bottom:0;'>Monitoreo del desperdicio alimentario 🍽️♻️</p>",
            unsafe_allow_html=True
        )

    # Línea divisoria inferior
    st.markdown("---")


# =====================================================
# TARJETAS DE INDICADORES (KPIs)
# =====================================================
def kpi_card(title, value, color="#2E7D32", col=None):
    """
    Renderiza una tarjeta individual de KPI (Indicador Clave de Desempeño).

    Las tarjetas KPI presentan información resumida en formato visual atractivo,
    con color de acento, valor numérico y texto descriptivo.

    Args:
        title (str): Título o descripción del indicador.
        value (str | float | int): Valor principal a mostrar (por ejemplo: "120 kg").
        color (str): Color hexadecimal del título (por defecto: verde institucional).
        col (st.column, opcional): Columna de Streamlit donde se renderizará la tarjeta.

    Diseño:
        - Fondo blanco con sombra suave.
        - Borde redondeado.
        - Fuente seminegrita y color de acento configurable.
    """
    card_html = f"""
    <div class="kpi-card" style="
        background-color:white;
        padding:1rem;
        border-radius:12px;
        box-shadow:0 4px 6px rgba(0,0,0,0.1);
        text-align:center;
    ">
        <div class="kpi-label" style="color:{color}; font-weight:600; margin-bottom:8px;">{title}</div>
        <div class="kpi-value" style="color:#333; font-size:22px; font-weight:700;">{value}</div>
    </div>
    """

    # Mostrar tarjeta en columna o en layout general
    if col:
        with col:
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


# =====================================================
# PIE DE PÁGINA
# =====================================================
def footer():
    """
    Muestra un pie de página estándar en la parte inferior del dashboard.

    Incluye:
        - Línea divisoria superior
        - Créditos institucionales
        - Año de copyright
    """
    st.markdown("""
        <hr style="margin-top:30px;margin-bottom:10px;">
        <p style="text-align:center;color:#616161;font-size:13px;">
        ZeroWaste Campus — Fundación Universitaria Cafam | © 2025
        </p>
    """, unsafe_allow_html=True)