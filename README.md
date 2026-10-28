# Lab 3 Estructura de un backend

Código base del curso para leer, ejecutar y modificar a mano, sin IA.
Hardware de referencia: NodeMCU ESP8266, DHT11 y LED RGB de cátodo común.
Este proyecto es una propuesta de material base para acompañar la guía.

## Backend en Windows
Desde backend, en una terminal Command Prompt de VS Code:
```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger: http://127.0.0.1:8000/docs
En macOS/Linux: python3 -m venv .venv y usar .venv/bin/python.
Los cinco endpoints base están en app/routes.py. La lista guarda como máximo
100 lecturas en memoria y se pierde al reiniciar. Ejecutar un solo proceso.
POST /lecturas retorna HTTP 201 con {"lectura": {...}, "led": "apagado"}.
PUT /led acepta rojo, verde, azul o apagado. No hay autenticación:
utilizar únicamente en la red de laboratorio autorizada.

## Firmware
Abrir firmware con PlatformIO IDE en VS Code. Copiar include/config.example.h
a include/config.h y completar WiFi, URL con IPv4 del PC e identificador.
Build, Upload y Monitor a 115200 baudios. El ESP envía cada 5 segundos y aplica
el color devuelto por POST /lecturas; PUT /led se refleja en el próximo envío.
Conexiones y pruebas: ver guía. Las dependencias se descargan la primera vez.
No publicar config.h, contraseñas ni tokens.

## Reto
Implementar GET /lecturas/promedio?n=3 a mano; no se incluye la solución.
Devolver cantidad, temperatura_promedio y humedad_promedio (dos decimales).
Validar n de 1 a 100; sin lecturas responder 404; si hay menos de n, usar todas.

## Antes de la sesión
El docente debe probar el firmware en el hardware real y la red del aula,
precargar las herramientas y validar las dependencias en los equipos.
La guía destina 105 minutos a trabajar con el entorno ya preparado.

## Registro para GitHub
**Nombre:** Diego Escalante
**Paralelo:** 104

**Objetivo:**
Identificar la entrada de la aplicación, las rutas, los modelos, la lógica y el almacenamiento de un backend. Ejecutar la API localmente, probar sus endpoints desde Swagger, conectar el ESP8266 y agregar un nuevo endpoint.

**Cómo ejecutar el proyecto:**
1. Abrir una terminal en la carpeta `backend`.
2. Crear el entorno virtual ejecutando: `python -m venv .venv`
3. Instalar las dependencias con: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
4. Iniciar el servidor web con el comando: `.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
5. Abrir el navegador en `http://127.0.0.1:8000/docs` para acceder a la interfaz de Swagger.

**Respuestas a las preguntas de comprensión:**
*   **Pregunta 1:** La función asociada al método POST en `routes.py` es la que recibe el JSON, mientras que la función `guardar_lectura` ubicada en `services.py` es la encargada de guardarlo.
*   **Pregunta 2:** Para añadir una URL se debe modificar `routes.py` (para definir la ruta y el método HTTP) y `services.py` (para agregar la lógica o servicio que ejecutará esa ruta).
*   **Pregunta 3:** Al reiniciar la API, los datos de lectura y el color del LED se borran porque la aplicación guarda esta información de forma temporal en la memoria del proceso local (`store.py`), no en una base de datos persistente.
*   **Pregunta 4:** Puede devolver el error 422 si los valores enviados exceden los límites permitidos (por ejemplo, una humedad de 150). Esta validación de reglas y formatos se define en el archivo `schemas.py`.
*   **Pregunta 5:** El ESP8266 envía la petición HTTP con los datos; la ruta (`routes.py`) la recibe, el modelo (`schemas.py`) valida los formatos, el servicio (`services.py`) procesa la operación, y el almacenamiento (`store.py`) guarda el registro. El LED cambia físicamente cuando el microcontrolador recibe la respuesta de su siguiente petición al servidor.

**Modificación del backend (Parte 5):**
Se modificó el archivo `routes.py` en el endpoint `GET /salud`. Se añadió el campo `"laboratorio": 3` al diccionario retornado. La respuesta cambió de `{"estado": "ok"}` a `{"estado": "ok", "laboratorio": 3}`.

**Resultados de las pruebas de los Endpoints (Parte 3):**
*   **GET /salud:** Código esperado: 200 | Código obtenido: 200
*   **GET /lecturas:** Código esperado: 200 | Código obtenido: 200
*   **GET /led:** Código esperado: 200 | Código obtenido: 200 
*   **PUT /led (verde):** Código esperado: 200 | Código obtenido: 200
*   **POST /lecturas (Datos válidos):** Código esperado: 201 | Código obtenido: 201
*   **GET /lecturas (Validación):** Código esperado: 200 | Código obtenido: 200 (Contiene la lectura)
*   **POST /lecturas (Humedad 150):** Código esperado: 422 | Código obtenido: 422
*   **PUT /led (Amarillo):** Código esperado: 422 | Código obtenido: 422