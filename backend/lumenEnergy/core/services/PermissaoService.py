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
        "ANALISTA",
        "FINANCEIRO",
        "INVESTIDOR",
        "CLIENTE",
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
from contas.models import Pessoa, Empresa, Usuario
from core.exceptions import PermissaoNegadaException, UsuarioInativoException


class PermissaoService:
    """
    Serviço responsável por validar permissões de acesso
    respeitando a hierarquia de perfis.
    """

    HIERARQUIA = [
        "EMPRESA",
        "GERENTE",
        "ANALISTA",
        "FINANCEIRO",
        "INVESTIDOR",
        "CLIENTE",
    ]

    def __init__(self, user):
        if not user or not user.is_authenticated:
            raise PermissaoNegadaException("Usuário não autenticado")

        if user.tipo_status != Usuario.StatusUsuario.ATIVA:
            raise UsuarioInativoException("Usuário desativado")

        self.user = user

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _get_pessoa(self) -> Pessoa | None:
        try:
            return self.user.pessoa
        except Pessoa.DoesNotExist:
            return None

    def _get_empresa(self) -> Empresa | None:
        try:
            return self.user.empresa
        except Empresa.DoesNotExist:
            return None

    # ------------------------------------------------------------------
    # Perfil do usuário logado
    # ------------------------------------------------------------------

    def perfil_logado(self) -> str:
        """
        Retorna o perfil do usuário logado:
        - "EMPRESA" se for empresa ativa
        - TipoPerfil da Pessoa se for pessoa ativa
        """
        empresa = self._get_empresa()
        if empresa:
            return "EMPRESA"

        pessoa = self._get_pessoa()
        if pessoa:
            return pessoa.tipo_perfil

        raise UsuarioInativoException("Usuário sem perfil válido")

    # ------------------------------------------------------------------
    # Hierarquia
    # ------------------------------------------------------------------

    def _perfil_valido(self, perfil_logado: str, perfil_requerido: str) -> bool:
        """
        Verifica se o perfil logado possui permissão
        para o perfil requerido, respeitando hierarquia.
        """
        if perfil_logado == "EMPRESA":
            return True

        try:
            idx_logado = self.HIERARQUIA.index(perfil_logado)
            idx_requerido = self.HIERARQUIA.index(perfil_requerido)
        except ValueError:
            raise PermissaoNegadaException("Perfil inválido na hierarquia")

        return idx_logado <= idx_requerido

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def acesso(self, perfis: list[str]) -> bool:
        """
        Recebe uma lista de perfis permitidos.
        Libera se o usuário tiver qualquer um deles
        ou superior na hierarquia.
        """
        perfil = self.perfil_logado()

        for perfil_requerido in perfis:
            if self._perfil_valido(perfil, perfil_requerido):
                return True

        raise PermissaoNegadaException(
            f"Usuário '{self.user.username}' não possui permissão. "
            f"Perfis exigidos: {', '.join(perfis)}"
        )

        self._log_warning(erro)
        return erro

    # ------------------------------------------------------------------
    # Erro + Log
    # ------------------------------------------------------------------

    def _erro(self, *, mensagem, status_code, data=None):
        return Erro(
            **self.erro_base,
            mensagem=mensagem,
            status_code=status_code,
            data=data or {},
            tipo="PERMISSAO",
        )

    def _log_warning(self, erro: Erro):
        permission_logger.warning(
            erro.mensagem,
            extra={
                **self.erro_base,
                "status_code": erro.status_code,
                "data": erro.data,
            }
        )
