from datetime import date

from django.test import TestCase

from contas.models import Pessoa, Vendedor
from contas.services import VendedorService
from core.error import Erro

from .factories import ContaFactory


class VendedorServiceTestCase(TestCase):
    def setUp(self):
        self.empresa_user, self.empresa = ContaFactory.criar_empresa_com_usuario()
        self.gerente_user, self.gerente = ContaFactory.criar_pessoa_com_usuario(
            empresa = self.empresa,
            tipo_perfil = Pessoa.TipoPerfil.GERENTE,
            criado_por = self.empresa_user,
        )
        self.investidor_user, self.investidor = ContaFactory.criar_pessoa_com_usuario(
            empresa = self.empresa,
            tipo_perfil = Pessoa.TipoPerfil.INVESTIDOR,
            criado_por = self.gerente_user,
        )

    def _payload(self, **overrides):
        data = {
            "nome_completo": "Vendedor Teste",
            "cpf": "123.456.789-00",
            "email_contato": "vendedor@solara.local",
            "telefone": "(11) 98888-7777",
            "percentual_comissao": "7.50",
            "tipo_comissao": Vendedor.TipoComissao.PERCENTUAL,
            "inicio_vigencia": date(2026, 1, 1),
            "fim_vigencia": date(2026, 12, 31),
            "tipo_status": Vendedor.TipoStatus.ATIVO,
        }
        data.update(overrides)
        return data

    def test_criar_vendedor_com_empresa(self):
        resultado = VendedorService.criar(
            usuario_logado = self.empresa_user,
            data = self._payload(),
        )

        self.assertFalse(isinstance(resultado, Erro))
        self.assertEqual(resultado.empresa, self.empresa)
        self.assertEqual(resultado.cpf, "12345678900")

    def test_criar_vendedor_sem_permissao(self):
        resultado = VendedorService.criar(
            usuario_logado = self.investidor_user,
            data = self._payload(),
        )

        self.assertIsInstance(resultado, Erro)
        self.assertEqual(resultado.status_code, 403)

    def test_listar_vendedores_filtrando_por_nome(self):
        VendedorService.criar(usuario_logado = self.empresa_user, data = self._payload(nome_completo = "Ana Maria", cpf = "123.456.789-11"))
        VendedorService.criar(usuario_logado = self.empresa_user, data = self._payload(nome_completo = "Bruno Lima", cpf = "123.456.789-12"))

        resultado = VendedorService.listar(
            usuario_logado = self.gerente_user,
            filtros = {"nome": "ana"},
        )

        self.assertFalse(isinstance(resultado, Erro))
        self.assertEqual(resultado.count(), 1)
        self.assertEqual(resultado.first().nome_completo, "Ana Maria")

    def test_atualizar_vendedor(self):
        vendedor = VendedorService.criar(
            usuario_logado = self.empresa_user,
            data = self._payload(),
        )

        resultado = VendedorService.atualizar(
            usuario_logado = self.gerente_user,
            id = vendedor.id,
            data = {"telefone": "(11) 99999-0000"},
        )

        self.assertFalse(isinstance(resultado, Erro))
        vendedor.refresh_from_db()
        self.assertEqual(vendedor.telefone, "11999990000")

    def test_remover_vendedor_com_pendencia(self):
        vendedor = VendedorService.criar(
            usuario_logado = self.empresa_user,
            data = self._payload(),
        )

        vendedor.comissionamento_pendente = True
        vendedor.save(update_fields = ["comissionamento_pendente"])

        resultado = VendedorService.remover(
            usuario_logado = self.gerente_user,
            id = vendedor.id,
        )

        self.assertIsInstance(resultado, Erro)
        self.assertEqual(resultado.status_code, 409)
        self.assertTrue(Vendedor.objects.filter(id = vendedor.id).exists())

    def test_remover_vendedor_com_sucesso(self):
        vendedor = VendedorService.criar(
            usuario_logado = self.empresa_user,
            data = self._payload(),
        )

        resultado = VendedorService.remover(
            usuario_logado = self.gerente_user,
            id = vendedor.id,
        )

        self.assertIsNone(resultado)
        self.assertFalse(Vendedor.objects.filter(id = vendedor.id).exists())
