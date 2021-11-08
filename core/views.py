from django.contrib.auth.decorators import login_required
from core.forms import CertificadoForm, UsuarioForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.shortcuts import redirect
from core.models import Certificados
from django.shortcuts import render
from django.db import transaction
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.http import FileResponse
import io
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle


def get_user(request):
    user = request.user

    return user


@login_required()
def listar_certificados(request):
    certificados = Certificados.objects.all().order_by('empresa')
    user = get_user(request)

    return render(request, 'index.html',
                  {'certificados': certificados, 'user': user})


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
    certificados = Certificados.objects.all().order_by('empresa')
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


@login_required()
@transaction.atomic()
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


def gerar_relatorio_pdf(request):
    pdf = io.BytesIO()

    doc = SimpleDocTemplate(pdf, pagesize=A4, title='Relatório de Certificados')

    certificados = Certificados.objects.all().order_by('empresa')

    story = []

    data = [['EMPRESA', 'CPF/CNPJ', 'DATA VENCIMENTO', 'DIAS EXP.']]

    for certificado in certificados:
        data.append([certificado.empresa,
                     certificado.cnpj,
                     certificado.datavencimento,
                     certificado.calcula_dias_vencimento(), ])

    t = Table(data)

    t.setStyle(TableStyle(
        [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('LEFTPADDING', (0, 0), (-1, 0), 8),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, '#000000'),
            ('BOX', (0, 0), (-1, -1), 0.25, '#000000'),
        ]
    ))

    story.append(t)

    doc.build(story)
    pdf.seek(0)

    return FileResponse(pdf, as_attachment=True, filename='relatorio.pdf')
