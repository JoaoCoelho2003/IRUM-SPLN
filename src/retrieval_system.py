import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from config import *
from utils import load_json
from query_processor import QueryProcessor
from caching_system import EmbeddingCache
from colorama import Fore, Style, init

init(autoreset=True)


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
            print(f"{Fore.GREEN}Model loaded from: {model_path}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}Error loading model from: {model_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Loading base model...{Style.RESET_ALL}")
            self.model = SentenceTransformer(BASE_MODEL)

    def load_collection(self, filepath: str = JSON_FILE) -> None:
        self.documents = load_json(filepath)
        print(f"{Fore.GREEN}Loaded {len(self.documents)} documents{Style.RESET_ALL}")

        self._precompute_embeddings()

    def _precompute_embeddings(self) -> None:
        print(f"{Fore.CYAN}Checking document embedding cache...{Style.RESET_ALL}")

        model_name = self.model._modules["0"].auto_model.config.name_or_path
        abstracts = [doc["abstract"] for doc in self.documents]

        cached_embeddings = self.cache.batch_get_embeddings(abstracts, model_name)

        if len(cached_embeddings) == len(abstracts):
            print(
                f"{Fore.GREEN}✅ All {len(abstracts)} embeddings found in cache!{Style.RESET_ALL}"
            )
            self.document_embeddings = np.array(
                [cached_embeddings[abstract] for abstract in abstracts]
            )
        else:
            print(
                f"{Fore.BLUE}📊 Cache: {len(cached_embeddings)}/{len(abstracts)} embeddings found{Style.RESET_ALL}"
            )
            print(f"{Fore.YELLOW}Computing missing embeddings...{Style.RESET_ALL}")

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
                    f"{Fore.GREEN}💾 {len(uncached_abstracts)} new embeddings saved to cache{Style.RESET_ALL}"
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
            f"{Fore.BLUE}📈 Cache stats: {cache_stats['memory_cached_items']} in memory, {cache_stats['disk_cached_items']} on disk{Style.RESET_ALL}"
        )
        print(f"{Fore.GREEN}Document embeddings ready!{Style.RESET_ALL}")

    def retrieve(
        self, query: str, top_k: int = 10
    ) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents or self.document_embeddings is None:
            raise ValueError("Collection not loaded")

        print(f"{Fore.CYAN}Processing query: '{query}'{Style.RESET_ALL}")

        processed_query_data = self.query_processor.process_query(query)

        enhanced_query = self.query_processor.enhance_query_for_similarity(
            processed_query_data
        )

        final_query = enhanced_query if enhanced_query.strip() else query

        print(
            f"{Fore.YELLOW}Processed query: '{processed_query_data['processed_query']}'{Style.RESET_ALL}"
        )
        print(
            f"{Fore.BLUE}Query type: {processed_query_data['query_type']}{Style.RESET_ALL}"
        )

        model_name = self.model._modules["0"].auto_model.config.name_or_path
        cached_query_embedding = self.cache.get_embedding(final_query, model_name)

        if cached_query_embedding is not None:
            print(f"{Fore.GREEN}🚀 Query embedding found in cache!{Style.RESET_ALL}")
            query_embedding = cached_query_embedding
        else:
            print(f"{Fore.YELLOW}🔄 Computing query embedding...{Style.RESET_ALL}")
            query_embedding = self.model.encode([final_query], convert_to_numpy=True)[0]
            self.cache.store_embedding(final_query, model_name, query_embedding)
            print(f"{Fore.GREEN}💾 Query embedding saved to cache{Style.RESET_ALL}")

        similarities = self._calculate_similarities(query_embedding)

        similarities = self._apply_query_processing_boost(
            similarities, processed_query_data
        )

        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for i in ranked_indices[:top_k]:
            results.append((self.documents[i], float(similarities[i])))

        return results

    def retrieve_similar_documents(
        self, doc_index: int, top_k: int = 10
    ) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents or self.document_embeddings is None:
            raise ValueError("Collection not loaded")

        if doc_index < 0 or doc_index >= len(self.documents):
            raise ValueError(
                f"Document index {doc_index} out of range (0-{len(self.documents)-1})"
            )

        print(
            f"{Fore.CYAN}Finding documents similar to document #{doc_index}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}Title: {self.documents[doc_index]['title']}{Style.RESET_ALL}"
        )

        doc_embedding = self.document_embeddings[doc_index]
        similarities = self._calculate_similarities(doc_embedding)
        similarities[doc_index] = -1
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
        print(f"{Fore.MAGENTA}RESULTS FOR: '{query}'{Style.RESET_ALL}")
        print(f"{'='*80}")

        for i, (doc, score) in enumerate(results, 1):
            print(f"\n{Fore.CYAN}{i}. SCORE: {score:.4f}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}TITLE: {doc['title']}{Style.RESET_ALL}")
            print(
                f"{Fore.GREEN}AUTHORS: {', '.join(doc.get('authors', []))}{Style.RESET_ALL}"
            )
            print(f"{Fore.BLUE}DATE: {doc.get('date', 'N/A')}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}ABSTRACT: {doc['abstract'][:300]}...{Style.RESET_ALL}")

            if doc.get("keywords"):
                print(
                    f"{Fore.MAGENTA}KEYWORDS: {', '.join(doc['keywords'][:5])}{Style.RESET_ALL}"
                )

            print("-" * 80)

    def display_document(self, doc_index: int) -> None:
        """Display the full details of a document"""
        if doc_index < 0 or doc_index >= len(self.documents):
            print(f"{Fore.RED}Invalid document index: {doc_index}{Style.RESET_ALL}")
            return

        doc = self.documents[doc_index]

        print(f"\n{'='*80}")
        print(f"{Fore.MAGENTA}DOCUMENT #{doc_index}{Style.RESET_ALL}")
        print(f"{'='*80}")

        print(f"{Fore.YELLOW}TITLE: {doc['title']}{Style.RESET_ALL}")
        print(
            f"{Fore.GREEN}AUTHORS: {', '.join(doc.get('authors', []))}{Style.RESET_ALL}"
        )
        print(f"{Fore.BLUE}DATE: {doc.get('date', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}TYPE: {doc.get('type', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}LANGUAGE: {doc.get('language', 'N/A')}{Style.RESET_ALL}")

        if doc.get("keywords"):
            print(
                f"{Fore.MAGENTA}KEYWORDS: {', '.join(doc['keywords'])}{Style.RESET_ALL}"
            )

        print(f"\n{Fore.WHITE}ABSTRACT:{Style.RESET_ALL}")
        print(f"{doc['abstract']}")

        print("-" * 80)

    def find_and_display_similar_documents(
        self, doc_index: int, top_k: int = 5
    ) -> None:
        try:
            self.display_document(doc_index)

            results = self.retrieve_similar_documents(doc_index, top_k)

            print(f"\n{'='*80}")
            print(
                f"{Fore.MAGENTA}SIMILAR DOCUMENTS TO #{doc_index}: '{self.documents[doc_index]['title']}'{Style.RESET_ALL}"
            )
            print(f"{'='*80}")

            for i, (doc, score) in enumerate(results, 1):
                print(f"\n{Fore.CYAN}{i}. SCORE: {score:.4f}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}TITLE: {doc['title']}{Style.RESET_ALL}")
                print(
                    f"{Fore.GREEN}AUTHORS: {', '.join(doc.get('authors', []))}{Style.RESET_ALL}"
                )
                print(f"{Fore.BLUE}DATE: {doc.get('date', 'N/A')}{Style.RESET_ALL}")
                print(
                    f"{Fore.WHITE}ABSTRACT: {doc['abstract'][:300]}...{Style.RESET_ALL}"
                )

                if doc.get("keywords"):
                    print(
                        f"{Fore.MAGENTA}KEYWORDS: {', '.join(doc['keywords'][:5])}{Style.RESET_ALL}"
                    )

                print("-" * 80)

        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def get_cache_stats(self) -> Dict[str, Any]:
        return self.cache.get_cache_stats()

    def clear_cache(self) -> None:
        self.cache.clear_cache()
        print(f"{Fore.GREEN}Cache cleared!{Style.RESET_ALL}")


def main():
    ir_system = InformationRetrievalSystem()

    ir_system.load_collection()

    print(
        f"\n{Fore.BLUE}Cache statistics: {ir_system.get_cache_stats()}{Style.RESET_ALL}"
    )

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

    print(
        f"\n{Fore.BLUE}Final cache statistics: {ir_system.get_cache_stats()}{Style.RESET_ALL}"
    )


if __name__ == "__main__":
    main()
