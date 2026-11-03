# Task Manager API

API REST para gestionar tareas, desarrollada con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg
- Pydantic
- pytest
- httpx

## Funcionalidades actuales

- Crear tareas
- Listar tareas
- Obtener una tarea por ID
- Actualizar tareas
- Eliminar tareas
- Validación de datos
- Base de datos separada para tests
- Tests automáticos del CRUD

## Estructura del proyecto

```text
GestorTareas/
├── main.py
├── crud.py
├── database.py
├── models.py
├── requirements.txt
├── .env.example
├── README.md
└── tests/
    └── test_main.py
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
python -m uvicorn main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación automática de FastAPI estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### Comprobar API

```http
GET /
```

### Obtener todas las tareas

```http
GET /tasks
```

### Obtener una tarea

```http
GET /tasks/{task_id}
```

### Crear una tarea

```http
POST /tasks
```

Ejemplo:

```json
{
  "title": "Estudiar FastAPI"
}
```

### Actualizar una tarea

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

### Eliminar una tarea

```http
DELETE /tasks/{task_id}
```

## Tests

El proyecto utiliza `pytest` y una base de datos PostgreSQL separada para los tests.

Ejecutar todos los tests:

```powershell
python -m pytest
```

Actualmente se prueban:

- funcionamiento básico de la API
- listado de tareas
- obtención de tareas por ID
- creación de tareas
- actualización de tareas
- eliminación de tareas
- errores `404`
- validación de títulos incorrectos

## Próximas mejoras

- Sistema de usuarios
- Autenticación con JWT
- Protección de endpoints
- Relación entre usuarios y tareas
- Docker
- GitHub Actions
- Deploy de la API

## Estado del proyecto

Proyecto en desarrollo.

La API CRUD y los tests básicos están implementados. Las siguientes fases estarán centradas en autenticación, usuarios y preparación para producción.