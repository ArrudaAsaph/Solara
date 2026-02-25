from django.db.models.signals import post_migrate
from django.dispatch import receiver

from core.services.grupo_perfil_service import GrupoPerfilService


@receiver(post_migrate)
def sync_group_permissions_after_migrate(sender, **kwargs):
    GrupoPerfilService.sync_group_permissions()
