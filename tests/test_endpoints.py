import pytest
import json
import tempfile
from pathlib import Path
from models.document import Document
from repositories.document_repository import DocumentRepository
from services.document_service import DocumentService
import sys

# Adiciona a pasta raiz ao path para importar main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app


@pytest.fixture
def client():
    """Cria um cliente de teste Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_data_dir(monkeypatch):
    """Cria um diretório temporário para dados de teste"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Substitui o diretório de dados pelo temporário
        temp_path = Path(tmpdir)
        monkeypatch.setattr('main._repo._DATA_DIR', temp_path)
        yield temp_path


@pytest.fixture
def app_with_temp_dir(monkeypatch):
    """Configura app com diretório temporário"""
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)
        # Recria repositório com diretório temporário
        from main import _repo
        monkeypatch.setattr(_repo, '_DATA_DIR', temp_path)
        yield temp_path


class TestCreateEndpoint:
    """Testes para endpoint POST /create"""

    def test_create_document_success(self, client, app_with_temp_dir):
        """Testa criação bem-sucedida de documento"""
        payload = {
            "title": "Test Document",
            "content": "This is test content"
        }
        response = client.post(
            '/create',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "Documento criado com sucesso."

    def test_create_document_missing_title(self, client, app_with_temp_dir):
        """Testa criação com título faltando"""
        payload = {
            "content": "This is test content"
        }
        response = client.post(
            '/create',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_document_missing_content(self, client, app_with_temp_dir):
        """Testa criação com conteúdo faltando"""
        payload = {
            "title": "Test Document"
        }
        response = client.post(
            '/create',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_duplicate_document(self, client, app_with_temp_dir):
        """Testa criação de documento duplicado"""
        payload = {
            "title": "Test Document",
            "content": "Content"
        }
        
        # Primeira criação
        response1 = client.post(
            '/create',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response1.status_code == 200
        
        # Segunda criação com mesmo título
        response2 = client.post(
            '/create',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response2.status_code == 400
        data = response2.get_json()
        assert "error" in data


class TestReadEndpoint:
    """Testes para endpoint GET /read/<title>"""

    def test_read_existing_document(self, client, app_with_temp_dir):
        """Testa leitura de documento existente"""
        # Primeiro cria um documento
        create_payload = {
            "title": "Test Document",
            "content": "This is test content"
        }
        client.post(
            '/create',
            data=json.dumps(create_payload),
            content_type='application/json'
        )
        
        # Depois lê
        response = client.get('/read/Test Document')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Test Document"
        assert data["content"] == "This is test content"

    def test_read_nonexistent_document(self, client, app_with_temp_dir):
        """Testa leitura de documento inexistente"""
        response = client.get('/read/Nonexistent')
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestUpdateEndpoint:
    """Testes para endpoint PUT /update/<title>"""

    def test_update_document_success(self, client, app_with_temp_dir):
        """Testa atualização bem-sucedida"""
        # Cria documento
        create_payload = {
            "title": "Test Document",
            "content": "Original content"
        }
        client.post(
            '/create',
            data=json.dumps(create_payload),
            content_type='application/json'
        )
        
        # Atualiza
        update_payload = {
            "content": "Updated content"
        }
        response = client.put(
            '/update/Test Document',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Documento atualizado com sucesso."

    def test_update_nonexistent_document(self, client, app_with_temp_dir):
        """Testa atualização de documento inexistente"""
        update_payload = {
            "content": "Updated content"
        }
        response = client.put(
            '/update/Nonexistent',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestDeleteEndpoint:
    """Testes para endpoint DELETE /delete/<title>"""

    def test_delete_existing_document(self, client, app_with_temp_dir):
        """Testa exclusão de documento existente"""
        # Cria documento
        create_payload = {
            "title": "Test Document",
            "content": "Content"
        }
        client.post(
            '/create',
            data=json.dumps(create_payload),
            content_type='application/json'
        )
        
        # Deleta
        response = client.delete('/delete/Test Document')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Documento excluído com sucesso."

    def test_delete_nonexistent_document(self, client, app_with_temp_dir):
        """Testa exclusão de documento inexistente"""
        response = client.delete('/delete/Nonexistent')
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestListEndpoint:
    """Testes para endpoint GET /list"""

    def test_list_documents_empty(self, client, app_with_temp_dir):
        """Testa listagem de documentos vazio"""
        response = client.get('/list')
        
        assert response.status_code == 200
        data = response.get_json()
        assert "documents" in data
        assert data["documents"] == []

    def test_list_documents_multiple(self, client, app_with_temp_dir):
        """Testa listagem com múltiplos documentos"""
        # Cria múltiplos documentos
        for i in range(3):
            payload = {
                "title": f"Document {i}",
                "content": f"Content {i}"
            }
            client.post(
                '/create',
                data=json.dumps(payload),
                content_type='application/json'
            )
        
        # Lista
        response = client.get('/list')
        
        assert response.status_code == 200
        data = response.get_json()
        assert "documents" in data
        assert len(data["documents"]) == 3

    def test_list_documents_structure(self, client, app_with_temp_dir):
        """Testa estrutura de documentos na listagem"""
        # Cria documento
        payload = {
            "title": "Test Doc",
            "content": "Test Content"
        }
        client.post(
            '/create',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Lista
        response = client.get('/list')
        
        data = response.get_json()
        assert len(data["documents"]) == 1
        doc = data["documents"][0]
        assert "title" in doc
        assert "content" in doc
        assert doc["title"] == "Test Doc"
        assert doc["content"] == "Test Content"
