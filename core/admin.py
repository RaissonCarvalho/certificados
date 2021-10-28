from django.contrib import admin
from core.models import Certificados
# Register your models here.
@admin.register(Certificados)
class CertificadosAdmin(admin.ModelAdmin):
    pass