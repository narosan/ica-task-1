import pytest
from unittest.mock import MagicMock
from services.document_service import DocumentService
from repositories.document_repository import DocumentRepository
from models.document import Document

@pytest.fixture
def mock_repository():
    return MagicMock(spec=DocumentRepository)

@pytest.fixture
def document_service(mock_repository):
    return DocumentService(mock_repository)

@pytest.fixture
def sample_document():
    return Document(title="Sample Document", content="This is a sample document.")