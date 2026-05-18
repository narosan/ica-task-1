import pytest
from models.document import Document


class TestDocument:
    """Testes para a classe Document"""

    def test_create_valid_document(self):
        """Testa criação de documento válido"""
        doc = Document(title="Test Doc", content="This is test content")
        assert doc.title == "Test Doc"
        assert doc.content == "This is test content"

    def test_document_with_empty_title(self):
        """Testa que ValueError é lançado com título vazio"""
        with pytest.raises(ValueError, match="Titulo não pode ser vazio"):
            Document(title="", content="Some content")

    def test_document_with_empty_content(self):
        """Testa que ValueError é lançado com conteúdo vazio"""
        with pytest.raises(ValueError, match="Conteúdo não pode ser vazio"):
            Document(title="Valid Title", content="")

    def test_document_with_none_title(self):
        """Testa que ValueError é lançado com título None"""
        with pytest.raises(ValueError, match="Titulo não pode ser vazio"):
            Document(title=None, content="Some content")

    def test_document_with_none_content(self):
        """Testa que ValueError é lançado com conteúdo None"""
        with pytest.raises(ValueError, match="Conteúdo não pode ser vazio"):
            Document(title="Valid Title", content=None)

    def test_document_dict_representation(self):
        """Testa representação de Document em dicionário"""
        doc = Document(title="Test", content="Content")
        doc_dict = doc.__dict__
        assert "title" in doc_dict
        assert "content" in doc_dict
        assert doc_dict["title"] == "Test"
        assert doc_dict["content"] == "Content"
