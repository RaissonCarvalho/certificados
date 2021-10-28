from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
# Create your models here.


class Certificados(models.Model):
    cod_cert = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    empresa = models.CharField(max_length=255, null=False)
    cnpj = models.CharField(max_length=255, null=False)
    datacompra = models.DateField(null = False)
    datavencimento = models.DateField(null= False)
    tipos = [("A1","A1"), ("A3","A3")]
    tipo = models.CharField(max_length=2, blank=True, choices=tipos)
    fone = models.CharField(max_length=15, blank=True)
    responsavel = models.CharField(max_length=255, blank=True)
    funcionario = models.CharField(max_length=40, blank=True)
    datacadastro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'certificados'

    def calcula_dias_vencimento(self):
        dias_vencimento = (self.datavencimento - date.today())

        return dias_vencimento.days

    def verifica_expirou(self):
        # Verifica se certificado expirou.
        # Comparadando a data de vencimento com o dia de hoje
        # Retorna True caso expirado e False caso ainda válido
        if self.datavencimento <= date.today():
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('listar_certificados')

    def __str__(self):
        return self.empresa


class Usuarios(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    nome = models.CharField(max_length=40)
    usuario = models.OneToOneField(User, related_name='usuario', on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=255)
    senha = models.CharField(max_length=40)
    datacadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
