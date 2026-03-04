from rest_framework import serializers

from contas.models import Vendedor


class VendedorCreateRequest(serializers.Serializer):
    nome_completo = serializers.CharField(max_length = 255, required = True)
    cpf = serializers.CharField(max_length = 14, required = True)
    email_contato = serializers.EmailField(required = False, allow_blank = True, allow_null = True)
    telefone = serializers.CharField(max_length = 14, required = True)
    percentual_comissao = serializers.DecimalField(max_digits = 5, decimal_places = 2, required = True)
    tipo_comissao = serializers.ChoiceField(choices = Vendedor.TipoComissao.choices, required = True)
    inicio_vigencia = serializers.DateField(required = True)
    fim_vigencia = serializers.DateField(required = False, allow_null = True)
    tipo_status = serializers.ChoiceField(choices = Vendedor.TipoStatus.choices, required = False)


class VendedorUpdateRequest(serializers.Serializer):
    nome_completo = serializers.CharField(max_length = 255, required = False)
    cpf = serializers.CharField(max_length = 14, required = False)
    email_contato = serializers.EmailField(required = False, allow_blank = True, allow_null = True)
    telefone = serializers.CharField(max_length = 14, required = False)
    percentual_comissao = serializers.DecimalField(max_digits = 5, decimal_places = 2, required = False)
    tipo_comissao = serializers.ChoiceField(choices = Vendedor.TipoComissao.choices, required = False)
    inicio_vigencia = serializers.DateField(required = False)
    fim_vigencia = serializers.DateField(required = False, allow_null = True)
    tipo_status = serializers.ChoiceField(choices = Vendedor.TipoStatus.choices, required = False)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("É obrigatório informar ao menos um campo para atualização.")

        inicio = attrs.get("inicio_vigencia")
        fim = attrs.get("fim_vigencia")

        if inicio and fim and fim < inicio:
            raise serializers.ValidationError({
                "fim_vigencia": "A data final não pode ser menor que a data inicial."
            })

        return attrs
