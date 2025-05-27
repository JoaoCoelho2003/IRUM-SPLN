REPOSITORIUM_BASE_URL = "https://repositorium.sdum.uminho.pt/oai/oai"

COLLECTIONS = {"msc_di": "col_1822_21316", "msc": "col_1822_2", "phd": "col_1822_3"}

METADATA_PREFIX = "dim"
BATCH_SIZE = 100
MAX_RECORDS = 1000

DATA_DIR = "data"
XML_FILE = f"{DATA_DIR}/repositorium_data.xml"
JSON_FILE = f"{DATA_DIR}/collection_documents.json"
TRAIN_FILE = f"{DATA_DIR}/training_similarities.json"
MODEL_DIR = "models"

BASE_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SIMILARITY_THRESHOLD = 0.3
TRAIN_EPOCHS = 3
BATCH_SIZE_TRAIN = 16

MIN_ABSTRACT_LENGTH = 50
MAX_ABSTRACT_LENGTH = 2000
COMMON_KEYWORDS_THRESHOLD = 2
RARE_KEYWORD_THRESHOLD = 5

EXTRACTION_TIMEOUT = 45
MAX_RETRIES = 3
BASE_DELAY = 1.0
MAX_CONSECUTIVE_ERRORS = 5
