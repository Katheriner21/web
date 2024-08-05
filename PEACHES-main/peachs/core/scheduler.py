from datetime import timedelta
from django.utils import timezone
import time
import schedule

def eliminar_historias_antiguas():
    from core.models import Historia
    print('ejecucion')
    hrs_24 = timezone.now() - timedelta(hours=24)
    historias_antiguas = Historia.objects.filter(fecha_creacion__lte=hrs_24)
    print(historias_antiguas)
    for historia in historias_antiguas:
        print('Fecha actual:', hrs_24)
        print('Fecha de la historia:', historia.fecha_creacion)
        historia.imagen.delete()
        historia.delete() 
        
def cerrar_session():
    print('ejec')
    from .views import cerrar_sesion
    schedule.every().second.do(cerrar_sesion)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
        
def start():
    schedule.every().minute.do(eliminar_historias_antiguas)
    while True:
        schedule.run_pending()
        time.sleep(1)