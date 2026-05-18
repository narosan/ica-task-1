from flask import Flask, request
from flasgger import Swagger

from repositories.document_repository import DocumentRepository
from services.document_service import DocumentService

_repo = DocumentRepository()
document_service = DocumentService(_repo)

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/create', methods=['POST'])
def create_document():
    """
    Endpoint para criar um novo documento.
    ---
    tags:
      - Create Document
    parameters:
      - in: body
        name: document
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
    responses:
      200:
        description: Documento criado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
    """
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        document_service.create_document(title, content)
        return {'message': 'Documento criado com sucesso.'}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/read/<title>', methods=['GET'])
def read_document(title):
    """
    Endpoint para ler um documento existente.
    ---
    tags:
      - Read Document
    parameters:
      - in: path
        name: title
        type: string
        required: true
    responses:
      200:
        description: Retorna um documento específico.
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
    """
    try:
        doc = document_service.read_document(title)
        return {'title': doc.title, 'content': doc.content}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/delete/<title>', methods=['DELETE'])
def delete_document(title):
    """
    Endpoint para excluir um documento existente.
    ---
    tags:
      - Delete Document
    parameters:
      - in: path
        name: title
        type: string
        required: true
    responses:
      200:
        description: Documento excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
    """
    try:
        document_service.delete_document(title)
        return {'message': 'Documento excluído com sucesso.'}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/update/<title>', methods=['PUT'])
def update_document(title):
    """
    Endpoint para atualizar um documento existente.
    ---
    tags:
      - Update Document
    parameters:
      - in: path
        name: title
        type: string
        required: true
      - in: body
        name: document
        schema:
          type: object
          properties:
            content:
              type: string
    responses:
      200:
        description: Documento atualizado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
    """
    try:
        data = request.get_json()
        new_content = data.get('content')
        document_service.update_document(title, new_content)
        return {'message': 'Documento atualizado com sucesso.'}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/list', methods=['GET'])
def list_documents():
    """
    Endpoint para listar todos os documentos existentes.
    ---
    tags:
      - List Documents
    responses:
      200:
        description: Lista de documentos.
        schema:
          type: object
          properties:
            documents:
              type: array
              items:
                type: object
                properties:
                  title:
                    type: string
                  content:
                    type: string
    """
    try:
        documents = document_service.list_documents()
        return {'documents': [doc.__dict__ for doc in documents]}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == "__main__":
    app.run(debug=True)