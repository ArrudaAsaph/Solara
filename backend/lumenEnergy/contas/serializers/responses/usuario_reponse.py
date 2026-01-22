from rest_framework import serializers
from contas.models import Usuario

class UsuarioSimpleResponse(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'tipo_usuario',
            'tipo_status'
        ]

class UsuarioResponse(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'tipo_usuario',
            'tipo_status',
            'data_criacao',
            'data_atualizacao',
            'ultimo_login'
        ]

