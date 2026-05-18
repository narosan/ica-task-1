from dataclasses import dataclass, field

@dataclass
class Document:
    title: str
    content: str

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("Titulo não pode ser vazio.")
        if not self.content:
            raise ValueError("Conteúdo não pode ser vazio.")