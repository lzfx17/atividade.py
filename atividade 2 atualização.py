# =============================================================================
# conftest.py — Configurações compartilhadas entre todos os testes
# =============================================================================
#
# O pytest carrega este arquivo automaticamente antes de executar qualquer
# teste. Aqui ficam os "fixtures": funções reutilizáveis que preparam o
# ambiente antes de cada teste e fazem a limpeza depois.
#
# O que é um fixture?
#   É uma função decorada com @pytest.fixture que devolve um objeto pronto
#   para ser usado nos testes. Os testes declaram o fixture como parâmetro
#   e o pytest cuida de executá-lo e injetá-lo automaticamente.
# =============================================================================

import pytest
from fastapi.testclient import TestClient
from main import app
from repositories.memory import db


@pytest.fixture(autouse=True)
def reset_memory_db():
    """Limpa o banco de dados em memória antes de cada teste.

    Por que isso é necessário?
    Os testes não podem depender uns dos outros. Se um teste criar um cliente
    e o próximo esperar que o banco esteja vazio, o segundo falhará por causa
    do primeiro. Resetar o banco antes de cada teste garante isolamento total.

    O parâmetro autouse=True faz com que este fixture seja executado
    automaticamente para TODOS os testes, sem precisar declará-lo como
    parâmetro nas funções de teste.

    O comando `yield` separa a fase de preparação (antes) da fase de
    limpeza (depois). Aqui só há preparação, mas o yield é necessário
    para que o pytest saiba quando o teste terminou.
    """
    db.clientes_por_cpf.clear()
    db.produtos_por_id.clear()
    db.pedidos_por_codigo.clear()
    yield


@pytest.fixture
def client():
    """Cria um cliente HTTP para testar a API sem subir um servidor real.

    O TestClient simula requisições HTTP diretamente na aplicação FastAPI,
    sem precisar de uma porta de rede. Isso torna os testes muito mais
    rápidos e simples de rodar em qualquer ambiente.

    Como usar:
        def test_exemplo(client):        # <-- pytest injeta o client aqui
            r = client.get("/health")
            assert r.status_code == 200
    """
    return TestClient(app)
