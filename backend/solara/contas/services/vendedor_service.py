import re
import logging

from django.db import transaction

from contas.models import Vendedor
from core.services import PermissaoService
from core.error import Erro


audit_logger = logging.getLogger("audit")


class VendedorService:

    @classmethod
    def _erro_base(cls, *, usuario_logado):
        return {
            "domain": "vendedor",
            "entidade": "Vendedor",
            "usuario": {
                "id": getattr(usuario_logado, "id", None),
                "username": getattr(usuario_logado, "username", None),
            },
        }

    @classmethod
    def _normalizar_cpf(cls, cpf):
        return re.sub(r"\D", "", cpf or "")

    @classmethod
    def _normalizar_telefone(cls, telefone):
        return re.sub(r"\D", "", telefone or "")

    @classmethod
    def _validar_permissao(cls, *, usuario_logado, acao, erro_base):
        permissao = PermissaoService(usuario_logado)

        if not permissao.acesso(["EMPRESA", "GERENTE"]):
            return Erro(
                **erro_base,
                acao = acao,
                mensagem = "Usuário sem permissão para gerenciar vendedores",
                status_code = 403,
            )

        return None

    @classmethod
    def _buscar_vendedor(cls, *, id, usuario_logado, acao, erro_base):
        vendedor = (
            Vendedor.objects
            .select_related("empresa", "criado_por")
            .filter(id = id)
            .first()
        )

        if not vendedor or vendedor.empresa != usuario_logado.empresa_vinculada:
            return Erro(
                **erro_base,
                acao = acao,
                mensagem = "Vendedor não encontrado",
                status_code = 404,
            )

        return vendedor

    @classmethod
    @transaction.atomic
    def criar(cls, *, usuario_logado, data):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        erro_permissao = cls._validar_permissao(
            usuario_logado = usuario_logado,
            acao = "criar",
            erro_base = erro_base,
        )

        if erro_permissao:
            return erro_permissao

        data["cpf"] = cls._normalizar_cpf(data.get("cpf"))
        data["telefone"] = cls._normalizar_telefone(data.get("telefone"))

        empresa = usuario_logado.empresa_vinculada

        if Vendedor.objects.filter(empresa = empresa, cpf = data["cpf"]).exists():
            return Erro(
                **erro_base,
                acao = "criar",
                mensagem = "CPF já cadastrado para vendedor nesta empresa",
                field = "cpf",
                data = {"cpf": data["cpf"]},
                status_code = 409,
            )

        vendedor = Vendedor.objects.create(
            nome_completo = data["nome_completo"],
            cpf = data["cpf"],
            email_contato = data.get("email_contato") or None,
            telefone = data["telefone"],
            percentual_comissao = data["percentual_comissao"],
            tipo_comissao = data["tipo_comissao"],
            inicio_vigencia = data["inicio_vigencia"],
            fim_vigencia = data.get("fim_vigencia"),
            tipo_status = data.get("tipo_status", Vendedor.TipoStatus.ATIVO),
            empresa = empresa,
            criado_por = usuario_logado,
        )

        audit_logger.info(
            "Vendedor criado",
            extra={
                "domain": "vendedor",
                "entidade": "Vendedor",
                "acao": "criar",
                "vendedor_id": vendedor.id,
                "usuario": usuario_logado.id,
                "empresa": empresa.id,
            }
        )

        return vendedor

    @classmethod
    def listar(cls, *, usuario_logado, filtros=None):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        erro_permissao = cls._validar_permissao(
            usuario_logado = usuario_logado,
            acao = "listar",
            erro_base = erro_base,
        )

        if erro_permissao:
            return erro_permissao

        filtros = filtros or {}

        qs = (
            Vendedor.objects
            .select_related("empresa", "criado_por")
            .filter(empresa = usuario_logado.empresa_vinculada)
            .order_by("nome_completo")
        )

        nome = filtros.get("nome")
        status = filtros.get("status")
        data_inicio = filtros.get("data_inicio")
        data_fim = filtros.get("data_fim")

        if nome:
            qs = qs.filter(nome_completo__icontains = nome)

        if status:
            qs = qs.filter(tipo_status = status)

        if data_inicio:
            qs = qs.filter(data_criacao__date__gte = data_inicio)

        if data_fim:
            qs = qs.filter(data_criacao__date__lte = data_fim)

        return qs

    @classmethod
    @transaction.atomic
    def atualizar(cls, *, usuario_logado, id, data):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        erro_permissao = cls._validar_permissao(
            usuario_logado = usuario_logado,
            acao = "atualizar",
            erro_base = erro_base,
        )

        if erro_permissao:
            return erro_permissao

        vendedor = cls._buscar_vendedor(
            id = id,
            usuario_logado = usuario_logado,
            acao = "atualizar",
            erro_base = erro_base,
        )

        if isinstance(vendedor, Erro):
            return vendedor

        if "cpf" in data:
            data["cpf"] = cls._normalizar_cpf(data["cpf"])

        if "telefone" in data:
            data["telefone"] = cls._normalizar_telefone(data["telefone"])

        if "cpf" in data:
            cpf_duplicado = Vendedor.objects.filter(
                empresa = usuario_logado.empresa_vinculada,
                cpf = data["cpf"],
            ).exclude(id = vendedor.id).exists()

            if cpf_duplicado:
                return Erro(
                    **erro_base,
                    acao = "atualizar",
                    mensagem = "CPF já cadastrado para vendedor nesta empresa",
                    field = "cpf",
                    data = {"cpf": data["cpf"]},
                    status_code = 409,
                )

        for campo, valor in data.items():
            setattr(vendedor, campo, valor)

        vendedor.save()

        audit_logger.info(
            "Vendedor atualizado",
            extra={
                "domain": "vendedor",
                "entidade": "Vendedor",
                "acao": "atualizar",
                "vendedor_id": vendedor.id,
                "usuario": usuario_logado.id,
                "empresa": usuario_logado.empresa_vinculada.id,
            }
        )

        return vendedor

    @classmethod
    @transaction.atomic
    def remover(cls, *, usuario_logado, id):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        erro_permissao = cls._validar_permissao(
            usuario_logado = usuario_logado,
            acao = "remover",
            erro_base = erro_base,
        )

        if erro_permissao:
            return erro_permissao

        vendedor = cls._buscar_vendedor(
            id = id,
            usuario_logado = usuario_logado,
            acao = "remover",
            erro_base = erro_base,
        )

        if isinstance(vendedor, Erro):
            return vendedor

        if vendedor.contrato_ativo or vendedor.comissionamento_pendente:
            return Erro(
                **erro_base,
                acao = "remover",
                mensagem = "Não é permitido remover vendedor com contrato ativo ou comissionamento pendente",
                status_code = 409,
            )

        vendedor_id = vendedor.id
        empresa_id = vendedor.empresa.id

        vendedor.delete()

        audit_logger.info(
            "Vendedor removido",
            extra={
                "domain": "vendedor",
                "entidade": "Vendedor",
                "acao": "remover",
                "vendedor_id": vendedor_id,
                "usuario": usuario_logado.id,
                "empresa": empresa_id,
            }
        )

        return None
