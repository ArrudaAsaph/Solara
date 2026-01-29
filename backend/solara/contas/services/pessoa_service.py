from django.db import transaction
import logging
audit_logger = logging.getLogger("audit")

from contas.models import Pessoa
from core.services import PermissaoService
from core.error import Erro
from django.contrib.auth.hashers import check_password
from django.db import transaction
class PessoaService:
    
    @classmethod
    def _erro_base(cls, *, usuario_logado):
        return {
            "domain": "pessoa",
            "entidade": "Pessoa",
            "usuario": {
                "id": getattr(usuario_logado, "id", None),
                "username": getattr(usuario_logado, "username", None),
            },
        }
    
    # metodo publico para usuarios
    @classmethod
    def listar(cls, *, usuario_logado, filtros=None):
        filtros = filtros or {}

        erro_base = cls._erro_base(usuario_logado=usuario_logado)
        permissao = PermissaoService(usuario_logado)

        hierarquia_de_perfil = permissao.hierarquia()

        if not hierarquia_de_perfil:
            return Erro(
                **erro_base,
                acao = "listar",
                mensagem = "Usuário não possui permissão para listar pessoas",
                status_code = 403
            )
        
        qs = (
            Pessoa.objects
                .select_related("usuario", "empresa")
                .filter(
                    empresa = usuario_logado.empresa_vinculada,
                    tipo_perfil__in = hierarquia_de_perfil
                )
                .exclude(usuario = usuario_logado)
        )

        # filtros

        nome = filtros.get("nome")
        tipo_perfil = filtros.get("tipo_perfil")
        status = filtros.get("status")

        if nome:
            qs = qs.filter(
                nome_completo__icontains = nome
            )
        
        if tipo_perfil:
            if tipo_perfil in hierarquia_de_perfil:
                qs = qs.filter(
                    tipo_perfil = tipo_perfil
                )
            else:
                return Erro(
                    **erro_base,
                    acao = "listar",
                    mensagem = "Usuário não possui permissão para listar esse tipo de perfil",
                    status_code = 403,
                    data={
                        "tipo_perfil_solicitado": tipo_perfil,
                        "tipos_permitidos": hierarquia_de_perfil,
                    }
                )
        
        if status:
            qs = qs.filter(usuario__tipo_status=status)

        return qs

    # metodo privado para gerentes e empresa
    @classmethod
    def buscar_por_id(cls, *, usuario_logado, id):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)

        permissaoService = PermissaoService(usuario_logado)

        if not permissaoService.acesso(
            ["EMPRESA", 
             Pessoa.TipoPerfil.GERENTE, 
             Pessoa.TipoPerfil.ANALISTA_ENERGETICO, 
             Pessoa.TipoPerfil.ANALISTA_FINANCEIRO
             ]):
                return Erro(
                **erro_base,
                acao = "buscar_por_id",
                mensagem = "Usuário sem permissão para acessar pessoas",
                status_code = 403
            )
        
        pessoa = (
            Pessoa.objects
            .select_related("usuario", "empresa")
            .filter(id=id)
            .first()
        )

        if not pessoa:
            return Erro(
                **erro_base,
                acao = "buscar_por_id",
                mensagem = "Pessoa não encontrada",
                status_code = 404
            )

        if pessoa.empresa != usuario_logado.empresa_vinculada:
            return Erro(
                **erro_base,
                acao = "buscar_por_id",
                mensagem = "Pessoa não encontrada",
                status_code = 404
            )
        
        hierarquia_de_perfil = permissaoService.hierarquia()
        if not permissaoService.pode_ver(pessoa_alvo = pessoa):
            return Erro(
                **erro_base,
                acao = "buscar_por_id",
                mensagem = "Usuário não possui permissão para visualizar este perfil",
                status_code = 403,
                data={
                        "tipo_perfil_solicitado": pessoa.tipo_perfil ,
                        "tipos_permitidos": hierarquia_de_perfil,
                    }
            )

        return pessoa
    
    @classmethod
    @transaction.atomic
    def atualizar(cls, *, data, id, usuario_logado):
        erro_base = cls._erro_base(usuario_logado = usuario_logado)
        permissaoService = PermissaoService(usuario_logado)

        if not permissaoService.acesso(["EMPRESA", "GERENTE"]):
            print("estour aqui")
            return Erro(
                **erro_base,
                acao = "atualizar",
                mensagem = "Usuário sem permissão para atualizar pessoas",
                status_code = 403
            )
        
        if "tipo_perfil" in data:
            if (
                data["tipo_perfil"] == Pessoa.TipoPerfil.GERENTE 
                and permissaoService.perfil_logado() == Pessoa.TipoPerfil.GERENTE ):
                    return Erro(
                    **erro_base,
                    acao = "atualizar",
                    mensagem = "Usuário sem permissão para atualizar pessoas para o tipo Gerente",
                    field = "tipo_perfil",
                    data = data["tipo_perfil"],
                    status_code = 403
                )
        # checar senha
        if not usuario_logado.check_password(data["password"]):
            return Erro(
                **erro_base,
                acao = "atualizar",
                mensagem = "Senha inválida",
                status_code = 401
            )
        
        pessoa_atualizada = cls.buscar_por_id(usuario_logado = usuario_logado, id = id)

        if isinstance(pessoa_atualizada, Erro):
            return pessoa_atualizada
        
        alterou = False

        if "tipo_perfil" in data:
            pessoa_atualizada.tipo_perfil = data["tipo_perfil"]
            alterou = True

        if "cpf" in data:
            pessoa_atualizada.usuario.cpf = data["cpf"]
            pessoa_atualizada.usuario.save(update_fields=["cpf"])
            alterou = True

        if not alterou:
            return Erro(
                **erro_base,
                acao="atualizar",
                mensagem="Nenhum dado válido foi informado para atualização",
                status_code=422
            )

        pessoa_atualizada.save()

        audit_logger.info(
            "Pessoa atualizada",
            extra={
                "domain": "pessoa",
                "entidade": "Pessoa",
                "acao": "atualizar",
                "pessoa_id": pessoa_atualizada.id,
                "usuario": usuario_logado.id,
                "empresa": usuario_logado.empresa_vinculada,
            }
        )

        return pessoa_atualizada
        
