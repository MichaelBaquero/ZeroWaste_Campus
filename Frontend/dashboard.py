"""==========================================================
Módulo: dashboard.py
Descripción:
    Dashboard interactivo del proyecto ZeroWaste Campus. Presenta métricas
    y visualizaciones sobre desperdicio alimentario, con filtro de rango
    de fechas. Tema claro fijo (sin alternancia claro/oscuro).

Estructura del módulo:
    1 Cálculo de métricas clave (calculate_metrics)
    2 Gráfico de desperdicio diario con promedio móvil (create_trend_chart)
    3 Gráficos de composición: tipo de alimento y motivo (create_composition_charts)
    4 Ejecución del dashboard principal (run_dashboard)
==========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from Frontend.components import header_section, kpi_card, footer

try:
    from Frontend.theme_config import load_theme
    HAVE_THEME = True
except Exception:
    HAVE_THEME = False


# ==========================================================
# 1️ CÁLCULO DE MÉTRICAS CLAVE
# ==========================================================
def calculate_metrics(df):
    """
    Calcula las métricas clave que se muestran en el dashboard.

    Retorna:
        dict con: total_desperdicio, promedio_diario, total_dias,
        dias_con_desperdicio, dias_atipicos, dias_sin_dato_kg.
    """
    metrics = {}
    df = df.copy()
    col_kg = "cantidad_aproximada_desperdiciada_kg"

    if col_kg in df.columns:
        df[col_kg] = pd.to_numeric(df[col_kg], errors="coerce")
        # No se rellena con 0: .sum()/.mean() ignoran NaN de forma nativa,
        # y así no se inventa un dato en la metrica principal del proyecto.
    else:
        df[col_kg] = pd.NA

    metrics["dias_sin_dato_kg"] = int(df[col_kg].isna().sum())

    if "fecha_de_registro" in df.columns:
        df["fecha_only"] = pd.to_datetime(df["fecha_de_registro"], errors="coerce").dt.date
        diarios = df.groupby("fecha_only")[col_kg].sum()
        metrics["promedio_diario"] = diarios.mean() if not diarios.empty else 0
        metrics["total_desperdicio"] = diarios.sum() if not diarios.empty else 0
        metrics["total_dias"] = diarios.shape[0]
    else:
        metrics["promedio_diario"] = df[col_kg].mean()
        metrics["total_desperdicio"] = df[col_kg].sum()
        metrics["total_dias"] = len(df)

    if "hubo_desperdicio_de_alimentos" in df.columns:
        metrics["dias_con_desperdicio"] = int(
            df["hubo_desperdicio_de_alimentos"].fillna(0).astype(int).sum()
        )
    else:
        metrics["dias_con_desperdicio"] = int((df[col_kg] > 0).sum())

    col_outlier = f"{col_kg}_outlier"
    metrics["dias_atipicos"] = int(df[col_outlier].sum()) if col_outlier in df.columns else 0

    return metrics


# ==========================================================
# ESTILO COMÚN PARA GRÁFICOS PLOTLY
# ==========================================================
def _aplicar_estilo_grafico(fig, colors, titulo_color=None):
    """
    Fija explícitamente plantilla, fondo, color de fuente y posición de
    la leyenda (abajo, horizontal) para todos los gráficos del dashboard.
    """
    fig.update_layout(
        template=colors["plotly_template"],
        plot_bgcolor=colors["card_bg"],
        paper_bgcolor=colors["card_bg"],
        font_color=colors["text_primary"],
        title_font_color=titulo_color or colors["primary"],
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font_color=colors["text_primary"],
        ),
        margin=dict(b=80),
    )
    return fig


# ==========================================================
# 2️ GRÁFICO DE DESPERDICIO DIARIO
# ==========================================================
def create_trend_chart(df, colors):
    """
    Genera un gráfico de desperdicio diario, con marcador por cada día
    con dato y una línea de promedio móvil de 7 días para leer la
    tendencia sin que el ruido diario la oculte.
    """
    if "fecha_de_registro" not in df.columns:
        return None

    df = df.copy()
    df["fecha_de_registro"] = pd.to_datetime(df["fecha_de_registro"], errors="coerce")
    col_kg = "cantidad_aproximada_desperdiciada_kg"

    df_diario = (
        df.groupby(df["fecha_de_registro"].dt.date)[col_kg]
        .sum()
        .reset_index()
        .rename(columns={"fecha_de_registro": "fecha"})
    )
    df_diario["fecha"] = pd.to_datetime(df_diario["fecha"])

    if df_diario.empty or df_diario[col_kg].sum() == 0:
        return None

    df_diario["promedio_movil_7d"] = df_diario[col_kg].rolling(window=7, min_periods=1).mean()

    fig = px.line(
        df_diario,
        x="fecha",
        y=col_kg,
        markers=True,
        title="📈 Desperdicio Diario",
        labels={"fecha": "Fecha", col_kg: "Kg desperdiciados"},
    )
    fig.update_traces(
        line=dict(color=colors["primary_light"], width=1.5),
        marker=dict(size=6),
        name="Diario",
        showlegend=True,
    )

    fig.add_scatter(
        x=df_diario["fecha"],
        y=df_diario["promedio_movil_7d"],
        mode="lines",
        name="Promedio móvil (7 días)",
        line=dict(color=colors["primary"], width=3),
    )

    return _aplicar_estilo_grafico(fig, colors)


# ==========================================================
# 3️ GRÁFICOS DE COMPOSICIÓN
# ==========================================================
def create_composition_charts(df, colors):
    """
    Genera gráficos de composición por tipo de alimento y motivo.

    Nota sobre tipos_de_alimentos_mas_desperdiciados:
        Es una columna de selección múltiple (respuestas separadas por
        coma, ej. "frutas, lacteos"). Antes de agrupar, se separa cada
        combinación en filas individuales (explode) para que el pie
        chart muestre categorías reales en vez de una porción distinta
        por cada combinación única. Como consecuencia, un mismo evento
        de desperdicio puede contribuir a más de una categoría a la vez,
        por lo que la suma de las porciones del pie puede superar el
        100% del desperdicio total — esto es esperado, no un error.
    """
    charts = {}
    col_kg = "cantidad_aproximada_desperdiciada_kg"
    col_tipo = "tipos_de_alimentos_mas_desperdiciados"

    if col_tipo in df.columns:
        df_exploded = df.assign(**{col_tipo: df[col_tipo].str.split(", ")}).explode(col_tipo)
        alimentos = (
            df_exploded.groupby(col_tipo)[col_kg]
            .sum()
            .reset_index()
        )
        alimentos = alimentos[alimentos[col_tipo] != "no aplica / no hubo desperdicio"]
        if not alimentos.empty:
            fig = px.pie(
                alimentos,
                values=col_kg,
                names=col_tipo,
                title="🍎 Distribución por Tipo de Alimento"
            )
            charts["alimentos"] = _aplicar_estilo_grafico(fig, colors)

    if "principal_motivo_de_desperdicio" in df.columns:
        motivos = (
            df.groupby("principal_motivo_de_desperdicio")[col_kg]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        motivos = motivos[motivos["principal_motivo_de_desperdicio"] != "no aplica / no hubo desperdicio"]
        if not motivos.empty:
            fig = px.bar(
                motivos,
                y="principal_motivo_de_desperdicio",
                x=col_kg,
                orientation="h",
                title="🧩 Desperdicio por Motivo Principal"
            )
            fig.update_traces(marker_color=colors["primary"])
            charts["motivos"] = _aplicar_estilo_grafico(fig, colors)

    return charts


# ==========================================================
# 4️ BLOQUE PRINCIPAL DEL DASHBOARD
# ==========================================================
def run_dashboard(df, title=None):
    """
    Ejecuta el dashboard completo de visualización.

    Flujo general:
        1. Carga del tema visual (claro, fijo).
        2. Renderiza encabezado con logo y título.
        3. Filtro de rango de fechas interactivo.
        4. Calcula métricas y muestra KPIs.
        5. Renderiza gráficos y tabla de datos.
    """
    colors = None
    if HAVE_THEME:
        try:
            colors, css = load_theme(mode="light")
            st.markdown(css, unsafe_allow_html=True)
        except Exception as e:
            st.caption(f"⚠️ No se pudo cargar el tema visual: {e}")

    if colors is None:
        colors = {
            "background": "#FFFFFF", "card_bg": "#FFFFFF", "text_primary": "#212121",
            "primary": "#1B5E20", "primary_light": "#4CAF50", "alert": "#E65100",
            "plotly_template": "plotly_white",
        }

    header_section()

    # --- Filtro principal por fecha ---
    if "fecha_de_registro" in df.columns:
        df = df.copy()
        df["fecha_de_registro"] = pd.to_datetime(df["fecha_de_registro"], errors="coerce")
        df = df.dropna(subset=["fecha_de_registro"])

        if df.empty:
            st.warning("⚠️ No hay datos con fechas válidas.")
            footer()
            return

        min_date = df["fecha_de_registro"].min().date()
        max_date = df["fecha_de_registro"].max().date()

        # Rango por defecto anclado a los propios datos (no a la fecha del
        # sistema), para que nunca quede invertido si el dataset es antiguo.
        default_end = max_date
        default_start = max(min_date, max_date - pd.Timedelta(days=365))

        try:
            date_range = st.date_input(
                "📅 Selecciona un rango de fechas:",
                value=(default_start, default_end),
                min_value=min_date,
                max_value=max_date,
                key="filtro_fecha_central"
            )

            if not date_range:
                st.info("🕒 Esperando selección de fecha...")
                footer()
                return

            if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                start_date, end_date = map(pd.to_datetime, date_range)
            else:
                start_date = end_date = pd.to_datetime(date_range)

            if start_date > end_date:
                start_date, end_date = end_date, start_date

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

    # --- Cálculo y visualización de métricas ---
    metrics = calculate_metrics(df_filtered)

    st.markdown("## 📊 Métricas Clave")
    col1, col2, col3, col4, col5 = st.columns(5)
    kpi_card("Desperdicio Total", f"{metrics['total_desperdicio']:.1f} kg", colors["primary"], col1)
    kpi_card("Promedio Diario", f"{metrics['promedio_diario']:.1f} kg", colors["primary"], col2)
    kpi_card("Días Analizados", f"{metrics['total_dias']}", colors["primary"], col3)
    kpi_card("Días con Desperdicio", f"{metrics['dias_con_desperdicio']}", colors["primary"], col4)
    kpi_card("Días Atípicos", f"{metrics['dias_atipicos']}", colors["alert"], col5, alert=True)

    if metrics["dias_sin_dato_kg"] > 0:
        st.caption(
            f"ℹ️ {metrics['dias_sin_dato_kg']} registro(s) sin dato de cantidad desperdiciada "
            "(no se incluyen en los totales, no se estiman)."
        )

    # --- Visualizaciones ---
    trend_chart = create_trend_chart(df_filtered, colors)
    if trend_chart:
        st.plotly_chart(trend_chart, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar la evolución temporal.")

    st.markdown("## 🍽️ ¿Cómo y por qué se desperdició?")
    charts = create_composition_charts(df_filtered, colors)
    cols = st.columns(2)
    if "alimentos" in charts:
        cols[0].plotly_chart(charts["alimentos"], use_container_width=True)
    if "motivos" in charts:
        cols[1].plotly_chart(charts["motivos"], use_container_width=True)

    # --- Tabla detallada ---
    with st.expander("🔍 Ver datos detallados"):
        st.dataframe(df_filtered.head(1000))

    footer()