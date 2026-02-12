from django.test import TestCase

from contas.models import Pessoa
from contas.services import PessoaService
from core.error import Erro

from .factories import ContaFactory


class PessoaServiceTestCase(TestCase):
    def setUp(self):
        self.empresa_user, self.empresa = ContaFactory.criar_empresa_com_usuario()
        self.gerente_user, self.gerente = ContaFactory.criar_pessoa_com_usuario(
            empresa=self.empresa,
            tipo_perfil=Pessoa.TipoPerfil.GERENTE,
            criado_por=self.empresa_user,
            password="SenhaGerente@123",
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
        _, self.analista_outra_empresa = ContaFactory.criar_pessoa_com_usuario(
            empresa=empresa_b,
            tipo_perfil=Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
        )

    def test_listar_para_gerente_retorna_somente_hierarquia_da_empresa(self):
        resultado = PessoaService.listar(usuario_logado=self.gerente_user)

        self.assertFalse(isinstance(resultado, Erro))
        ids = set(resultado.values_list("id", flat=True))
        self.assertIn(self.analista.id, ids)
        self.assertIn(self.investidor.id, ids)
        self.assertNotIn(self.gerente.id, ids)
        self.assertNotIn(self.outro_gerente.id, ids)
        self.assertNotIn(self.analista_outra_empresa.id, ids)

    def test_buscar_por_id_retorna_erro_para_perfil_nao_visualizavel(self):
        resultado = PessoaService.buscar_por_id(
            usuario_logado=self.gerente_user,
            id=self.outro_gerente.id,
        )

        self.assertIsInstance(resultado, Erro)
        self.assertEqual(resultado.status_code, 403)

    def test_atualizar_altera_tipo_perfil_quando_senha_valida(self):
        dados = {
            "password": "SenhaGerente@123",
            "tipo_perfil": Pessoa.TipoPerfil.CONSUMIDOR,
        }

        resultado = PessoaService.atualizar(
            data=dados,
            id=self.investidor.id,
            usuario_logado=self.gerente_user,
        )

        self.assertFalse(isinstance(resultado, Erro))
        self.investidor.refresh_from_db()
        self.assertEqual(self.investidor.tipo_perfil, Pessoa.TipoPerfil.CONSUMIDOR)
