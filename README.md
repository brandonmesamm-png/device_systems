
/
















Readme · MD
# 🖥️ device_systems
 
API REST para la gestión de **usuarios, dispositivos tecnológicos y préstamos**, desarrollada con **FastAPI**, **SQLAlchemy** y **Alembic**, y asegurada con **OAuth2 + JWT**.
 
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00)
![Alembic](https://img.shields.io/badge/Alembic-migraciones-6BA81E)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-OAuth2%20%2B%20JWT-critical)
 
> **EV10** — GA1-220501096-01-AA1-EV10 · FastAPI avanzado: migraciones con Alembic, asociaciones de modelos y consultas con joins.
> **EV11** — GA1-220501096-01-AA1-EV11 · Seguridad: autenticación OAuth2 + JWT, middleware, CORS, rate limiting y validación avanzada.
> **Aprendiz:** Brandon Maldonado Mey · SENA · Tecnólogo en Análisis y Desarrollo de Software · Ficha JU6901
 
---
 
## 📑 Índice
 
1. [Descripción general](#1--descripción-general)
2. [Tecnologías](#2--tecnologías)
3. [Estructura del proyecto](#3--estructura-del-proyecto)
4. [Modelo de datos y asociaciones](#4--modelo-de-datos-y-asociaciones)
5. [Migraciones con Alembic](#5--migraciones-con-alembic)
6. [Instalación y ejecución](#6--instalación-y-ejecución)
7. [Endpoints](#7--endpoints)
8. [Consultas con joins y filtros](#8--consultas-con-joins-y-filtros)
9. [Manejo de errores y reglas de negocio](#9--manejo-de-errores-y-reglas-de-negocio)
10. [Pruebas funcionales EV10 (16 escenarios)](#10--pruebas-funcionales-ev10-16-escenarios)
11. [Evidencias de la actividad anterior](#11--evidencias-de-la-actividad-anterior)
12. [🔐 Seguridad y autenticación (EV11)](#12--seguridad-y-autenticación-ev11)
13. [Reflexión final](#13--reflexión-final)
14. [Ramas y entrega](#14--ramas-y-entrega)
15. [🎥 Video de socialización](#15--video-de-socialización)
---
 
## 1. 📋 Descripción general
 
`device_systems` evolucionó de un CRUD de una sola tabla (`users`) a un sistema **relacional y seguro** con cuatro recursos:
 
| Recurso | Qué permite |
|---|---|
| `/auth` | Registro, login (OAuth2 + JWT) y consulta del usuario autenticado |
| `/users` | CRUD de usuarios y su historial de préstamos |
| `/devices` | CRUD de dispositivos, filtros e historial de préstamos de cada equipo |
| `/loans` | Registrar préstamos, devolverlos y consultarlos con joins y filtros avanzados |
 
**Lo nuevo en EV10**
 
- ✅ **Migraciones versionadas** con Alembic (`upgrade` y `downgrade`).
- ✅ **Asociaciones One-to-Many / Many-to-One** entre `User`, `Device` y `Loan`.
- ✅ **Integridad referencial** con llaves foráneas activas en SQLite.
- ✅ **Consultas con `join()`**, `where()`, `ilike()`, `or_()` y `and_()`.
- ✅ **Reglas de negocio** con respuestas `409 Conflict`.
**Lo nuevo en EV11**
 
- ✅ **Autenticación OAuth2 + JWT** (`/auth/register`, `/auth/login`, `/auth/me`).
- ✅ **Contraseñas con hash bcrypt** (passlib), nunca en texto plano.
- ✅ **Autorización por roles** (`admin`, `support`, `user`) protegiendo rutas sensibles.
- ✅ **CORS** configurado para orígenes de desarrollo controlados.
- ✅ **Middleware personalizado** con cabeceras de trazabilidad (`X-Process-Time`, `X-Request-ID`, `X-App-Name`).
- ✅ **Rate limiting** con `slowapi` en los endpoints más sensibles.
- ✅ Documentación **Swagger** con esquema OAuth2 y candados por ruta.
---
 
## 2. 🛠️ Tecnologías
 
| Tecnología | Uso |
|---|---|
| Python 3.14 | Lenguaje base |
| FastAPI | Framework de la API |
| Uvicorn | Servidor ASGI |
| SQLAlchemy 2.x | ORM, relaciones y joins |
| Alembic | Migraciones de base de datos |
| SQLite | Base de datos relacional |
| Pydantic v2 | Validación y serialización |
| python-jose | Generación y validación de JWT |
| passlib + bcrypt | Hash seguro de contraseñas |
| slowapi | Rate limiting |
| Swagger UI / ReDoc | Documentación automática |
| Git y GitHub | Control de versiones |
 
---
 
## 3. 📁 Estructura del proyecto
 
```
device_systems/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── user_model.py            # incluye hashed_password, role, is_active
│   │   ├── device_model.py
│   │   └── loan_model.py
│   ├── auth/                         # 🔐 EV11
│   │   ├── security.py               # hash y JWT
│   │   ├── auth_service.py           # lógica de registro/login
│   │   └── auth_routes.py            # /auth/register /auth/login /auth/me
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   ├── loan_schema.py
│   │   └── auth_schema.py            # 🔐 EV11
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   ├── dependencies/
│   │   ├── database_dependency.py
│   │   ├── user_dependencies.py
│   │   ├── device_dependencies.py
│   │   ├── loan_dependencies.py
│   │   └── auth_dependency.py        # 🔐 EV11 (get_current_user, require_admin...)
│   └── middlewares/                  # 🔐 EV11
│       └── request_middleware.py     # cabeceras y trazabilidad
├── alembic/
│   └── versions/
│       ├── 2559e22fb356_create_users_devices_and_loans_tables.py
│       ├── c7b5b83c3f83_create_devices_and_loans_tables.py
│       └── 5b12b86d156a_add_hashed_password_to_users.py   # 🔐 EV11
├── alembic.ini
├── .env.example                      # 🔐 EV11
├── requirements.txt
└── README.md
```
 
| Capa | Responsabilidad |
|---|---|
| **database** | Conexión, sesiones y `Base`. Activa las llaves foráneas de SQLite. |
| **models** | Tablas reales, constraints y relaciones (`ForeignKey`, `relationship`). |
| **auth** | Hash de contraseñas, generación/validación de JWT y lógica de registro/login. |
| **schemas** | Contratos de entrada/salida en Pydantic, con ejemplos para Swagger. |
| **services** | Lógica de negocio, joins, filtros y reglas de disponibilidad. |
| **routes** | Endpoints, documentación, códigos de respuesta y protección por rol. |
| **dependencies** | Funciones reutilizables con `Depends()` (sesión, `get_*_or_404`, autenticación y roles). |
| **middlewares** | Cabeceras de trazabilidad y medición de tiempo de respuesta. |
 
---
 
## 4. 🗃️ Modelo de datos y asociaciones
 
### Diagrama entidad-relación
 
```mermaid
erDiagram
    USERS ||--o{ LOANS : "tiene muchos"
    DEVICES ||--o{ LOANS : "aparece en muchos"
 
    USERS {
        int id PK
        string name
        string email UK
        string role
        bool is_active
        string hashed_password
        datetime created_at
    }
    DEVICES {
        int id PK
        string name
        string serial_number UK
        string device_type
        string brand
        bool is_available
        datetime created_at
    }
    LOANS {
        int id PK
        int user_id FK
        int device_id FK
        datetime loan_date
        datetime return_date
        string status
    }
```
 
### Tablas
 
| Tabla | Campos clave |
|---|---|
| `users` | `id`, `name`, `email` (único), `role`, `is_active`, `hashed_password`, `created_at` |
| `devices` | `id`, `name`, `serial_number` (único), `device_type`, `brand` (opcional), `is_available` (default `True`), `created_at` |
| `loans` | `id`, `user_id` → `users.id`, `device_id` → `devices.id`, `loan_date`, `return_date` (opcional), `status` |
 
- **Roles de usuario:** `admin`, `support`, `user`.
- **Tipos de dispositivo:** `laptop`, `tablet`, `proyector`, `camara`, `router`, `monitor`.
- **Estados de préstamo:** `active`, `returned`, `overdue`.
### Asociaciones
 
```python
# User
loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
 
# Device
loans = relationship("Loan", back_populates="device", cascade="all, delete-orphan")
 
# Loan
user = relationship("User", back_populates="loans")
device = relationship("Device", back_populates="loans")
```
 
### Ciclo de vida de un préstamo
 
```mermaid
stateDiagram-v2
    [*] --> active: POST /loans (dispositivo pasa a no disponible)
    active --> overdue: PATCH /loans/{id}
    active --> returned: PATCH /loans/{id}/return
    overdue --> returned: PATCH /loans/{id}/return
    returned --> [*]: dispositivo vuelve a estar disponible
```
 
### Integridad referencial
 
- `Loan.user_id` y `Loan.device_id` son llaves foráneas con `nullable=False`.
- SQLite no las aplica por defecto: `connection.py` ejecuta `PRAGMA foreign_keys=ON` en cada conexión con un listener de SQLAlchemy.
- Además, la API valida antes de escribir y responde `404` si el usuario o el dispositivo no existen.
---
 
## 5. 🔄 Migraciones con Alembic
 
`alembic/env.py` se configuró para usar la URL de la app, la metadata de SQLAlchemy, e importar los modelos `user_model`, `device_model` y `loan_model` para que `--autogenerate` los detecte.
 
### Historial de migraciones
 
```
c7b5b83c3f83 -> 5b12b86d156a (head), add hashed_password to users
2559e22fb356 -> c7b5b83c3f83, create devices and loans tables.
<base> -> 2559e22fb356, create users devices and loans tables
```
 
![Historial de migraciones](images/security/12_migracion_alembic.png)
 
### Comandos usados
 
```bash
python -m alembic revision --autogenerate -m "create devices and loans tables"
python -m alembic revision --autogenerate -m "add hashed_password to users"
python -m alembic upgrade head
python -m alembic history
```
 
### Si falla una migración
 
| Situación | Qué hacer |
|---|---|
| Saber en qué versión está la base | `python -m alembic current` |
| Revertir la última migración | `python -m alembic downgrade -1` |
| Volver a aplicar tras corregir | `python -m alembic upgrade head` |
| Error `table ... already exists` o base inconsistente | Eliminar `device_systems.db` y ejecutar `python -m alembic upgrade head` de nuevo |
 
---
 
## 6. ⚙️ Instalación y ejecución
 
```bash
# 1. Clonar el repositorio
git clone https://github.com/brandonmesamm-png/device_systems.git
cd device_systems
 
# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows (CMD)
# source venv/bin/activate     # Linux / Mac
 
# 3. Instalar dependencias
pip install -r requirements.txt
 
# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env y generar una SECRET_KEY real:
python -c "import secrets; print(secrets.token_hex(32))"
 
# 5. Aplicar las migraciones (crea las tablas)
python -m alembic upgrade head
 
# 6. Ejecutar el servidor
python -m uvicorn app.main:app --reload
```
 
| Recurso | URL |
|---|---|
| API | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
 
---
 
## 7. 📌 Endpoints
 
> Las rutas están definidas con barra final (por ejemplo `/devices/`). Sin ella, FastAPI redirige automáticamente (307).
 
### 🔐 Auth
 
| Operación | Método | Endpoint | Protección | Códigos |
|---|---|---|---|---|
| Registrar usuario | POST | `/auth/register` | Pública (rate limit 3/min) | 201 · 400 · 422 · 429 |
| Iniciar sesión | POST | `/auth/login` | Pública (rate limit 5/min) | 200 · 401 · 429 |
| Perfil autenticado | GET | `/auth/me` | Requiere token | 200 · 401 |
 
### 👤 Users
 
| Operación | Método | Endpoint | Protección | Códigos |
|---|---|---|---|---|
| Listar / filtrar | GET | `/users/` | Autenticado (rate limit 30/min) | 200 · 401 |
| Consultar por ID | GET | `/users/{user_id}` | Autenticado | 200 · 401 · 404 |
| Crear | POST | `/users/` | — | 201 · 400 |
| Actualizar completo | PUT | `/users/{user_id}` | — | 200 · 400 · 404 |
| Actualizar parcial | PATCH | `/users/{user_id}` | — | 200 · 400 · 404 |
| Eliminar | DELETE | `/users/{user_id}` | — | 204 · 404 · 409 |
| Préstamos de un usuario | GET | `/users/{user_id}/loans` | — | 200 · 404 |
 
### 💻 Devices
 
| Operación | Método | Endpoint | Protección | Códigos |
|---|---|---|---|---|
| Listar / filtrar | GET | `/devices/` | Pública | 200 |
| Consultar por ID | GET | `/devices/{device_id}` | Pública | 200 · 404 |
| Crear | POST | `/devices/` | Admin o support | 201 · 400 · 401 · 403 |
| Actualizar completo | PUT | `/devices/{device_id}` | Admin o support | 200 · 400 · 401 · 403 · 404 |
| Actualizar parcial | PATCH | `/devices/{device_id}` | Admin o support | 200 · 400 · 401 · 403 · 404 |
| Eliminar | DELETE | `/devices/{device_id}` | **Solo admin** | 204 · 401 · 403 · 404 · 409 |
| Historial de préstamos | GET | `/devices/{device_id}/loans` | Pública | 200 · 404 |
 
### 📦 Loans
 
| Operación | Método | Endpoint | Protección | Códigos |
|---|---|---|---|---|
| Listar / filtrar | GET | `/loans/` | Pública | 200 |
| Listar con detalle (join) | GET | `/loans/details` | Admin o support | 200 · 400 · 401 · 403 |
| Consultar por ID (detalle) | GET | `/loans/{loan_id}` | Pública | 200 · 404 |
| Crear préstamo | POST | `/loans/` | Autenticado (rate limit 10/min) | 201 · 401 · 404 · 409 |
| Devolver préstamo | PATCH | `/loans/{loan_id}/return` | Admin o support | 200 · 401 · 403 · 404 · 409 |
| Actualizar estado | PATCH | `/loans/{loan_id}` | — | 200 · 400 · 404 · 409 |
 
---
 
## 8. 🔗 Consultas con joins y filtros
 
`loan_service.py` arma una consulta base con **`join()`** explícito hacia `users` y `devices`, y `joinedload()` para traer usuario y dispositivo en la misma consulta (evita el problema N+1):
 
```python
select(Loan)
    .join(User, Loan.user_id == User.id)
    .join(Device, Loan.device_id == Device.id)
    .options(joinedload(Loan.user), joinedload(Loan.device))
```
 
| Herramienta | Uso |
|---|---|
| `where()` | Estado, usuario, dispositivo y tipo de dispositivo |
| `ilike()` | Búsqueda parcial sin distinguir mayúsculas (correo, marca, nombre) |
| `or_()` | Búsqueda libre en nombre/correo del usuario y nombre/serie del dispositivo |
| `and_()` | Rango de fechas `from_date` / `to_date` |
 
`GET /loans/details` acepta: `status`, `user_id`, `device_id`, `user_email`, `device_type`, `search`, `from_date`, `to_date`.
 
---
 
## 9. ⚠️ Manejo de errores y reglas de negocio
 
| Caso | Código |
|---|---|
| Registro / recurso creado | `201 Created` |
| Consulta o devolución exitosa | `200 OK` |
| Eliminación exitosa | `204 No Content` |
| Usuario, dispositivo o préstamo inexistente | `404 Not Found` |
| Correo o número de serie duplicado · contraseña débil | `400 Bad Request` / `422 Unprocessable Entity` |
| Token faltante, inválido o expirado | `401 Unauthorized` |
| Rol sin permisos para la acción | `403 Forbidden` |
| Dispositivo no disponible · préstamo ya devuelto | `409 Conflict` |
| Límite de peticiones excedido | `429 Too Many Requests` |
 
---
 
## 10. 🧪 Pruebas funcionales EV10 (16 escenarios)
 
| # | Escenario | Evidencia |
|---|---|---|
| 1 | Inicializar Alembic | [`01_alembic_init.png`](images/alembic/01_alembic_init.png) |
| 2 | Generar migración con autogenerate | [`02_alembic_revision.png`](images/alembic/02_alembic_revision.png) |
| 3 | Ejecutar migraciones con Alembic | [`03_alembic_upgrade.png`](images/alembic/03_alembic_upgrade.png) |
| 4 | Verificar tablas generadas en la base de datos | [`05_tablas.png`](images/alembic/05_tablas.png) |
| 5 | Vista general de Swagger UI | [`06_swagger_general.png`](images/alembic/06_swagger_general.png) |
| 6 | Crear usuario | [`07_crear_usuario.png`](images/alembic/07_crear_usuario.png) |
| 7 | Crear dispositivo | [`08_crear_dispositivo.png`](images/alembic/08_crear_dispositivo.png) |
| 8 | Crear préstamo | [`09_crear_prestamo.png`](images/alembic/09_crear_prestamo.png) |
| 9 | Prestar un dispositivo no disponible (409) | [`10_dispositivo_no_disponible.png`](images/alembic/10_dispositivo_no_disponible.png) |
| 10 | Listar préstamos con usuario y dispositivo (join) | [`11_join_details.png`](images/alembic/11_join_details.png) |
| 11 | Filtrar préstamos por estado | [`12_filtro_status.png`](images/alembic/12_filtro_status.png) |
| 12 | Filtrar préstamos por tipo de dispositivo | [`13_filtro_device_type.png`](images/alembic/13_filtro_device_type.png) |
| 13 | Consultar préstamos de un usuario | [`14_prestamos_usuario.png`](images/alembic/14_prestamos_usuario.png) |
| 14 | Devolver un préstamo | [`15_devolucion.png`](images/alembic/15_devolucion.png) |
| 15 | Consultar historial de préstamos del dispositivo | [`17_historial_dispositivo.png`](images/alembic/17_historial_dispositivo.png) |
| 16 | Modificar el estado de un préstamo ya devuelto (409) | [`16_error_patch_prestamo_devuelto.png`](images/alembic/16_error_patch_prestamo_devuelto.png) |
 
<details>
<summary><b>Ver capturas EV10</b></summary>
![Swagger general](images/alembic/06_swagger_general.png)
![Crear usuario](images/alembic/07_crear_usuario.png)
![Crear dispositivo](images/alembic/08_crear_dispositivo.png)
![Crear préstamo](images/alembic/09_crear_prestamo.png)
![Dispositivo no disponible](images/alembic/10_dispositivo_no_disponible.png)
![Join details](images/alembic/11_join_details.png)
![Filtro status](images/alembic/12_filtro_status.png)
![Filtro device_type](images/alembic/13_filtro_device_type.png)
![Préstamos de usuario](images/alembic/14_prestamos_usuario.png)
![Devolución](images/alembic/15_devolucion.png)
![Historial del dispositivo](images/alembic/17_historial_dispositivo.png)
![Error patch préstamo devuelto](images/alembic/16_error_patch_prestamo_devuelto.png)
 
</details>
---
 
## 11. 🗂️ Evidencias de la actividad anterior
 
Se conservan las pruebas del CRUD de `/users` de la versión con SQLAlchemy (previas a EV10).
 
<details>
<summary><b>Swagger UI y ReDoc (versión anterior)</b></summary>
![Swagger UI](images/imagesEndpoint/swagger1.png)
![ReDoc](images/imagesEndpoint/swagger2.png)
 
</details>
<details>
<summary><b>Pruebas de endpoints exitosos</b></summary>
![Prueba 1](images/imagen-1.png)
![Prueba 2](images/images-2.png)
![Prueba 3](images/images-4.png)
![PUT](images/imagesEndpoint/put.png)
![PATCH](images/imagesEndpoint/patch.png)
![DELETE](images/imagesEndpoint/delete.png)
 
</details>
<details>
<summary><b>Pruebas de escenarios de error</b></summary>
![Error 1](images/imgaes_3.png)
![Error 2](images/images-5.png)
![Error 422](images/post_422.png)
![PUT error](images/imagesEndpoint/put_error.png)
![PATCH error](images/imagesEndpoint/patch_error.png)
![DELETE error](images/imagesEndpoint/delete_error.png)
 
</details>
---
 
## 12. 🔐 Seguridad y autenticación (EV11)
 
### 12.1 Autenticación OAuth2 + JWT
 
- **Hash de contraseñas:** `passlib` con backend `bcrypt`. Las contraseñas nunca se guardan ni se muestran en texto plano; solo se almacena `hashed_password`.
- **Tokens JWT:** generados y validados con `python-jose` (`create_access_token` / `decode_access_token`), firmados con una `SECRET_KEY` leída desde `.env`.
- **Flujo estándar OAuth2 password:** el botón *Authorize* de Swagger envía `username`/`password` como formulario contra `/auth/login`, que internamente valida las credenciales y devuelve un `access_token` tipo `bearer`.
### 12.2 Autorización por roles
 
Roles soportados: `admin`, `support`, `user`. Las dependencias `get_current_user`, `get_current_active_user`, `require_admin` y `require_admin_or_support` (en `app/dependencies/auth_dependency.py`) protegen las rutas sensibles según la tabla de la sección 7. Un token faltante o inválido responde `401 Unauthorized`; un rol sin permisos responde `403 Forbidden`.
 
### 12.3 CORS
 
Configurado en `app/main.py`:
 
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
 
**¿Por qué no se usa `"*"` en `allow_origins`?** Porque `allow_credentials=True` está activo. El estándar CORS no permite combinar un origen comodín (`*`) con credenciales (cookies o cabeceras `Authorization`): si se permitiera, cualquier sitio web ajeno podría hacer peticiones autenticadas en nombre de un usuario con sesión iniciada en el navegador, exponiendo sus datos. Por eso en desarrollo se listan explícitamente los orígenes del frontend (`localhost:5173`, `localhost:3000`), y en producción deben ser los dominios reales de la aplicación cliente.
 
### 12.4 Middleware personalizado
 
`app/middlewares/request_middleware.py` agrega a cada respuesta:
 
- `X-App-Name: device_systems`
- `X-Process-Time`: tiempo de procesamiento de la petición, en segundos.
- `X-Request-ID`: identificador único de la petición (generado o propagado).
Además registra en el log el método, la ruta y el código de estado de cada petición.
 
### 12.5 Rate limiting
 
Configurado con `slowapi`:
 
| Endpoint | Límite |
|---|---|
| `POST /auth/login` | 5 por minuto |
| `POST /auth/register` | 3 por minuto |
| `GET /users/` | 30 por minuto |
| `POST /loans/` | 10 por minuto |
 
Al superar el límite, la API responde `429 Too Many Requests`.
 
### 12.6 Pruebas funcionales EV11
 
| # | Escenario | Evidencia |
|---|---|---|
| 1 | Estructura del proyecto con los módulos de seguridad | [`11_estructura_proyecto.png`](images/security/11_estructura_proyecto.png) |
| 2 | Migración Alembic aplicada (`add_hashed_password_to_users`) | [`12_migracion_alembic.png`](images/security/12_migracion_alembic.png) |
| 3 | Registro de usuario | [`02_registro_usuario.png`](images/security/02_registro_usuario.png) |
| 4 | Registro con contraseña débil (422) | [`03_registro_password_debil.png`](images/security/03_registro_password_debil.png) |
| 5 | Registro con correo duplicado (400) | [`04_registro_email_duplicado.png`](images/security/04_registro_email_duplicado.png) |
| 6 | Login correcto (token generado) | [`05_login_correcto.png`](images/security/05_login_correcto.png) |
| 7 | Login con contraseña incorrecta (401) | [`06_login_incorrecto.png`](images/security/06_login_incorrecto.png) |
| 8 | Consulta de `/auth/me` | [`07_auth_me.png`](images/security/07_auth_me.png) |
| 9 | Acceso a ruta protegida sin token (401) | [`08_sin_token.png`](images/security/08_sin_token.png) |
| 10 | Creación de dispositivo con rol permitido (admin) | [`09_crear_dispositivo_rol_permitido.png`](images/security/09_crear_dispositivo_rol_permitido.png) |
| 11 | Eliminación de dispositivo con rol no permitido (403) | [`10_rol_no_permitido_403.png`](images/security/10_rol_no_permitido_403.png) |
| 12 | Cabeceras generadas por el middleware | [`13_cabeceras_middleware.png`](images/security/13_cabeceras_middleware.png) |
| 13 | Activación de rate limiting (429) | [`14_rate_limiting.png`](images/security/14_rate_limiting.png) |
| 14 | Swagger/OpenAPI con esquema OAuth2 autenticado | [`15_swagger_oauth2.png`](images/security/15_swagger_oauth2.png) |
 
<details open>
<summary><b>Ver capturas EV11</b></summary>
![Estructura del proyecto](images/security/11_estructura_proyecto.png)
![Migración Alembic](images/security/12_migracion_alembic.png)
![Registro de usuario](images/security/02_registro_usuario.png)
![Contraseña débil](images/security/03_registro_password_debil.png)
![Correo duplicado](images/security/04_registro_email_duplicado.png)
![Login correcto](images/security/05_login_correcto.png)
![Login incorrecto](images/security/06_login_incorrecto.png)
![/auth/me](images/security/07_auth_me.png)
![Sin token](images/security/08_sin_token.png)
![Crear dispositivo rol permitido](images/security/09_crear_dispositivo_rol_permitido.png)
![Rol no permitido](images/security/10_rol_no_permitido_403.png)
![Cabeceras del middleware](images/security/13_cabeceras_middleware.png)
![Rate limiting](images/security/14_rate_limiting.png)
![Swagger OAuth2](images/security/15_swagger_oauth2.png)
 
</details>
---
 
## 13. 🧠 Reflexión final
 
### Sobre EV10 (relaciones, migraciones y joins)
 
Pasar de un CRUD de una sola tabla a un sistema con usuarios, dispositivos y préstamos cambió la forma en que pienso una API: ya no se trata solo de guardar y devolver registros, sino de **proteger la coherencia entre ellos**. Un préstamo no tiene sentido sin un usuario y un dispositivo reales, y un dispositivo prestado no puede prestarse otra vez. Esas reglas viven en las relaciones del modelo (`ForeignKey`, `relationship`, `back_populates`) y en los servicios.
 
**Las migraciones** con Alembic fueron el cambio más importante de mentalidad. Antes, `create_all()` creaba las tablas la primera vez y cualquier cambio obligaba a borrar la base de datos. Con Alembic, cada cambio estructural queda como una versión con `upgrade()` y `downgrade()`, se puede aplicar y revertir de forma controlada y queda registrado en el repositorio junto al código.
 
**Las consultas avanzadas** con `join()`, `where()`, `ilike()`, `or_()` y `and_()` permiten responder preguntas reales en una sola consulta, y `joinedload()` evita una consulta adicional por cada préstamo.
 
### Sobre EV11 (seguridad)
 
Agregar seguridad me obligó a pensar la API desde el punto de vista de un atacante, no solo de un usuario legítimo. Aprendí que el **hash de contraseñas** no es opcional: incluso en un proyecto académico, guardar una contraseña en texto plano es un error que no se debería cometer nunca, y `passlib` con `bcrypt` lo resuelve con una sola línea de código, aunque tuve que fijar la versión de `bcrypt` a `4.0.1` porque las versiones más nuevas rompen la compatibilidad con `passlib 1.7.4`.
 
El flujo **OAuth2 + JWT** me enseñó que el estándar importa: al principio hice que `/auth/login` recibiera JSON directamente, y aunque funcionaba con `curl`, el botón *Authorize* de Swagger no podía usarlo porque espera específicamente un formulario `OAuth2PasswordRequestForm`. Ajustar el endpoint a ese estándar no fue solo un capricho de Swagger, sino lo que permite que cualquier cliente OAuth2 (no solo el mío) pueda autenticarse contra la API.
 
La **autorización por roles** reveló un descuido real durante las pruebas: al probar el escenario de "rol no permitido", descubrí que `DELETE /devices/{id}` no tenía ninguna dependencia de seguridad aplicada, y un usuario con rol `user` pudo borrar un dispositivo sin ningún problema. Esto confirmó algo importante: una ruta "protegida a medias" (con el modelo y las dependencias ya creadas, pero sin conectarlas al endpoint) es tan insegura como una sin ninguna protección, y solo probar cada escenario explícitamente (no solo el camino feliz) permitió encontrar el fallo antes de la entrega.
 
Configurar **CORS** correctamente me hizo entender por qué `allow_origins=["*"]` junto con `allow_credentials=True` es una combinación peligrosa: no es una regla arbitraria de FastAPI, sino una protección del estándar CORS para que un sitio malicioso no pueda hacer peticiones autenticadas en nombre de un usuario.
 
Finalmente, el **middleware personalizado** y el **rate limiting** me mostraron el valor de la trazabilidad y la protección contra abuso: una cabecera como `X-Request-ID` parece trivial hasta que se necesita rastrear un error específico en producción, y un límite de 3 registros por minuto evita que alguien intente crear cientos de cuentas de forma automatizada.
 
En conjunto, EV11 mostró que la seguridad no es una capa que se agrega al final, sino un conjunto de decisiones que deben verificarse endpoint por endpoint, con evidencia real de que cada regla efectivamente se cumple.
 
---
 
## 14. 🌱 Ramas y entrega
 
| Rama | Contenido |
|---|---|
| `main` | Rama principal, versión estable |
| `develop` | Integración de las funcionalidades completas |
| `feature` | Estructura base del proyecto |
| `feature-crud-completo` | CRUD en memoria (actividad anterior) |
| `feature-crud-sqlalchemy` | Persistencia de usuarios con SQLAlchemy + SQLite |
| `device_systems_alembic_relaciones` | EV10: Alembic, `Device` y `Loan`, asociaciones, joins y filtros. Unificada con `main`. |
| `device_systems_security` | **EV11:** autenticación OAuth2 + JWT, roles, CORS, middleware y rate limiting. Se unifica con `main`. |
 
---
 
## 15. 🎥 Video de socialización
 
> Video explicativo (máx. 15 minutos) cubriendo: funcionalidades construidas, cambios respecto a la versión anterior, cómo se protegieron las rutas, cómo se implementó el hash de contraseñas, cómo funciona el login con OAuth2 y JWT, cómo se aplicó middleware y CORS, cómo se configuró el rate limiting, y qué se aprendió sobre seguridad en APIs.








 
📺 **Enlace al video:** [_video de youtube_](https://youtu.be/WwcAZhceExg)
 






















