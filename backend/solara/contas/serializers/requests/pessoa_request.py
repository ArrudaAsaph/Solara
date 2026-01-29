from rest_framework import serializers
from contas.models import Pessoa

class PessoaUpdateRequest(serializers.Serializer):
    id = serializers.IntegerField(required = True)
    
    email_contato = serializers.EmailField(required = False)

    nome_completo = serializers.CharField(
        max_length = 255,
        required = False
    )

    telefone = serializers.CharField(
        max_length = 14,
        required = True
    )

class PessoaUpdatePrivateRequest(serializers.Serializer):
    tipo_perfil = serializers.ChoiceField(
        choices = Pessoa.TipoPerfil.choices,
        required = False
    )

    cpf = serializers.CharField(
        max_length = 14,
        required = False
    )

    password = serializers.CharField(
        write_only = True,
        min_length = 8,
        required = True
    )

    def validate(self, attrs):
        tipo_perfil = attrs.get("tipo_perfil")
        cpf = attrs.get("cpf")

        if not tipo_perfil and not cpf:
            raise serializers.ValidationError(
                "É obrigatório informar ao menos um dos campos: tipo_perfil ou cpf."
            )

        return attrs