from rest_framework import serializers
from contas.models import Usuario


class UsuarioUpdateRequest(serializers.Serializer):
    id = serializers.IntegerField(required = True)
    
    username = serializers.CharField(
        max_length=150,
        required=False
    )

    antiga_password = serializers.CharField(
        min_length=6,
        required=False,
        write_only=True
    )

    nova_password1 = serializers.CharField(
        min_length=6,
        required=False,
        write_only=True
    )

    nova_password2 = serializers.CharField(
        min_length=6,
        required=False,
        write_only=True
    )
    
    email = serializers.EmailField(
        required = False
        )
    
    tipo_status = serializers.ChoiceField(
        choices=Usuario.StatusUsuario.choices,
        required=True
    )

    def validate(self, attrs):
        antiga = attrs.get("antiga_password")
        nova1 = attrs.get("nova_password1")
        nova2 = attrs.get("nova_password2")

        if antiga and (not nova1 or not nova2):
            raise serializers.ValidationError({
                "password": (
                    "Para alterar a senha, é necessário informar "
                    "as duas novas senhas."
                )
            })

        return attrs


class UsuarioUpdateMeRequest(serializers.Serializer):
   
    username = serializers.CharField(
        max_length=150,
        required=False
    )

    antiga_password = serializers.CharField(
        min_length=6,
        required=False,
        write_only=True
    )

    nova_password1 = serializers.CharField(
        min_length=6,
        required=False,
        write_only=True
    )

    nova_password2 = serializers.CharField(
        min_length=6,
        required=False,
        write_only=True
    )
    
    email = serializers.EmailField(
        required = False
        )
    
    
    def validate(self, attrs):
        antiga = attrs.get("antiga_password")
        nova1 = attrs.get("nova_password1")
        nova2 = attrs.get("nova_password2")

        if antiga and (not nova1 or not nova2):
            raise serializers.ValidationError({
                "password": (
                    "Para alterar a senha, é necessário informar "
                    "as duas novas senhas."
                )
            })

        return attrs
