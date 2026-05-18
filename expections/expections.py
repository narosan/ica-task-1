class DocumentNotFoundError(Exception):
    """Exceção aciona quando o documento não é encontrado."""
    pass

class DuplicateDocumentError(Exception):
    """Exceção aciona quando um documento duplicado é encontrado."""
    pass