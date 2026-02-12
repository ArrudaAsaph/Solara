import re
from django.db import transaction
import logging
audit_logger = logging.getLogger("audit")

from core.error import Erro
from core.services import PermissaoService
from contas.models import Usuario, Pessoa

class CadastroService():
   
    @classmethod
    def _erro_base(cls, *, usuario_logado):
        return {
            "domain": "cadastro",
            "entidade": "Pessoa",
            "usuario": {
                "id": getattr(usuario_logado, "id", None),
                "username": getattr(usuario_logado, "username", None),
            },
        }
    

    @classmethod
    @transaction.atomic
    def criar(cls, *, usuario_logado, data):
        erro = cls._antes_criar(
            usuario_logado = usuario_logado,
            data = data
        )

        if erro:
            return erro
        
        novo_usuario = Usuario(
            username = data["username"],
            email = data["email"],
        )

        novo_usuario.set_password(data["password"])

        novo_usuario.save()

        
        nova_pessoa = Pessoa(
            primeiro_nome = data["primeiro_nome"],
            ultimo_nome = data["ultimo_nome"],
            nome_completo = data["nome_completo"],
            cpf = data["cpf"],                     
            email_contato = data["email_contato"],
            telefone = data["telefone"],          
            tipo_perfil=data["tipo_perfil"],
            empresa = usuario_logado.empresa_vinculada,
            usuario = novo_usuario,
            criado_por = usuario_logado,
        )

        nova_pessoa.save()
        audit_logger.info(
            "Pessoa criada",
            extra={
                "domain": "cadastro",
                "entidade": "Pessoa",
                "acao": "criar",
                "pessoa_id": nova_pessoa.id,
                "usuario": usuario_logado.id,
                "empresa": usuario_logado.empresa_vinculada,
            }
        )
        return nova_pessoa
            
    @classmethod
    def _antes_criar(cls, *, usuario_logado, data):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        erro = cls._permissao(
            usuario_logado=usuario_logado,
            data=data,
            erro_base=erro_base
            )
        if erro:
            return erro

        data["cpf"] = cls._normalizar_cpf(data["cpf"])
        data["telefone"] = cls._normalizar_telefone(data["telefone"])
        data["primeiro_nome"], data["ultimo_nome"] = cls._normalizar_nome(data["nome_completo"])

        
        return cls._validar(data = data, erro_base = erro_base)   
   
    @classmethod
    def _validar(cls, *, data, erro_base):
        erros = []

        # Usuario
        if Usuario.objects.filter(username=data["username"]).exists():
            erros.append({
                "field": "username",
                "mensagem": "Usuário já existente",
                "value": data["username"]
            })

        if Usuario.objects.filter(email=data["email"]).exists():
            erros.append({
                "field": "email",
                "mensagem": "Usuário já existente",
                "value": data["email"]
            })

        # Pessoa
        if Pessoa.objects.filter(cpf=data["cpf"]).exists():
            erros.append({
                "field": "cpf",
                "mensagem": "CPF já cadastrado",
                "value": data["cpf"]
            })

        if Pessoa.objects.filter(email_contato=data["email_contato"]).exists():
            erros.append({
                "field": "email_contato",
                "mensagem": "Email já cadastrado",
                "value": data["email_contato"]
            })

        if Pessoa.objects.filter(telefone=data["telefone"]).exists():
            erros.append({
                "field": "telefone",
                "mensagem": "Telefone já cadastrado",
                "value": data["telefone"]
            })

        if erros:
            return Erro(
                **erro_base,
                acao="criar",
                mensagem="Erro de validação",
                field=None,
                status_code=409,
                data={
                    "erros": erros
                }
            )

        return None

    @classmethod
    def _permissao(cls, *, usuario_logado, data, erro_base):
        permissao = PermissaoService(usuario_logado)

        perfil_logado = permissao.perfil_logado()

        if perfil_logado not in ["EMPRESA", Pessoa.TipoPerfil.GERENTE]:
            return Erro(
                **erro_base,
                acao="criar",
                mensagem = "Usuário sem permissão para cadastro",
                status_code = 403
            )
        
        if data["tipo_perfil"] == Pessoa.TipoPerfil.GERENTE and perfil_logado != "EMPRESA":
            return Erro(
                **erro_base,
                acao="criar",
                mensagem = "Usuário sem permissão para cadastro",
                extra = "Apenas a empresa pode cadastrar gerentes",
                status_code = 403
            )

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
