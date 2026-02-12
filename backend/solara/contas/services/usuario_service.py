from django.db import transaction
import logging
audit_logger = logging.getLogger("audit")

from contas.models import Usuario
from core.services import PermissaoService
from core.error import Erro

class UsuarioService:
    VISIBILIDADE = {
        "GERENTE": {
            "excluir_perfis": ["GERENTE"],
            "excluir_empresa": True,
        },
        "ANALISTA": {
            "excluir_perfis": ["GERENTE", "ANALISTA_ENERGETICO", "ANALISTA_FINANCEIRO"],
            "excluir_empresa": True,
        },
        "INVESTIDOR": {
            "ver": False,
        },
        "CONSUMIDOR": {
            "ver": False,
        },
    }

    @classmethod
    def _erro_base(cls, *, usuario_logado):
        return {
            "domain": "usuario",
            "entidade": "Usuario",
            "usuario": {
                "id": getattr(usuario_logado, "id", None),
                "username": getattr(usuario_logado, "username", None),
            },
        }
    

    @classmethod
    def listar(cls, *, usuario_logado):
        permissaoService = PermissaoService(usuario_logado)
        
        if not permissaoService.acesso(["EMPRESA","GERENTE"]):
            erro_base = cls._erro_base(usuario_logado = usuario_logado)

            return Erro(
                **erro_base,
                acao = "listar",
                mensagem = "Usuario sem permissao de acesso",
                status_code = 403
            )
        
        qs = Usuario.objects.filter(
        pessoa__empresa=usuario_logado.empresa_vinculada
    )

        # EMPRESA vê tudo
        if usuario_logado.tipo_usuario == Usuario.TipoUsuario.EMPRESA:
            return qs

        # Pessoa sem perfil válido não vê nada
        perfil = usuario_logado.pessoa.tipo_perfil
        regra = cls.VISIBILIDADE.get(perfil)

        if not regra or regra.get("ver") is False:
            return Usuario.objects.none()

        # Excluir empresas
        if regra.get("excluir_empresa"):
            qs = qs.exclude(tipo_usuario=Usuario.TipoUsuario.EMPRESA)

        # Excluir perfis de pessoas
        perfis_excluidos = regra.get("excluir_perfis", [])
        if perfis_excluidos:
            qs = qs.exclude(pessoa__tipo_perfil__in=perfis_excluidos)

        return qs

        
