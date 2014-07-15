from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    name = 'appointments.apps.common'
    verbose_name = 'Appointments'
    
    def ready(self):
        # Register my signals
        from .utils import availability_for_range_handler