"""
Módulo: config.py
Descripción:
    Variables de configuración global del proyecto ZeroWaste Campus.
    Al clonar este repositorio, basta con modificar los valores de este
    archivo (ID de la hoja de cálculo y categorías válidas) para adaptar
    el proyecto a un nuevo Google Sheet sin tocar el resto del código.
"""

# =====================================================
# CONEXIÓN A GOOGLE SHEETS
# =====================================================
SHEET_ID = "1utENsDjsbVrT9G4J2lfKPCqIdxgxnBnpNYrSFR1le1E"

# =====================================================
# CATEGORÍAS VÁLIDAS PARA COLUMNAS CATEGÓRICAS
# =====================================================
CATEGORIAS_VALIDAS = {
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