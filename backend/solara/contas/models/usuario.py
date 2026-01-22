from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):

    class StatusUsuario(models.TextChoices):
        ATIVA = "ATIVA", "ativa"
        INATIVA = "INATIVA", "inativa"
        BLOQUEADA = "BLOQUEADA", "bloqueada"

    tipo_status = models.CharField(
        max_length = 15,
        choices = StatusUsuario.choices,
        verbose_name = "Tipo de status",
        default = StatusUsuario.ATIVA
    )

    class TipoUsuario(models.TextChoices):
        PESSOA = "PESSOA", "Pessoa"
        EMPRESA = "EMPRESA", "Empresa"

    tipo_usuario = models.CharField(
        max_length=10,
        choices = TipoUsuario.choices,
        verbose_name = "Tipo de usuário",
        default = TipoUsuario.PESSOA
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de atualização"
    )

    ultimo_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.username} - {self.email} - {self.last_login}"
    
    @property
    def empresa_vinculada (self):
        if hasattr(self, "empresa"):
            return self.empresa
        return self.pessoa.empresa