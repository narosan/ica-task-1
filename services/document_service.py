from models.document import Document
from repositories.base_repository import BaseRepository

class DocumentService:
    def __init__(self, repository: BaseRepository[Document]):
        self.repository = repository

    def create_document(self, title: str, content: str):
        document = Document(title=title, content=content)
        return self.repository.create(document)

    def read_document(self, title):
        return self.repository.read(title)

    def delete_document(self, title):
        self.repository.delete(title)

    def update_document(self, title, new_content):
        updated_document = Document(title=title, content=new_content)
        return self.repository.update(title, updated_document)

    def list_documents(self):
        return self.repository.read_all()