from django.db import models

class Equipamento(models.Model):

    class TipoEquipamento(models.TextChoices):
        MODULO_MONOFACIAL = "MODULO_FOTOVOLTAICO_MONOFACIAL", "Módulo fotovoltaico Monofacial",
        MODULO_BIFACIAL = "MODULO_FOTOVOLTAICO_BIFACIAL", "Módulo fotovoltaico Bifacial"
        INVERSOR_CONVENCIONAL = "INVERSOR_CONVENCIONAL", "Inversor Convencional"
        INVERSOR_MICRO = "INVERSOR_MICRO", "Inversor Micro"

    fabricante = models.CharField(max_length = 120)
    potencia = models.DecimalField(max_digits = 8, decimal_places = 2)
    tensao = models.DecimalField(max_digits = 8, decimal_places = 0)
    tipo_equipamento = models.CharField(
        max_length = 40,
        choices = TipoEquipamento.choices,
        verbose_name = "Tipo do equipamento"
    )
    
    def __str__(self):
        return f"{self.get_tipo_equipamento_display()} - {self.fabricante} - {self.potencia}W"
    
    class Meta:
        unique_together = ("fabricante", "tipo_equipamento", "potencia", "tensao")
