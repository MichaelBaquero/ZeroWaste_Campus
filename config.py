"""
Módulo: config.py
Descripción:
    Variables de configuración global del proyecto ZeroWaste Campus.
    Al clonar este repositorio, basta con modificar los valores de este
    archivo (ID de la hoja de cálculo y categorías válidas) para adaptar
    el proyecto a un nuevo Google Sheet sin tocar el resto del código.

    Las categorías se almacenan en minúsculas y sin tildes; la comparación
    contra los datos reales también elimina tildes antes de comparar
    (ver Backend/str_clean.py), por lo que no es necesario que coincidan
    caracter por caracter con el texto exacto del Google Form.
"""

# =====================================================
# CONEXIÓN A GOOGLE SHEETS
# =====================================================
SHEET_ID = "1utENsDjsbVrT9G4J2lfKPCqIdxgxnBnpNYrSFR1le1E"

# =====================================================
# COLUMNAS CATEGÓRICAS DE SELECCIÓN MÚLTIPLE
# =====================================================
# Estas columnas permiten varias respuestas por celda, separadas por coma
# (así es como Google Sheets guarda las respuestas de tipo "casillas de
# verificación" del Form).
COLUMNAS_MULTISELECCION = [
    "tipos_de_alimentos_mas_desperdiciados",
]

# =====================================================
# CATEGORÍAS VÁLIDAS POR COLUMNA (según el Google Form vigente)
# =====================================================
CATEGORIAS_VALIDAS = {
    "tipos_de_alimentos_mas_desperdiciados": [
        "frutas",
        "verduras / ensaladas",
        "proteina (carne, pollo, pescado, huevo)",
        "cereales / harinas (arroz, pasta, pan)",
        "lacteos",
        "postres / dulces",
        "bebidas",
        "no aplica / no hubo desperdicio",
    ],
    "principal_motivo_de_desperdicio": [
        "porciones muy grandes",
        "baja aceptacion / sabor",
        "baja asistencia de estudiantes",
        "error en el calculo de raciones",
        "alimento repetido en la semana",
        "menu poco atractivo",
        "condiciones climaticas (menor asistencia)",
        "no aplica / no hubo desperdicio",
    ],
    "que_se_hizo_con_el_excedente": [
        "se desecho totalmente",
        "se almaceno para consumo posterior",
        "donado a fundacion / comedor comunitario",
        "compostaje institucional",
        "reutilizacion al dia siguiente",
        "no aplica / no hubo excedente",
    ],
}