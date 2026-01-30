from rest_framework import serializers
from equipamentos.models import Equipamento

class EquipamentoResponse(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = [
            'id',
            'fabricante',
            'potencia',
            'tensao',
            'tipo_equipamento'
        ]