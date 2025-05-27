from typing import List, Dict, Any, Tuple
import numpy as np
from collections import Counter
from config import *
from utils import load_json, save_json, extract_keywords, calculate_jaccard_similarity, normalize_score

class SimilarityCalculator:    
    def __init__(self):
        self.keyword_frequencies = {}
        self.total_docs = 0
    
    def create_training_collection(self, documents: List[Dict[str, Any]]) -> List[Tuple[str, str, float]]:
        print("A criar coleção de treino...")
        
        self._calculate_keyword_frequencies(documents)
        
        training_pairs = []
        total_pairs = len(documents) * (len(documents) - 1) // 2
        
        print(f"A calcular similaridades para {total_pairs} pares...")
        
        processed = 0
        for i, doc1 in enumerate(documents):
            for j, doc2 in enumerate(documents[i+1:], i+1):
                similarity = self.guess_similarity(doc1, doc2)
                
                if similarity >= SIMILARITY_THRESHOLD:
                    training_pairs.append((
                        doc1['abstract'],
                        doc2['abstract'],
                        similarity
                    ))
                
                processed += 1
                if processed % 1000 == 0:
                    print(f"Processados {processed}/{total_pairs} pares...")
        
        print(f"Coleção de treino criada: {len(training_pairs)} pares relevantes")
        return training_pairs
    
    def guess_similarity(self, doc1: Dict[str, Any], doc2: Dict[str, Any]) -> float:
        similarities = []
        
        keyword_sim = self._keyword_similarity(doc1, doc2)
        similarities.append(keyword_sim * 0.4)
        
        udc_sim = self._subject_similarity(doc1.get('subjects_udc', []), doc2.get('subjects_udc', []))
        similarities.append(udc_sim * 0.3)
        
        fos_sim = self._subject_similarity(doc1.get('subjects_fos', []), doc2.get('subjects_fos', []))
        similarities.append(fos_sim * 0.2)
        
        collection_sim = self._collection_similarity(doc1, doc2)
        similarities.append(collection_sim * 0.1)
        
        total_similarity = sum(similarities)
        
        return normalize_score(total_similarity)
    
    def _calculate_keyword_frequencies(self, documents: List[Dict[str, Any]]) -> None:
        print("A calcular frequências de palavras-chave...")
        
        self.total_docs = len(documents)
        keyword_counts = Counter()
        
        for doc in documents:
            text_keywords = extract_keywords(doc.get('abstract', ''))
            explicit_keywords = [kw.lower() for kw in doc.get('keywords', [])]
            
            all_keywords = set(text_keywords + explicit_keywords)
            
            for keyword in all_keywords:
                keyword_counts[keyword] += 1
        
        self.keyword_frequencies = {
            keyword: count / self.total_docs 
            for keyword, count in keyword_counts.items()
        }
        
        print(f"Calculadas frequências para {len(self.keyword_frequencies)} palavras-chave")
    
    def _keyword_similarity(self, doc1: Dict[str, Any], doc2: Dict[str, Any]) -> float:
        keywords1 = self._get_document_keywords(doc1)
        keywords2 = self._get_document_keywords(doc2)
        
        if not keywords1 or not keywords2:
            return 0.0
        
        common_keywords = keywords1.intersection(keywords2)
        
        if not common_keywords:
            return 0.0
        
        weighted_score = 0.0
        for keyword in common_keywords:
            rarity_weight = 1.0 - self.keyword_frequencies.get(keyword, 0.5)
            weighted_score += rarity_weight
        
        max_keywords = max(len(keywords1), len(keywords2))
        normalized_score = weighted_score / max_keywords
        
        return normalize_score(normalized_score)
    
    def _get_document_keywords(self, doc: Dict[str, Any]) -> set:
        keywords = set()
        
        text_keywords = extract_keywords(doc.get('abstract', ''))
        keywords.update(text_keywords)
        
        explicit_keywords = [kw.lower() for kw in doc.get('keywords', [])]
        keywords.update(explicit_keywords)
        
        filtered_keywords = {
            kw for kw in keywords 
            if self.keyword_frequencies.get(kw, 0) > 0.01 and 
               self.keyword_frequencies.get(kw, 1) < 0.5
        }
        
        return filtered_keywords
    
    def _subject_similarity(self, subjects1: List[str], subjects2: List[str]) -> float:
        if not subjects1 or not subjects2:
            return 0.0
        
        set1 = set(s.lower() for s in subjects1)
        set2 = set(s.lower() for s in subjects2)
        
        return calculate_jaccard_similarity(set1, set2)
    
    def _collection_similarity(self, doc1: Dict[str, Any], doc2: Dict[str, Any]) -> float:
        collections1 = doc1.get('collections', [])
        collections2 = doc2.get('collections', [])
        
        if not collections1 or not collections2:
            return 0.0
        
        set1 = set(c.lower() for c in collections1)
        set2 = set(c.lower() for c in collections2)
        
        return calculate_jaccard_similarity(set1, set2)
    
    def save_training_data(self, training_pairs: List[Tuple[str, str, float]], 
                          filepath: str = TRAIN_FILE) -> None:
        training_data = [
            {
                'text1': pair[0],
                'text2': pair[1],
                'similarity': pair[2]
            }
            for pair in training_pairs
        ]
        
        save_json(training_data, filepath)
        print(f"Dados de treino guardados em: {filepath}")

def main():
    documents = load_json(JSON_FILE)
    print(f"Carregados {len(documents)} documentos")
    
    calculator = SimilarityCalculator()
    training_pairs = calculator.create_training_collection(documents)
    
    calculator.save_training_data(training_pairs)
    
    if training_pairs:
        similarities = [pair[2] for pair in training_pairs]
        print(f"\nEstatísticas das similaridades:")
        print(f"Média: {np.mean(similarities):.3f}")
        print(f"Mediana: {np.median(similarities):.3f}")
        print(f"Desvio padrão: {np.std(similarities):.3f}")
        print(f"Min: {np.min(similarities):.3f}")
        print(f"Max: {np.max(similarities):.3f}")

if __name__ == "__main__":
    main()
