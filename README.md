# device_systems

API REST desarrollada con **FastAPI** para la gestión del recurso `users` del sistema `device_systems`. Permite listar, consultar, filtrar y registrar usuarios, aplicando validación de datos con **Pydantic v2**, parámetros de ruta, parámetros de consulta, modelos de respuesta (`response_model`) y cabeceras HTTP personalizadas.

## 📁 Estructura del proyecto

device_systems/
│── requirements.txt
│── README.md
└── app/
    ├── __init__.py
    ├── main.py
    ├── schemas/
    │   ├── __init__.py
    │   └── user_schema.py
    └── routes/
        ├── __init__.py
        └── user_routes.py

## ⚙️ Instalación de dependencias

Crear y activar el entorno virtual:

python -m venv venv
venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

## 🚀 Ejecución del servidor

uvicorn app.main:app --reload

El servidor queda disponible en http://127.0.0.1:8000.

La documentación interactiva (Swagger UI) se genera automáticamente en:

http://127.0.0.1:8000/docs

## 📋 Tabla de endpoints

| Método | Ruta                     | Descripción                                                |
|--------|--------------------------|-------------------------------------------------------------|
| GET    | /users                   | Lista todos los usuarios                                    |
| GET    | /users?role=admin        | Filtra usuarios por rol (admin, support, user)               |
| GET    | /users?is_active=true    | Filtra usuarios por estado activo/inactivo                   |
| GET    | /users/{user_id}         | Consulta un usuario específico por su ID (Path Parameter)    |
| POST   | /users                   | Registra un nuevo usuario                                    |

## 🧩 Modelo de usuario (Pydantic)

Campos:

| Campo       | Tipo      | Validación                                       |
|-------------|-----------|---------------------------------------------------|
| id          | int       | Generado automáticamente por el servidor           |
| name        | str       | Obligatorio, mínimo 3 caracteres                    |
| email       | EmailStr  | Debe tener formato de correo válido                 |
| role        | Enum      | Solo permite: admin, support, user                  |
| is_active   | bool      | Verdadero o falso (por defecto true)                |

## 📨 Ejemplos de peticiones

### GET /users

Solicitud:

GET http://127.0.0.1:8000/users

Respuesta (200):

[
  {
    "id": 1,
    "name": "Ana Torres",
    "email": "ana@example.com",
    "role": "admin",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Luis Pérez",
    "email": "luis@example.com",
    "role": "user",
    "is_active": true
  }
]

### GET /users/{user_id}

Solicitud:

GET http://127.0.0.1:8000/users/1

Respuesta (200):

{
  "id": 1,
  "name": "Ana Torres",
  "email": "ana@example.com",
  "role": "admin",
  "is_active": true
}

Si el ID no existe, responde con error 404:

{
  "detail": "No se encontró un usuario con id 99."
}

### POST /users

Solicitud:

POST http://127.0.0.1:8000/users
Content-Type: application/json

{
  "name": "Carlos Ruiz",
  "email": "carlos@example.com",
  "role": "user",
  "is_active": true
}

Respuesta (201):

{
  "id": 4,
  "name": "Carlos Ruiz",
  "email": "carlos@example.com",
  "role": "user",
  "is_active": true
}

Si el correo ya existe, responde con error 400:

{
  "detail": "Ya existe un usuario registrado con el correo carlos@example.com."
}

## 🔐 Cabeceras HTTP personalizadas

Todas las respuestas incluyen las siguientes cabeceras:

X-App-Name: device_systems
X-API-Version: 1.0

## 🖼️ Capturas de Swagger UI

![GET /users](images/imagen-1.png)


![GET /users](images/images-2.png)


![GET /users](images/imgaes_3.png)


![GET /users](images/images-4.png)

![GET /users](images/images-5.png)



## 💭 Reflexión sobre el uso de FastAPI

Antes de este reto pensaba que hacer una API era mucho más complicado. Lo que más me sorprendió fue lo poco código que se necesita para tener validaciones sólidas: con Pydantic solo describo cómo deben ser los datos y FastAPI se encarga de rechazar lo que no cumpla, sin que yo tenga que escribir validaciones a mano.

Swagger UI también me ayudó bastante, porque pude probar cada endpoint directamente desde el navegador y detectar errores rápido, como cuando se me olvidó instalar `email-validator`.

Entender la diferencia entre Path Parameter y Query Parameter me quedó mucho más claro haciéndolo que solo leyéndolo, y separar `UserCreate` de `UserResponse` me hizo entender por qué es importante no devolver siempre lo mismo que se recibe. En general, aprendí que una buena API no es solo la que funciona, sino la que también es clara y segura.

## 🌱 Organización de ramas

- **main**: rama principal, reservada para futuras implementaciones.
- **feature**: contiene únicamente la estructura base del proyecto.
- **develop**: contiene la implementación completa y funcional de la API.