# 📄 Document CRUD API

API REST em Flask para criação e gerenciamento de documentos em arquivos `.txt`, seguindo princípios de Clean Code e Design Patterns (Repository Pattern, Dependency Injection, SRP).

---

## 🗂️ Estrutura do Projeto

```
ica-task-1/
├── models/
│   └── document.py            # Dataclass — entidade principal
├── repositories/
│   ├── base_repository.py     # Interface ABC (equivalente ao IRepository<T> do C#)
│   └── document_repository.py # Implementação concreta — lê/escreve arquivos .txt
├── services/
│   └── document_service.py    # Regras de negócio — camada de serviço
├── exceptions/
│   └── exceptions.py          # Exceções customizadas
├── tests/
│   ├── conftest.py            # Fixtures do pytest
│   └── test_document_service.py
├── data/                      # Gerado automaticamente — armazena os .txt
├── app.py                     # Entry point Flask
├── Dockerfile
└── .dockerignore
```

### Responsabilidade de cada camada

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| Model | `document.py` | Define a entidade e valida os dados |
| Repository | `document_repository.py` | Lê e escreve arquivos `.txt` em `/data` |
| Service | `document_service.py` | Orquestra as regras de negócio |
| API | `app.py` | Expõe os endpoints HTTP |

---

## ✅ Pré-requisitos

- Python `3.12+`
- pip
- Docker (opcional)

---

## 🐍 Executando sem Docker

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/ica-task-1.git
cd ica-task-1
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install flask pytest
```

### 4. Execute a aplicação

```bash
flask run
```

A API estará disponível em: `http://localhost:5000`

O Swagger estará disponível em: `http://localhost:5000/apidocs`

---

## 🐳 Executando com Docker

### 1. Build da imagem

```bash
docker build -t document-api .
```

### 2. Rode o container

```bash
# Windows (PowerShell)
docker run -p 5000:5000 -v ${PWD}/data:/app/data document-api

# Linux / macOS
docker run -p 5000:5000 -v $(pwd)/data:/app/data document-api
```

> O `-v` mapeia a pasta `/data` do container para sua máquina local,
> garantindo que os arquivos `.txt` **persistam** entre execuções do container.

A API estará disponível em: `http://localhost:5000`

O Swagger estará disponível em: `http://localhost:5000/apidocs`

---

## 🔌 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/documents` | Cria um novo documento (gera um `.txt` em `/data`) |
| `GET` | `/documents` | Lista todos os documentos |
| `GET` | `/documents/<id>` | Busca um documento pelo ID |
| `PUT` | `/documents/<id>` | Atualiza um documento existente |
| `DELETE` | `/documents/<id>` | Remove o documento e o arquivo `.txt` |

### Exemplos de uso

```bash
# Criar documento
curl -X POST http://localhost:5000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "Meu Doc", "content": "Conteúdo aqui"}'

# Listar todos
curl http://localhost:5000/documents

# Buscar por ID
curl http://localhost:5000/documents/{id}

# Atualizar
curl -X PUT http://localhost:5000/documents/{id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Novo título", "content": "Novo conteúdo"}'

# Deletar
curl -X DELETE http://localhost:5000/documents/{id}
```

---

## 🧪 Executando os testes com pytest

### Sem Docker

```bash
# Windows (PowerShell) — exibe as últimas 50 linhas do output
python -m pytest tests/ -v --tb=line 2>&1 | Select-Object -Last 50

# Linux / macOS
python -m pytest tests/ -v --tb=line 2>&1 | tail -50
```

### Com Docker

```bash
docker run --rm document-api python -m pytest tests/ -v --tb=line
```

### O que cada flag significa

| Flag | Descrição |
|---|---|
| `-v` | Verbose — exibe o nome de cada teste |
| `--tb=line` | Traceback resumido — mostra só a linha do erro |
| `2>&1` | Redireciona stderr para stdout |
| `Select-Object -Last 50` | Exibe apenas as últimas 50 linhas (PowerShell) |

### Saída esperada

```
tests/test_document_service.py::TestAddDocument::test_creates_new_file_on_each_call PASSED
tests/test_document_service.py::TestAddDocument::test_returns_document_with_generated_id PASSED
tests/test_document_service.py::TestAddDocument::test_empty_title_raises PASSED
tests/test_document_service.py::TestGetDocument::test_get_existing_document PASSED
tests/test_document_service.py::TestGetDocument::test_get_nonexistent_raises PASSED
tests/test_document_service.py::TestDeleteDocument::test_delete_removes_file PASSED

====== 6 passed in 0.42s ======
```

---

## 📐 Design Patterns aplicados

| Pattern | Onde | Descrição |
|---|---|---|
| **Repository** | `base_repository.py` + `document_repository.py` | Isola o acesso a dados do restante da aplicação |
| **Dependency Injection** | `DocumentService.__init__` | Recebe a interface, não a implementação concreta |
| **Fail Fast** | `Document.__post_init__` | Valida os dados no momento da criação |

---

## 📁 Como os arquivos são salvos

Cada chamada ao `POST /documents` gera um arquivo `.txt` exclusivo dentro de `/data`:

```
data/
├── 3f2a1b4c-uuid.txt   ← POST #1
├── 9e8d7c6b-uuid.txt   ← POST #2
└── 1a2b3c4d-uuid.txt   ← POST #3
```

Formato interno do `.txt`:

```
3f2a1b4c-...     ← linha 1: id
Meu Documento    ← linha 2: title
Conteúdo aqui    ← linha 3+: content (pode ter múltiplas linhas)
```
