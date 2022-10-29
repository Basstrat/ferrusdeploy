from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin
from .models import EstadoOrdentrabajo
from .models import EstadoVenta
from .models import Persona
from .models import Empleado
from .models import Puestoempleado


admin.site.register(EstadoOrdentrabajo)
admin.site.register(EstadoVenta)
admin.site.register(Persona)
admin.site.register(Empleado)
admin.site.register(Puestoempleado)