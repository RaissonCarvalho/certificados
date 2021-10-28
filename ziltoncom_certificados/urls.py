"""ziltoncom_certificados URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core.views import EditarCertificadoView
from core import views as core_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', core_views.listar_certificados, name='listar_certificados'),
    path('admin/', admin.site.urls),
    path('certificados/', core_views.listar_certificados, name='listar_certificados'),
    path('certificados_vencidos/', core_views.listar_vencidos, name='listar_vencidos'),
    path('certificados_a_vencer/', core_views.listar_a_vencer, name='listar_a_vencer'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('cadastrar_usuario/', core_views.cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar_certficado/', core_views.cadastrar_certificado, name='cadastrar_certificado'),
    path('certificados/delete/<int:cod_cert>/', core_views.excluir_certificado, name='excluir_certificado'),
    path('certificados/editar/<int:pk>/', login_required(EditarCertificadoView.as_view()), name='editar_certificado'),
]
