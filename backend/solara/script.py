from contas.models import Empresa, Pessoa
from contas.services import CadastroService
from django.db import transaction

# =========================
# Geradores utilitários
# =========================

def gerar_cpf(idx):
    return f"{idx:011d}"

def gerar_telefone(idx):
    return f"8499{idx:07d}"

def gerar_email(prefixo, idx, dominio="example.com"):
    return f"{prefixo}{idx}@{dominio}"


PERFIS = {
    Pessoa.TipoPerfil.GERENTE: 10,
    Pessoa.TipoPerfil.ANALISTA_ENERGETICO: 20,
    Pessoa.TipoPerfil.ANALISTA_FINANCEIRO: 20,
    Pessoa.TipoPerfil.INVESTIDOR: 10,
    Pessoa.TipoPerfil.CONSUMIDOR: 200,
}


def criar_pessoas_empresa(*, empresa, usuario_empresa, contador_inicio):
    print(f"\n🏢 Criando pessoas da empresa {empresa.nome_fantasia}")

    gerentes = []
    contador = contador_inicio

    # =========================
    # 1️⃣ Criar GERENTES
    # =========================
    for i in range(PERFIS[Pessoa.TipoPerfil.GERENTE]):
        data = {
            "username": f"gerente_{empresa.id}_{i}",
            "email": gerar_email("gerente", contador),
            "password": "Teste@123",
            "nome_completo": f"Gerente {empresa.id} {i}",
            "cpf": gerar_cpf(contador),
            "email_contato": gerar_email("contato_gerente", contador),
            "telefone": gerar_telefone(contador),
            "tipo_perfil": Pessoa.TipoPerfil.GERENTE,
        }

        pessoa = CadastroService.criar(
            usuario_logado=usuario_empresa,
            data=data
        )

        if isinstance(pessoa, Pessoa):
            gerentes.append(pessoa.usuario)
        else:
            print(
                f"❌ Erro ao criar gerente | "
                f"mensagem={getattr(pessoa, 'mensagem', None)} | "
                f"data={getattr(pessoa, 'data', None)}"
            )

        contador += 1

    # ⚠️ REGRA DE SOBREVIVÊNCIA
    if not gerentes:
        print("🚨 Nenhum gerente criado. Pulando empresa.")
        return contador

    # =========================
    # 2️⃣ Criar demais perfis
    # =========================
    for perfil, quantidade in PERFIS.items():
        if perfil == Pessoa.TipoPerfil.GERENTE:
            continue

        for i in range(quantidade):
            gerente = gerentes[i % len(gerentes)]

            data = {
                "username": f"{perfil.lower()}_{empresa.id}_{contador}",
                "email": gerar_email(perfil.lower(), contador),
                "password": "Teste@123",
                "nome_completo": f"{perfil.replace('_', ' ').title()} {empresa.id} {i}",
                "cpf": gerar_cpf(contador),
                "email_contato": gerar_email(f"contato_{perfil.lower()}", contador),
                "telefone": gerar_telefone(contador),
                "tipo_perfil": perfil,
            }

            pessoa = CadastroService.criar(
                usuario_logado=gerente,
                data=data
            )

            if not isinstance(pessoa, Pessoa):
                print(
                    f"❌ Erro ao criar {perfil} | "
                    f"mensagem={getattr(pessoa, 'mensagem', None)} | "
                    f"data={getattr(pessoa, 'data', None)}"
                )

            contador += 1


    return contador


# =========================
# Seed principal
# =========================
@transaction.atomic
def seed():
    empresas = Empresa.objects.all()[:10]

    contador_global = 1

    for empresa in empresas:
        contador_global = criar_pessoas_empresa(
            empresa=empresa,
            usuario_empresa=empresa.usuario,
            contador_inicio=contador_global
        )

    print("\n✅ Seed finalizado com sucesso")
