from django.db import models
from contas.models import Usuario, Empresa

class Pessoa(models.Model):

    class TipoPerfil(models.TextChoices):
        GERENTE = "GERENTE", "Gerente"
        INVESTIDOR = "INVESTIDOR", "Investidor"
        ANALISTA_ENERGETICO = "ANALISTA_ENERGETICO", "Analista Energético"
        ANALISTA_FINANCEIRO = "ANALISTA_FINANCEIRO", "Analista Financeiro"
        CONSUMIDOR = "CONSUMIDOR", "Consumidor"

    primeiro_nome = models.CharField(
        max_length = 50,
        blank = True
    )

    ultimo_nome = models.CharField(
        max_length = 50,
        blank = True
    )

    nome_completo = models.CharField(
        max_length = 255
    )

    cpf = models.CharField(
        max_length = 14,
        unique = True
    )

    email_contato = models.EmailField(
        unique = True,
        blank = True,
        null = True
    )

    telefone = models.CharField(
        max_length = 14,
        unique = True
    )

    tipo_perfil = models.CharField(
        max_length = 25,
        choices = TipoPerfil.choices,
        verbose_name = "Tipo de perfil",
        default = TipoPerfil.CONSUMIDOR
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete = models.CASCADE,
        related_name = "pessoas"
    )

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name = "pessoa",
    )

    criado_por = models.ForeignKey(
        Usuario,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name="pessoas_criadas"
    )


    def __str__(self):
        return f"{self.nome_completo} ({self.tipo_perfil})"
