from django import forms
from core.models import Certificados
from django.contrib.auth.models import User
from datetime import date
import datetime
import calendar
from django.forms.utils import ErrorList


class CertificadoForm(forms.ModelForm):
    # empresa = forms.CharField(required=True, label='Empresa/Pessoa:')
    # cnpj = forms.CharField(required=True, label='CNPJ:')
    # responsavel = forms.CharField(required=False, label='Responsável:')
    # fone = forms.CharField(required=False)
    # tipo = forms.ChoiceField(choices=Certificados.tipos, label='Selecione um tipo', required=True)
    # datacompra = forms.DateField(required=True)
    # datavencimento = forms.DateField(required=True)

    class Meta:
        model = Certificados
        fields = [
            'empresa',
            'cnpj',
            'responsavel',
            'fone',
            'tipo',
            'datacompra',
            'datavencimento']

    def is_valid(self):
        valid = True
        if not super(CertificadoForm, self).is_valid():
            valid = False
        empresa_exists = Certificados.objects.filter(empresa=self.cleaned_data['empresa']).exists()
        if empresa_exists:
            self.adiciona_erro('Já existe certificado cadastrado para essa empresa!')
            valid = False

        cnpj_exists = Certificados.objects.filter(cnpj=self.cleaned_data['cnpj']).exists()
        if cnpj_exists:
            self.adiciona_erro('Já existe certificado cadastrado para esse CNPJ')
            valid = False

        if self.cleaned_data['datacompra'] >= self.cleaned_data['datavencimento']:
            self.adiciona_erro('Data de vencimento não pode ser inferior a data de compra')
            valid = False

        return valid

    def __init__(self, *args, **kwargs):
        super(CertificadoForm, self).__init__(*args, **kwargs)

        self.fields['tipo'] = forms.ChoiceField(choices=Certificados.tipos, label='Selecione um tipo', required=True)
        self.fields['cnpj'] = forms.CharField(required=True, label='CPF ou CNPJ')

        today = date.today()
        self.fields['datacompra'].initial = today

        one_year_delta = datetime.timedelta(days=366 if ((today.month >= 3 and calendar.isleap(today.year + 1)) or
                                                         (today.month < 3 and calendar.isleap(today.year))) else 365)
        self.fields['datavencimento'].initial = today + one_year_delta

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)


class UsuarioForm(forms.Form):
    nome = forms.CharField(max_length=40, required=True, label='Nome:')
    usuario = forms.CharField(required=True, label='Nome de Usuário:')
    email = forms.EmailField(label='E-mail:', required=False)
    senha = forms.CharField(required=True, widget=forms.PasswordInput(), label='Senha:')

    def is_valid(self):
        valid = True
        if not super(UsuarioForm, self).is_valid():
            valid = False
        user_name_exists = User.objects.filter(username=self.cleaned_data['usuario']).exists()
        if user_name_exists:
            self.adiciona_erro('Já existe cadastro para esse nome de Usuário')
            valid = False
        email_exists = User.objects.filter(email=self.cleaned_data['email']).exists()
        if user_name_exists:
            self.adiciona_erro('Já existe usuário cadastrado com esse E-mail')
            valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)
