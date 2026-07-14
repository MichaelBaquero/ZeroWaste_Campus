# SETUP — ZeroWaste Campus

Guía para conectar el proyecto una vez que ya existen el Google Form y su Sheet
vinculado (ver [`01_ESTRUCTURA_GOOGLE_FORM.md`](./01_ESTRUCTURA_GOOGLE_FORM.md)).
Cubre credenciales, permisos y arranque de la app.

---

## 1. Crear las credenciales (`creds.json`)

El proyecto usa una **cuenta de servicio** de Google Cloud (no tu cuenta personal)
para leer el Sheet vía API. Pasos:

1. Ve a [console.cloud.google.com](https://console.cloud.google.com/) y crea un
   proyecto nuevo (o usa uno existente).
2. En el buscador superior, activa estas dos APIs (una por una):
   - **Google Sheets API**
   - **Google Drive API**
3. Ve a **IAM y administración → Cuentas de servicio → Crear cuenta de servicio**.
   - Nombre: el que quieras (ej. `zerowaste-reader`)
   - No necesitas asignarle ningún rol de proyecto — el acceso al Sheet se da en el paso 2.
4. Dentro de la cuenta de servicio creada, ve a la pestaña **Claves → Agregar clave
   → Crear clave nueva → JSON**. Esto descarga un archivo `.json`.
5. Renombra ese archivo a **`creds.json`** y colócalo en:
   ```
   Data_connection/creds.json
   ```
   (Ya está en `.gitignore` — nunca se sube al repo. Verifica que siga ahí si algo cambia.)

---

## 2. Compartir el Sheet con la cuenta de servicio

La cuenta de servicio **no tiene acceso automático** a tu Sheet solo por tener las
APIs activadas. Debes compartirlo explícitamente:

1. Abre `creds.json` y copia el valor del campo `"client_email"`
   (se ve así: `zerowaste-reader@tu-proyecto.iam.gserviceaccount.com`)
2. Abre el Google Sheet → botón **Compartir**
3. Pega ese correo y dale acceso de **Lector** (es suficiente, ya que el código
   solo pide scope `readonly`)

Si te saltas este paso, el error que verás **no** será el 404 que ya resolvimos,
sino un `403 PERMISSION_DENIED` — son errores distintos, no te confundas si
aparece más adelante.

---

## 3. Configurar el `sheet_id`

1. Abre tu Sheet y copia el ID desde la URL:
   ```
   https://docs.google.com/spreadsheets/d/ESTE-ES-EL-ID/edit...
   ```
2. **Estado actual (temporal):** actualiza el valor directamente en
   `Data_connection/initial_read.py`, en el parámetro `sheet_id` de la función
   `initial_read()`.
   > 🔧 Pendiente: este valor se moverá a `config.py` como variable global
   > en la siguiente fase del proyecto. Cuando eso ocurra, actualiza este paso.

---

## 4. Instalar dependencias y correr el proyecto

```bash
pip install -r requirements.txt
streamlit run app.py
```

Si `app.py` carga sin errores y ves el dashboard con datos, el setup fue exitoso.