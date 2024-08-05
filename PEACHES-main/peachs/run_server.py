from core.scheduler import start as start_scheduler, cerrar_session
from django.core.management import execute_from_command_line
import threading
import os
from django.core.management import execute_from_command_line

# Configura la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "peachs.settings")

# Asegúrate de que la configuración de Django se haya cargado correctamente
import django
django.setup()

# Ahora puedes ejecutar el servidor Django
def run_server():
    execute_from_command_line(['manage.py', 'runserver'])

# Inicia el planificador en un hilo separado
scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

cerrar_session_thread = threading.Thread(target=cerrar_session)
cerrar_session_thread.daemon = True
cerrar_session_thread.start()

# Inicia el servidor Django
run_server()