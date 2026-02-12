from django.test import TestCase

from contas.models import Pessoa, Usuario
from contas.services import CadastroService
from core.error import Erro

from .factories import ContaFactory


class CadastroServiceTestCase(TestCase):
    def setUp(self):
        self.empresa_user, self.empresa = ContaFactory.criar_empresa_com_usuario()
        self.gerente_user, self.gerente = ContaFactory.criar_pessoa_com_usuario(
            empresa=self.empresa,
            tipo_perfil=Pessoa.TipoPerfil.GERENTE,
            criado_por=self.empresa_user,
        )

    def _payload_valido(self, **overrides):
        payload = {
            "username": "novo_usuario",
            "email": "novo_usuario@solara.local",
            "password": "Senha@123456",
            "nome_completo": "joao da silva",
            "cpf": "123.456.789-00",
            "email_contato": "joao.contato@solara.local",
            "telefone": "(11) 91234-5678",
            "tipo_perfil": Pessoa.TipoPerfil.CONSUMIDOR,
        }
        payload.update(overrides)
        return payload

    def test_criar_com_empresa_normaliza_e_persiste_dados(self):
        data = self._payload_valido()

        resultado = CadastroService.criar(usuario_logado=self.empresa_user, data=data)

        self.assertIsInstance(resultado, Pessoa)
        self.assertEqual(resultado.empresa, self.empresa)
        self.assertEqual(resultado.criado_por, self.empresa_user)
        self.assertEqual(resultado.cpf, "12345678900")
        self.assertEqual(resultado.telefone, "11912345678")
        self.assertEqual(resultado.primeiro_nome, "Joao")
        self.assertEqual(resultado.ultimo_nome, "Silva")
        self.assertTrue(resultado.usuario.check_password("Senha@123456"))

    def test_criar_retorna_erro_quando_gerente_tenta_cadastrar_gerente(self):
        data = self._payload_valido(tipo_perfil=Pessoa.TipoPerfil.GERENTE)

        resultado = CadastroService.criar(usuario_logado=self.gerente_user, data=data)

        self.assertIsInstance(resultado, Erro)
        self.assertEqual(resultado.status_code, 403)

    def test_criar_retorna_erro_de_validacao_para_username_duplicado(self):
        ContaFactory.criar_usuario(username="ja_existe", email="existe@solara.local")
        data = self._payload_valido(username="ja_existe")

        resultado = CadastroService.criar(usuario_logado=self.empresa_user, data=data)

        self.assertIsInstance(resultado, Erro)
        self.assertEqual(resultado.status_code, 409)
        campos = {erro["field"] for erro in resultado.data["erros"]}
        self.assertIn("username", campos)
        self.assertEqual(Usuario.objects.filter(username="ja_existe").count(), 1)
