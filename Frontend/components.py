"""
Módulo: components.py
Descripción:
    Componentes visuales reutilizables del dashboard: encabezado, tarjetas
    KPI y pie de página.

Notas de diseño:
    - El logo se incrusta como HTML/base64 (no st.image), para controlar
      tamaño y alineación con precisión y evitar el contenedor adicional
      que Streamlit agrega por defecto a las imágenes (padding, ícono de
      pantalla completa al pasar el mouse).
    - El logo tiene prioridad visual sobre el título (130px vs. tipografía
      reducida del encabezado) para que no se pierda en la interfaz.
"""

import os
import base64
import streamlit as st

_ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))


def _logo_a_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def header_section(logo_filename="assets/logo_wzc.png"):
    """
    Renderiza el encabezado principal del dashboard con el logo como
    elemento protagonista y el título en un tamaño secundario.

    Args:
        logo_filename (str): Ruta relativa a este módulo (Frontend/) donde
            se encuentra el logo institucional.

    Notas:
        - Si el archivo del logo no existe, se muestra un cuadro verde
          con las siglas "ZWC" como respaldo visual.
    """
    logo_path = os.path.join(_ASSETS_DIR, logo_filename)

    if os.path.exists(logo_path):
        logo_b64 = _logo_a_base64(logo_path)
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="width:130px; height:130px; object-fit:contain; border-radius:16px;" />'
        )
    else:
        logo_html = """
            <div style="width:130px;height:130px;background:#4CAF50;border-radius:16px;
                        display:flex;align-items:center;justify-content:center;
                        color:white;font-weight:bold;font-size:32px;">ZWC</div>
        """

    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:24px; margin-bottom:0.5rem;">
            {logo_html}
            <div>
                <h1 style="margin:0; line-height:1; font-size:30px; font-family: Poppins, sans-serif; font-weight:500;">
                    Zero Waste Campus
                </h1>
                <p style="opacity:0.7; margin-top:6px; margin-bottom:0; font-size:14px;">
                    Monitoreo del desperdicio alimentario 🍽️♻️
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")


def kpi_card(title, value, color="#2E7D32", col=None, alert=False):
    """
    Renderiza una tarjeta individual de KPI.

    Args:
        title (str): Título del indicador.
        value (str | float | int): Valor principal a mostrar.
        color (str): Color hexadecimal del título.
        col (st.column, opcional): Columna donde se renderiza.
        alert (bool): Si es True, aplica el estilo de alerta (borde naranja).
    """
    css_class = "kpi-card alert" if alert else "kpi-card"
    card_html = f"""
    <div class="{css_class}">
        <div class="kpi-label" style="color:{color};">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """
    target = col if col else st
    with (target if col else st.container()):
        st.markdown(card_html, unsafe_allow_html=True)


def footer():
    """Muestra el pie de página institucional."""
    st.markdown("""
        <hr style="margin-top:30px;margin-bottom:10px;">
        <p style="text-align:center;color:#616161;font-size:13px;">
        ZeroWaste Campus — Fundación Universitaria Cafam | © 2026
        </p>
    """, unsafe_allow_html=True)