# Pedrera-API

Esta API REST ha sido diseñada para gestionar la administración de centros educativos y sus estudiantes en Barcelona. El sistema permite controlar la capacidad máxima de las escuelas y realizar búsquedas eficientes de información. 

Puedes encontrar la documentation para las APIs en [este documento](API_README.md)

## Requisitos Previos

* **Docker** y **Docker Compose**
* **Python 3.9+**.
* Sistema operativo basado en Unix para el script de instalación.

## Instalación y Ejecución

### Opción A: Script de Instalación Automatizada

Para configurar el entorno virtual e instalar todas las dependencias de forma automática:

1.  Otorgue permisos de ejecución al script:
    ```bash
    chmod +x install.sh
    ```
2.  Ejecute el script:
    ```bash
    ./install.sh
    ```

### Opción B: Uso de Docker

Si prefiere ejecutar la aplicación en un contenedor:

1.  Inicie los servicios:
    ```bash
    docker compose up --build
    ```
2.  La API estará disponible en `http://localhost:5000`.

## Características de la API

* **Escuelas**: Creación, eliminación y consulta detallada con estudiantes.
* **Estudiantes**: Registro de alumnos con validación de capacidad, eliminación y consultas por ID.
* **Búsqueda Avanzada**: 
    * Búsqueda de escuelas por nombre.
    * Búsqueda de alumnos por nombre o apellido.
    * **Nota**: Todas las funciones de búsqueda son **insensibles a mayúsculas y minúsculas** (*case-insensitive*) y permiten coincidencias parciales.

## Notas Técnicas y Suposiciones

* **Capacidad Máxima**: No se permite la inscripción de un alumno si la escuela ha alcanzado su límite establecido.
* **Identificadores**: Cada estudiante debe poseer un ID único al ser creado correspondiente a su DNI.
* **Pruebas**: Se incluyen pruebas unitarias para verificar la integridad de los endpoints.
