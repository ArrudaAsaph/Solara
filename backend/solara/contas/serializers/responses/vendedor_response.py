from rest_framework import serializers

from contas.models import Vendedor
from .usuario_reponse import UsuarioSimpleResponse


class VendedorSimpleResponse(serializers.ModelSerializer):

    class Meta:
        model = Vendedor
        fields = [
            "id",
            "nome_completo",
            "cpf",
            "tipo_status",
            "data_criacao",
        ]


class VendedorResponse(serializers.ModelSerializer):
    criado_por = UsuarioSimpleResponse(read_only = True)

    class Meta:
        model = Vendedor
        fields = [
            "id",
            "nome_completo",
            "cpf",
            "email_contato",
            "telefone",
            "percentual_comissao",
            "tipo_comissao",
            "inicio_vigencia",
            "fim_vigencia",
            "tipo_status",
            "contrato_ativo",
            "comissionamento_pendente",
            "criado_por",
            "data_criacao",
            "data_atualizacao",
        ]
