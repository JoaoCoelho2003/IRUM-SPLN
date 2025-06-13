import os
from config import *
from data_extraction import CollectionExtractor
from data_processing import DocumentProcessor
from similarity_calculator import SimilarityCalculator
from model_trainer import SentenceTransformerTrainer
from caching_system import PerformanceMonitor
from data_validator import DataValidator
from retrieval_system import InformationRetrievalSystem
from utils import ensure_dir, load_json, save_json
from colorama import Fore, Style, init

init(autoreset=True)


def setup_directories():
    ensure_dir(DATA_DIR)
    ensure_dir(MODEL_DIR)
    ensure_dir("cache")


def extract_data():
    print("=" * 60)
    print(f"{Fore.CYAN}PHASE 1: DATA EXTRACTION{Style.RESET_ALL}")
    print("=" * 60)

    extractor = CollectionExtractor()

    xml_data = extractor.extract_multiple_collections(
        COLLECTIONS, max_records=MAX_RECORDS
    )
    extractor.save_xml(xml_data)

    return xml_data


def process_data():
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}PHASE 2: DATA PROCESSING{Style.RESET_ALL}")
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
    print(f"{Fore.CYAN}PHASE 2.5: DATA VALIDATION AND CLEANING{Style.RESET_ALL}")
    print("=" * 60)

    validator = DataValidator()
    documents = load_json(JSON_FILE)
    clean_documents = validator.validate_and_clean_documents(documents)
    save_json(clean_documents, JSON_FILE)

    return clean_documents


def calculate_similarities(documents):
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}PHASE 3: SIMILARITY CALCULATION{Style.RESET_ALL}")
    print("=" * 60)

    monitor = PerformanceMonitor()
    monitor.start_timer("similarity_calculation")

    calculator = SimilarityCalculator(
        sample_ratio=0.05, use_clustering=True, n_clusters=min(50, len(documents) // 20)
    )

    training_pairs = calculator.create_training_collection(documents)
    calculator.save_training_data(training_pairs, TRAIN_FILE)

    duration = monitor.end_timer("similarity_calculation")
    print(
        f"{Fore.GREEN}Similarity calculation completed in {duration:.2f} seconds{Style.RESET_ALL}"
    )

    return training_pairs


def train_model():
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}PHASE 4: MODEL TRAINING{Style.RESET_ALL}")
    print("=" * 60)

    monitor = PerformanceMonitor()
    monitor.start_timer("model_training")

    trainer = SentenceTransformerTrainer()
    training_examples = trainer.load_training_data(TRAIN_FILE)

    if not training_examples:
        print(f"{Fore.RED}No training data available!{Style.RESET_ALL}")
        return None

    if len(training_examples) > 100:
        model = trainer.train_with_early_stopping(training_examples)
    else:
        model = trainer.train_model(training_examples)

    trainer.save_model(MODEL_DIR)

    duration = monitor.end_timer("model_training")
    print(
        f"{Fore.GREEN}Model training completed in {duration:.2f} seconds{Style.RESET_ALL}"
    )

    return model


def initialize_retrieval_system():
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}INITIALIZING RETRIEVAL SYSTEM{Style.RESET_ALL}")
    print("=" * 60)

    ir_system = InformationRetrievalSystem()
    ir_system.load_collection()

    return ir_system


def test_retrieval(ir_system):
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}PHASE 5: RETRIEVAL SYSTEM TEST{Style.RESET_ALL}")
    print("=" * 60)

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

        print(f"\n{Fore.YELLOW}Testing with query: '{query}'{Style.RESET_ALL}")
        results = ir_system.retrieve(query, top_k=3)

        duration = monitor.end_timer("query_processing")

        for i, (doc, score) in enumerate(results, 1):
            print(
                f"{Fore.GREEN}{i}. [{score:.3f}] {doc['title'][:80]}...{Style.RESET_ALL}"
            )


def interactive_search(ir_system):
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}INTERACTIVE MODE{Style.RESET_ALL}")
    print("=" * 60)

    monitor = PerformanceMonitor()

    print(f"{Fore.GREEN}System loaded and ready!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Enter your queries (or 'quit' to exit):{Style.RESET_ALL}")

    while True:
        query = input(f"\n{Fore.CYAN}Query: {Style.RESET_ALL}").strip()

        if query.lower() in ["quit", "exit", "sair"]:
            break

        if query:
            monitor.start_timer("interactive_query")
            ir_system.search_and_display(query, top_k=5)
            duration = monitor.end_timer("interactive_query")


def main():
    print(f"{Fore.MAGENTA}INFORMATION RETRIEVAL SYSTEM - REPOSITORIUM{Style.RESET_ALL}")
    print("=" * 60)

    total_monitor = PerformanceMonitor()
    total_monitor.start_timer("total_pipeline")

    setup_directories()

    if not os.path.exists(JSON_FILE):
        print(
            f"{Fore.YELLOW}Data not found. Running complete pipeline...{Style.RESET_ALL}"
        )

        if not os.path.exists(XML_FILE):
            extract_data()

        documents = process_data()
        documents = validate_data()

        if len(documents) > 1:
            calculate_similarities(documents)

        if os.path.exists(TRAIN_FILE):
            train_model()

    else:
        print(f"{Fore.GREEN}Data found.{Style.RESET_ALL}")

        documents = load_json(JSON_FILE)
        print(
            f"{Fore.BLUE}Current collection has {len(documents)} documents{Style.RESET_ALL}"
        )

        response = input(
            f"{Fore.YELLOW}Do you want to validate and clean the existing collection? (y/n): {Style.RESET_ALL}"
        )
        if response.lower() in ["s", "sim", "y", "yes"]:
            documents = validate_data()

        print(f"{Fore.CYAN}Proceeding to system test...{Style.RESET_ALL}")

    if os.path.exists(JSON_FILE):
        ir_system = initialize_retrieval_system()

        test_retrieval(ir_system)

        total_duration = total_monitor.end_timer("total_pipeline")
        print(
            f"\n{Fore.GREEN}Total pipeline executed in {total_duration:.2f}s{Style.RESET_ALL}"
        )

        response = input(
            f"\n{Fore.YELLOW}Do you want to enter interactive mode? (y/n): {Style.RESET_ALL}"
        )
        if response.lower() in ["s", "sim", "y", "yes"]:
            interactive_search(ir_system)

    print(f"\n{Fore.GREEN}Process completed!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
