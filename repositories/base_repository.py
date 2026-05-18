from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, document: T) -> None:
        """Criar novo documento no repositório."""
        pass

    @abstractmethod
    def read(self, document_title: str) -> Optional[T]:
        """Ler o documento pelo nome."""
        pass

    @abstractmethod
    def update(self, document_title: str, updated_document: T) -> None:
        """Atualizar um documento existente no repositório."""
        pass

    @abstractmethod
    def delete(self, document_title: str) -> None:
        """Excluir um documento do repositório pelo seu nome."""
        pass

    @abstractmethod
    def read_all(self) -> list[T]:
        """Listar todos os documentos no repositório."""
        pass