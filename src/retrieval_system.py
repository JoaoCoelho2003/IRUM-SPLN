import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from config import *
from utils import load_json

class InformationRetrievalSystem:    
    def __init__(self, model_path: str = MODEL_DIR):
        self.model = None
        self.documents = []
        self.document_embeddings = None
        self.load_model(model_path)
    
    def load_model(self, model_path: str) -> None:
        try:
            self.model = SentenceTransformer(model_path)
            print(f"Modelo carregado de: {model_path}")
        except:
            print(f"Erro ao carregar modelo de: {model_path}")
            print("A carregar modelo base...")
            self.model = SentenceTransformer(BASE_MODEL)
    
    def load_collection(self, filepath: str = JSON_FILE) -> None:
        self.documents = load_json(filepath)
        print(f"Carregados {len(self.documents)} documentos")
        
        self._precompute_embeddings()
    
    def _precompute_embeddings(self) -> None:
        print("A calcular embeddings dos documentos...")
        
        abstracts = [doc['abstract'] for doc in self.documents]
        self.document_embeddings = self.model.encode(
            abstracts, 
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print("Embeddings calculados!")
    
    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents or self.document_embeddings is None:
            raise ValueError("Coleção não foi carregada")
        
        print(f"A processar query: '{query}'")
        
        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]
        
        similarities = self._calculate_similarities(query_embedding)
        
        ranked_indices = np.argsort(similarities)[::-1]
        
        results = []
        for i in ranked_indices[:top_k]:
            results.append((self.documents[i], float(similarities[i])))
        
        return results
    
    def _calculate_similarities(self, query_embedding: np.ndarray) -> np.ndarray:
        similarities = np.dot(self.document_embeddings, query_embedding) / (
            np.linalg.norm(self.document_embeddings, axis=1) * 
            np.linalg.norm(query_embedding)
        )
        
        return similarities
    
    def search_and_display(self, query: str, top_k: int = 5) -> None:
        results = self.retrieve(query, top_k)
        
        print(f"\n{'='*80}")
        print(f"RESULTADOS PARA: '{query}'")
        print(f"{'='*80}")
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n{i}. SCORE: {score:.4f}")
            print(f"TÍTULO: {doc['title']}")
            print(f"AUTORES: {', '.join(doc.get('authors', []))}")
            print(f"DATA: {doc.get('date', 'N/A')}")
            print(f"ABSTRACT: {doc['abstract'][:300]}...")
            
            if doc.get('keywords'):
                print(f"KEYWORDS: {', '.join(doc['keywords'][:5])}")
            
            print("-" * 80)
    
    def evaluate_retrieval(self, test_queries: List[Dict[str, Any]]) -> Dict[str, float]:
        print("A avaliar sistema de retrieval...")
        
        precisions = []
        recalls = []
        
        for query_data in test_queries:
            query = query_data['query']
            relevant_docs = set(query_data['relevant_docs'])
            
            results = self.retrieve(query, top_k=20)
            retrieved_docs = {doc['id'] for doc, _ in results}
            
            if retrieved_docs:
                precision = len(relevant_docs.intersection(retrieved_docs)) / len(retrieved_docs)
                precisions.append(precision)
            
            if relevant_docs:
                recall = len(relevant_docs.intersection(retrieved_docs)) / len(relevant_docs)
                recalls.append(recall)
        
        avg_precision = np.mean(precisions) if precisions else 0.0
        avg_recall = np.mean(recalls) if recalls else 0.0
        f1_score = 2 * avg_precision * avg_recall / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0.0
        
        metrics = {
            'precision': avg_precision,
            'recall': avg_recall,
            'f1_score': f1_score
        }
        
        print(f"Métricas de retrieval:")
        print(f"Precisão: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1_score']:.4f}")
        
        return metrics

def main():
    ir_system = InformationRetrievalSystem()
    
    ir_system.load_collection()
    
    test_queries = [
        "machine learning algorithms",
        "redes neurais artificiais",
        "processamento de linguagem natural",
        "inteligência artificial",
        "algoritmos de otimização"
    ]
    
    for query in test_queries:
        ir_system.search_and_display(query, top_k=3)
        print("\n" + "="*100 + "\n")

if __name__ == "__main__":
    main()
