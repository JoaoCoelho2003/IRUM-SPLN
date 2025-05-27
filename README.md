![alt text](public/banner.png)

Este projeto implementa um sistema completo de Information Retrieval baseado no RepositoriUM da Universidade do Minho. Recorre a sentence transformers para calcular similaridades semânticas entre documentos.

## 📋 Estrutura do Projeto

```
src/
├── config.py                 # Configurações do projeto
├── utils.py                  # Funções utilitárias
├── data_extraction.py        # Extração de dados do RepositoriUM
├── data_processing.py        # Processamento XML → JSON
├── similarity_calculator.py  # Cálculo de similaridades
├── model_trainer.py         # Treino do sentence transformer
├── retrieval_system.py     # Sistema de retrieval
├── main.py                  # Script principal
├── requirements.txt         # Dependências
├── data/                    # Dados extraídos e processados
├── models/                  # Modelos treinados
```

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd repositorium-ir-system
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Download de recursos NLTK:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 📊 Pipeline Completo

### 1. Extração de Dados
```bash
python data_extraction.py
```
- Extrai dados do RepositoriUM via OAI-PMH
- Suporta diferentes coleções (mestrados, doutoramentos)
- Guarda dados em formato XML

### 2. Processamento de Dados
```bash
python data_processing.py
```
- Converte XML para JSON estruturado
- Limpa e normaliza metadados
- Filtra documentos por qualidade

### 3. Cálculo de Similaridades
```bash
python similarity_calculator.py
```
- Calcula similaridades heurísticas entre documentos
- Considera keywords, assuntos UDC/FOS, coleções
- Cria dados de treino para o modelo

### 4. Treino do Modelo
```bash
python model_trainer.py
```
- Treina sentence transformer personalizado
- Usa dados de similaridade calculados
- Avalia performance do modelo

### 5. Sistema de Retrieval
```bash
python retrieval_system.py
```
- Sistema completo de busca semântica
- Interface para queries interativas
- Ranking por similaridade

## 🔧 Uso Rápido

### Executar Pipeline Completo
```bash
python main.py
```

### Usar Sistema Interativo
```python
from retrieval_system import InformationRetrievalSystem

# Inicializa sistema
ir_system = InformationRetrievalSystem()
ir_system.load_collection()

# Executa procura
results = ir_system.retrieve("machine learning", top_k=5)

# Mostra resultados
ir_system.search_and_display("machine learning")
```

## ⚙️ Configuração

Edite `config.py` para personalizar:

- **Coleções**: Escolha diferentes coleções do RepositoriUM
- **Parâmetros do modelo**: Modelo base, épocas de treino, batch size
- **Thresholds**: Similaridade mínima, tamanhos de texto
- **Caminhos**: Diretorias de dados e modelos

## 🎯 Funcionalidades

### Extração de Dados
- ✅ Suporte a OAI-PMH
- ✅ Múltiplas coleções
- ✅ Rate limiting automático
- ✅ Tratamento de erros

### Processamento
- ✅ Limpeza de metadados
- ✅ Normalização de texto
- ✅ Filtragem por qualidade
- ✅ Estruturação JSON

### Cálculo de Similaridades
- ✅ Similaridade de keywords ponderada
- ✅ Assuntos UDC e FOS
- ✅ Análise de coleções
- ✅ Heurísticas configuráveis

### Modelo
- ✅ Sentence transformer multilíngue
- ✅ Fine-tuning personalizado
- ✅ Avaliação automática
- ✅ Métricas de performance

### Sistema de Retrieval
- ✅ Procura semântica
- ✅ Ranking por similaridade
- ✅ Interface interativa
- ✅ Análise de resultados

## 📈 Métricas e Avaliação

O sistema inclui várias métricas:

- **Similaridade**: MSE, MAE, correlação
- **Retrieval**: Precisão, recall, F1-score
- **Performance**: Tempo de resposta, throughput

## 🔍 Exemplos de Uso

### Procura Básica
```python
results = ir_system.retrieve("redes neurais", top_k=10)
for doc, score in results:
    print(f"[{score:.3f}] {doc['title']}")
```

### Análise de Similaridade
```python
from similarity_calculator import SimilarityCalculator

calculator = SimilarityCalculator()
similarity = calculator.guess_similarity(doc1, doc2)
print(f"Similaridade: {similarity:.3f}")
```

### Treino Personalizado
```python
from model_trainer import SentenceTransformerTrainer

trainer = SentenceTransformerTrainer("custom-model")
model = trainer.train_model(training_examples)
```

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Erro de memória durante treino**
   - Reduza `BATCH_SIZE_TRAIN` em `config.py`
   - Use menos dados de treino

2. **Timeout na extração**
   - Aumente timeout em `data_extraction.py`
   - Reduza `MAX_RECORDS`

3. **Modelo não encontrado**
   - Execute primeiro o treino: `python model_trainer.py`
   - Verifique caminho em `config.py`

## 👥 Autores

- **João Coelho**
- **José Rodrigues**
- **Mariana Silva**

---
