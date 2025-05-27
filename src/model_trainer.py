import os
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from typing import List, Dict
import numpy as np
from config import *
from utils import load_json, ensure_dir

class SentenceTransformerTrainer:    
    def __init__(self, base_model: str = BASE_MODEL):
        self.base_model = base_model
        self.model = None
        
    def load_training_data(self, filepath: str = TRAIN_FILE) -> List[InputExample]:
        print("A carregar dados de treino...")
        
        training_data = load_json(filepath)
        
        examples = []
        for item in training_data:
            example = InputExample(
                texts=[item['text1'], item['text2']],
                label=float(item['similarity'])
            )
            examples.append(example)
        
        print(f"Carregados {len(examples)} exemplos de treino")
        return examples
    
    def train_model(self, training_examples: List[InputExample]) -> SentenceTransformer:
        print(f"A iniciar treino do modelo baseado em: {self.base_model}")
        
        self.model = SentenceTransformer(self.base_model)
        
        train_dataloader = DataLoader(
            training_examples, 
            shuffle=True, 
            batch_size=BATCH_SIZE_TRAIN
        )
        
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        print(f"A treinar por {TRAIN_EPOCHS} épocas...")
        
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=TRAIN_EPOCHS,
            warmup_steps=int(len(train_dataloader) * 0.1),
            output_path=MODEL_DIR,
            show_progress_bar=True
        )
        
        print("Treino concluído!")
        return self.model
    
    def evaluate_model(self, test_examples: List[InputExample]) -> Dict[str, float]:
        if not self.model:
            raise ValueError("Modelo não foi treinado")
        
        print("A avaliar modelo...")
        
        predictions = []
        ground_truth = []
        
        for example in test_examples:
            embeddings = self.model.encode(example.texts)
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            
            predictions.append(similarity)
            ground_truth.append(example.label)
        
        predictions = np.array(predictions)
        ground_truth = np.array(ground_truth)
        
        mse = np.mean((predictions - ground_truth) ** 2)
        mae = np.mean(np.abs(predictions - ground_truth))
        correlation = np.corrcoef(predictions, ground_truth)[0, 1]
        
        metrics = {
            'mse': float(mse),
            'mae': float(mae),
            'correlation': float(correlation)
        }
        
        print(f"Métricas de avaliação:")
        print(f"MSE: {metrics['mse']:.4f}")
        print(f"MAE: {metrics['mae']:.4f}")
        print(f"Correlação: {metrics['correlation']:.4f}")
        
        return metrics
    
    def save_model(self, model_path: str = MODEL_DIR) -> None:
        if not self.model:
            raise ValueError("Modelo não foi treinado")
        
        ensure_dir(model_path)
        self.model.save(model_path)
        print(f"Modelo guardado em: {model_path}")
    
    def load_model(self, model_path: str = MODEL_DIR) -> SentenceTransformer:
        if os.path.exists(model_path):
            self.model = SentenceTransformer(model_path)
            print(f"Modelo carregado de: {model_path}")
        else:
            print(f"Modelo não encontrado em: {model_path}")
            print("A carregar modelo base...")
            self.model = SentenceTransformer(self.base_model)
        
        return self.model

def main():
    trainer = SentenceTransformerTrainer()
    
    training_examples = trainer.load_training_data()
    
    if not training_examples:
        print("Nenhum dado de treino encontrado!")
        return
    
    split_idx = int(0.8 * len(training_examples))
    train_examples = training_examples[:split_idx]
    test_examples = training_examples[split_idx:]
    
    print(f"Treino: {len(train_examples)} exemplos")
    print(f"Teste: {len(test_examples)} exemplos")
    
    model = trainer.train_model(train_examples)
    
    if test_examples:
        metrics = trainer.evaluate_model(test_examples)
    
    trainer.save_model()
    
    print("Processo de treino concluído!")

if __name__ == "__main__":
    main()
