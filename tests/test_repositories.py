import pytest
import tempfile
from pathlib import Path
from models.document import Document
from repositories.document_repository import DocumentRepository
from expections.expections import DocumentNotFoundError, DuplicateDocumentError


@pytest.fixture
def temp_data_dir():
    """Cria um diretório temporário para dados de teste"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def repo_with_temp_dir(temp_data_dir, monkeypatch):
    """Cria um repositório que usa diretório temporário"""
    repo = DocumentRepository()
    # Substitui o diretório de dados pelo temporário
    monkeypatch.setattr(repo, '_DATA_DIR', temp_data_dir)
    return repo


class TestDocumentRepository:
    """Testes para a classe DocumentRepository"""

    def test_create_document(self, repo_with_temp_dir):
        """Testa criação de documento"""
        doc = Document(title="Test Doc", content="Test content")
        repo_with_temp_dir.create(doc)
        
        # Verifica que o arquivo foi criado
        file_path = repo_with_temp_dir._file_path("Test Doc")
        assert file_path.exists()

    def test_read_document(self, repo_with_temp_dir):
        """Testa leitura de documento"""
        # Cria documento primeiro
        original_doc = Document(title="Test Doc", content="Test content")
        repo_with_temp_dir.create(original_doc)
        
        # Lê documento
        read_doc = repo_with_temp_dir.read("Test Doc")
        assert read_doc.title == "Test Doc"
        assert read_doc.content == "Test content"

    def test_read_nonexistent_document(self, repo_with_temp_dir):
        """Testa leitura de documento inexistente"""
        with pytest.raises(DocumentNotFoundError, match="não foi encontrado"):
            repo_with_temp_dir.read("Nonexistent Doc")

    def test_create_duplicate_document(self, repo_with_temp_dir):
        """Testa que DuplicateDocumentError é lançado ao criar documento duplicado"""
        doc = Document(title="Test Doc", content="Test content")
        repo_with_temp_dir.create(doc)
        
        # Tenta criar documento com mesmo título
        with pytest.raises(DuplicateDocumentError, match="já existe no sistema"):
            repo_with_temp_dir.create(doc)

    def test_update_document(self, repo_with_temp_dir):
        """Testa atualização de documento"""
        # Cria documento
        original_doc = Document(title="Test Doc", content="Original content")
        repo_with_temp_dir.create(original_doc)
        
        # Atualiza documento
        updated_doc = Document(title="Test Doc", content="Updated content")
        repo_with_temp_dir.update("Test Doc", updated_doc)
        
        # Verifica atualização
        read_doc = repo_with_temp_dir.read("Test Doc")
        assert read_doc.content == "Updated content"

    def test_update_nonexistent_document(self, repo_with_temp_dir):
        """Testa que erro é lançado ao atualizar documento inexistente"""
        doc = Document(title="Test Doc", content="Content")
        with pytest.raises(DocumentNotFoundError, match="não foi encontrado"):
            repo_with_temp_dir.update("Nonexistent Doc", doc)

    def test_delete_document(self, repo_with_temp_dir):
        """Testa exclusão de documento"""
        # Cria documento
        doc = Document(title="Test Doc", content="Test content")
        repo_with_temp_dir.create(doc)
        
        # Deleta documento
        repo_with_temp_dir.delete("Test Doc")
        
        # Verifica que arquivo foi deletado
        file_path = repo_with_temp_dir._file_path("Test Doc")
        assert not file_path.exists()

    def test_delete_nonexistent_document(self, repo_with_temp_dir):
        """Testa que erro é lançado ao deletar documento inexistente"""
        with pytest.raises(DocumentNotFoundError, match="não foi encontrado"):
            repo_with_temp_dir.delete("Nonexistent Doc")

    def test_read_all_documents(self, repo_with_temp_dir):
        """Testa leitura de todos os documentos"""
        # Cria múltiplos documentos
        doc1 = Document(title="Doc1", content="Content 1")
        doc2 = Document(title="Doc2", content="Content 2")
        doc3 = Document(title="Doc3", content="Content 3")
        
        repo_with_temp_dir.create(doc1)
        repo_with_temp_dir.create(doc2)
        repo_with_temp_dir.create(doc3)
        
        # Lê todos
        docs = repo_with_temp_dir.read_all()
        
        assert len(docs) == 3
        titles = {doc.title for doc in docs}
        assert titles == {"Doc1", "Doc2", "Doc3"}

    def test_read_all_empty_repository(self, repo_with_temp_dir):
        """Testa read_all em repositório vazio"""
        docs = repo_with_temp_dir.read_all()
        assert len(docs) == 0
        assert docs == []
