from django.db import models
from .usuario import Usuario

class Empresa(models.Model):
    
    razao_social = models.CharField(max_length = 100)
    nome_fantasia = models.CharField(max_length = 100)
    cnpj = models.CharField(max_length = 18, unique = True)
    email_contato = models.EmailField(unique = True, blank = True)
    telefone = models.CharField(max_length = 14, unique = True)

    usuario = models.OneToOneField(
        Usuario,
        on_delete = models.CASCADE,
        related_name = "empresa"
    )

    def __str__(self):
        return f"{self.nome_fantasia} - {self.cnpj}"
