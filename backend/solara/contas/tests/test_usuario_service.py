from django.test import TestCase

from contas.models import Pessoa
from contas.services import UsuarioService
from core.error import Erro

from .factories import ContaFactory


class UsuarioServiceTestCase(TestCase):
    def setUp(self):
        self.empresa_user, self.empresa = ContaFactory.criar_empresa_com_usuario()
        self.gerente_user, self.gerente = ContaFactory.criar_pessoa_com_usuario(
            empresa=self.empresa,
            tipo_perfil=Pessoa.TipoPerfil.GERENTE,
            criado_por=self.empresa_user,
        )
        self.analista_user, self.analista = ContaFactory.criar_pessoa_com_usuario(
            empresa=self.empresa,
            tipo_perfil=Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
            criado_por=self.gerente_user,
        )
        self.investidor_user, self.investidor = ContaFactory.criar_pessoa_com_usuario(
            empresa=self.empresa,
            tipo_perfil=Pessoa.TipoPerfil.INVESTIDOR,
            criado_por=self.gerente_user,
        )
        self.outro_gerente_user, self.outro_gerente = ContaFactory.criar_pessoa_com_usuario(
            empresa=self.empresa,
            tipo_perfil=Pessoa.TipoPerfil.GERENTE,
            criado_por=self.empresa_user,
        )

        _, empresa_b = ContaFactory.criar_empresa_com_usuario()
        self.user_outra_empresa, self.pessoa_outra_empresa = ContaFactory.criar_pessoa_com_usuario(
            empresa=empresa_b,
            tipo_perfil=Pessoa.TipoPerfil.INVESTIDOR,
        )

    def test_listar_para_empresa_retorna_usuarios_de_pessoas_da_empresa(self):
        resultado = UsuarioService.listar(usuario_logado=self.empresa_user)

        self.assertFalse(isinstance(resultado, Erro))
        ids = set(resultado.values_list("id", flat=True))
        self.assertIn(self.gerente_user.id, ids)
        self.assertIn(self.analista_user.id, ids)
        self.assertIn(self.investidor_user.id, ids)
        self.assertNotIn(self.user_outra_empresa.id, ids)

    def test_listar_para_gerente_exclui_perfil_gerente(self):
        resultado = UsuarioService.listar(usuario_logado=self.gerente_user)

        self.assertFalse(isinstance(resultado, Erro))
        ids = set(resultado.values_list("id", flat=True))
        self.assertIn(self.analista_user.id, ids)
        self.assertIn(self.investidor_user.id, ids)
        self.assertNotIn(self.outro_gerente_user.id, ids)
