from contas.models import Pessoa, Empresa, Usuario
from core.error import Erro
import logging

permission_logger = logging.getLogger("core.permission")


class PermissaoService:
    """
    Serviço responsável por validar permissões de acesso
    respeitando a hierarquia de perfis.
    """

    HIERARQUIA = [
        "EMPRESA",
        "GERENTE",
        "ANALISTA_FINANCEIRO",
        "ANALISTA_ENERGETICO",
        "INVESTIDOR",
        "CONSUMIDOR",
    ]

    def __init__(self, user):
        self.user = user

        self.erro_base = {
            "domain": "permissao",
            "entidade": "Usuario",
            "acao": "verificar_acesso",
            "usuario": {
                "id": getattr(user, "id", None),
                "username": getattr(user, "username", None),
            },
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_pessoa(self) -> Pessoa | None:
        return getattr(self.user, "pessoa", None)

    def _get_empresa(self) -> Empresa | None:
        return getattr(self.user, "empresa", None)

    # ------------------------------------------------------------------
    # Validações iniciais
    # ------------------------------------------------------------------

    def _validar_usuario(self):
        if not self.user or not self.user.is_authenticated:
            return self._erro(
                mensagem="Usuário não autenticado",
                status_code=401,
            )

        if self.user.tipo_status != Usuario.StatusUsuario.ATIVA:
            return self._erro(
                mensagem="Usuário desativado",
                status_code=403,
            )

        return None

    # ------------------------------------------------------------------
    # Perfil
    # ------------------------------------------------------------------

    def perfil_logado(self):
        empresa = self._get_empresa()
        if empresa:
            return "EMPRESA"

        pessoa = self._get_pessoa()
        if pessoa:
            return pessoa.tipo_perfil

        return None

    # ------------------------------------------------------------------
    # Hierarquia
    # ------------------------------------------------------------------

    def _perfil_valido(self, perfil_logado: str, perfil_requerido: str) -> bool:
        if perfil_logado == "EMPRESA":
            return True

        try:
            idx_logado = self.HIERARQUIA.index(perfil_logado)
            idx_requerido = self.HIERARQUIA.index(perfil_requerido)
        except ValueError:
            return False

        return idx_logado <= idx_requerido

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def acesso(self, perfis: list[str]):
        # 1️⃣ valida usuário
        erro = self._validar_usuario()
        if erro:
            self._log_warning(erro)
            return erro

        perfil = self.perfil_logado()

        if not perfil:
            erro = self._erro(
                mensagem="Usuário sem perfil válido",
                status_code=403,
            )
            self._log_warning(erro)
            return erro

        # 2️⃣ valida permissão
        for perfil_requerido in perfis:
            if self._perfil_valido(perfil, perfil_requerido):
                return True

        erro = self._erro(
            mensagem="Usuário não possui permissão para executar esta ação",
            status_code=403,
            data={
                "perfil_logado": perfil,
                "perfis_permitidos": perfis,
            },
        )

    def pode_ver(self, *, pessoa_alvo: Pessoa) -> bool:
        if self._validar_usuario():
            return False

        perfil_logado = self.perfil_logado()
        if not perfil_logado:
            return False

        if perfil_logado == "EMPRESA":
            return pessoa_alvo.usuario.tipo_usuario != Usuario.TipoUsuario.EMPRESA

        if perfil_logado == Pessoa.TipoPerfil.GERENTE:
            return (
                pessoa_alvo.usuario.tipo_usuario != Usuario.TipoUsuario.EMPRESA
                and pessoa_alvo.tipo_perfil != Pessoa.TipoPerfil.GERENTE
            )

        if perfil_logado in {
            Pessoa.TipoPerfil.ANALISTA_FINANCEIRO,
            Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
        }:
            return pessoa_alvo.tipo_perfil in {
                Pessoa.TipoPerfil.CONSUMIDOR,
                Pessoa.TipoPerfil.INVESTIDOR,
            }

        return False
    
    def hierarquia(self):
        perfil_logado = self.perfil_logado()

        if perfil_logado == "EMPRESA":
            return [
                Pessoa.TipoPerfil.GERENTE,
                Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
                Pessoa.TipoPerfil.ANALISTA_FINANCEIRO,
                Pessoa.TipoPerfil.INVESTIDOR,
                Pessoa.TipoPerfil.CONSUMIDOR
            ]
        
        if perfil_logado == Pessoa.TipoPerfil.GERENTE:
            return [
                Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
                Pessoa.TipoPerfil.ANALISTA_FINANCEIRO,
                Pessoa.TipoPerfil.INVESTIDOR,
                Pessoa.TipoPerfil.CONSUMIDOR
            ]
        
        if perfil_logado in (
                Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
                Pessoa.TipoPerfil.ANALISTA_FINANCEIRO,
            ):
            return [
                Pessoa.TipoPerfil.INVESTIDOR,
                Pessoa.TipoPerfil.CONSUMIDOR
            ]
        
        return []
