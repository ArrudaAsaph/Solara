from rest_framework import serializers
from contas.serializers import PessoaResponse, EmpresaResponse

class LoginResponse(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    empresa = EmpresaResponse(required=False, allow_null=True)
    pessoa = PessoaResponse(required=False, allow_null=True)
