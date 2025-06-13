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


def search_by_query(ir_system, monitor):
    query = input(f"\n{Fore.CYAN}Enter your query: {Style.RESET_ALL}").strip()
    
    if query:
        monitor.start_timer("interactive_query")
        ir_system.search_and_display(query, top_k=5)
        monitor.end_timer("interactive_query")


def search_by_document(ir_system, monitor):
    print(f"{Fore.YELLOW}First, let's find a document to use as reference.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}You can search by entering a query or browse by entering 'browse'.{Style.RESET_ALL}")
    
    query = input(f"\n{Fore.CYAN}Enter search query or 'browse': {Style.RESET_ALL}").strip()
    
    if query.lower() == 'browse':
        page_size = 5
        page = 0
        total_pages = (len(ir_system.documents) + page_size - 1) // page_size
        
        while True:
            print(f"\n{Fore.MAGENTA}BROWSING DOCUMENTS - PAGE {page+1}/{total_pages}{Style.RESET_ALL}")
            print("=" * 60)
            
            start_idx = page * page_size
            end_idx = min(start_idx + page_size, len(ir_system.documents))
            
            for i in range(start_idx, end_idx):
                doc = ir_system.documents[i]
                print(f"{Fore.CYAN}[{i}] {Fore.YELLOW}{doc['title']}{Style.RESET_ALL}")
                print(f"    {Fore.GREEN}{', '.join(doc.get('authors', [])[:2])}{Style.RESET_ALL} ({doc.get('date', 'N/A')})")
                print(f"    {doc['abstract'][:100]}...{Style.RESET_ALL}")
                print()
                
            nav = input(f"{Fore.YELLOW}Enter document number, 'n' for next page, 'p' for previous, or 'q' to quit browsing: {Style.RESET_ALL}").strip()
            
            if nav.lower() == 'q':
                return
            elif nav.lower() == 'n':
                page = (page + 1) % total_pages
            elif nav.lower() == 'p':
                page = (page - 1) % total_pages
            elif nav.isdigit():
                doc_idx = int(nav)
                if 0 <= doc_idx < len(ir_system.documents):
                    monitor.start_timer("document_similarity")
                    ir_system.find_and_display_similar_documents(doc_idx, top_k=5)
                    monitor.end_timer("document_similarity")
                    
                    cont = input(f"\n{Fore.YELLOW}Continue browsing? (y/n): {Style.RESET_ALL}").strip().lower()
                    if cont != 'y':
                        return
                else:
                    print(f"{Fore.RED}Invalid document number. Please try again.{Style.RESET_ALL}")
    else:
        monitor.start_timer("interactive_query")
        results = ir_system.retrieve(query, top_k=10)
        monitor.end_timer("interactive_query")
        
        print(f"\n{'='*80}")
        print(f"{Fore.MAGENTA}SEARCH RESULTS FOR: '{query}'{Style.RESET_ALL}")
        print(f"{'='*80}")
        
        for i, (doc, score) in enumerate(results, 1):
            doc_idx = ir_system.documents.index(doc)  # Find the document's index in the collection
            print(f"\n{Fore.CYAN}{i}. [{doc_idx}] SCORE: {score:.4f}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}TITLE: {doc['title']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}AUTHORS: {', '.join(doc.get('authors', []))}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}ABSTRACT: {doc['abstract'][:150]}...{Style.RESET_ALL}")
            print("-" * 40)
            
        selection = input(f"\n{Fore.YELLOW}Enter the number of the document to find similar documents (1-{len(results)}): {Style.RESET_ALL}").strip()
        
        if selection.isdigit():
            selection_idx = int(selection) - 1
            if 0 <= selection_idx < len(results):
                doc = results[selection_idx][0]
                doc_idx = ir_system.documents.index(doc)
                
                monitor.start_timer("document_similarity")
                ir_system.find_and_display_similar_documents(doc_idx, top_k=5)
                monitor.end_timer("document_similarity")
            else:
                print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")


def interactive_search(ir_system):
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}INTERACTIVE MODE{Style.RESET_ALL}")
    print("=" * 60)

    monitor = PerformanceMonitor()

    print(f"{Fore.GREEN}System loaded and ready!{Style.RESET_ALL}")

    while True:
        print(f"\n{Fore.MAGENTA}SEARCH OPTIONS:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Search by query{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Find similar documents to a document{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            search_by_query(ir_system, monitor)
        elif choice == '2':
            search_by_document(ir_system, monitor)
        elif choice == '3':
            print(f"{Fore.GREEN}Exiting interactive mode.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")


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
