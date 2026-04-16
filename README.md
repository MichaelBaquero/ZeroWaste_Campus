# ZeroWaste Campus 🍽️📊

**Datos que alimentan el cambio**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Plataforma digital orientada a la gestión y análisis del desperdicio alimentario en entornos educativos. Integra procesos de lectura, limpieza y transformación de datos, simulación estadística y visualización interactiva mediante dashboards y reportes automáticos.

---

## 🎯 Propósito

El desperdicio de alimentos en comedores escolares y universitarios es una problemática persistente y, en muchos casos, poco cuantificada. La falta de datos confiables y herramientas accesibles dificulta la toma de decisiones informadas.

**ZeroWaste Campus** busca:

- Medir y visualizar patrones de desperdicio alimentario.
- Facilitar el análisis de datos para la toma de decisiones.
- Generar reportes automáticos para la gestión eficiente de recursos.

---

## 🧠 Estado del proyecto

✅ **Prototipo funcional (MVP)** – TRL 4–6  

- Desarrollo técnico completo y operativo.  
- Uso de datos simulados para validación.  
- Flujo de datos, procesamiento y visualización verificados.  

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Propósito |
|------------|----------|
| **Python** | Lenguaje principal |
| **Streamlit** | Interfaz de usuario |
| **Pandas** | Procesamiento y análisis de datos |
| **Plotly** | Visualización interactiva |
| **gspread + oauth2client** | Integración con Google Sheets |
| **unidecode** | Normalización de texto |
| **re** | Validación y limpieza de cadenas |
| **os** | Manejo de archivos |

---

## 🚀 Cómo ejecutar el proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/ZeroWaste-Campus.git
   cd ZeroWaste-Campus
   ```

2. **Crear entorno virtual (opcional)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar credenciales de Google Sheets**
   - Ubica el archivo `creds.json` en la raíz del proyecto.
   - Comparte la hoja de cálculo con el `client_email` de la cuenta de servicio.
   - Habilita la API de Google Sheets en Google Cloud.

5. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

---

## 📚 Referentes

- EatCloud – Economía circular aplicada a alimentos.
- Winnow Solutions – Reducción de desperdicio con analítica.
- FoodWise – Visualización y gamificación en entornos educativos.

---

## 📄 Licencia

Distribuido bajo licencia MIT. Ver archivo `LICENSE` para más información.

---

**ZeroWaste Campus** – *Datos que alimentan el cambio*  
Desarrollado por Michael Yesid Baquero Gómez, Angie Paola Montero Tique y Elquin Retavisca Linares\
Fundación Universitaria Cafam  
Bogotá, Colombia – 2025