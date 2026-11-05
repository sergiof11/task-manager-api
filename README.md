# Task Manager API

API REST para gestionar tareas y usuarios, desarrollada con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg
- Pydantic
- pwdlib
- Argon2
- pytest
- httpx

## Funcionalidades actuales

- Crear tareas
- Listar tareas
- Obtener una tarea por ID
- Actualizar tareas
- Eliminar tareas
- Validación de datos
- Registro de usuarios
- Validación de emails
- Protección frente a emails duplicados
- Hash seguro de contraseñas con Argon2
- Organización de endpoints mediante routers
- Base de datos PostgreSQL separada para tests
- Tests automáticos del CRUD y registro de usuarios

## Estructura del proyecto

```text
GestorTareas/
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── db_models.py
│   ├── models.py
│   ├── security.py
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py
│       └── users.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

1. Clonar el repositorio.

2. Crear un entorno virtual.

```powershell
python -m venv venv
```

3. Activar el entorno virtual.

```powershell
.\venv\Scripts\Activate
```

4. Instalar las dependencias.

```powershell
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` a partir de `.env.example`.

Ejemplo:

```env
DB_NAME=gestor_tareas
DB_PASSWORD=your_password_here
```

También es necesario tener PostgreSQL instalado y crear una base de datos llamada:

```text
gestor_tareas
```

## Ejecutar la API

Con el entorno virtual activado:

```powershell
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva de FastAPI estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### Tasks

#### Obtener todas las tareas

```http
GET /tasks
```

#### Obtener una tarea

```http
GET /tasks/{task_id}
```

#### Crear una tarea

```http
POST /tasks
```

Ejemplo:

```json
{
  "title": "Estudiar FastAPI"
}
```

El campo `completed` es opcional al crear una tarea y por defecto es `false`.

#### Actualizar una tarea

```http
PUT /tasks/{task_id}
```

Ejemplo:

```json
{
  "title": "Estudiar FastAPI y PostgreSQL",
  "completed": true
}
```

#### Eliminar una tarea

```http
DELETE /tasks/{task_id}
```

### Users

#### Registrar un usuario

```http
POST /users/register
```

Ejemplo:

```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

Las contraseñas no se almacenan en texto plano. Se guardan mediante un hash seguro utilizando Argon2.

El email debe tener un formato válido y no puede estar registrado previamente.

## Tests

El proyecto utiliza `pytest` y una base de datos PostgreSQL separada para los tests.

Ejecutar todos los tests:

```powershell
python -m pytest
```

Actualmente el proyecto cuenta con 12 tests que comprueban:

- listado de tareas
- obtención de tareas por ID
- creación de tareas
- actualización de tareas
- eliminación de tareas
- errores `404`
- validación de títulos incorrectos
- registro de usuarios
- emails duplicados
- validación de emails incorrectos
- que las contraseñas no se expongan en las respuestas

## Próximas mejoras

- Login de usuarios
- Autenticación con JWT
- Protección de endpoints
- Relación entre usuarios y tareas
- Autorización para que cada usuario acceda únicamente a sus tareas
- Ampliación de tests de autenticación y autorización
- Docker
- GitHub Actions
- Deploy en Azure
- README final para portfolio

## Estado del proyecto

Proyecto en desarrollo.

El CRUD de tareas, el registro de usuarios, la validación de datos, el hashing de contraseñas, SQLAlchemy y los tests básicos están implementados.

La siguiente fase estará centrada en login, autenticación JWT y protección de endpoints.