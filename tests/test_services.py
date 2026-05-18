import pytest
from unittest.mock import Mock, MagicMock, patch
from models.document import Document
from services.document_service import DocumentService
from expections.expections import DocumentNotFoundError


@pytest.fixture
def mock_repository():
    """Cria um mock do repositório"""
    return Mock()


@pytest.fixture
def document_service(mock_repository):
    """Cria um serviço com repositório mock"""
    return DocumentService(mock_repository)


class TestDocumentService:
    """Testes para a classe DocumentService"""

    def test_create_document(self, document_service, mock_repository):
        """Testa criação de documento através do serviço"""
        document_service.create_document("Test Title", "Test Content")
        
        # Verifica que repositório.create foi chamado
        mock_repository.create.assert_called_once()
        call_args = mock_repository.create.call_args[0][0]
        assert call_args.title == "Test Title"
        assert call_args.content == "Test Content"

    def test_read_document(self, document_service, mock_repository):
        """Testa leitura de documento através do serviço"""
        expected_doc = Document(title="Test", content="Content")
        mock_repository.read.return_value = expected_doc
        
        result = document_service.read_document("Test")
        
        mock_repository.read.assert_called_once_with("Test")
        assert result == expected_doc

    def test_read_nonexistent_document(self, document_service, mock_repository):
        """Testa leitura de documento inexistente"""
        mock_repository.read.side_effect = DocumentNotFoundError("Not found")
        
        with pytest.raises(DocumentNotFoundError):
            document_service.read_document("Nonexistent")

    def test_delete_document(self, document_service, mock_repository):
        """Testa exclusão de documento"""
        document_service.delete_document("Test")
        
        mock_repository.delete.assert_called_once_with("Test")

    def test_update_document(self, document_service, mock_repository):
        """Testa atualização de documento"""
        document_service.update_document("Test", "New Content")
        
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args[0]
        assert call_args[0] == "Test"
        assert call_args[1].title == "Test"
        assert call_args[1].content == "New Content"

    def test_list_documents(self, document_service, mock_repository):
        """Testa listagem de documentos"""
        expected_docs = [
            Document(title="Doc1", content="Content 1"),
            Document(title="Doc2", content="Content 2"),
        ]
        mock_repository.read_all.return_value = expected_docs
        
        result = document_service.list_documents()
        
        mock_repository.read_all.assert_called_once()
        assert result == expected_docs
        assert len(result) == 2

    def test_list_empty_documents(self, document_service, mock_repository):
        """Testa listagem quando não há documentos"""
        mock_repository.read_all.return_value = []
        
        result = document_service.list_documents()
        
        assert result == []
        assert len(result) == 0
