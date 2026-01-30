from django.db import models
from .equipamento import Equipamento

from usinas.models import Usina
class KitSolar(models.Model):
    quantidade = models.IntegerField()
    
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete = models.PROTECT,
        related_name = "kits_solares"
    )

    usina = models.ForeignKey(
        Usina,
        on_delete = models.PROTECT,
        related_name = "kits_solares"
    )

    def __str__(self):
        return f"{self.quantidade} x {self.equipamento}"