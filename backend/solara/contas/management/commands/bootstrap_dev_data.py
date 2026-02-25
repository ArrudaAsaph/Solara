from django.core.management.base import BaseCommand
from django.db import transaction

from contas.models import Empresa, Pessoa, Usuario
from core.services.grupo_perfil_service import GrupoPerfilService


class Command(BaseCommand):
    help = (
        "Cria/atualiza superadmin, empresas de desenvolvimento e usuarios "
        "vinculados a cada empresa."
    )

    def add_arguments(self, parser):
        parser.add_argument("--superuser-username", default="admin")
        parser.add_argument("--superuser-email", default="admin@solara.local")
        parser.add_argument("--superuser-password", default="admin123")
        parser.add_argument("--empresas", type=int, default=4)
        parser.add_argument("--usuarios-por-empresa", type=int, default=8)
        parser.add_argument("--prefixo", default="dev")

    @transaction.atomic
    def handle(self, *args, **options):
        superuser = self._create_or_update_superuser(
            username=options["superuser_username"],
            email=options["superuser_email"],
            password=options["superuser_password"],
        )

        empresas = max(options["empresas"], 1)
        usuarios_por_empresa = max(options["usuarios_por_empresa"], 1)
        prefixo = options["prefixo"].strip().lower() or "dev"

        total_pessoas = 0
        for idx in range(1, empresas + 1):
            empresa_user, empresa = self._create_or_update_empresa(idx=idx, prefixo=prefixo)
            total_pessoas += self._seed_pessoas_da_empresa(
                empresa=empresa,
                empresa_user=empresa_user,
                qtd=usuarios_por_empresa,
                prefixo=prefixo,
            )

        self.stdout.write(self.style.SUCCESS("Bootstrap finalizado com sucesso."))
        self.stdout.write(f"Superadmin: {superuser.username}")
        self.stdout.write(f"Empresas processadas: {empresas}")
        self.stdout.write(f"Pessoas processadas: {total_pessoas}")

    def _create_or_update_superuser(self, *, username, email, password):
        user, _ = Usuario.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "tipo_status": Usuario.StatusUsuario.ATIVA,
                "tipo_usuario": Usuario.TipoUsuario.PESSOA,
            },
        )

        updates = []
        if user.email != email:
            user.email = email
            updates.append("email")
        if not user.is_staff:
            user.is_staff = True
            updates.append("is_staff")
        if not user.is_superuser:
            user.is_superuser = True
            updates.append("is_superuser")
        if not user.is_active:
            user.is_active = True
            updates.append("is_active")
        if user.tipo_status != Usuario.StatusUsuario.ATIVA:
            user.tipo_status = Usuario.StatusUsuario.ATIVA
            updates.append("tipo_status")

        user.set_password(password)
        updates.append("password")
        user.save(update_fields=updates)
        GrupoPerfilService.sync_usuario_groups(
            usuario=user,
            tipo_usuario=Usuario.TipoUsuario.PESSOA,
        )

        return user

    def _create_or_update_empresa(self, *, idx, prefixo):
        username = f"{prefixo}_empresa_{idx}"
        email = f"{prefixo}.empresa.{idx}@solara.local"
        empresa_user, _ = Usuario.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "tipo_usuario": Usuario.TipoUsuario.EMPRESA,
                "tipo_status": Usuario.StatusUsuario.ATIVA,
                "is_active": True,
            },
        )

        user_updates = []
        if empresa_user.email != email:
            empresa_user.email = email
            user_updates.append("email")
        if empresa_user.tipo_usuario != Usuario.TipoUsuario.EMPRESA:
            empresa_user.tipo_usuario = Usuario.TipoUsuario.EMPRESA
            user_updates.append("tipo_usuario")
        if empresa_user.tipo_status != Usuario.StatusUsuario.ATIVA:
            empresa_user.tipo_status = Usuario.StatusUsuario.ATIVA
            user_updates.append("tipo_status")
        if not empresa_user.is_active:
            empresa_user.is_active = True
            user_updates.append("is_active")

        empresa_user.set_password("Senha@123456")
        user_updates.append("password")
        if user_updates:
            empresa_user.save(update_fields=user_updates)

        GrupoPerfilService.sync_usuario_groups(
            usuario=empresa_user,
            tipo_usuario=Usuario.TipoUsuario.EMPRESA,
        )

        empresa_defaults = {
            "razao_social": f"{prefixo.capitalize()} Razao {idx}",
            "nome_fantasia": f"{prefixo.capitalize()} Energia {idx}",
            "cnpj": f"{idx:014d}",
            "email_contato": f"contato.{prefixo}.empresa.{idx}@solara.local",
            "telefone": f"1197{idx:06d}",
        }

        empresa, created = Empresa.objects.get_or_create(
            usuario=empresa_user,
            defaults=empresa_defaults,
        )

        if not created:
            for field, value in empresa_defaults.items():
                setattr(empresa, field, value)
            empresa.save(update_fields=list(empresa_defaults.keys()))

        return empresa_user, empresa

    def _seed_pessoas_da_empresa(self, *, empresa, empresa_user, qtd, prefixo):
        perfis = [
            Pessoa.TipoPerfil.GERENTE,
            Pessoa.TipoPerfil.ANALISTA_ENERGETICO,
            Pessoa.TipoPerfil.ANALISTA_FINANCEIRO,
            Pessoa.TipoPerfil.INVESTIDOR,
            Pessoa.TipoPerfil.CONSUMIDOR,
        ]

        created_or_updated = 0
        for idx in range(1, qtd + 1):
            perfil = perfis[(idx - 1) % len(perfis)]
            username = f"{prefixo}_e{empresa.id}_u{idx}"
            email = f"{prefixo}.e{empresa.id}.u{idx}@solara.local"

            user, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "tipo_usuario": Usuario.TipoUsuario.PESSOA,
                    "tipo_status": Usuario.StatusUsuario.ATIVA,
                    "is_active": True,
                },
            )

            user_updates = []
            if user.email != email:
                user.email = email
                user_updates.append("email")
            if user.tipo_usuario != Usuario.TipoUsuario.PESSOA:
                user.tipo_usuario = Usuario.TipoUsuario.PESSOA
                user_updates.append("tipo_usuario")
            if user.tipo_status != Usuario.StatusUsuario.ATIVA:
                user.tipo_status = Usuario.StatusUsuario.ATIVA
                user_updates.append("tipo_status")
            if not user.is_active:
                user.is_active = True
                user_updates.append("is_active")

            user.set_password("Senha@123456")
            user_updates.append("password")
            if user_updates:
                user.save(update_fields=user_updates)

            pessoa_defaults = {
                "primeiro_nome": f"Pessoa{idx}",
                "ultimo_nome": f"Empresa{empresa.id}",
                "nome_completo": f"Pessoa {idx} Empresa {empresa.id}",
                "cpf": f"{empresa.id:03d}{idx:08d}",
                "email_contato": f"contato.{prefixo}.e{empresa.id}.u{idx}@solara.local",
                "telefone": f"118{empresa.id % 10}{idx:06d}",
                "tipo_perfil": perfil,
                "empresa": empresa,
                "criado_por": empresa_user,
            }

            pessoa, created = Pessoa.objects.get_or_create(
                usuario=user,
                defaults=pessoa_defaults,
            )

            if not created:
                for field, value in pessoa_defaults.items():
                    setattr(pessoa, field, value)
                pessoa.save(update_fields=list(pessoa_defaults.keys()))

            GrupoPerfilService.sync_usuario_groups(
                usuario=user,
                tipo_perfil=perfil,
            )

            created_or_updated += 1

        return created_or_updated
