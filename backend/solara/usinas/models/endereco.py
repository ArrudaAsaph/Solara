from django.db import models

class Endereco(models.Model):
    class TipoEndereco(models.TextChoices):
        USINA = "USINA", "Usina"
        EMPRESA = "EMPRESA", "Empresa"
        UNIDADE_CONSUMIDORA = "UNIDADE_CONSUMIDORA", "Unidade Consumidora"

    rua = models.CharField(max_length = 255)
    numero = models.CharField(max_length = 10, blank = True, null = True)
    complemento = models.CharField(max_length = 50, blank = True, null = True)
    bairro = models.CharField(max_length = 100, blank = True, null = True)
    cidade = models.CharField(max_length = 100)
    estado = models.CharField(max_length = 2)
    cep = models.CharField(max_length = 10)

    tipo_endereco = models.CharField(
        max_length = 19,
        choices = TipoEndereco.choices,
        verbose_name = "Tipo de endereço",
        default = TipoEndereco.UNIDADE_CONSUMIDORA
    )
    
    def __str__(self):
        return f"{self.rua}, {self.numero or ''} - {self.cidade}/{self.estado}"

