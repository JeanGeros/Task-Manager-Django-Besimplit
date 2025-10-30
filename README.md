# Task Manager - Desafío Técnico Besimplit

Sistema de gestión de tareas desarrollado con Django, HTMX y Tailwind CSS que permite realizar operaciones CRUD sin recargar la página.

## Características Implementadas

### Core Features
- ✅ Ver lista de tareas
- ✅ Agregar nuevas tareas (título + descripción)
- ✅ Actualizar tareas existentes
- ✅ Marcar tareas como completadas/pendientes (toggle)
- ✅ Eliminar tareas
- ✅ API REST para consultar y crear tareas
- ✅ Interfaz moderna y responsive con Tailwind CSS
- ✅ Interacciones dinámicas sin recarga usando HTMX
- ✅ Modal para creación de tareas con HTMX 

### Bonus: Export de Reportes 📥
- ✅ Exportación de reportes en **CSV** y **Excel (.xlsx)**
- ✅ Mejoras en UI/UX

## Stack Tecnológico

- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Frontend**: HTMX 1.9.10 (CDN)
- **Estilos**: Tailwind CSS 3.x (CDN)
- **Base de datos**: SQLite

## Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Besimplit
```

2. **Crear y activar entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Crear datos de demostración (opcional)**
```bash
python manage.py create_demo_tasks
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
- Aplicación web: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/tasks/

## Estructura del Proyecto

```
besimplit/
├── config/                      # Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── task_manager/               # App principal
│   ├── api/                    # API REST
│   │   ├── serializers.py     # Serializers de DRF
│   │   ├── views.py           # ViewSets de la API
│   │   └── urls.py            # Rutas de la API
│   ├── management/
│   │   └── commands/
│   │       └── create_demo_tasks.py
│   ├── migrations/
│   ├── templates/
│   │   └── task_manager/
│   │       ├── base.html
│   │       ├── task_list.html
│   │       └── partials/
│   │           ├── task_item.html
│   │           └── task_form.html
│   ├── models.py              # Modelo Task
│   ├── views.py               # Vistas HTMX
│   ├── urls.py                # Rutas de la app
│   └── admin.py
├── manage.py
├── requirements.txt
└── README.md
```

## Decisiones Técnicas

### 1. Arquitectura de Templates con HTMX

**Decisión**: Utilizar un patrón de templates parciales (partials) para componentes reutilizables.

**Razón**:
- Permite actualizaciones granulares del DOM sin recargar la página completa
- Facilita el mantenimiento al separar la lógica de presentación
- HTMX puede intercambiar fragmentos HTML específicos manteniendo el estado de la aplicación

**Implementación**:
- `task_item.html`: Representa una tarea individual (lectura)
- `task_form.html`: Formulario de edición inline
- Las vistas retornan estos partials cuando son llamadas vía HTMX

### 2. API REST Separada

**Decisión**: Mantener endpoints de API REST completamente separados de las vistas HTMX.

**Razón**:
- Separación de responsabilidades (SoC)
- Permite consumir la API desde otras aplicaciones (móvil, servicios externos)
- Facilita testing y mantenimiento independiente
- Escalabilidad futura

**Trade-off**: Ligera duplicación de lógica entre vistas HTMX y API, pero ganamos en claridad y flexibilidad.

### 3. Uso de CDN para HTMX y Tailwind

**Decisión**: Utilizar CDN en lugar de build process local.

**Razón**:
- Setup más rápido para una prueba técnica
- Cero configuración adicional
- Suficiente para el alcance del proyecto

**Trade-off**: En producción consideraría:
- Tailwind con purging para reducir tamaño
- Bundle de HTMX local para control de versiones
- Pero para esta prueba, la velocidad de desarrollo es prioritaria

### 4. Modelo Simple pero Extensible

**Decisión**: Agregar campo `updated_at` además de los requeridos.

**Razón**:
- Buena práctica de auditoría
- Útil para features futuras (ordenar por última modificación)
- Costo mínimo en complejidad

### 5. Manejo de Estado con HTMX

**Decisión**: Usar atributos `hx-target` y `hx-swap` para controlar actualizaciones del DOM.

**Razón**:
- Permite feedback visual inmediato
- Mantiene el estado de otras tareas intacto
- Experiencia de usuario fluida

**Ejemplo**: Al editar una tarea, solo ese componente se reemplaza por el formulario, el resto permanece inalterado.

### 6. Modal con HTMX

**Decisión**: Implementar modal usando solo HTMX sin JavaScript adicional.

**Razón**:
- UX más limpia y profesional
- Interfaz menos saturada
- Mantiene la filosofía "cero JavaScript" del proyecto
- HTMX puede cargar y controlar el modal completamente

**Implementación**:
- Botón "Nueva Tarea" que carga el modal con `hx-get`
- Modal se inserta en `#modal-container` vacío
- Backdrop y botón X usan `hx-get` para vaciar el container (cerrar modal)
- Al crear tarea exitosamente, el formulario limpia el modal con `hx-on::after-request`
- Todo sin una sola línea de JavaScript custom

### 7. Exportación en CSV

**Decisión**: Usar CSV en lugar de Excel o PDF para reportes.

**Razón**:
- No requiere dependencias adicionales (usa librería csv nativa de Python)
- Universal: se abre en Excel, Google Sheets, LibreOffice
- Ligero y rápido de generar
- Fácil de parsear programáticamente si se necesita
- Cumple perfectamente con los requisitos del bonus

**Implementación**:
- Vista que genera HttpResponse con content_type CSV
- Estructura clara: Resumen ejecutivo + Detalle de tareas
- Timestamp en nombre de archivo para organización
- Encoding UTF-8 para caracteres especiales

## Endpoints de la API

### GET /api/tasks/
Lista todas las tareas

**Respuesta**:
```json
[
  {
    "id": 1,
    "title": "Título de la tarea",
    "description": "Descripción",
    "completed": false,
    "created_at": "2024-10-29T20:30:00Z",
    "updated_at": "2024-10-29T20:30:00Z"
  }
]
```

### POST /api/tasks/
Crea una nueva tarea

**Body**:
```json
{
  "title": "Nueva tarea",
  "description": "Descripción opcional",
  "completed": false
}
```

### GET /api/tasks/{id}/
Obtiene detalle de una tarea

### PUT /api/tasks/{id}/
Actualiza una tarea completa

### PATCH /api/tasks/{id}/
Actualiza parcialmente una tarea

### DELETE /api/tasks/{id}/
Elimina una tarea

## Características de la Interfaz

### Interacciones HTMX

1. **Crear Tarea**:
   - Formulario con `hx-post` que agrega la tarea al inicio de la lista
   - Se resetea automáticamente tras crear

2. **Editar Tarea**:
   - Click en ícono de lápiz carga formulario inline
   - Botón cancelar restaura vista original
   - Guardar actualiza solo ese elemento

3. **Toggle Completado**:
   - Click en checkbox alterna estado
   - Actualización visual inmediata (tachado, color)

4. **Eliminar Tarea**:
   - Confirmación antes de eliminar
   - Animación suave de salida (1s)

5. **Exportar Reporte**:
   - Botón verde "Exportar" en la parte superior
   - Genera archivo CSV con timestamp
   - Descarga automática

## Funcionalidad de Exportación de Reportes

### Formato del Reporte CSV

El reporte generado incluye:

#### Resumen Ejecutivo:
- Total de tareas creadas
- Número de tareas completadas
- Número de tareas pendientes
- Porcentaje de completitud

#### Detalle de Tareas:
Listado completo con:
- ID de la tarea
- Título
- Descripción
- Estado (Completada/Pendiente)
- Fecha de creación
- Fecha de última actualización

### Uso:

1. Click en el botón **"Exportar"** (verde, esquina superior derecha)
2. El archivo CSV se descarga automáticamente con nombre: `reporte_tareas_YYYYMMDD_HHMMSS.csv`
3. Abrir con Excel, Google Sheets o cualquier editor de CSV

### Ejemplo de salida:

```csv
REPORTE DE TAREAS - TASK MANAGER BESIMPLIT
Fecha de generación: 29/10/2024 20:45:00

RESUMEN EJECUTIVO
Métrica,Valor
Total de tareas creadas,8
Tareas completadas,3
Tareas pendientes,5
Porcentaje de completitud,37.5%

DETALLE DE TAREAS
ID,Título,Descripción,Estado,Fecha Creación,Última Actualización
1,Implementar autenticación,Sistema de login...,Completada,29/10/2024 20:28:00,29/10/2024 20:28:00
...
```

### Estilos con Tailwind

- **Responsive**: Funciona en móviles y desktop
- **Estados visuales**: Hover, focus, completed
- **Componentes**: Cards, forms, buttons consistentes
- **Colores**: Palette profesional (gray, blue, green, red)

## Testing

Para ejecutar tests (si se implementaran en el futuro):
```bash
python manage.py test task_manager
```

## Mejoras Futuras

Con más tiempo, implementaría:

1. **Testing**:
   - Tests unitarios del modelo Task
   - Tests de API endpoints
   - Tests funcionales de vistas HTMX

2. **Features**:
   - Filtros (completadas/pendientes/todas) con HTMX
   - Búsqueda en tiempo real
   - Ordenamiento (fecha, alfabético)
   - Paginación para listas largas

3. **UX/UI**:
   - Animaciones más suaves con Tailwind transitions
   - Loading states durante operaciones HTMX
   - Notificaciones toast para feedback
   - Dark mode

4. **Optimización**:
   - Tailwind con purging para producción
   - Compresión de assets
   - Índices en base de datos para queries frecuentes

5. **DevOps**:
   - Docker para desarrollo consistente
   - CI/CD pipeline
   - Variables de entorno para configuración

## Contacto

Desarrollado por Jean para Besimplit

---

Gracias por revisar este proyecto!
