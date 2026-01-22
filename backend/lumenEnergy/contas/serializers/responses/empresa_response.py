from rest_framework import serializers
from contas.models import Empresa
from .usuario_reponse import UsuarioResponse

class EmpresaSimpleResponse(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'id',
            'nome_fantasia',
            'cnpj',
        ]

class EmpresaResponse(serializers.ModelSerializer):
    usuario = UsuarioResponse(read_only=True)

    class Meta:
        model = Empresa
        fields = [
            'id',
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'email_contato',
            'telefone',
            'usuario',
        ]
