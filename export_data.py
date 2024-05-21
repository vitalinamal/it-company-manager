import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
application = get_wsgi_application()

with open('data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata',  "tasks", indent=4, stdout=f)
