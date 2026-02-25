from django.db import migrations


PERFIS_GERENCIADOS = [
    "EMPRESA",
    "GERENTE",
    "ANALISTA_FINANCEIRO",
    "ANALISTA_ENERGETICO",
    "INVESTIDOR",
    "CONSUMIDOR",
]


def sync_grupos_usuarios(apps, schema_editor):
    Usuario = apps.get_model("contas", "Usuario")
    Pessoa = apps.get_model("contas", "Pessoa")
    Group = apps.get_model("auth", "Group")

    for nome in PERFIS_GERENCIADOS:
        Group.objects.get_or_create(name=nome)

    managed_groups = list(Group.objects.filter(name__in=PERFIS_GERENCIADOS))
    managed_by_name = {group.name: group for group in managed_groups}

    pessoas_por_usuario = dict(
        Pessoa.objects.values_list("usuario_id", "tipo_perfil")
    )

    for usuario in Usuario.objects.all().iterator():
        usuario.groups.remove(*managed_groups)

        if usuario.tipo_usuario == "EMPRESA":
            usuario.groups.add(managed_by_name["EMPRESA"])
            continue

        tipo_perfil = pessoas_por_usuario.get(usuario.id)
        if tipo_perfil in managed_by_name:
            usuario.groups.add(managed_by_name[tipo_perfil])


def noop_reverse(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ("contas", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(sync_grupos_usuarios, noop_reverse),
    ]
