from contas.models import Empresa, Pessoa, Usuario
from core.services.grupo_perfil_service import GrupoPerfilService


class ContaFactory:
    _seq = 0

    @classmethod
    def _next_seq(cls):
        cls._seq += 1
        return cls._seq

    @classmethod
    def criar_usuario(
        cls,
        *,
        username=None,
        email=None,
        password="Senha@123456",
        tipo_usuario=Usuario.TipoUsuario.PESSOA,
        tipo_status=Usuario.StatusUsuario.ATIVA,
    ):
        seq = cls._next_seq()
        user = Usuario.objects.create(
            username=username or f"user_{seq}",
            email=email or f"user_{seq}@solara.local",
            tipo_usuario=tipo_usuario,
            tipo_status=tipo_status,
        )
        user.set_password(password)
        user.save(update_fields=["password"])
        return user

    @classmethod
    def criar_empresa_com_usuario(
        cls,
        *,
        username=None,
        email=None,
        password="Senha@123456",
        razao_social=None,
        nome_fantasia=None,
    ):
        seq = cls._next_seq()
        usuario = cls.criar_usuario(
            username=username or f"empresa_user_{seq}",
            email=email or f"empresa_{seq}@solara.local",
            password=password,
            tipo_usuario=Usuario.TipoUsuario.EMPRESA,
        )
        empresa = Empresa.objects.create(
            razao_social=razao_social or f"Empresa Razao {seq}",
            nome_fantasia=nome_fantasia or f"Empresa {seq}",
            cnpj=f"{seq:014d}",
            email_contato=f"contato_empresa_{seq}@solara.local",
            telefone=f"1199{seq:06d}",
            usuario=usuario,
        )
        GrupoPerfilService.sync_usuario_groups(
            usuario=usuario,
            tipo_usuario=Usuario.TipoUsuario.EMPRESA,
        )
        return usuario, empresa

    @classmethod
    def criar_pessoa_com_usuario(
        cls,
        *,
        empresa,
        tipo_perfil=Pessoa.TipoPerfil.CONSUMIDOR,
        nome_completo=None,
        username=None,
        email=None,
        password="Senha@123456",
        tipo_status=Usuario.StatusUsuario.ATIVA,
        criado_por=None,
    ):
        seq = cls._next_seq()
        usuario = cls.criar_usuario(
            username=username or f"pessoa_user_{seq}",
            email=email or f"pessoa_{seq}@solara.local",
            password=password,
            tipo_usuario=Usuario.TipoUsuario.PESSOA,
            tipo_status=tipo_status,
        )
        pessoa = Pessoa.objects.create(
            primeiro_nome="Pessoa",
            ultimo_nome=str(seq),
            nome_completo=nome_completo or f"Pessoa Teste {seq}",
            cpf=f"{seq:011d}",
            email_contato=f"pessoa_contato_{seq}@solara.local",
            telefone=f"1198{seq:06d}",
            tipo_perfil=tipo_perfil,
            empresa=empresa,
            usuario=usuario,
            criado_por=criado_por,
        )
        GrupoPerfilService.sync_usuario_groups(
            usuario=usuario,
            tipo_perfil=tipo_perfil,
        )
        return usuario, pessoa
