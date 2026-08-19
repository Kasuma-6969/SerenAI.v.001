# memory/mlp.py
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import uuid

class MemoriaLargoPlazo:
    def __init__(self, ruta_persistencia):
        self.cliente = chromadb.PersistentClient(path=str(ruta_persistencia))
        self.funcion_embedding = embedding_functions.DefaultEmbeddingFunction()
        
        try:
            self.coleccion = self.cliente.get_collection(
                name="recuerdos", 
                embedding_function=self.funcion_embedding
            )
        except:
            self.coleccion = self.cliente.create_collection(
                name="recuerdos", 
                embedding_function=self.funcion_embedding
            )

    def guardar_recuerdo(self, texto, tipo="general", importancia=0.5):
        id_unico = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        self.coleccion.add(
            documents=[texto],
            ids=[id_unico],
            metadatas=[{
                "tipo": tipo,
                "timestamp": timestamp, 
                "importancia": importancia,
                "accesos": 0, 
                "ultimo_acceso": timestamp
            }]
        )
        return id_unico

    def buscar_recuerdos(self, consulta, n_resultados=3):
        resultados = self.coleccion.query(
            query_texts=[consulta], 
            n_results=n_resultados
        )
        for doc_id in resultados['ids'][0]:
            self._incrementar_acceso(doc_id)
        return resultados['documents'][0] if resultados['documents'][0] else []

    def _incrementar_acceso(self, doc_id):
        recuerdo = self.coleccion.get(ids=[doc_id])
        if recuerdo['metadatas']:
            meta = recuerdo['metadatas'][0]
            meta['accesos'] = meta.get('accesos', 0) + 1
            meta['ultimo_acceso'] = datetime.now().isoformat()
            self.coleccion.update(ids=[doc_id], metadatas=[meta])

    def podar_recuerdos_obsoletos(self, max_dias_inactivo=30):
        """ESPACIO RESERVADO PARA FUTURO OLVIDO INTELIGENTE"""
        print("Función de poda aún no implementada.")
        pass