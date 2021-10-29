from django.contrib.auth.decorators import login_required
from core.forms import CertificadoForm, UsuarioForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import redirect
from core.models import Certificados
from django.shortcuts import render
from django.db import transaction
import json


def get_user(request):
    user = request.user

    return user


@login_required()
def listar_certificados(request):
    certificados = Certificados.objects.all().order_by('empresa')
    certificados_json = json.dumps(list(Certificados.objects.values()), default=str)
    user = get_user(request)

    return render(request, 'index.html',
                  {'certificados': certificados, 'certificados_json': certificados_json, 'user': user})


@login_required()
@transaction.atomic()
def cadastrar_certificado(request):
    form = CertificadoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        dados_form = form.cleaned_data
        certificado = Certificados(
            empresa=dados_form['empresa'],
            cnpj=dados_form['cnpj'],
            datacompra=dados_form['datacompra'],
            datavencimento=dados_form['datavencimento'],
            responsavel=dados_form['responsavel'],
            tipo=dados_form['tipo'],
            fone=dados_form['fone'],
            funcionario=request.user.first_name + " " + request.user.last_name)
        certificado.save()
        return redirect('listar_certificados')

    return render(request, 'cadastrar_certificado.html', {'form': form})


@login_required()
def listar_vencidos(request):
    certificados = Certificados.objects.all()
    certificados_vencidos = []
    for certificado in certificados:
        if certificado.verifica_expirou():
            certificados_vencidos.append(certificado)

    return render(request, 'lista_vencidos.html', {'certificados_vencidos': certificados_vencidos})


@login_required()
def listar_a_vencer(request):
    certificados = Certificados.objects.all()
    certificados_a_vencer = []

    for certificado in certificados:
        if not certificado.verifica_expirou() and certificado.calcula_dias_vencimento() <= 15:
            certificados_a_vencer.append(certificado)

    return render(request, 'lista_a_vencer.html', {'certificados_a_vencer': certificados_a_vencer})


@login_required()
@transaction.atomic()
def excluir_certificado(request, cod_cert):
    certificado = Certificados.objects.get(cod_cert=cod_cert)
    certificado.delete()

    return redirect('listar_certificados')


class EditarCertificadoView(UpdateView):
    model = Certificados
    template_name = 'editar_certificado.html'
    form_class = CertificadoForm
    success_url = 'listar_certificado'

    # def get


def cadastrar_usuario(request):
    form = UsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        dados_form = form.cleaned_data
        User.objects.create_user(
            username=dados_form['usuario'],
            first_name=dados_form['nome'],
            email=dados_form['email'],
            password=dados_form['senha'])

        return redirect('listar_certificados')

    return render(request, 'cadastrar_usuario.html', {'form': form})
