# =============================================================================
# conftest.py — Configurações compartilhadas entre todos os testes
# =============================================================================
#
# Com a migração para Tortoise ORM async, este arquivo foi reescrito para:
#
#   1. Inicializar o Tortoise com SQLite em memória (:memory:) antes de cada
#      teste, garantindo que cada teste parte de um banco totalmente vazio.
#   2. Fechar a conexão após o teste — o SQLite :memory: é destruído junto,
#      sem deixar nada no disco.
#   3. Fornecer um cliente HTTP assíncrono (httpx.AsyncClient) que despacha
#      requisições direto ao app FastAPI, sem abrir porta de rede.
#
# Por que não usar TestClient (síncrono)?
#   O TestClient cria seu próprio event loop, o que conflita com o Tortoise
#   que já tem uma conexão assíncrona ativa no event loop do pytest-asyncio.
#   O AsyncClient + ASGITransport reutiliza o mesmo event loop, evitando o
#   conflito.
#
# Por que SQLite :memory: e não lanchonete.db?
#   O banco em arquivo acumularia dados entre testes, quebrando o isolamento.
#   Com :memory:, cada conexão começa do zero — sem estado residual.
# =============================================================================

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from main import app

_TORTOISE_TEST_MODULES = {"models": ["infrastructure.tortoise.models"]}


@pytest_asyncio.fixture(autouse=True)
async def init_test_db():
    """Inicializa o banco SQLite em memória e cria as tabelas antes de cada teste.

    Por que isso é necessário?
        O Tortoise ORM precisa de uma conexão ativa para executar qualquer
        operação assíncrona de banco. Em testes, usamos :memory: para garantir
        que cada teste começa com um banco completamente vazio, sem depender
        de estado deixado por testes anteriores.

    O autouse=True faz este fixture rodar automaticamente para TODOS os
    testes, sem precisar declará-lo como parâmetro nas funções de teste.

    Fluxo (separado pelo yield):
        ANTES do teste:
            1. Tortoise.init()       → abre conexão com SQLite :memory:
            2. generate_schemas()    → cria as tabelas (ClienteModel, etc.)
        DEPOIS do teste:
            3. close_connections()   → fecha a conexão, destruindo o :memory:
    """
    await Tortoise.init(db_url="sqlite://:memory:", modules=_TORTOISE_TEST_MODULES)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture
async def client():
    """Cria um cliente HTTP assíncrono para testar a API sem subir um servidor real.

    O AsyncClient do httpx com ASGITransport despacha as requisições
    diretamente para o app FastAPI no mesmo event loop assíncrono do
    pytest-asyncio. Isso mantém compatibilidade com o Tortoise já
    inicializado pelo fixture init_test_db.

    Como o ASGITransport funciona?
        Ele implementa a interface ASGI, simulando as requisições HTTP
        dentro do processo Python, sem usar sockets de rede reais.
        Isso torna os testes muito mais rápidos.

    Como usar:
        async def test_exemplo(client):        # pytest injeta o client aqui
            r = await client.get("/health")
            assert r.status_code == 200
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

# tests/test_api_atividade.py
import pytest
from d

# =============================================================================
# 1. Integração — Promain.produto import Produto
oduto não encontrado
# =============================================================================

async def test_get_produto_inexistente(client):
    """GET /produtos/9999 com produto inexistente deve retornar 404."""
    response = await client.get("/produtos/9999")

    assert response.status_code == 404


# =============================================================================
# 2. Integração — Atualizar valor do produto
# =============================================================================

async def test_atualizar_valor_produto(client):
    """Cria produto e altera o valor via PUT. Verifica status 200 e {"alterou": true}."""
    await client.post("/produtos", json={
        "codigo": 1,
        "valor": 10.0,
        "tipo": 1,
        "desconto_percentual": 0.0
    })

    response = await client.put("/produtos/1/valor", json={"novo_valor": 25.99})

    assert response.status_code == 200
    assert response.json() == {"alterou": True}


# =============================================================================
# 3. End-to-end — Buscar pedido pelo código
# =============================================================================

async def test_buscar_pedido_por_codigo(client):
    """Cria pedido e busca via GET /lanchonete/pedidos/{cod_pedido}.
    Verifica status 200 e que o CPF retornado é o mesmo do cliente criado.
    """
    # 1. Cria cliente e produto
    await client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 1, "desconto_percentual": 0.0})

    # 2. Cria o pedido e salva o codigo
    r = await client.post("/lanchonete/pedidos", json={
        "cpf": "11122233344",
        "cod_produto": 1,
        "qtd_max_produtos": 5
    })
    assert r.status_code == 200
    cod_pedido = r.json()["codigo"]

    # 3. GET /lanchonete/pedidos/{cod_pedido}
    response = await client.get(f"/lanchonete/pedidos/{cod_pedido}")

    # 4. assert status_code == 200
    assert response.status_code == 200

    # 5. assert cpf == "11122233344"
    assert response.json()["cpf"] == "11122233344"


# =============================================================================
# 4. Integração — CPF vazio deve retornar 400
# =============================================================================

async def test_criar_cliente_cpf_vazio(client):
    """POST /clientes com CPF vazio deve retornar 400."""
    response = await client.post("/clientes", json={"cpf": "", "nome": "X"})

    assert response.status_code == 400


# =============================================================================
# 5. Sad path — Pedido com limite atingido
# =============================================================================

async def test_pedido_limite_atingido(client):
    """Cria pedido com qtd_max_produtos=1, tenta adicionar segundo produto.
    O segundo PUT deve retornar 400.
    """
    await client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 1, "desconto_percentual": 0.0})
    await client.post("/produtos", json={"codigo": 2, "valor": 20.0, "tipo": 2, "desconto_percentual": 0.0})

    # Cria pedido com limite 1 — produto 1 já ocupa a vaga na criação
    r = await client.post("/lanchonete/pedidos", json={
        "cpf": "11122233344",
        "cod_produto": 1,
        "qtd_max_produtos": 1
    })
    assert r.status_code == 200
    cod_pedido = r.json()["codigo"]

    # Tenta adicionar segundo produto — deve retornar 400
    response = await client.put(f"/lanchonete/pedidos/{cod_pedido}/itens", json={"cod_produto": 2})

    assert response.status_code == 400
