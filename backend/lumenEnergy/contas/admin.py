from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from contas.models import Empresa, Usuario


class EmpresaAdminForm(forms.ModelForm):
    novo_status = forms.ChoiceField(
        choices=Usuario.StatusUsuario.choices,
        required=False,
        label="Alterar status da empresa"
    )

    senha_admin = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirme sua senha de administrador"
    )

    class Meta:
        model = Empresa
        fields = (
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "email_contato",
            "telefone",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario:
            self.fields["novo_status"].initial = self.instance.usuario.tipo_status

    def clean(self):
        cleaned_data = super().clean()

        novo_status = cleaned_data.get("novo_status")
        senha_admin = cleaned_data.get("senha_admin")

        # Só valida alteração de status se já existe um usuário (edição)
        if self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario:
            if novo_status and novo_status != self.instance.usuario.tipo_status:
                if not senha_admin:
                    raise ValidationError(
                        "Para alterar o status da empresa, informe sua senha de administrador."
                    )

                admin_user = self.request.user

                if not admin_user.check_password(senha_admin):
                    raise ValidationError("Senha do administrador incorreta.")

        return cleaned_data

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    form = EmpresaAdminForm

    list_display = (
        "id",
        "nome_fantasia",
        "cnpj",
        "status_empresa",
        "usuario",
    )

    search_fields = ("nome_fantasia", "cnpj")
    readonly_fields = ("usuario",)

    fieldsets = (
        ("Dados da Empresa", {
            "fields": (
                "razao_social",
                "nome_fantasia",
                "cnpj",
                "email_contato",
                "telefone",
            )
        }),
        ("Status e Controle", {
            "fields": (
                "novo_status",
                "senha_admin",
            )
        }),
        ("Usuário Vinculado", {
            "fields": ("usuario",)
        }),
    )

    def status_empresa(self, obj):
        if hasattr(obj, 'usuario') and obj.usuario:
            return obj.usuario.tipo_status
        return "-"
    status_empresa.short_description = "Status"

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class RequestWrappedForm(Form):
            def __new__(cls, *args, **kw):
                kw["request"] = request
                return Form(*args, **kw)

        return RequestWrappedForm

    def save_model(self, request, obj, form, change):
        # CRIAÇÃO DA EMPRESA + USUÁRIO
        if not change:
            usuario = Usuario.objects.create_user(
                username=obj.cnpj,
                email=obj.email_contato,
                tipo_usuario=Usuario.TipoUsuario.EMPRESA,
                tipo_status=Usuario.StatusUsuario.ATIVA,
                is_active=True,
                password="Lumen@1234",
            )
            obj.usuario = usuario
            # Salva primeiro para garantir que o usuário está vinculado
            super().save_model(request, obj, form, change)
        else:
            # ALTERAÇÃO DE STATUS (apenas em edição)
            novo_status = form.cleaned_data.get("novo_status")

            if novo_status and obj.usuario:
                obj.usuario.tipo_status = novo_status
                obj.usuario.is_active = novo_status == Usuario.StatusUsuario.ATIVA
                obj.usuario.save()
            
            super().save_model(request, obj, form, change)