import json
from pathlib import Path
from typing import Optional

from models.document import Document
from repositories.base_repository import BaseRepository
from expections.expections import DocumentNotFoundError, DuplicateDocumentError

class DocumentRepository(BaseRepository[Document]):

    _BASE_DIR = Path(__file__).parent.parent
    _DATA_DIR = _BASE_DIR / 'data'

    def __init__(self):
         self._DATA_DIR.mkdir(parents=True, exist_ok=True)

    # PRIVATE METHODS
    def _ensure_file_exists(self) -> None:
        self._path.touch(exist_ok=True)
    
    def _file_path(self, document_title: str) -> Path:
        return self._DATA_DIR / f"{document_title}.txt"
    
    def _read_file(self, document_title: str) -> Document:
        path = self._file_path(document_title)

        if not path.exists():
            raise DocumentNotFoundError(f"Documento {document_title} não foi encontrado.")
        
        lines = path.read_text(encoding="utf-8").splitlines()

        return Document(title=document_title, content="\n".join(lines))
    
    def _write_file(self, document: Document) -> None:
        path = self._file_path(document.title)

        path.write_text(document.content, encoding="utf-8")

    # PUBLIC METHODS
    def create(self, document: Document) -> None:
        if self._file_path(document.title).exists():
            raise DuplicateDocumentError(f"Documento {document.title} já existe no sistema.")
        
        self._write_file(document)

    def read(self, document_title: str) -> Document:
        if not self._file_path(document_title).exists():
            raise DocumentNotFoundError(f"Documento {document_title} não foi encontrado.")
        
        return self._read_file(document_title)

    def delete(self, document_title: str):
        path = self._file_path(document_title)

        if not path.exists():
            raise DocumentNotFoundError(f"Documento {document_title} não foi encontrado.")

        path.unlink()

    def update(self, document_title: str, updated_document: Document) -> None:
        if not self._file_path(document_title).exists():
            raise DocumentNotFoundError(f"Documento {document_title} não foi encontrado.")
        
        self._write_file(updated_document)

    def read_all(self) -> list[Document]:
        documents = []

        for file in self._DATA_DIR.glob("*.txt"):
            document = self._read_file(file.stem)
            documents.append(document)

        return documents