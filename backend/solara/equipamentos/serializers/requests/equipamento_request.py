from rest_framework import serializers
from equipamentos.models import Equipamento

class EquipamentoRequest(serializers.Serializer):
    fabricante = serializers.CharField(max_length = 120, required = True)
    potencia = serializers.DecimalField(
        max_digits = 8, 
        decimal_places = 0, 
        required = True
        )
    
    tensao = serializers.DecimalField(
        max_digits = 8, 
        decimal_places = 0, 
        required = True
        )
    
    tipo_equipamento = serializers.ChoiceField(
        choices = Equipamento.TipoEquipamento.choices,
        required = True
    )

    