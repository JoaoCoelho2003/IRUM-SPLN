import os
import json
import re
import unicodedata
from typing import List, Dict, Any
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from colorama import Fore, Style, init

init(autoreset=True)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


def ensure_dir(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_json(data: Any, filepath: str) -> None:
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath: str) -> Any:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = "".join(char for char in text if unicodedata.category(char)[0] != "C")

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


def extract_keywords(text: str, language: str = "portuguese") -> List[str]:
    if not text:
        return []

    tokens = word_tokenize(text.lower())

    try:
        stop_words = set(stopwords.words(language))
    except:
        stop_words = set(stopwords.words("english"))

    keywords = [
        token
        for token in tokens
        if token.isalpha() and len(token) > 2 and token not in stop_words
    ]

    return keywords


def calculate_jaccard_similarity(set1: set, set2: set) -> float:
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union if union > 0 else 0.0


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    return max(min_val, min(max_val, score))


print(f"{Fore.GREEN}Utils module loaded successfully!{Style.RESET_ALL}")
