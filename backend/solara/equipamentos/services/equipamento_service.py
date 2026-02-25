import logging
from django.db import transaction
audit_logger = logging.getLogger("audit")

from equipamentos.models import Equipamento

from core.error import Erro
from core.services import PermissaoService

class EquipamentoService:

    @classmethod
    def _erro_base(cls, *, usuario_logado):
        return {
            "domain": "equipamento",
            "entidade": "Equipamento",
            "usuario": {
                "id": getattr(usuario_logado, "id", None),
                "username": getattr(usuario_logado, "username", None),
            },
        }

    @classmethod
    @transaction.atomic
    def criar(cls, *, usuario_logado, data):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        permissaoService = PermissaoService(usuario_logado)

        if not permissaoService.acesso_permissoes(["equipamentos.add_equipamento"]):
            return Erro(
                **erro_base,
                acao = "criar",
                mensagem = "Usuario sem permissao cadastro",
                status_code = 403
            )

        fabricante = cls._normalizar_fabricante(data["fabricante"])
        potencia = data["potencia"]
        tensao = data["tensao"]
        tipo_equipamento = data["tipo_equipamento"]

        existente = Equipamento.objects.filter(
            fabricante = fabricante,
            potencia = potencia,
            tensao = tensao
        ).first()

        if existente:
            return Erro(
                **erro_base,
                acao = "criar",
                mensagem = "Equipamento já cadastrado",
                status_code = 409,
                data = {
                    "id": existente.id,
                    "descricao": str(existente)
                }
            )


        novo_equipamento = Equipamento(
            fabricante = fabricante,
            tipo_equipamento = tipo_equipamento,
            potencia = potencia,
            tensao = tensao,
        )

        novo_equipamento.save()

        audit_logger.info(
            "Pessoa criada",
            extra = {
                "domain": "equipamento",
                "entidade": "Equipamento",
                "acao": "criar",
                "pessoa_id": novo_equipamento.id,
                "usuario": usuario_logado.id,
                "empresa": usuario_logado.empresa_vinculada,
            }
        )
        return novo_equipamento

    @classmethod
    def listar(cls, usuario_logado, filtros = None):
        filtros = filtros or {}

        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        permissaoService = PermissaoService(usuario_logado)

        if not permissaoService.acesso_permissoes(["equipamentos.view_equipamento"]):
            return Erro (
                **erro_base,
                acao = "listar",
                mensagem = "Usuário sem permissão para acessar os equipamentos"
            )


        fabricante = filtros.get("fabricante")
        tipo = filtros.get("tipo_equipamento")
        potencia_min = filtros.get("potencia_min")
        potencia_max = filtros.get("potencia_max")
        tensao = filtros.get("tensao")
        qs = Equipamento.objects.all()
        if fabricante:
            qs = qs.filter(fabricante__icontains = fabricante)

        if tipo:
            qs = qs.filter(tipo_equipamento = tipo)

        if potencia_min:
            qs = qs.filter(potencia__gte = potencia_min)

        if potencia_max:
            qs = qs.filter(potencia__lte = potencia_max)

        if tensao:
            qs = qs.filter(tensao = tensao)

        return qs.order_by("tipo_equipamento", "fabricante", "potencia")



    @staticmethod
    def _normalizar_fabricante(fabricante):
        return fabricante.upper()
