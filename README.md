# Task Manager API

API REST para gestionar tareas y usuarios, desarrollada con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg
- Alembic
- Pydantic
- pydantic-settings
- pwdlib
- Argon2
- PyJWT
- pytest
- httpx
- Ruff
- GitHub Actions

## Funcionalidades actuales

- Crear tareas
- Listar tareas
- Obtener una tarea por ID
- Actualizar tareas
- Eliminar tareas
- Validación de datos
- Registro de usuarios
- Login de usuarios
- Generación de access tokens JWT
- Validación de access tokens JWT
- Tokens JWT con identificación de usuario y expiración
- Obtención del usuario autenticado mediante JWT
- Endpoint protegido `GET /auth/me`
- Protección mediante JWT de todos los endpoints `/tasks`
- Relación entre usuarios y tareas mediante `user_id`
- Asignación automática del usuario autenticado al crear una tarea
- Foreign key entre `tasks.user_id` y `users.id`
- Índice sobre `tasks.user_id`
- Aislamiento de tareas por usuario
- Listado exclusivo de las tareas del usuario autenticado
- Protección frente al acceso a tareas de otros usuarios
- Protección frente a la modificación de tareas de otros usuarios
- Protección frente a la eliminación de tareas de otros usuarios
- Respuesta `404 Not Found` para tareas inexistentes o pertenecientes a otro usuario
- Paginación de tareas mediante `skip` y `limit`
- Límite máximo de 100 tareas por petición
- Filtro de tareas por estado `completed`
- Validación automática de parámetros de paginación
- Endpoint público `GET /health`
- Respuestas `401 Unauthorized` para peticiones sin token o con token inválido
- Cabecera `WWW-Authenticate: Bearer` en errores de autenticación
- Validación de emails
- Protección frente a emails duplicados
- Verificación segura de contraseñas
- Hash seguro de contraseñas con Argon2
- Acceso a PostgreSQL mediante SQLAlchemy
- Migraciones y versionado del esquema con Alembic
- Configuración centralizada con `pydantic-settings`
- Organización de endpoints mediante routers
- Base de datos PostgreSQL separada para tests
- Suite de tests organizada por tareas, usuarios, autenticación y healthcheck
- Fixtures compartidas con pytest
- Tests de aislamiento utilizando múltiples usuarios
- Tests de paginación y filtros
- Análisis estático y linting con Ruff
- Integración continua con GitHub Actions

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
│   ├── README
│   └── script.py.mako
├── app/
│   ├── main.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── auth.py
│       ├── tasks.py
│       └── users.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_tasks.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

Los archivos y carpetas locales como `.env`, `venv/`, `__pycache__/`, `.pytest_cache/` y `.ruff_cache/` están excluidos mediante `.gitignore`.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/sergiof11/task-manager-api.git
cd task-manager-api
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` a partir de `.env.example`.

Ejemplo:

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

También es necesario tener PostgreSQL instalado y crear una base de datos llamada:

```text
gestor_tareas
```

Para los tests se utiliza una base de datos PostgreSQL separada:

```text
gestor_tareas_test
```

La configuración de la aplicación se centraliza en `app/config.py` mediante `pydantic-settings`.

## Migraciones de base de datos

El proyecto utiliza Alembic para gestionar y versionar los cambios del esquema de PostgreSQL.

Actualmente existen dos migraciones:

- `902afd450102_initial_schema.py`: crea las tablas iniciales `users` y `tasks`
- `5fc071f53c9f_add_user_to_tasks.py`: añade `user_id` a las tareas y crea la relación con `users`

La relación entre tareas y usuarios utiliza:

- `tasks.user_id`
- foreign key hacia `users.id`
- índice sobre `tasks.user_id`
- restricción `NOT NULL` para garantizar que toda tarea tenga propietario

Aplicar todas las migraciones pendientes:

```bash
alembic upgrade head
```

Comprobar la versión actual de la base de datos:

```bash
alembic current
```

Crear una nueva migración detectando cambios en los modelos SQLAlchemy:

```bash
alembic revision --autogenerate -m "descripcion de la migracion"
```

Deshacer la última migración:

```bash
alembic downgrade -1
```

La aplicación ya no utiliza `Base.metadata.create_all()` para crear o evolucionar las tablas. El esquema de PostgreSQL se gestiona mediante las migraciones de Alembic.

## Ejecutar la API

Antes de iniciar la aplicación, asegúrate de que las migraciones están aplicadas:

```bash
alembic upgrade head
```

Después, con el entorno virtual activado:

```bash
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

Todos los endpoints de tareas están protegidos mediante autenticación JWT.

Es necesario enviar un access token válido mediante la cabecera:

```text
Authorization: Bearer <access_token>
```

Si no se proporciona un token válido, la API devuelve:

```text
401 Unauthorized
```

junto con:

```text
WWW-Authenticate: Bearer
```

Cada tarea almacena internamente el ID del usuario que la creó mediante `user_id`.

El cliente no envía manualmente este valor. La API obtiene el usuario autenticado a partir del JWT y asigna automáticamente:

```text
tasks.user_id = current_user.id
```

Además, todas las operaciones sobre tareas están filtradas por el usuario autenticado.

Esto significa que un usuario únicamente puede listar, consultar, actualizar o eliminar sus propias tareas.

Si intenta acceder a una tarea perteneciente a otro usuario, la API responde:

```text
404 Not Found
```

La API utiliza `404` en lugar de revelar que la tarea existe pero pertenece a otro usuario.

#### Obtener todas las tareas

```http
GET /tasks
```

Devuelve únicamente las tareas cuyo `user_id` corresponde al usuario autenticado.

El endpoint admite paginación mediante los parámetros:

- `skip`: número de tareas que se omiten. Valor por defecto: `0`
- `limit`: número máximo de tareas devueltas. Valor por defecto: `10`
- `limit` debe estar entre `1` y `100`

Ejemplo:

```http
GET /tasks?skip=0&limit=10
```

También permite filtrar las tareas por su estado:

```http
GET /tasks?completed=true
```

o:

```http
GET /tasks?completed=false
```

Los parámetros pueden combinarse:

```http
GET /tasks?completed=true&skip=0&limit=10
```

La paginación mantiene un orden estable por ID.

Si los parámetros de paginación no cumplen las restricciones definidas, FastAPI devuelve automáticamente:

```text
422 Unprocessable Entity
```

#### Obtener una tarea

```http
GET /tasks/{task_id}
```

Solo devuelve la tarea si pertenece al usuario autenticado.

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

El propietario de la tarea se obtiene automáticamente del usuario autenticado y no debe enviarse en el cuerpo de la petición.

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

Solo se puede actualizar una tarea perteneciente al usuario autenticado.

#### Eliminar una tarea

```http
DELETE /tasks/{task_id}
```

Solo se puede eliminar una tarea perteneciente al usuario autenticado.

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

Las contraseñas no se almacenan en texto plano. Se transforman mediante Argon2 antes de guardarse en PostgreSQL.

El email debe tener un formato válido y no puede estar registrado previamente.

### Auth

#### Login de usuario

```http
POST /auth/login
```

Ejemplo:

```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

El endpoint comprueba que el usuario existe y que la contraseña coincide con el hash almacenado.

Si las credenciales son correctas, genera y devuelve un access token JWT:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

El token contiene:

- `sub`: ID del usuario autenticado
- `exp`: fecha y hora de expiración del token

La duración del token se configura mediante:

```text
ACCESS_TOKEN_EXPIRE_MINUTES
```

Si el email no existe o la contraseña es incorrecta, devuelve:

```text
401 Unauthorized
```

La API utiliza el mismo mensaje de error para ambos casos para no revelar si un email concreto está registrado.

#### Obtener usuario autenticado

```http
GET /auth/me
```

Este endpoint está protegido y requiere enviar un access token JWT válido mediante la cabecera:

```text
Authorization: Bearer <access_token>
```

La API:

- extrae el token Bearer
- valida la firma del JWT
- comprueba automáticamente su expiración
- obtiene el ID del usuario desde el claim `sub`
- busca el usuario en PostgreSQL
- devuelve únicamente sus datos públicos

Ejemplo de respuesta:

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

Si el token es inválido, ha expirado o hace referencia a un usuario que ya no existe, devuelve:

```text
401 Unauthorized
```

### Health

#### Comprobar el estado de la API

```http
GET /health
```

Este endpoint es público y no requiere autenticación.

Ejemplo de respuesta:

```json
{
  "status": "ok"
}
```

Permite comprobar rápidamente que la aplicación está disponible y puede utilizarse posteriormente en entornos de despliegue o contenedores.

## Tests

El proyecto utiliza `pytest` y una base de datos PostgreSQL separada para evitar que los tests modifiquen los datos de desarrollo.

La suite está organizada por áreas de responsabilidad:

```text
tests/
├── conftest.py
├── test_auth.py
├── test_health.py
├── test_tasks.py
└── test_users.py
```

`conftest.py` contiene las fixtures compartidas de pytest, incluyendo:

- cliente de FastAPI
- limpieza automática de la base de datos antes de cada test
- creación de un usuario autenticado
- generación automática de cabeceras `Authorization` mediante `auth_headers`
- segundo usuario autenticado mediante `second_auth_headers`

Los tests se distribuyen de la siguiente forma:

- `test_tasks.py`: CRUD, validaciones, autenticación, propiedad, aislamiento, paginación y filtros de tareas
- `test_users.py`: registro y validaciones de usuarios
- `test_auth.py`: login, generación de JWT y autenticación
- `test_health.py`: comprobación del endpoint de estado de la API
- `conftest.py`: configuración y fixtures compartidas

Ejecutar todos los tests:

```bash
python -m pytest
```

Actualmente el proyecto cuenta con 30 tests que comprueban:

- listado de tareas con usuario autenticado
- rechazo del acceso a tareas sin token (`401`)
- rechazo del acceso a tareas con token inválido (`401`)
- cabecera `WWW-Authenticate: Bearer`
- obtención de una tarea existente por ID
- obtención de una tarea inexistente (`404`)
- creación de tareas
- actualización de tareas
- actualización de una tarea inexistente (`404`)
- eliminación de tareas
- eliminación de una tarea inexistente (`404`)
- validación de títulos formados solo por espacios
- registro de usuarios
- rechazo de emails duplicados
- validación de emails incorrectos
- login con credenciales correctas y generación de JWT válido
- rechazo de login con contraseña incorrecta (`401`)
- rechazo de login con usuario inexistente (`401`)
- obtención del usuario autenticado con un JWT válido
- rechazo de tokens inválidos o expirados (`401`)
- comprobación de que una tarea creada pertenece al usuario autenticado
- listado aislado de tareas entre dos usuarios
- rechazo del acceso a una tarea de otro usuario (`404`)
- rechazo de la modificación de una tarea de otro usuario (`404`)
- rechazo de la eliminación de una tarea de otro usuario (`404`)
- paginación mediante `skip` y `limit`
- filtrado de tareas completadas
- filtrado de tareas pendientes
- validación de límites de paginación (`422`)
- funcionamiento del endpoint `GET /health`

Los tests de aislamiento crean usuarios independientes y comprueban que cada uno únicamente puede operar sobre sus propias tareas.

El test de propiedad comprueba directamente en PostgreSQL que el `user_id` almacenado en la tarea coincide con el ID contenido en el claim `sub` del JWT del usuario autenticado.

Los tests de autenticación comprueban también que el JWT generado tiene una firma válida, contiene los claims `sub` y `exp` y permite recuperar correctamente al usuario autenticado.

## Calidad de código

El proyecto utiliza Ruff para analizar el código y detectar problemas de estilo, imports y posibles errores.

Ejecutar Ruff:

```bash
ruff check .
```

Antes de realizar commits importantes se recomienda ejecutar:

```bash
ruff check .
python -m pytest
```

## Integración continua

El proyecto utiliza GitHub Actions para ejecutar automáticamente las comprobaciones después de cada `push` y en los pull requests.

El workflow de CI:

- crea un entorno Ubuntu temporal
- levanta una instancia PostgreSQL temporal
- instala Python y las dependencias del proyecto
- ejecuta Ruff
- aplica las migraciones con `alembic upgrade head`
- ejecuta los tests con pytest

Esto permite comprobar que una base de datos PostgreSQL vacía puede construirse correctamente utilizando únicamente las migraciones del proyecto.

La configuración se encuentra en:

```text
.github/workflows/ci.yml
```

## Próximas mejoras

- Revisión y mejora del manejo de errores
- Cobertura de tests con `pytest-cov`
- Revisión final y reorganización de la suite de tests
- Revisión de casos límite
- Docker y Docker Compose
- CI completo con cobertura y validaciones adicionales
- Deploy en Azure
- Revisión de secretos y configuración
- README final para portfolio
- Revisión completa y cierre del proyecto

## Estado del proyecto

Proyecto en desarrollo.

Actualmente están implementados:

- CRUD completo de tareas
- PostgreSQL con SQLAlchemy
- separación entre modelos ORM y esquemas Pydantic
- registro de usuarios
- login de usuarios con verificación de credenciales
- hashing de contraseñas con Argon2
- verificación segura de contraseñas
- generación de access tokens JWT
- validación de access tokens JWT
- identificación del usuario mediante el claim `sub`
- expiración de tokens mediante el claim `exp`
- obtención del usuario autenticado mediante JWT
- endpoint protegido `GET /auth/me`
- protección JWT de todos los endpoints `/tasks`
- relación entre tareas y usuarios mediante `user_id`
- foreign key `tasks.user_id → users.id`
- índice sobre `tasks.user_id`
- asignación automática del propietario de una tarea desde el JWT
- aislamiento completo de tareas entre usuarios
- listado de tareas filtrado por usuario autenticado
- protección de consulta de tareas ajenas
- protección de modificación de tareas ajenas
- protección de eliminación de tareas ajenas
- uso de `404` para evitar revelar recursos pertenecientes a otros usuarios
- paginación mediante `skip` y `limit`
- límite máximo de 100 tareas por petición
- filtrado por estado `completed`
- validación de parámetros de paginación
- endpoint público `GET /health`
- migración Alembic `5fc071f53c9f_add_user_to_tasks.py`
- respuestas `401` para peticiones no autenticadas
- cabecera `WWW-Authenticate: Bearer`
- dependencias de autenticación separadas en `app/dependencies.py`
- configuración centralizada con `pydantic-settings`
- configuración JWT mediante variables de entorno
- validación de datos
- organización de rutas mediante routers
- migraciones y versionado de base de datos con Alembic
- migraciones reproducibles desde una base de datos vacía
- base de datos de test separada
- suite de tests separada por tareas, usuarios, autenticación y healthcheck
- fixtures compartidas mediante `conftest.py`
- fixtures `auth_headers` y `second_auth_headers`
- limpieza automática de la base de datos entre tests
- comprobación automática de la propiedad de las tareas
- tests de aislamiento entre múltiples usuarios
- tests de paginación y filtros
- 30 tests automáticos
- análisis de código con Ruff
- CI con GitHub Actions, PostgreSQL y migraciones

La siguiente fase estará centrada en revisar la calidad final de la API y de su suite de tests antes de comenzar con Docker y el despliegue.