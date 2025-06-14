from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MiniBatchKMeans
from typing import List, Dict, Any, Tuple
import random
from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)


class SimilarityCalculator:
    def __init__(self, sample_ratio=0.1, use_clustering=True, n_clusters=50):
        self.sample_ratio = sample_ratio
        self.use_clustering = use_clustering
        self.n_clusters = n_clusters
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8,
        )
        self.document_vectors = None
        self.clusters = None

    def create_training_collection(
        self, documents: List[Dict[str, Any]]
    ) -> List[Tuple[str, str, float]]:
        print(
            f"{Fore.CYAN}Processing similarity calculation for {len(documents)} documents...{Style.RESET_ALL}"
        )

        abstracts = [doc.get("abstract", "") for doc in documents]
        print(f"{Fore.YELLOW}Creating TF-IDF vectors...{Style.RESET_ALL}")
        self.document_vectors = self.tfidf_vectorizer.fit_transform(abstracts)

        training_pairs = []

        if self.use_clustering and len(documents) > 1000:
            training_pairs = self._clustering_based_sampling(documents)
        else:
            training_pairs = self._smart_sampling(documents)

        print(
            f"{Fore.GREEN}Generated {len(training_pairs)} training pairs{Style.RESET_ALL}"
        )
        return training_pairs

    def _clustering_based_sampling(
        self, documents: List[Dict[str, Any]]
    ) -> List[Tuple[str, str, float]]:
        print(
            f"{Fore.MAGENTA}Using clustering-based sampling with {self.n_clusters} clusters...{Style.RESET_ALL}"
        )

        kmeans = MiniBatchKMeans(
            n_clusters=self.n_clusters, random_state=2025, batch_size=1000
        )
        cluster_labels = kmeans.fit_predict(self.document_vectors)

        clusters = defaultdict(list)
        for idx, label in enumerate(cluster_labels):
            clusters[label].append(idx)

        training_pairs = []

        for cluster_id, doc_indices in clusters.items():
            if len(doc_indices) < 2:
                continue

            n_pairs = min(len(doc_indices) * 2, 100)
            for _ in range(n_pairs):
                if len(doc_indices) >= 2:
                    idx1, idx2 = random.sample(doc_indices, 2)
                    similarity = self._calculate_fast_similarity(
                        documents[idx1], documents[idx2], idx1, idx2
                    )
                    if similarity > 0.3:
                        training_pairs.append(
                            (
                                documents[idx1]["abstract"],
                                documents[idx2]["abstract"],
                                similarity,
                            )
                        )

        cluster_ids = list(clusters.keys())
        for _ in range(len(training_pairs) // 3):
            if len(cluster_ids) >= 2:
                cluster1, cluster2 = random.sample(cluster_ids, 2)
                if clusters[cluster1] and clusters[cluster2]:
                    idx1 = random.choice(clusters[cluster1])
                    idx2 = random.choice(clusters[cluster2])
                    similarity = self._calculate_fast_similarity(
                        documents[idx1], documents[idx2], idx1, idx2
                    )
                    training_pairs.append(
                        (
                            documents[idx1]["abstract"],
                            documents[idx2]["abstract"],
                            similarity,
                        )
                    )

        return training_pairs

    def _smart_sampling(
        self, documents: List[Dict[str, Any]]
    ) -> List[Tuple[str, str, float]]:
        print(f"{Fore.BLUE}Using smart sampling strategy...{Style.RESET_ALL}")

        n_docs = len(documents)
        max_pairs = int(n_docs * self.sample_ratio * n_docs)

        training_pairs = []

        batch_size = 1000
        for i in range(0, n_docs, batch_size):
            end_i = min(i + batch_size, n_docs)
            batch_vectors_i = self.document_vectors[i:end_i]

            for j in range(i, n_docs, batch_size):
                end_j = min(j + batch_size, n_docs)
                batch_vectors_j = self.document_vectors[j:end_j]

                similarity_matrix = cosine_similarity(batch_vectors_i, batch_vectors_j)

                for local_i in range(similarity_matrix.shape[0]):
                    start_j = 0 if j > i else local_i + 1
                    for local_j in range(start_j, similarity_matrix.shape[1]):
                        global_i = i + local_i
                        global_j = j + local_j

                        if global_i >= global_j:
                            continue

                        tfidf_sim = similarity_matrix[local_i, local_j]

                        if tfidf_sim > 0.1:
                            enhanced_sim = self._enhance_similarity(
                                documents[global_i], documents[global_j], tfidf_sim
                            )

                            if enhanced_sim > 0.2:
                                training_pairs.append(
                                    (
                                        documents[global_i]["abstract"],
                                        documents[global_j]["abstract"],
                                        enhanced_sim,
                                    )
                                )

                if len(training_pairs) >= max_pairs:
                    return training_pairs[:max_pairs]

        return training_pairs

    def _calculate_fast_similarity(
        self, doc1: Dict[str, Any], doc2: Dict[str, Any], idx1: int, idx2: int
    ) -> float:
        tfidf_sim = cosine_similarity(
            self.document_vectors[idx1 : idx1 + 1],
            self.document_vectors[idx2 : idx2 + 1],
        )[0, 0]

        return self._enhance_similarity(doc1, doc2, tfidf_sim)

    def _enhance_similarity(
        self, doc1: Dict[str, Any], doc2: Dict[str, Any], base_similarity: float
    ) -> float:
        enhancements = []

        subjects1 = set(
            s.lower()
            for s in doc1.get("subjects_udc", []) + doc1.get("subjects_fos", [])
        )
        subjects2 = set(
            s.lower()
            for s in doc2.get("subjects_udc", []) + doc2.get("subjects_fos", [])
        )

        if subjects1 and subjects2:
            subject_sim = len(subjects1.intersection(subjects2)) / len(
                subjects1.union(subjects2)
            )
            enhancements.append(subject_sim * 0.3)

        keywords1 = set(kw.lower() for kw in doc1.get("keywords", []))
        keywords2 = set(kw.lower() for kw in doc2.get("keywords", []))

        if keywords1 and keywords2:
            keyword_sim = len(keywords1.intersection(keywords2)) / len(
                keywords1.union(keywords2)
            )
            enhancements.append(keyword_sim * 0.2)

        total_enhancement = sum(enhancements)
        final_similarity = base_similarity * 0.7 + total_enhancement

        return min(1.0, final_similarity)

    def save_training_data(
        self, training_pairs: List[Tuple[str, str, float]], filepath: str
    ) -> None:
        training_data = [
            {"text1": pair[0], "text2": pair[1], "similarity": pair[2]}
            for pair in training_pairs
        ]

        from utils import save_json

        save_json(training_data, filepath)
        print(f"{Fore.GREEN}Training data saved to: {filepath}{Style.RESET_ALL}")
