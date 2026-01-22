import re
from django.db import transaction

from contas.models import Usuario, Pessoa



class CadastroService():

    @classmethod
    @transaction.atomic
    def criar(cls, *, usuario_logado, data):
        cls._antes_criar(
            usuario_logado = usuario_logado,
            data = data
        )
    @classmethod
    def _antes_criar(cls, *, usuario_logado, data):
        data["cpf"] = cls._normalizar_cpf(data["cpf"])
        data["telefone"] = cls._normalizar_telefone(data["telefone"])
        data["primeiro_nome"], data["ultimo_nome"] = cls._normalizar_nome(data["nome_completo"])
    

        

    
    # Normalização

    @staticmethod
    def _normalizar_cpf(cpf):
        return re.sub(r"\D", "", cpf or "")
    
    @staticmethod
    def _normalizar_telefone(telefone):
        return re.sub(r"\D", "", telefone or "")

    @staticmethod
    def _normalizar_nome(nome):
        nome = nome.split()
        primeiro_nome = nome[0].capitalize()
        ultimo_nome = nome[-1].capitalize()
        return primeiro_nome, ultimo_nome
