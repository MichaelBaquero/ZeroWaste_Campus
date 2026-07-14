# Estructura del Google Form — ZeroWaste Campus

Este documento define **exactamente** cómo debe quedar configurado el Google Form
para que el pipeline (`initial_read.py` → `Cleaning_data/*`) lo pueda leer sin
tocar código adicional.

⚠️ **Regla de oro:** el texto de cada pregunta debe copiarse **tal cual** (mayúsculas,
tildes, signos `¿?`) porque Google Forms usa ese texto como encabezado de columna
en el Sheet, y `initial_read.py` valida esos encabezados exactamente.

---

## Configuración general del Form

- Activa **"Recopilar direcciones de correo electrónico"** → NO (no lo necesitamos)
- Activa **"Limitar a 1 respuesta"** → opcional, según si quieres 1 registro por persona/día
- La columna `Marca temporal` la agrega Google automáticamente — no la crees tú, ya está contemplada en el pipeline.

---

## Preguntas (en este orden)

### 1. Fecha de registro
- **Tipo:** Fecha
- **Obligatoria:** Sí

### 2. Número de estudiantes atendidos hoy
- **Tipo:** Respuesta corta
- **Obligatoria:** Sí
- **Validación de respuesta:** Número → Mayor o igual que → `0`

### 3. Número de estudiantes ausentes en el servicio de alimentación
- **Tipo:** Respuesta corta
- **Obligatoria:** Sí
- **Validación de respuesta:** Número → Mayor o igual que → `0`

### 4. ¿Hubo desperdicio de alimentos?
- **Tipo:** Selección múltiple (una sola opción)
- **Obligatoria:** Sí
- **Opciones:**
  - Sí
  - No

### 5. Tipos de alimentos más desperdiciados
- **Tipo:** Casillas de verificación (multi-selección)
- **Obligatoria:** Sí
- **Opciones:**
  - Frutas
  - Verduras / Ensaladas
  - Proteína (carne, pollo, pescado, huevo)
  - Cereales / Harinas (arroz, pasta, pan)
  - Lácteos
  - Postres / Dulces
  - Bebidas
  - No aplica / No hubo desperdicio
- 💡 Al ser multi-selección, Google Sheets guardará las opciones elegidas separadas por coma en una sola celda (ej: `"Frutas, Lácteos"`). Esto se maneja en `Cleaning_data/str_clean.py`.

### 6. Cantidad aproximada desperdiciada (Kg)
- **Tipo:** Respuesta corta
- **Obligatoria:** Sí
- **Validación de respuesta:** Número → Mayor o igual que → `0`
- **Texto de ayuda (debajo de la pregunta):** "Usa punto (.) para decimales. Ejemplo: 2.5. Si no hubo desperdicio, escribe 0."

### 7. Principal motivo de desperdicio
- **Tipo:** Selección múltiple (una sola opción)
- **Obligatoria:** Sí
- **Opciones:**
  - Porciones muy grandes
  - Baja aceptación / Sabor
  - Baja asistencia de estudiantes
  - Error en el cálculo de raciones
  - Alimento repetido en la semana
  - Menú poco atractivo
  - Condiciones climáticas (menor asistencia)
  - No aplica / No hubo desperdicio

### 8. ¿Qué se hizo con el excedente?
- **Tipo:** Selección múltiple (una sola opción)
- **Obligatoria:** Sí
- **Opciones:**
  - Se desechó totalmente
  - Se almacenó para consumo posterior
  - Donado a fundación / comedor comunitario
  - Compostaje institucional
  - Reutilización al día siguiente
  - No aplica / No hubo excedente

### 9. Comentarios o notas del día
- **Tipo:** Párrafo
- **Obligatoria:** No
- Nota técnica: cuando el Form no tiene respuesta aquí, Google Sheets guarda la celda como texto vacío `""`, no como `NaN`. Eso es justo lo que `clean_text()` ya espera manejar.

---

## Vincular el Form a un Sheet

En **Respuestas → ícono de Sheets (verde) → Crear hoja de cálculo**, vincula el
Form a un Sheet nuevo. Ese Sheet es tu fuente de datos, y su ID (visible en la URL)
es lo que necesitarás para el siguiente documento: [`02_SETUP.md`](./02_SETUP.md).