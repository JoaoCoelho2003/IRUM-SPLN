import pickle
import hashlib
import os
from typing import Dict, List, Any
import numpy as np


class EmbeddingCache:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.memory_cache = {}
        self.max_memory_items = 1000

    def _get_cache_key(self, text: str, model_name: str) -> str:
        content = f"{model_name}:{text}"
        return hashlib.md5(content.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> str:
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")

    def get_embedding(self, text: str, model_name: str) -> np.ndarray:
        cache_key = self._get_cache_key(text, model_name)

        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]

        cache_path = self._get_cache_path(cache_key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "rb") as f:
                    embedding = pickle.load(f)

                if len(self.memory_cache) < self.max_memory_items:
                    self.memory_cache[cache_key] = embedding

                return embedding
            except:
                os.remove(cache_path)

        return None

    def store_embedding(self, text: str, model_name: str, embedding: np.ndarray):
        cache_key = self._get_cache_key(text, model_name)

        if len(self.memory_cache) < self.max_memory_items:
            self.memory_cache[cache_key] = embedding

        cache_path = self._get_cache_path(cache_key)
        try:
            with open(cache_path, "wb") as f:
                pickle.dump(embedding, f)
        except Exception as e:
            print(f"Warning: Could not cache embedding: {e}")

    def batch_get_embeddings(
        self, texts: List[str], model_name: str
    ) -> Dict[str, np.ndarray]:
        cached_embeddings = {}

        for text in texts:
            embedding = self.get_embedding(text, model_name)
            if embedding is not None:
                cached_embeddings[text] = embedding

        return cached_embeddings

    def batch_store_embeddings(
        self, text_embedding_pairs: List[tuple], model_name: str
    ):
        for text, embedding in text_embedding_pairs:
            self.store_embedding(text, model_name, embedding)

    def clear_cache(self):
        self.memory_cache.clear()

        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".pkl"):
                os.remove(os.path.join(self.cache_dir, filename))

    def get_cache_stats(self) -> Dict[str, Any]:
        disk_files = len([f for f in os.listdir(self.cache_dir) if f.endswith(".pkl")])
        memory_items = len(self.memory_cache)

        return {
            "memory_cached_items": memory_items,
            "disk_cached_items": disk_files,
            "cache_directory": self.cache_dir,
        }


class PerformanceMonitor:
    def __init__(self):
        self.timings = {}
        self.counters = {}

    def start_timer(self, operation: str):
        import time

        self.timings[operation] = time.time()

    def end_timer(self, operation: str):
        import time

        if operation in self.timings:
            duration = time.time() - self.timings[operation]
            if f"{operation}_total" not in self.counters:
                self.counters[f"{operation}_total"] = 0
                self.counters[f"{operation}_count"] = 0

            self.counters[f"{operation}_total"] += duration
            self.counters[f"{operation}_count"] += 1

            return duration
        return 0

    def get_stats(self) -> Dict[str, float]:
        stats = {}
        for key, value in self.counters.items():
            if key.endswith("_total"):
                operation = key[:-6]
                count_key = f"{operation}_count"
                if count_key in self.counters:
                    avg_time = value / self.counters[count_key]
                    stats[f"{operation}_avg_time"] = avg_time
                    stats[f"{operation}_total_time"] = value
                    stats[f"{operation}_count"] = self.counters[count_key]

        return stats
