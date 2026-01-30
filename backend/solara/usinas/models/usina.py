from django.db import models
from contas.models import Pessoa, Usuario, Empresa

from .endereco import Endereco
class Usina(models.Model):
    class StatusUsina(models.TextChoices):
        ATIVA = "ATIVA", "ativa"
        INATIVA = "INATIVA", "inativa"
        BLOQUEADA = "BLOQUEADA", "bloqueada"

    nome = models.CharField(max_length = 255)
    potencia_instalada = models.DecimalField(max_digits = 10, decimal_places = 2)
    data_instalacao = models.DateField()

    tipo_status = models.CharField(
        max_length = 15,
        choices = StatusUsina.choices,
        verbose_name = "Tipo de status da usina",
        default = StatusUsina.ATIVA
    )

    investidor = models.ForeignKey(
        Pessoa,
        on_delete = models.PROTECT,
        related_name = "usinas"
    )

    criado_por = models.ForeignKey(
        Usuario,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name="usinas_criadas"
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete = models.CASCADE,
        related_name = "usinas"
    )

    endereco = models.OneToOneField(
        Endereco,
        on_delete = models.PROTECT,
        related_name = "usina" 
    )
   
    def __str__(self):
        return f"Usina {self.nome} ({self.potencia_instalada} kWp)"