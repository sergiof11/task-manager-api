# Task Manager API

API REST para la gestión de tareas desarrollada con **FastAPI, PostgreSQL y SQLAlchemy**.

Incluye autenticación JWT, aislamiento de tareas por usuario, migraciones de base de datos, tests automatizados, Docker e integración continua.

## Funcionalidades

- Registro y login de usuarios
- Hash seguro de contraseñas con Argon2
- Autenticación JWT con expiración
- Endpoints de tareas protegidos
- CRUD completo de tareas
- Propiedad y aislamiento de tareas por usuario
- Paginación y filtrado por estado
- Validación de datos y manejo de errores
- Persistencia con PostgreSQL y SQLAlchemy
- Migraciones mediante Alembic
- Docker y Docker Compose
- Tests automatizados con 100% de cobertura sobre `app/`
- Análisis de código con Ruff
- Integración continua con GitHub Actions

## Tecnologías

| Área | Tecnologías |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Base de datos | PostgreSQL, SQLAlchemy, psycopg |
| Validación y configuración | Pydantic, pydantic-settings |
| Autenticación | PyJWT, Argon2, pwdlib |
| Migraciones | Alembic |
| Testing | pytest, pytest-cov, httpx |
| Calidad de código | Ruff |
| Infraestructura | Docker, Docker Compose |
| CI | GitHub Actions |

## Estructura del proyecto

```text
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   ├── versions/
│   │   ├── 902afd450102_initial_schema.py
│   │   └── 5fc071f53c9f_add_user_to_tasks.py
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── users.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_tasks_authorization.py
│   ├── test_tasks_crud.py
│   ├── test_tasks_filters.py
│   └── test_users.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Arquitectura

La aplicación separa responsabilidades entre distintos módulos:

- `routers/` — Endpoints HTTP
- `schemas.py` — Modelos de entrada y salida
- `models.py` — Modelos SQLAlchemy
- `crud.py` — Operaciones con la base de datos
- `dependencies.py` — Dependencias de autenticación
- `security.py` — Hashing de contraseñas y creación de JWT
- `config.py` — Configuración mediante variables de entorno
- `database.py` — Engine y sesiones de SQLAlchemy

La evolución del esquema de base de datos se gestiona mediante **migraciones de Alembic**.

## Endpoints

| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| `POST` | `/users/register` | No | Registrar un usuario |
| `POST` | `/auth/login` | No | Autenticarse y obtener un JWT |
| `GET` | `/auth/me` | Sí | Obtener el usuario autenticado |
| `GET` | `/tasks` | Sí | Listar las tareas propias |
| `GET` | `/tasks/{task_id}` | Sí | Obtener una tarea |
| `POST` | `/tasks` | Sí | Crear una tarea |
| `PUT` | `/tasks/{task_id}` | Sí | Actualizar una tarea |
| `DELETE` | `/tasks/{task_id}` | Sí | Eliminar una tarea |
| `GET` | `/health` | No | Comprobar el estado de la API |

Documentación interactiva:

```text
http://127.0.0.1:8000/docs
```

## Autenticación y autorización

Los usuarios inician sesión mediante:

```http
POST /auth/login
```

Un login correcto devuelve un JWT que contiene:

- `sub`: ID del usuario autenticado
- `exp`: Fecha de expiración del token

Las peticiones protegidas utilizan:

```text
Authorization: Bearer <access_token>
```

El cliente nunca envía manualmente el `user_id` al crear una tarea.

La API asigna automáticamente:

```text
tasks.user_id = current_user.id
```

Todas las operaciones sobre tareas se filtran por el usuario autenticado.

De esta forma, cada usuario únicamente puede consultar, modificar o eliminar sus propias tareas.

Las tareas inexistentes o pertenecientes a otro usuario devuelven:

```text
404 Not Found
```

Esto evita revelar la existencia de recursos pertenecientes a otros usuarios.

## Paginación y filtros

`GET /tasks` permite paginación mediante:

```http
GET /tasks?skip=0&limit=10
```

Valores por defecto:

```text
skip = 0
limit = 10
```

El límite máximo permitido es:

```text
limit = 100
```

También es posible filtrar por estado:

```http
GET /tasks?completed=true
```

O:

```http
GET /tasks?completed=false
```

Los parámetros pueden combinarse:

```http
GET /tasks?completed=false&skip=0&limit=10
```

## Validación y manejo de errores

La API valida:

- Formato de email
- Longitud de contraseñas
- Títulos de tareas
- IDs de tareas
- Parámetros de paginación
- Filtros booleanos

Principales respuestas de error:

| Estado | Uso |
|---|---|
| `401 Unauthorized` | Autenticación inválida o inexistente |
| `404 Not Found` | Tarea inexistente o perteneciente a otro usuario |
| `409 Conflict` | Email ya registrado |
| `422 Unprocessable Entity` | Datos de entrada inválidos |

Los errores de autenticación incluyen:

```text
WWW-Authenticate: Bearer
```

El login devuelve el mismo mensaje tanto para un email inexistente como para una contraseña incorrecta.

PostgreSQL mantiene además una restricción `UNIQUE` sobre el email como protección definitiva frente a duplicados.

Si se produce un `IntegrityError`, la sesión de SQLAlchemy ejecuta `rollback()` antes de devolver `409 Conflict`.

## Configuración

Crear un archivo `.env` a partir de `.env.example`.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestor_tareas
DB_USER=postgres
DB_PASSWORD=your_password_here

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

La configuración se carga mediante `pydantic-settings`.

Los secretos almacenados en `.env` están excluidos de Git.

## Ejecutar con Docker

Docker Compose ejecuta FastAPI y PostgreSQL como servicios independientes:

```text
Docker Compose
├── api → FastAPI
└── db  → PostgreSQL 16
```

La API se conecta a PostgreSQL a través de la red interna de Docker utilizando:

```text
DB_HOST=db
```

PostgreSQL dispone de un healthcheck y la API espera a que la base de datos esté disponible antes de iniciar.

Las migraciones de Alembic se aplican automáticamente antes de arrancar Uvicorn.

### Iniciar

```bash
docker compose up --build
```

Cuando la imagen ya está construida:

```bash
docker compose up
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Detener

```bash
docker compose down
```

Los datos de PostgreSQL se almacenan en un volumen persistente, por lo que recrear los contenedores no elimina usuarios ni tareas.

Para eliminar también los datos almacenados:

```bash
docker compose down -v
```

## Desarrollo local

Clonar el repositorio:

```bash
git clone https://github.com/sergiof11/task-manager-api.git
cd task-manager-api
```

Crear el entorno virtual:

```bash
python -m venv venv
```

Activarlo en Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Crear las bases de datos PostgreSQL:

```text
gestor_tareas
gestor_tareas_test
```

Aplicar las migraciones:

```bash
alembic upgrade head
```

Iniciar la API:

```bash
python -m uvicorn app.main:app --reload
```

## Migraciones

Alembic es la fuente de verdad para la evolución del esquema de base de datos.

Aplicar migraciones pendientes:

```bash
alembic upgrade head
```

Comprobar la revisión actual:

```bash
alembic current
```

La aplicación no utiliza `Base.metadata.create_all()` para gestionar cambios de esquema.

## Tests

Actualmente el proyecto cuenta con:

```text
39 tests
100% de cobertura sobre app/
```

La suite cubre:

- Registro de usuarios
- Emails duplicados
- Autenticación
- JWT válidos, inválidos y expirados
- Obtención del usuario autenticado
- CRUD de tareas
- Propiedad y aislamiento entre usuarios
- Paginación
- Filtros
- Validaciones
- Errores de integridad
- Healthcheck

Ejecutar todos los tests:

```bash
python -m pytest
```

Ejecutar los tests con cobertura:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Ejecutar la misma comprobación de cobertura utilizada en CI:

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

Los tests utilizan una base de datos PostgreSQL separada:

```text
gestor_tareas_test
```

## Calidad de código

Ejecutar Ruff:

```bash
ruff check .
```

Aplicar correcciones automáticas seguras:

```bash
ruff check . --fix
```

Comprobaciones recomendadas antes de un commit:

```bash
ruff check .
python -m pytest
```

## Integración continua

GitHub Actions se ejecuta automáticamente en los `push` y pull requests.

El workflow:

1. Inicia un entorno Ubuntu
2. Levanta PostgreSQL
3. Instala las dependencias
4. Ejecuta Ruff
5. Aplica las migraciones de Alembic sobre una base de datos vacía
6. Ejecuta la suite de tests con cobertura
7. Verifica que la cobertura de `app/` sea al menos del 90%

Configuración:

```text
.github/workflows/ci.yml
```

El workflow falla automáticamente si Ruff, las migraciones, los tests o el umbral mínimo de cobertura no se completan correctamente.

## Decisiones técnicas

- La propiedad de las tareas se obtiene del JWT y nunca del cuerpo de la petición.
- Las tareas de otros usuarios devuelven `404` para no revelar su existencia.
- Las consultas SQLAlchemy utilizan parámetros enlazados en lugar de concatenar entrada del usuario.
- Alembic gestiona todos los cambios del esquema.
- Desarrollo y tests utilizan bases de datos separadas.
- PostgreSQL utiliza un volumen Docker persistente.
- Docker espera a que PostgreSQL esté disponible antes de arrancar la API.
- Las migraciones se ejecutan automáticamente al iniciar el contenedor de la API.
- El login devuelve el mismo error para usuarios inexistentes y contraseñas incorrectas.
- El listado de tareas limita las respuestas a un máximo de 100 elementos.

## Estado del proyecto

El desarrollo principal de la API está completado.

Estado actual:

```text
39 tests superados
100% de cobertura sobre la aplicación
Ruff limpio
Docker Compose verificado
CI con cobertura verificada
```

Pendiente:

- Despliegue en Azure
- Revisión de configuración y secretos de producción
- Pulido final del portfolio