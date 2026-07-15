# Estructura del Google Form — ZeroWaste Campus

Este documento define la estructura que debe tener el Google Form para que el
pipeline de limpieza (`Backend/initial_read.py` → `Backend/*_clean.py`) pueda
procesarlo sin requerir cambios en el código.

⚠️ **Regla de oro:** el texto de cada pregunta debe copiarse de forma exacta
(mayúsculas, tildes, signos `¿?`), ya que Google Forms utiliza ese texto como
encabezado de columna en el Sheet, y `Backend/initial_read.py` valida esos
encabezados de forma exacta.

---

## Configuración general del Form

- La opción **"Recopilar direcciones de correo electrónico"** debe permanecer desactivada.
- La opción **"Limitar a 1 respuesta"** es opcional, según si se desea 1 registro por persona/día.
- La columna `Marca temporal` la agrega Google Forms automáticamente; no debe crearse manualmente, ya está contemplada en el pipeline.

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
- Nota técnica: al ser multi-selección, Google Sheets guarda las opciones elegidas separadas por coma en una sola celda (por ejemplo, `"Frutas, Lácteos"`). Este formato se procesa en `Backend/str_clean.py`.

### 6. Cantidad aproximada desperdiciada (Kg)
- **Tipo:** Respuesta corta
- **Obligatoria:** Sí
- **Validación de respuesta:** Número → Mayor o igual que → `0`
- **Texto de ayuda (debajo de la pregunta):** "Usar punto (.) para decimales. Ejemplo: 2.5. Si no hubo desperdicio, registrar 0."

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
- Nota técnica: cuando el Form no recibe respuesta en este campo, Google Sheets guarda la celda como texto vacío (`""`), no como valor nulo. Este comportamiento es compatible con lo que espera `clean_text()`.

---

## Vinculación del Form con un Sheet

Desde **Respuestas → ícono de Sheets (verde) → Crear hoja de cálculo**, el Form
debe vincularse a un Sheet nuevo. Ese Sheet constituye la fuente de datos del
proyecto, y su identificador (visible en la URL) es requerido en el siguiente
documento: [`02_SETUP.md`](./02_SETUP.md).