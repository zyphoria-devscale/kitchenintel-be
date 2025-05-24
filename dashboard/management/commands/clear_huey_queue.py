from django.core.management.base import BaseCommand
from huey.contrib.djhuey import HUEY


class Command(BaseCommand):
    help = 'Clears all tasks from the Huey task queue'

    def add_arguments(self, parser):
        parser.add_argument(
            '--task',
            type=str,
            help='Specific task name to clear (e.g., dashboard.task.daily). If not provided, all tasks will be cleared.',
            required=False
        )

    def handle(self, *args, **options):
        task_name = options.get('task')
        
        if task_name:
            # Clear specific task queue
            self.stdout.write(self.style.WARNING(f'Clearing task queue for: {task_name}'))
            count = HUEY.flush_queue(task_name)
            self.stdout.write(self.style.SUCCESS(f'Cleared {count} tasks from {task_name} queue'))
        else:
            # Clear all queues
            self.stdout.write(self.style.WARNING('Clearing all Huey task queues...'))
            HUEY.flush()
            self.stdout.write(self.style.SUCCESS('All Huey task queues have been cleared successfully'))
