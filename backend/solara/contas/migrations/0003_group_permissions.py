from django.db import migrations


PERMISSOES_GRUPO = {
    "EMPRESA": [
        "contas.view_usuario",
        "contas.add_usuario",
        "contas.view_pessoa",
        "contas.add_pessoa",
        "contas.change_pessoa",
        "equipamentos.view_equipamento",
        "equipamentos.add_equipamento",
    ],
    "GERENTE": [
        "contas.view_usuario",
        "contas.view_pessoa",
        "contas.add_pessoa",
        "contas.add_usuario",
        "contas.change_pessoa",
        "equipamentos.view_equipamento",
        "equipamentos.add_equipamento",
    ],
    "ANALISTA_FINANCEIRO": [
        "contas.view_pessoa",
        "equipamentos.view_equipamento",
    ],
    "ANALISTA_ENERGETICO": [
        "contas.view_pessoa",
        "equipamentos.view_equipamento",
    ],
    "INVESTIDOR": [
        "equipamentos.view_equipamento",
    ],
    "CONSUMIDOR": [],
}


def _buscar_permissao(Permission, perm_label):
    app_label, codename = perm_label.split(".", 1)
    return Permission.objects.filter(
        content_type__app_label=app_label,
        codename=codename,
    ).first()


def sync_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for group_name, permissoes in PERMISSOES_GRUPO.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        perms_instances = []
        for perm_label in permissoes:
            permissao = _buscar_permissao(Permission, perm_label)
            if permissao:
                perms_instances.append(permissao)

        group.permissions.set(perms_instances)


def noop_reverse(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ("contas", "0002_sync_grupos_usuarios"),
        ("equipamentos", "0002_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(sync_group_permissions, noop_reverse),
    ]
