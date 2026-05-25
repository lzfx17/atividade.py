# Lanchonete API

API REST para gerenciamento de clientes, produtos e pedidos de uma lanchonete, construída com **FastAPI** e **Python 3.12**.

---

## Requisitos

- Python 3.12
- pip

---

## Configuração do ambiente

### 1. Criar o ambiente virtual

```bash
sudo apt install python3.12-venv   # caso não tenha o módulo venv
python3 -m venv venv
```

### 2. Ativar / desativar o venv

```bash
source venv/bin/activate    # ativar
source venv/bin/deactivate  # desativar
```

### 3. Instalar dependências

```bash
pip install "fastapi[standard]"
```

---

## Executar o projeto

```bash
fastapi dev main.py
```

---

## Testes

### Instalar dependências de teste

```bash
pip install pytest httpx
```

### Rodar os testes

```bash
pytest -q
```

---

## Estrutura do projeto

```
main.py
api/
    __init__.py
    routes/
        __init__.py
        clientes.py
        health.py
        pedidos.py
        produtos.py
domain/
    __init__.py
    cliente.py
    pedido.py
    produto.py
repositories/
    __init__.py
    memory.py
schemas/
    __init__.py
    cliente.py
    pedido.py
    produto.py
services/
    __init__.py
    lanchonete_service.py
tests/
    conftest.py
    test_api_clientes.py
    test_api_pedidos.py
    test_domain_pedido.py
    test_domain_produto.py
```

---

## Deploy

### Gerar `requirements.txt`

```bash
# Com pip
pip freeze > requirements.txt

# Com poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Desinstalar todas as bibliotecas

```bash
pip freeze > uninstall.txt
pip uninstall -r uninstall.txt -y
```