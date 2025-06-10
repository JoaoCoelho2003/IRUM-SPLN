import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from config import *
from utils import load_json
from query_processor import QueryProcessor
from caching_system import EmbeddingCache


class InformationRetrievalSystem:
    def __init__(self, model_path: str = MODEL_DIR):
        self.model = None
        self.documents = []
        self.document_embeddings = None
        self.query_processor = QueryProcessor()
        self.cache = EmbeddingCache()
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
        print("A verificar cache de embeddings dos documentos...")

        model_name = self.model._modules["0"].auto_model.config.name_or_path
        abstracts = [doc["abstract"] for doc in self.documents]

        cached_embeddings = self.cache.batch_get_embeddings(abstracts, model_name)

        if len(cached_embeddings) == len(abstracts):
            print(f"✅ Todos os {len(abstracts)} embeddings encontrados em cache!")
            self.document_embeddings = np.array(
                [cached_embeddings[abstract] for abstract in abstracts]
            )
        else:
            print(
                f"📊 Cache: {len(cached_embeddings)}/{len(abstracts)} embeddings encontrados"
            )
            print("A calcular embeddings em falta...")

            uncached_abstracts = [
                abstract for abstract in abstracts if abstract not in cached_embeddings
            ]

            if uncached_abstracts:
                new_embeddings = self.model.encode(
                    uncached_abstracts, show_progress_bar=True, convert_to_numpy=True
                )

                embedding_pairs = list(zip(uncached_abstracts, new_embeddings))
                self.cache.batch_store_embeddings(embedding_pairs, model_name)
                print(
                    f"💾 {len(uncached_abstracts)} novos embeddings guardados em cache"
                )

            all_embeddings = []
            for abstract in abstracts:
                if abstract in cached_embeddings:
                    all_embeddings.append(cached_embeddings[abstract])
                else:
                    embedding = self.model.encode([abstract], convert_to_numpy=True)[0]
                    all_embeddings.append(embedding)
                    self.cache.store_embedding(abstract, model_name, embedding)

            self.document_embeddings = np.array(all_embeddings)

        cache_stats = self.cache.get_cache_stats()
        print(
            f"📈 Cache stats: {cache_stats['memory_cached_items']} em memória, {cache_stats['disk_cached_items']} em disco"
        )
        print("Embeddings dos documentos prontos!")

    def retrieve(
        self, query: str, top_k: int = 10
    ) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents or self.document_embeddings is None:
            raise ValueError("Coleção não foi carregada")

        print(f"A processar query: '{query}'")

        processed_query_data = self.query_processor.process_query(query)

        enhanced_query = self.query_processor.enhance_query_for_similarity(
            processed_query_data
        )

        final_query = enhanced_query if enhanced_query.strip() else query

        print(f"Query processada: '{processed_query_data['processed_query']}'")
        print(f"Tipo de query: {processed_query_data['query_type']}")

        model_name = self.model._modules["0"].auto_model.config.name_or_path
        cached_query_embedding = self.cache.get_embedding(final_query, model_name)

        if cached_query_embedding is not None:
            print("🚀 Embedding da query encontrado em cache!")
            query_embedding = cached_query_embedding
        else:
            print("🔄 A calcular embedding da query...")
            query_embedding = self.model.encode([final_query], convert_to_numpy=True)[0]
            self.cache.store_embedding(final_query, model_name, query_embedding)
            print("💾 Embedding da query guardado em cache")

        similarities = self._calculate_similarities(query_embedding)

        similarities = self._apply_query_processing_boost(
            similarities, processed_query_data
        )

        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for i in ranked_indices[:top_k]:
            results.append((self.documents[i], float(similarities[i])))

        return results

    def _calculate_similarities(self, query_embedding: np.ndarray) -> np.ndarray:
        similarities = np.dot(self.document_embeddings, query_embedding) / (
            np.linalg.norm(self.document_embeddings, axis=1)
            * np.linalg.norm(query_embedding)
        )

        return similarities

    def _apply_query_processing_boost(
        self, similarities: np.ndarray, processed_query_data: Dict[str, Any]
    ) -> np.ndarray:

        query_keywords = processed_query_data["keywords"]

        if not query_keywords:
            return similarities

        boosted_similarities = similarities.copy()

        for i, doc in enumerate(self.documents):
            boost_factor = 1.0

            doc_keywords = [kw.lower().strip() for kw in doc.get("keywords", [])]
            keyword_matches = sum(
                1 for token in query_keywords if token in doc_keywords
            )
            if keyword_matches > 0:
                boost_factor += 0.1 * keyword_matches

            doc_title = doc.get("title", "").lower()
            title_matches = sum(1 for token in query_keywords if token in doc_title)
            if title_matches > 0:
                boost_factor += 0.15 * title_matches

            boost_factor = min(boost_factor, 1.5)
            boosted_similarities[i] *= boost_factor

        return boosted_similarities

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

            if doc.get("keywords"):
                print(f"PALAVRAS-CHAVE: {', '.join(doc['keywords'][:5])}")

            print("-" * 80)

    def get_cache_stats(self) -> Dict[str, Any]:
        return self.cache.get_cache_stats()

    def clear_cache(self) -> None:
        self.cache.clear_cache()
        print("Cache limpo!")


def main():
    ir_system = InformationRetrievalSystem()

    ir_system.load_collection()

    print(f"\nEstatísticas do cache: {ir_system.get_cache_stats()}")

    test_queries = [
        "machine learning algorithms",
        "redes neurais artificiais",
        "processamento de linguagem natural",
        "inteligência artificial",
        "algoritmos de otimização",
    ]

    for query in test_queries:
        ir_system.search_and_display(query, top_k=3)
        print("\n" + "=" * 100 + "\n")

    print(f"\nEstatísticas finais do cache: {ir_system.get_cache_stats()}")


if __name__ == "__main__":
    main()
