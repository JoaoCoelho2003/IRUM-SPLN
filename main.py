import os
from config import *
from data_extraction import RepositoriumExtractor
from data_processing import DocumentProcessor
from similarity_calculator import SimilarityCalculator
from model_trainer import SentenceTransformerTrainer
from retrieval_system import InformationRetrievalSystem
from utils import ensure_dir

def setup_directories():
    ensure_dir(DATA_DIR)
    ensure_dir(MODEL_DIR)

def extract_data():
    print("="*60)
    print("FASE 1: EXTRAÇÃO DE DADOS")
    print("="*60)
    
    extractor = RepositoriumExtractor()
    collection_id = COLLECTIONS["msc_di"]
    
    xml_data = extractor.extract_collection(collection_id, max_records=MAX_RECORDS)
    extractor.save_xml(xml_data)
    
    return xml_data

def process_data():
    print("\n" + "="*60)
    print("FASE 2: PROCESSAMENTO DE DADOS")
    print("="*60)
    
    processor = DocumentProcessor()
    documents = processor.xml_to_json()
    processor.save_collection(documents)
    
    return documents

def calculate_similarities(documents):
    print("\n" + "="*60)
    print("FASE 3: CÁLCULO DE SIMILARIDADES")
    print("="*60)
    
    calculator = SimilarityCalculator()
    training_pairs = calculator.create_training_collection(documents)
    calculator.save_training_data(training_pairs)
    
    return training_pairs

def train_model():
    print("\n" + "="*60)
    print("FASE 4: TREINO DO MODELO")
    print("="*60)
    
    trainer = SentenceTransformerTrainer()
    training_examples = trainer.load_training_data()
    
    if training_examples:
        split_idx = int(0.8 * len(training_examples))
        train_examples = training_examples[:split_idx]
        test_examples = training_examples[split_idx:]
        
        model = trainer.train_model(train_examples)
        
        if test_examples:
            trainer.evaluate_model(test_examples)
        
        trainer.save_model()
        
        return model
    else:
        print("Nenhum dado de treino disponível!")
        return None

def test_retrieval():
    print("\n" + "="*60)
    print("FASE 5: TESTE DO SISTEMA DE RETRIEVAL")
    print("="*60)
    
    ir_system = InformationRetrievalSystem()
    ir_system.load_collection()
    
    test_queries = [
        "machine learning",
        "redes neurais",
        "processamento de linguagem natural",
        "algoritmos de otimização",
        "inteligência artificial"
    ]
    
    for query in test_queries:
        print(f"\nTeste com query: '{query}'")
        results = ir_system.retrieve(query, top_k=3)
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"{i}. [{score:.3f}] {doc['title'][:80]}...")

def interactive_search():
    print("\n" + "="*60)
    print("MODO INTERATIVO")
    print("="*60)
    
    ir_system = InformationRetrievalSystem()
    ir_system.load_collection()
    
    print("Digite as suas consultas (ou 'quit' para sair):")
    
    while True:
        query = input("\nQuery: ").strip()
        
        if query.lower() in ['quit', 'exit', 'sair']:
            break
        
        if query:
            ir_system.search_and_display(query, top_k=5)

def main():
    print("SISTEMA DE INFORMATION RETRIEVAL - REPOSITORIUM")
    print("="*60)
    
    setup_directories()
    
    if not os.path.exists(JSON_FILE):
        print("Dados não encontrados. A executar pipeline completo...")
        
        if not os.path.exists(XML_FILE):
            extract_data()
        
        documents = process_data()
        
        if len(documents) > 1:
            calculate_similarities(documents)
        
        if os.path.exists(TRAIN_FILE):
            train_model()
    
    else:
        print("Dados encontrados. A  avançar para teste do sistema...")
    
    if os.path.exists(JSON_FILE):
        test_retrieval()
        
        response = input("\nDeseja entrar no modo interativo? (s/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            interactive_search()
    
    print("\nProcesso concluído!")

if __name__ == "__main__":
    main()
