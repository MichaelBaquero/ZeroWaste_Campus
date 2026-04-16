"""==========================================================
Módulo: dashboard.py
Autor: Equipo ZeroWaste Campus
Descripción:
  Este módulo construye el dashboard interactivo del proyecto
  ZeroWaste Campus utilizando Streamlit y Plotly. 
  Presenta las métricas y visualizaciones clave relacionadas con
  el desperdicio alimentario, permitiendo al usuario explorar
  los datos por rango de fechas y categorías relevantes.

Dependencias principales:
  - streamlit: para la interfaz web y componentes visuales.
  - pandas: para la manipulación y agregación de datos.
  - plotly.express: para la generación de gráficos interactivos.
  - Visual_page.components: para encabezado, tarjetas KPI y pie de página.
  - Visual_page.theme_config (opcional): para aplicar temas visuales.

Estructura del módulo:
  1 Cálculo de métricas clave (calculate_metrics)
  2 Creación de gráficos de tendencia (create_trend_chart)
  3 Creación de gráficos de composición (create_composition_charts)
  4 Ejecución del dashboard principal (run_dashboard)
==========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from Visual_page.components import header_section, kpi_card, footer

# --- Carga opcional del tema visual ---
try:
    from Visual_page.theme_config import load_theme
    HAVE_THEME = True
except Exception:
    HAVE_THEME = False


# ==========================================================
# 1️ CÁLCULO DE MÉTRICAS CLAVE
# ==========================================================
def calculate_metrics(df):
    """
    Calcula métricas clave de desempeño relacionadas con el desperdicio alimentario,
    limitadas a las que realmente se visualizan en el dashboard principal.

    Parámetros:
        df (DataFrame): Datos ya limpios y filtrados.

    Retorna:
        dict: Diccionario con las siguientes métricas:
            - total_desperdicio: Suma total del desperdicio (kg)
            - promedio_diario: Promedio diario del desperdicio (kg)
            - total_dias: Número total de días registrados
            - dias_con_desperdicio: Conteo de días con algún desperdicio registrado (>0)
    """

    metrics = {}
    df = df.copy()

    # --- Asegurar tipo numérico y reemplazar valores nulos ---
    if "cantidad_aproximada_desperdiciada_kg" in df.columns:
        df["cantidad_aproximada_desperdiciada_kg"] = pd.to_numeric(
            df["cantidad_aproximada_desperdiciada_kg"], errors="coerce"
        ).fillna(0)
    else:
        df["cantidad_aproximada_desperdiciada_kg"] = 0

    # --- Agrupación diaria (por fecha de registro) ---
    if "fecha_de_registro" in df.columns:
        df["fecha_only"] = pd.to_datetime(df["fecha_de_registro"], errors="coerce").dt.date
        diarios = df.groupby("fecha_only")["cantidad_aproximada_desperdiciada_kg"].sum()
        metrics["promedio_diario"] = diarios.mean() if not diarios.empty else 0
        metrics["total_desperdicio"] = diarios.sum() if not diarios.empty else 0
        metrics["total_dias"] = diarios.shape[0]
    else:
        # Fallback si no existe columna de fecha
        metrics["promedio_diario"] = df["cantidad_aproximada_desperdiciada_kg"].mean()
        metrics["total_desperdicio"] = df["cantidad_aproximada_desperdiciada_kg"].sum()
        metrics["total_dias"] = len(df)

    # --- Cálculo de días con desperdicio ---
    if "hubo_desperdicio_de_alimentos" in df.columns:
        metrics["dias_con_desperdicio"] = int(
            df["hubo_desperdicio_de_alimentos"].fillna(0).astype(int).sum()
        )
    else:
        # Si no existe columna booleana, inferir según registros con desperdicio > 0
        metrics["dias_con_desperdicio"] = (
            (df["cantidad_aproximada_desperdiciada_kg"] > 0).sum()
            if "cantidad_aproximada_desperdiciada_kg" in df.columns
            else 0
        )

    return metrics


# ==========================================================
# 2️ GRÁFICOS DE TENDENCIA
# ==========================================================
def create_trend_chart(df):
    """
    Genera un gráfico de línea con la evolución mensual del desperdicio.

    Parámetros:
        df (DataFrame): Datos filtrados con columna 'fecha_de_registro'.

    Retorna:
        fig (plotly.Figure) o None: Gráfico de línea si existen datos válidos.
    """
    if "fecha_de_registro" not in df.columns:
        return None

    df["fecha_de_registro"] = pd.to_datetime(df["fecha_de_registro"], errors="coerce")
    df_mensual = (
        df.groupby(pd.Grouper(key="fecha_de_registro", freq="M"))["cantidad_aproximada_desperdiciada_kg"]
        .sum()
        .reset_index()
    )

    if df_mensual.empty or df_mensual["cantidad_aproximada_desperdiciada_kg"].sum() == 0:
        return None

    fig = px.line(
        df_mensual,
        x="fecha_de_registro",
        y="cantidad_aproximada_desperdiciada_kg",
        title="📈 Evolución Mensual del Desperdicio"
    )
    fig.update_traces(line=dict(color="#1B5E20", width=3))
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig


# ==========================================================
# 3️ GRÁFICOS DE COMPOSICIÓN
# ==========================================================
def create_composition_charts(df):
    """
    Crea visualizaciones sobre la composición del desperdicio:
    - Distribución por tipo de alimento.
    - Distribución por motivo principal.

    Parámetros:
        df (DataFrame): Datos filtrados.

    Retorna:
        dict: Diccionario con figuras 'alimentos' y 'motivos' (si existen datos válidos).
    """
    charts = {}

    # --- Gráfico de pastel por tipo de alimento ---
    if "tipos_de_alimentos_mas_desperdiciados" in df.columns:
        alimentos = (
            df.groupby("tipos_de_alimentos_mas_desperdiciados")["cantidad_aproximada_desperdiciada_kg"]
            .sum()
            .reset_index()
        )
        if not alimentos.empty:
            charts["alimentos"] = px.pie(
                alimentos,
                values="cantidad_aproximada_desperdiciada_kg",
                names="tipos_de_alimentos_mas_desperdiciados",
                title="🍎 Distribución por Tipo de Alimento"
            )

    # --- Gráfico de barras por motivo de desperdicio ---
    if "principal_motivo_de_desperdicio" in df.columns:
        motivos = (
            df.groupby("principal_motivo_de_desperdicio")["cantidad_aproximada_desperdiciada_kg"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        if not motivos.empty:
            charts["motivos"] = px.bar(
                motivos,
                y="principal_motivo_de_desperdicio",
                x="cantidad_aproximada_desperdiciada_kg",
                orientation="h",
                title="🧩 Desperdicio por Motivo Principal"
            )
    return charts


# ==========================================================
# 4️ BLOQUE PRINCIPAL DEL DASHBOARD
# ==========================================================
def run_dashboard(df, title=None):
    """
    Ejecuta el dashboard completo de visualización de desperdicio alimentario.

    Flujo general:
        1. Carga opcional del tema visual.
        2. Renderiza encabezado con logo y título.
        3. Habilita filtro de rango de fechas interactivo.
        4. Calcula métricas y muestra KPIs.
        5. Renderiza gráficos y tabla de datos.

    Parámetros:
        df (DataFrame): Datos limpios procesados desde el pipeline.
        title (str, opcional): Título adicional (no usado actualmente).
    """
    # --- 1. Cargar tema visual (opcional) ---
    if HAVE_THEME:
        try:
            theme, css = load_theme()
            if css:
                st.markdown(css, unsafe_allow_html=True)
        except Exception:
            pass

    # --- 2. Encabezado del dashboard ---
    header_section()

    # --- 3. Filtro principal por fecha ---
    if "fecha_de_registro" in df.columns:
        df["fecha_de_registro"] = pd.to_datetime(df["fecha_de_registro"], errors="coerce")
        df = df.dropna(subset=["fecha_de_registro"])

        if df.empty:
            st.warning("⚠️ No hay datos con fechas válidas.")
            footer()
            return

        # Determinar rango de fechas mínimo y máximo
        min_date = df["fecha_de_registro"].min().date()
        max_date = df["fecha_de_registro"].max().date()

        default_start = max(min_date, pd.Timestamp.today().date() - pd.Timedelta(days=365))
        default_end = min(max_date, pd.Timestamp.today().date())

        # Bloquear edición manual del campo de fecha
        st.markdown("""
            <style>
            input[type="text"][data-testid="stDateInput"] {
                pointer-events: none;
            }
            </style>
        """, unsafe_allow_html=True)

        # Selección segura de rango de fechas
        try:
            date_range = st.date_input(
                "📅 Selecciona un rango de fechas:",
                value=(default_start, default_end),
                min_value=min_date,
                max_value=max_date,
                key="filtro_fecha_central"
            )

            # Validaciones de selección
            if not date_range:
                st.info("🕒 Esperando selección de fecha...")
                footer()
                return

            if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                start_date, end_date = map(pd.to_datetime, date_range)
            else:
                start_date = end_date = pd.to_datetime(date_range)

            # Asegurar orden cronológico correcto
            if start_date > end_date:
                start_date, end_date = end_date, start_date

            # Filtrar datos por rango
            df_filtered = df[df["fecha_de_registro"].between(start_date, end_date)]

            if df_filtered.empty:
                st.warning("⚠️ No hay registros dentro del rango seleccionado.")
                footer()
                return
            else:
                st.success(f"Mostrando datos entre **{start_date.date()}** y **{end_date.date()}**")

        except Exception:
            st.info("🕒 Selecciona un rango de fechas válido para continuar.")
            footer()
            return

    else:
        df_filtered = df.copy()

    # --- 4. Cálculo y visualización de métricas ---
    metrics = calculate_metrics(df_filtered)

    st.markdown("## 📊 Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    kpi_card("Desperdicio Total", f"{metrics['total_desperdicio']:.1f} kg", "#1B5E20", col1)
    kpi_card("Promedio Diario", f"{metrics['promedio_diario']:.1f} kg", "#4CAF50", col2)
    kpi_card("Días Analizados", f"{metrics['total_dias']}", "#388E3C", col3)
    kpi_card("Días con Desperdicio", f"{metrics['dias_con_desperdicio']}", "#FFC107", col4)

    # --- 5. Visualizaciones ---
    trend_chart = create_trend_chart(df_filtered)
    if trend_chart:
        st.plotly_chart(trend_chart, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar la evolución temporal.")

    st.markdown("## 🍽️ ¿Cómo y porqué se desperdició?")
    charts = create_composition_charts(df_filtered)
    cols = st.columns(2)
    if "alimentos" in charts:
        cols[0].plotly_chart(charts["alimentos"], use_container_width=True)
    if "motivos" in charts:
        cols[1].plotly_chart(charts["motivos"], use_container_width=True)

    # --- 6. Tabla detallada ---
    with st.expander("🔍 Ver datos detallados"):
        st.dataframe(df_filtered.head(1000))

    # --- 7. Pie de página ---
    footer()