# SETUP — ZeroWaste Campus

Esta guía describe el proceso de conexión del proyecto una vez que existen el
Google Form y su Sheet vinculado (ver [`01_ESTRUCTURA_GOOGLE_FORM.md`](./01_ESTRUCTURA_GOOGLE_FORM.md)).
Cubre la creación de credenciales, la configuración de permisos y el arranque
de la aplicación.

---

## 1. Creación de las credenciales (`creds.json`)

El proyecto utiliza una **cuenta de servicio** de Google Cloud (independiente
de cualquier cuenta personal) para leer el Sheet a través de la API. Pasos:

1. Acceder a [console.cloud.google.com](https://console.cloud.google.com/) y crear un proyecto nuevo (o utilizar uno existente).
2. Activar las siguientes APIs:
   - **Google Sheets API**
   - **Google Drive API**
3. Ir a **IAM y administración → Cuentas de servicio → Crear cuenta de servicio**.
   - El nombre puede definirse libremente (por ejemplo, `zerowaste-reader`).
   - No es necesario asignar ningún rol de proyecto; el acceso al Sheet se otorga en el paso 2 de la siguiente sección.
4. Dentro de la cuenta de servicio creada, ir a la pestaña **Claves → Agregar clave → Crear clave nueva → JSON**. Esto descarga un archivo `.json`.
5. Renombrar ese archivo a **`creds.json`** y ubicarlo en:
   ```
   Backend/creds.json
   ```
   Este archivo ya está incluido en `.gitignore` y no debe subirse al repositorio bajo ninguna circunstancia.

---

## 2. Autorización del Sheet para la cuenta de servicio

La cuenta de servicio no obtiene acceso automático al Sheet por el solo hecho
de tener las APIs activadas; el acceso debe otorgarse explícitamente:

1. Abrir `creds.json` y copiar el valor del campo `"client_email"` (tiene un formato similar a `zerowaste-reader@nombre-proyecto.iam.gserviceaccount.com`).
2. Abrir el Google Sheet correspondiente y seleccionar **Compartir**.
3. Ingresar ese correo y otorgar acceso de **Lector** (es suficiente, dado que el código solicita únicamente el scope de solo lectura).

Si este paso se omite, el error resultante no será el 404 documentado en
versiones anteriores del proyecto, sino un `403 PERMISSION_DENIED`. Son
errores de naturaleza distinta.

---

## 3. Configuración de variables del proyecto

El identificador del Sheet y las categorías válidas para las columnas
categóricas se gestionan de forma centralizada en `config.py`, ubicado en la
raíz del proyecto. Al clonar el repositorio, deben actualizarse dos valores:

```python
SHEET_ID = "ID_DEL_NUEVO_SHEET"
```

El ID se obtiene desde la URL del Sheet:
```
https://docs.google.com/spreadsheets/d/ESTE-ES-EL-ID/edit...
```

Si las opciones del Google Form difieren de las definidas en
`01_ESTRUCTURA_GOOGLE_FORM.md`, el diccionario `CATEGORIAS_VALIDAS` en
`config.py` debe actualizarse para reflejar las categorías reales utilizadas.
No es necesario modificar ningún otro archivo del proyecto para estos ajustes.

---

## 4. Instalación de dependencias y ejecución

```bash
pip install -r requirements.txt
streamlit run app.py
```

Si `app.py` se ejecuta sin errores y el dashboard muestra los datos
correspondientes, el proceso de configuración se completó correctamente.