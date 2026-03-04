from django.db import models

from .empresa import Empresa
from .usuario import Usuario


class Vendedor(models.Model):

    class TipoStatus(models.TextChoices):
        ATIVO = "ATIVO", "ativo"
        INATIVO = "INATIVO", "inativo"

    class TipoComissao(models.TextChoices):
        PERCENTUAL = "PERCENTUAL", "Percentual"
        FIXA = "FIXA", "Fixa"

    nome_completo = models.CharField(max_length = 255)

    cpf = models.CharField(max_length = 14)

    email_contato = models.EmailField(blank = True, null = True)

    telefone = models.CharField(max_length = 14)

    percentual_comissao = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
        default = 0
    )

    tipo_comissao = models.CharField(
        max_length = 20,
        choices = TipoComissao.choices,
        default = TipoComissao.PERCENTUAL,
    )

    inicio_vigencia = models.DateField()

    fim_vigencia = models.DateField(blank = True, null = True)

    tipo_status = models.CharField(
        max_length = 10,
        choices = TipoStatus.choices,
        default = TipoStatus.ATIVO,
        verbose_name = "Status do vendedor",
    )

    contrato_ativo = models.BooleanField(default = False)

    comissionamento_pendente = models.BooleanField(default = False)

    empresa = models.ForeignKey(
        Empresa,
        on_delete = models.CASCADE,
        related_name = "vendedores"
    )

    criado_por = models.ForeignKey(
        Usuario,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "vendedores_criados"
    )

    data_criacao = models.DateTimeField(auto_now_add = True)

    data_atualizacao = models.DateTimeField(auto_now = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["empresa", "cpf"],
                name = "unique_vendedor_cpf_empresa"
            )
        ]

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"
