Este documento proporciona la referencia técnica detallada para la API de Gestión Escolar. Su objetivo es facilitar a los desarrolladores la integración y el uso de los servicios de administración de centros educativos y su alumnado.

La documentación está organizada en tres secciones principales:

* Códigos de Estado: Una guía de referencia para interpretar las respuestas del servidor (éxitos y errores).

* Gestión de Escuelas: Detalle de los endpoints para administrar los centros, que incluyen:
    * Creación: Registro de nuevos centros con capacidad definida.
    * Lectura: Obtención del listado completo de escuelas o consulta detallada por ID (incluyendo alumnos asociados a la escuela).
    * Búsqueda: Localización de escuelas mediante filtros de nombre.
    * Eliminación: Borrado de registros de centros específicos.

* Gestión de Estudiantes: Especificación de las rutas para el control de alumnos, que incluyen:
    * Registro: Alta de estudiantes vinculados a una escuela (con validación de capacidad).
    * Consulta: Recuperación de información individual o colectiva de estudiantes.
    * Búsqueda: Filtros por nombre o apellido.
    * Eliminación: Baja de alumnos del sistema mediante su identificador único.

Cada endpoint incluye su método HTTP, la URL correspondiente, la estructura del cuerpo en formato JSON (cuando aplica) y ejemplos prácticos mediante comandos cURL para pruebas rápidas. 

# Referencia de códigos de estado

| Código | Estado | Descripción |
| :--- | :--- | :--- |
| 200 | OK | Operación realizada con éxito |
| 201 | Created | Recurso creado con éxito |
| 400 | Bad Request | Faltan campos obligatorios o datos duplicados |
| 403 | Forbidden | Capacidad máxima de la escuela alcanzada |
| 404 | Not Found | El ID proporcionado no existe |
| 409 | Conflict | El ID del estudiante ya está en uso |

# Gestión de Escuelas

## Crear una Escuela

Registra un nuevo centro en el sistema.

* Método: POST

* URL: /schools

* Cuerpo (JSON):
```
    {
      "name": "Escola de Les Corts",
      "capacity": 150
    }
```

### Ejemplo cURL:

```Bash
curl -X POST http://localhost:5000/schools -H "Content-Type: application/json" -d '{"name": "Escola de Les Corts", "capacity": 150}'
```

#### Respuesta

```Bash
{
  "capacity": 150,
  "id": 3,
  "name": "Escola de Les Corts",
  "student_count": 0
}
```

##  Obtener Todas las Escuelas

Recupera el listado de todas las escuelas. Los estudiantes de cada centro aparecen como objetos anidados.

* Método: GET

* URL: /schools

### Ejemplo cURL:

```Bash
curl -X GET http://localhost:5000/schools
```

#### Respuesta


```Bash
[
  {
    "id": 1,
    "name": "Escola Gracia",
    "student_count": 1,
    "students": [
      {
        "first_name": "Jordi",
        "id": "ST-000001",
        "last_name": "Pujol",
        "school_id": 1
      }
    ]
  },
  {
    "capacity": 100,
    "id": 2,
    "name": "Escola Eixample",
    "student_count": 0,
    "students": []
  },
  {
    "capacity": 150,
    "id": 3,
    "name": "Escola de Les Corts",
    "student_count": 0,
    "students": []
  }
]
```

## Recuperar Escuela por ID

Obtiene los detalles de una escuela específica y su lista de alumnos.

* Método: GET

* URL: /schools/<id>

### Ejemplo cURL:

```Bash
curl -X GET http://localhost:5000/schools/1
```

#### Respuesta

```Bash
{
  "capacity": 2,
  "id": 1,
  "name": "Escola Gracia",
  "student_count": 1,
  "students": [
    {
      "first_name": "Jordi",
      "id": "ST-000001",
      "last_name": "Pujol",
      "school_id": 1
    }
  ]
}
```

## Búsqueda de Escuelas

Busca escuelas cuyo nombre contenga la cadena proporcionada.
Nota: La búsqueda es insensible a mayúsculas.

* Método: GET

* URL: /schools/search?query=<nombre>

### Ejemplo cURL:

```Bash
curl -X GET "http://localhost:5000/schools/search?query=corts"
```

#### Respuesta

```Bash
[
  {
    "capacity": 150,
    "id": 3,
    "name": "Escola de Les Corts",
    "student_count": 0
  }
]
```

## Eliminar Escuela

Borra un registro de escuela dado su ID.

* Método: DELETE

* URL: /schools/<id>

### Ejemplo cURL:

```Bash
curl -X DELETE http://localhost:5000/schools/1
```

#### Respuesta

```Bash
{
    "message": "School deleted successfully"
}
```

# Gestión de Estudiantes

### Crear Estudiante

Registra un alumno y lo asocia a una escuela existente.

* Método: POST

* URL: /students

* Cuerpo (JSON):
```
    {
      "id": "ST-000001",
      "first_name": "Jordi",
      "last_name": "Pujol",
      "school_id": 1
    }

```
    Validación: Si la escuela está llena, devolverá un error 403.

### Ejemplo cURL:
```Bash
curl -X POST http://localhost:5000/students -H "Content-Type: application/json" -d '{"id": "ST-000006", "first_name": "Jordi", "last_name": "Pujol", "school_id": 1}'
```

#### Respuesta

```Bash
{
  "first_name": "Jordi",
  "id": "ST-000006",
  "last_name": "Pujol",
  "school_id": 2
}
```

## Obtener Estudiantes

Recupera todos los estudiantes si no se provee ID, o uno específico mediante /students/<id>.

* Método: GET

* URL: /students o /students/<id>

### Ejemplo cURL:
``` Bash
curl -X GET http://localhost:5000/students/ST-000006
```
#### Respuesta

```Bash
{
  "first_name": "Jordi",
  "id": "ST-000006",
  "last_name": "Pujol",
  "school_id": 2
}
```

## Búsqueda de Estudiantes

Busca alumnos que contengan el texto en su nombre o apellido.

* Método: GET

* URL: /students/search?query=<texto>

### Ejemplo cURL:
```Bash
curl -X GET "http://localhost:5000/students/search?query=jordi"
```

#### Respuesta

```Bash
[
  {
    "first_name": "Jordi",
    "id": "ST-000006",
    "last_name": "Pujol",
    "school_id": 2
  }
]
```
### Eliminar Estudiante

Elimina a un alumno del sistema mediante su DNI único.

* Método: DELETE

* URL: /students/<id>

### Ejemplo cURL:
```Bash
curl -X DELETE http://localhost:5000/students/ST-000006
```

#### Respuesta

```Bash
{
  "message": "Student deleted successfully"
}
```
