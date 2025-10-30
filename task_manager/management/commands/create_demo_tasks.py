from django.core.management.base import BaseCommand
from task_manager.models import Task


class Command(BaseCommand):
    help = 'Crea tareas de demostración para visualizar la solución'

    def handle(self, *args, **kwargs):
        Task.objects.all().delete()

        demo_tasks = [
            {
                'title': 'Implementar autenticación de usuarios',
                'description': 'Agregar sistema de login y registro con Django Auth',
                'completed': True
            },
            {
                'title': 'Diseñar interfaz de dashboard',
                'description': 'Crear mockups y prototipos usando Figma',
                'completed': True
            },
            {
                'title': 'Configurar CI/CD con GitHub Actions',
                'description': 'Automatizar tests y deployment al servidor de staging',
                'completed': False
            },
            {
                'title': 'Optimizar queries de base de datos',
                'description': 'Revisar N+1 queries y agregar indices necesarios',
                'completed': False
            },
            {
                'title': 'Escribir documentación de API',
                'description': 'Documentar endpoints usando Swagger/OpenAPI',
                'completed': False
            },
            {
                'title': 'Implementar sistema de notificaciones',
                'description': 'Notificaciones en tiempo real usando WebSockets',
                'completed': False
            },
            {
                'title': 'Refactorizar componentes React',
                'description': 'Separar lógica de negocio en custom hooks',
                'completed': True
            },
            {
                'title': 'Configurar monitoreo con Sentry',
                'description': 'Integrar Sentry para tracking de errores en producción',
                'completed': False
            },
        ]

        for task_data in demo_tasks:
            Task.objects.create(**task_data)

        self.stdout.write(
            self.style.SUCCESS(f'✓ Se crearon {len(demo_tasks)} tareas de demostración')
        )
