from django.urls import path
from contas.views import *

app_name = "contas"

urlpatterns = [
    path("cadastro/", CadastroView.as_view(), name = "cadastro-usuarios"),
    # path("usuarios/", UsuarioDetalheView.as_view(), name = "usuarios"),
    # path("usuarios/<id>", UsuarioDetalheView.as_view(), name = "usuarios"),
    # path("usuarios/me/", UsuarioViewMe.as_view(), name = "usuarios-me"),
    path("usuarios/", UsuarioView.as_view(), name = "usuarios"),
    path("pessoas/", PessoaView.as_view(), name = "pessoas"),
    path("pessoas/<id>", PessoaPrivateView.as_view(), name = "pessoas"),
    

]
