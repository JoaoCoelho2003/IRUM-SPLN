import os
from config import *
from data_extraction import CollectionExtractor
from data_processing import DocumentProcessor
from similarity_calculator import SimilarityCalculator
from model_trainer import SentenceTransformerTrainer
from caching_system import EmbeddingCache, PerformanceMonitor
from data_validator import DataValidator
from retrieval_system import InformationRetrievalSystem
from utils import ensure_dir, load_json, save_json


def setup_directories():
    ensure_dir(DATA_DIR)
    ensure_dir(MODEL_DIR)
    ensure_dir("cache")


def extract_data():
    print("=" * 60)
    print("FASE 1: EXTRAÇÃO DE DADOS")
    print("=" * 60)

    extractor = CollectionExtractor()

    xml_data = extractor.extract_multiple_collections(
        COLLECTIONS, max_records=MAX_RECORDS
    )
    extractor.save_xml(xml_data)

    return xml_data


def process_data():
    print("\n" + "=" * 60)
    print("FASE 2: PROCESSAMENTO DE DADOS")
    print("=" * 60)

    validator = DataValidator()
    cleaned_xml_file = validator.validate_xml_before_processing(XML_FILE)

    processor = DocumentProcessor()
    if cleaned_xml_file != XML_FILE:
        documents = processor.xml_to_json(cleaned_xml_file)
    else:
        documents = processor.xml_to_json()

    processor.save_collection(documents)

    return documents


def validate_data():
    print("\n" + "=" * 60)
    print("FASE 2.5: VALIDAÇÃO E LIMPEZA DE DADOS")
    print("=" * 60)

    validator = DataValidator()
    documents = load_json(JSON_FILE)
    clean_documents = validator.validate_and_clean_documents(documents)
    save_json(clean_documents, JSON_FILE)

    return clean_documents


def calculate_similarities(documents):
    print("\n" + "=" * 60)
    print("FASE 3: CÁLCULO DE SIMILARIDADES")
    print("=" * 60)

    monitor = PerformanceMonitor()
    monitor.start_timer("similarity_calculation")

    calculator = SimilarityCalculator(
        sample_ratio=0.05, use_clustering=True, n_clusters=min(50, len(documents) // 20)
    )

    training_pairs = calculator.create_training_collection(documents)
    calculator.save_training_data(training_pairs, TRAIN_FILE)

    duration = monitor.end_timer("similarity_calculation")
    print(f"Similarity calculation completed in {duration:.2f} seconds")

    return training_pairs


def train_model():
    print("\n" + "=" * 60)
    print("FASE 4: TREINO DO MODELO")
    print("=" * 60)

    monitor = PerformanceMonitor()
    monitor.start_timer("model_training")

    trainer = SentenceTransformerTrainer()
    training_examples = trainer.load_training_data(TRAIN_FILE)

    if not training_examples:
        print("No training data available!")
        return None

    if len(training_examples) > 100:
        model = trainer.train_with_early_stopping(training_examples)
    else:
        model = trainer.train_model(training_examples)

    trainer.save_model(MODEL_DIR)

    duration = monitor.end_timer("model_training")
    print(f"Model training completed in {duration:.2f} seconds")

    return model


def initialize_retrieval_system():
    print("\n" + "=" * 60)
    print("INICIALIZANDO SISTEMA DE RETRIEVAL")
    print("=" * 60)

    ir_system = InformationRetrievalSystem()
    ir_system.load_collection()

    return ir_system


def test_retrieval(ir_system):
    print("\n" + "=" * 60)
    print("FASE 5: TESTE DO SISTEMA DE RETRIEVAL")
    print("=" * 60)

    cache = EmbeddingCache()
    monitor = PerformanceMonitor()

    test_queries = [
        "machine learning",
        "redes neurais",
        "processamento de linguagem natural",
        "algoritmos de otimização",
        "inteligência artificial",
    ]

    for query in test_queries:
        monitor.start_timer("query_processing")

        print(f"\nTeste com query: '{query}'")
        results = ir_system.retrieve(query, top_k=3)

        duration = monitor.end_timer("query_processing")

        for i, (doc, score) in enumerate(results, 1):
            print(f"{i}. [{score:.3f}] {doc['title'][:80]}...")


def interactive_search(ir_system):
    print("\n" + "=" * 60)
    print("MODO INTERATIVO")
    print("=" * 60)

    cache = EmbeddingCache()
    monitor = PerformanceMonitor()

    print("Sistema carregado e pronto!")
    print("Digite as suas consultas (ou 'quit' para sair):")

    while True:
        query = input("\nQuery: ").strip()

        if query.lower() in ["quit", "exit", "sair"]:
            break

        if query:
            monitor.start_timer("interactive_query")
            ir_system.search_and_display(query, top_k=5)
            duration = monitor.end_timer("interactive_query")


def main():
    print("SISTEMA DE INFORMATION RETRIEVAL - REPOSITORIUM")
    print("=" * 60)

    total_monitor = PerformanceMonitor()
    total_monitor.start_timer("total_pipeline")

    setup_directories()

    if not os.path.exists(JSON_FILE):
        print("Dados não encontrados. A executar pipeline completo...")

        if not os.path.exists(XML_FILE):
            extract_data()

        documents = process_data()
        documents = validate_data()

        if len(documents) > 1:
            calculate_similarities(documents)

        if os.path.exists(TRAIN_FILE):
            train_model()

    else:
        print("Dados encontrados.")

        documents = load_json(JSON_FILE)
        print(f"A coleção atual tem {len(documents)} documentos")

        response = input("Deseja validar e limpar a coleção existente? (s/n): ")
        if response.lower() in ["s", "sim", "y", "yes"]:
            documents = validate_data()

        print("A avançar para teste do sistema...")

    if os.path.exists(JSON_FILE):
        ir_system = initialize_retrieval_system()

        test_retrieval(ir_system)

        total_duration = total_monitor.end_timer("total_pipeline")
        print(f"\nPipeline total executado em {total_duration:.2f}s")

        response = input("\nDeseja entrar no modo interativo? (s/n): ")
        if response.lower() in ["s", "sim", "y", "yes"]:
            interactive_search(ir_system)

    print("\nProcesso concluído!")


if __name__ == "__main__":
    main()
