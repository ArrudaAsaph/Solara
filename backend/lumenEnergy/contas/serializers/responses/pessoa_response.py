from rest_framework import serializers
from contas.models import Pessoa
from .usuario_reponse import UsuarioSimpleResponse

class PessoaSimpleResponse(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = [
            'primeiro_nome',
            'ultimo_nome',
            'telefone',
            'tipo_perfil',
        ]

class PessoaResponse(serializers.ModelSerializer):
    usuario = UsuarioSimpleResponse(read_only = True)
    criado_por = UsuarioSimpleResponse(read_only = True)

    class Meta:
        model = Pessoa
        fields = [
            'id',
            'nome_completo',
            'primeiro_nome',
            'ultimo_nome',
            'telefone',
            'cpf',
            'email_contato',
            'usuario',
            'criado_por'
        ]
