import os
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import torch
from typing import List
import numpy as np
from config import BASE_MODEL


class SentenceTransformerTrainer:
    def __init__(self, base_model: str = BASE_MODEL):
        self.base_model = base_model
        self.model = None

    def create_training_setup(self, training_examples: List[InputExample]):
        print(f"Setting up training with {len(training_examples)} examples...")

        batch_size = 32
        epochs = 2

        self.model = SentenceTransformer(self.base_model)

        train_dataloader = DataLoader(
            training_examples,
            shuffle=True,
            batch_size=batch_size,
            num_workers=2 if torch.cuda.is_available() else 0,
            pin_memory=True if torch.cuda.is_available() else False,
        )

        train_loss = losses.CosineSimilarityLoss(self.model)

        return train_dataloader, train_loss, epochs

    def train_with_early_stopping(
        self,
        training_examples: List[InputExample],
        validation_examples: List[InputExample] = None,
    ):
        train_dataloader, train_loss, epochs = self.create_training_setup(
            training_examples
        )

        if validation_examples is None and len(training_examples) > 100:
            split_idx = int(0.9 * len(training_examples))
            validation_examples = training_examples[split_idx:]
            training_examples = training_examples[:split_idx]

            train_dataloader = DataLoader(
                training_examples,
                shuffle=True,
                batch_size=32,
                num_workers=2 if torch.cuda.is_available() else 0,
                pin_memory=True if torch.cuda.is_available() else False,
            )

        best_score = -1
        patience = 2
        patience_counter = 0

        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")

            self.model.fit(
                train_objectives=[(train_dataloader, train_loss)],
                epochs=1,
                warmup_steps=int(len(train_dataloader) * 0.1),
                show_progress_bar=True,
                output_path=None,
            )

            if validation_examples:
                val_score = self._evaluate_quickly(validation_examples)
                print(f"Validation correlation: {val_score:.4f}")

                if val_score > best_score:
                    best_score = val_score
                    patience_counter = 0
                    self.model.save("models/best_model_temp")
                else:
                    patience_counter += 1

                if patience_counter >= patience:
                    print("Early stopping triggered")
                    self.model = SentenceTransformer("models/best_model_temp")
                    break

        return self.model

    def _evaluate_quickly(self, validation_examples: List[InputExample]) -> float:
        if len(validation_examples) > 200:
            validation_examples = validation_examples[:200]

        predictions = []
        ground_truth = []

        batch_size = 32
        for i in range(0, len(validation_examples), batch_size):
            batch = validation_examples[i : i + batch_size]

            texts1 = [ex.texts[0] for ex in batch]
            texts2 = [ex.texts[1] for ex in batch]
            labels = [ex.label for ex in batch]

            embeddings1 = self.model.encode(texts1, convert_to_tensor=True)
            embeddings2 = self.model.encode(texts2, convert_to_tensor=True)

            similarities = torch.nn.functional.cosine_similarity(
                embeddings1, embeddings2
            )

            predictions.extend(similarities.cpu().numpy())
            ground_truth.extend(labels)

        correlation = np.corrcoef(predictions, ground_truth)[0, 1]
        return correlation if not np.isnan(correlation) else 0.0

    def load_training_data(self, filepath: str) -> List[InputExample]:
        print("Loading training data...")

        from utils import load_json

        training_data = load_json(filepath)

        examples = []
        for item in training_data:
            example = InputExample(
                texts=[item["text1"], item["text2"]], label=float(item["similarity"])
            )
            examples.append(example)

        print(f"Loaded {len(examples)} training examples")
        return examples

    def train_model(self, training_examples: List[InputExample]) -> SentenceTransformer:
        print(f"Starting model training based on: {self.base_model}")

        self.model = SentenceTransformer(self.base_model)

        train_dataloader = DataLoader(training_examples, shuffle=True, batch_size=32)

        train_loss = losses.CosineSimilarityLoss(self.model)

        print(f"Training for 2 epochs...")

        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=2,
            warmup_steps=int(len(train_dataloader) * 0.1),
            show_progress_bar=True,
        )

        print("Training completed!")
        return self.model

    def save_model(self, model_path: str) -> None:
        if not self.model:
            raise ValueError("Model not trained")

        from utils import ensure_dir

        ensure_dir(model_path)
        self.model.save(model_path)
        print(f"Model saved to: {model_path}")

    def load_model(self, model_path: str) -> SentenceTransformer:
        if os.path.exists(model_path):
            self.model = SentenceTransformer(model_path)
            print(f"Model loaded from: {model_path}")
        else:
            print(f"Model not found at: {model_path}")
            print("Loading base model...")
            self.model = SentenceTransformer(self.base_model)

        return self.model
