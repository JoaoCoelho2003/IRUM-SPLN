from typing import List, Dict, Any
from utils import clean_text, extract_keywords


class QueryProcessor:
    def __init__(self):
        pass

    def process_query(self, query: str, language: str = "portuguese") -> Dict[str, Any]:
        if not query or not query.strip():
            return {
                "original_query": query,
                "processed_query": "",
                "keywords": [],
                "query_type": "empty",
            }

        cleaned_query = clean_text(query)
        keywords = extract_keywords(cleaned_query, language)
        query_type = self._determine_query_type(keywords)

        processed_query = " ".join(keywords)

        return {
            "original_query": query,
            "processed_query": processed_query,
            "keywords": keywords,
            "query_type": query_type,
        }

    def _determine_query_type(self, keywords: List[str]) -> str:
        if not keywords:
            return "empty"
        elif len(keywords) == 1:
            return "single_term"
        elif len(keywords) <= 3:
            return "short_phrase"
        else:
            return "long_phrase"

    def enhance_query_for_similarity(self, processed_query_data: Dict[str, Any]) -> str:
        keywords = processed_query_data["keywords"]

        if not keywords:
            return processed_query_data["original_query"]

        enhanced_query = " ".join(keywords * 2)

        return enhanced_query


def main():
    processor = QueryProcessor()

    test_queries = [
        "machine learning",
        "redes neurais artificiais",
        "algoritmos de otimização para análise de dados",
        "inteligência artificial",
    ]

    print("Teste do Processador de Queries")
    print("=" * 50)

    for query in test_queries:
        print(f"\nQuery original: '{query}'")
        result = processor.process_query(query)

        print(f"Query processada: '{result['processed_query']}'")
        print(f"Keywords: {result['keywords']}")
        print(f"Tipo: {result['query_type']}")
        enhanced = processor.enhance_query_for_similarity(result)
        print(f"Query melhorada: '{enhanced}'")
        print("-" * 30)


if __name__ == "__main__":
    main()
