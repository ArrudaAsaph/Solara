from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from contas.models import Usuario


class LoginService:

    @staticmethod
    def login(data):
        username = data["username"]
        password = data["password"]

        usuario = Usuario.objects.filter(
            Q(username=username) | Q(email=username)
        ).first()

        if not usuario or not usuario.check_password(password):
            raise AuthenticationFailed("Usuário ou senha inválidos")

        if usuario.tipo_status != Usuario.StatusUsuario.ATIVA:
            raise AuthenticationFailed("Usuário está bloqueado.")
            
        refresh = RefreshToken.for_user(usuario)
        

        retorno = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        if usuario.tipo_usuario ==  'PERFIL':
            retorno["pessoa"] = usuario.pessoa
        else:
            retorno["empresa"] = usuario.empresa

        
        return retorno