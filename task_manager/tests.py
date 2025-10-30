from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class PruebasModeloTarea(TestCase):
    """Pruebas para el modelo Task"""

    def test_crear_tarea(self):
        """Prueba la creación de una tarea con título y descripción"""
        tarea = Task.objects.create(
            title="Tarea de Prueba",
            description="Esta es una tarea de prueba"
        )
        self.assertEqual(tarea.title, "Tarea de Prueba")
        self.assertEqual(tarea.description, "Esta es una tarea de prueba")
        self.assertFalse(tarea.completed)

    def test_representacion_string_tarea(self):
        """Prueba la representación en string de una tarea"""
        tarea = Task.objects.create(title="Mi Tarea")
        self.assertEqual(str(tarea), "Mi Tarea")

    def test_estado_completado_por_defecto(self):
        """Prueba que las tareas se crean con completed=False por defecto"""
        tarea = Task.objects.create(title="Tarea Nueva")
        self.assertFalse(tarea.completed)

    def test_ordenamiento_tareas(self):
        """Prueba que las tareas se ordenan por fecha de creación (más reciente primero)"""
        tarea1 = Task.objects.create(title="Primera Tarea")
        tarea2 = Task.objects.create(title="Segunda Tarea")
        tarea3 = Task.objects.create(title="Tercera Tarea")

        tareas = Task.objects.all()
        self.assertEqual(tareas[0], tarea3)  # Más reciente primero
        self.assertEqual(tareas[1], tarea2)
        self.assertEqual(tareas[2], tarea1)


class PruebasAPITarea(APITestCase):
    """Pruebas para los endpoints del API de tareas"""

    def setUp(self):
        """Crea tareas de ejemplo para las pruebas"""
        self.tarea1 = Task.objects.create(
            title="Tarea 1",
            description="Descripción 1"
        )
        self.tarea2 = Task.objects.create(
            title="Tarea 2",
            description="Descripción 2",
            completed=True
        )

    def test_obtener_todas_las_tareas(self):
        """Prueba obtener todas las tareas vía API"""
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_obtener_tarea_individual(self):
        """Prueba obtener una sola tarea vía API"""
        url = reverse('task-detail', args=[self.tarea1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Tarea 1")
        self.assertEqual(response.data['description'], "Descripción 1")

    def test_crear_tarea_via_api(self):
        """Prueba crear una nueva tarea vía API"""
        url = reverse('task-list')
        data = {
            'title': 'Nueva Tarea API',
            'description': 'Creada vía API'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Nueva Tarea API')

    def test_actualizar_tarea_via_api(self):
        """Prueba actualizar una tarea vía API"""
        url = reverse('task-detail', args=[self.tarea1.id])
        data = {
            'title': 'Tarea Actualizada',
            'description': 'Descripción actualizada',
            'completed': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tarea1.refresh_from_db()
        self.assertEqual(self.tarea1.title, 'Tarea Actualizada')
        self.assertTrue(self.tarea1.completed)

    def test_eliminar_tarea_via_api(self):
        """Prueba eliminar una tarea vía API"""
        url = reverse('task-detail', args=[self.tarea1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)


class PruebasVistasTarea(TestCase):
    """Pruebas para las vistas de tareas"""

    def setUp(self):
        """Crea una tarea de ejemplo para las pruebas"""
        self.tarea = Task.objects.create(
            title="Tarea de Prueba",
            description="Descripción de Prueba"
        )

    def test_vista_lista_tareas(self):
        """Prueba que la vista de lista de tareas carga correctamente"""
        response = self.client.get(reverse('task_manager:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarea de Prueba")

    def test_alternar_estado_tarea(self):
        """Prueba el cambio de estado de completado de una tarea"""
        self.assertFalse(self.tarea.completed)

        # Cambiar a completada
        response = self.client.post(reverse('task_manager:task_toggle', args=[self.tarea.id]))
        self.assertEqual(response.status_code, 200)
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completed)

        # Cambiar de vuelta a incompleta
        response = self.client.post(reverse('task_manager:task_toggle', args=[self.tarea.id]))
        self.assertEqual(response.status_code, 200)
        self.tarea.refresh_from_db()
        self.assertFalse(self.tarea.completed)

    def test_eliminar_tarea(self):
        """Prueba la eliminación de una tarea"""
        response = self.client.delete(reverse('task_manager:task_delete', args=[self.tarea.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)
