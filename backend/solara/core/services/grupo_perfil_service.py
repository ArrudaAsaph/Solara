from django.contrib.auth.models import Group, Permission

from contas.models import Pessoa, Usuario


class GrupoPerfilService:
    PERFIL_EMPRESA = "EMPRESA"
    PERFIS_GERENCIADOS = [
        PERFIL_EMPRESA,
        Pessoa.TipoPerfil.GERENTE,
        Pessoa.TipoPerfil.ANALISTA_FINANCEIRO,
        Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
        Pessoa.TipoPerfil.INVESTIDOR,
        Pessoa.TipoPerfil.CONSUMIDOR,
    ]

    HIERARQUIA = PERFIS_GERENCIADOS

    PERMISSOES_GRUPO = {
        PERFIL_EMPRESA: [
            "contas.view_usuario",
            "contas.add_usuario",
            "contas.view_pessoa",
            "contas.add_pessoa",
            "contas.change_pessoa",
            "equipamentos.view_equipamento",
            "equipamentos.add_equipamento",
        ],
        Pessoa.TipoPerfil.GERENTE: [
            "contas.view_usuario",
            "contas.view_pessoa",
            "contas.add_pessoa",
            "contas.add_usuario",
            "contas.change_pessoa",
            "equipamentos.view_equipamento",
            "equipamentos.add_equipamento",
        ],
        Pessoa.TipoPerfil.ANALISTA_FINANCEIRO: [
            "contas.view_pessoa",
            "equipamentos.view_equipamento",
        ],
        Pessoa.TipoPerfil.ANALISTA_ENERGETICO: [
            "contas.view_pessoa",
            "equipamentos.view_equipamento",
        ],
        Pessoa.TipoPerfil.INVESTIDOR: [
            "equipamentos.view_equipamento",
        ],
        Pessoa.TipoPerfil.CONSUMIDOR: [],
    }

    @classmethod
    def _group_name_for_user(cls, *, tipo_usuario: str, tipo_perfil: str | None):
        if tipo_usuario == Usuario.TipoUsuario.EMPRESA:
            return cls.PERFIL_EMPRESA

        if tipo_perfil in cls.PERFIS_GERENCIADOS:
            return tipo_perfil

        return None

    @classmethod
    def get_or_create_group(cls, nome: str):
        group, _ = Group.objects.get_or_create(name=nome)
        return group

    @classmethod
    def get_permissoes_por_grupo(cls, nome: str):
        return cls.PERMISSOES_GRUPO.get(nome, [])

    @classmethod
    def _buscar_permissao(cls, perm_label: str):
        app_label, codename = perm_label.split(".", 1)
        return Permission.objects.filter(
            content_type__app_label=app_label,
            codename=codename,
        ).first()

    @classmethod
    def sync_group_permissions(cls):
        for nome_grupo, permissoes in cls.PERMISSOES_GRUPO.items():
            grupo = cls.get_or_create_group(nome_grupo)

            perms_instances = []
            for perm_label in permissoes:
                permissao = cls._buscar_permissao(perm_label)
                if permissao:
                    perms_instances.append(permissao)

            grupo.permissions.set(perms_instances)

    @classmethod
    def sync_usuario_groups(
        cls,
        *,
        usuario: Usuario,
        tipo_perfil: str | None = None,
        tipo_usuario: str | None = None,
    ):
        cls.sync_group_permissions()

        tipo_usuario_final = tipo_usuario or usuario.tipo_usuario
        tipo_perfil_final = tipo_perfil

        if tipo_perfil_final is None:
            pessoa = getattr(usuario, "pessoa", None)
            tipo_perfil_final = getattr(pessoa, "tipo_perfil", None)

        group_name = cls._group_name_for_user(
            tipo_usuario=tipo_usuario_final,
            tipo_perfil=tipo_perfil_final,
        )

        grupos_managed = Group.objects.filter(name__in=cls.PERFIS_GERENCIADOS)
        usuario.groups.remove(*grupos_managed)

        if group_name:
            grupo = cls.get_or_create_group(group_name)
            usuario.groups.add(grupo)

        return group_name

    @classmethod
    def perfil_from_groups(cls, *, usuario: Usuario):
        if usuario.tipo_usuario == Usuario.TipoUsuario.EMPRESA:
            return cls.PERFIL_EMPRESA

        groups = set(usuario.groups.values_list("name", flat=True))
        for perfil in cls.HIERARQUIA:
            if perfil in groups:
                return perfil

        pessoa = getattr(usuario, "pessoa", None)
        if pessoa and pessoa.tipo_perfil in cls.PERFIS_GERENCIADOS:
            return pessoa.tipo_perfil

        return None
