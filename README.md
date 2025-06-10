![alt text](public/banner.png)

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Utilização](#-utilização)
- [Arquitectura](#-arquitectura)
- [Componentes Técnicos](#-componentes-técnicos-detalhados)
- [Pipeline Completo](#-pipeline-completo)
- [Configuração](#-configuração-avançada)
- [Performance](#-performance-e-optimizações)
- [Exemplos](#-exemplos-de-uso)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap-e-melhorias-futuras)

## 🎯 Visão Geral

Este sistema implementa uma solução completa de Information Retrieval para o RepositoriUM através de:

- **Embeddings Semânticos**: Utiliza sentence transformers fine-tuned para capturar significado profundo dos documentos
- **Clustering Inteligente**: Reduz complexidade computacional através de agrupamento adaptativo de documentos
- **Cache Híbrido**: Sistema de cache em memória e disco para máxima performance
- **Query Processing**: Normalização e enhancement automático de queries de pesquisa
- **Similarity Multi-dimensional**: Combina TF-IDF, metadados e embeddings neurais de forma a obter melhores resultados

## ✨ Funcionalidades

### 🔄 **Pipeline Automatizado Completo**
- Extração automática do RepositoriUM via protocolo OAI-PMH
- Processamento e limpeza de dados XML para formato JSON estruturado
- Validação rigorosa e remoção de duplicados
- Cálculo otimizado de similaridades com clustering adaptativo
- Fine-tuning de sentence transformers com dados específicos do domínio
- Sistema de cache inteligente para embeddings
- Interface de pesquisa interativa em tempo real

### 🧠 **Inteligência Artificial**
- **Sentence Transformers**: Embeddings contextuais de 384 dimensões otimizados para o domínio académico
- **Clustering Adaptativo**: MiniBatch K-Means para eficiência computacional em grandes coleções
- **Query Enhancement**: Processamento inteligente que melhora a qualidade das pesquisas
- **Multi-modal Similarity**: Combinação ponderada de TF-IDF, metadados e embeddings neurais

### ⚡ **Optimizações de Performance**
- **Cache Híbrido**: Combinação de memória RAM e armazenamento persistente
- **Vectorização NumPy**: Operações SIMD para cálculos matriciais eficientes
- **Batch Processing**: Processamento em lotes para maximizar throughput
- **Early Stopping**: Treino inteligente com validação automática para evitar overfitting
- **Memory Management**: Gestão otimizada de memória para grandes coleções

### 📊 **Sistema de Avaliação Robusto**
- **Métricas Padrão**: Implementação de Precision@K, Recall@K, MAP e MRR
- **Validação Automática**: Geração automática de test queries para avaliação
- **Performance Monitoring**: Estatísticas detalhadas em tempo real
- **Quality Assurance**: Validação multi-fase de dados para garantir qualidade

## 🚀 Instalação

### Instalação das Dependências
```bash
# Clona o repositório
git clone https://github.com/username/ir-repositorium.git
cd ir-repositorium

# Instala dependências
pip install -r requirements.txt

# Download de recursos NLTK necessários
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"
```

### Estrutura do Projeto
```
src/
├── main.py                    # Pipeline principal e orquestração
├── config.py                  # Configurações globais do sistema
├── utils.py                   # Utilitários partilhados entre componentes
├── data_extraction.py         # Extração de dados via OAI-PMH
├── data_processing.py         # Processamento XML→JSON
├── data_validator.py          # Validação e limpeza de dados
├── similarity_calculator.py   # Cálculo de similaridades com clustering
├── model_trainer.py           # Fine-tuning de sentence transformers
├── query_processor.py         # Processamento e enhancement de queries
├── retrieval_system.py        # Motor de pesquisa semântica
├── caching_system.py          # Sistema de cache híbrido
├── evaluation_system.py       # Avaliação e métricas de performance
├── cache/                     # Armazenamento de embeddings em cache
├── data/                      # Dados processados e estruturados
└── models/                    # Modelos treinados e checkpoints
```

## 🎮 Utilização

### Execução Completa do Pipeline

O sistema executa automaticamente todas as fases necessárias através de um único comando. 

```bash
python3 main.py
```

O pipeline inclui extração de dados, processamento, validação, cálculo de similaridades, treino do modelo, pré-computação de embeddings e entrada em modo interativo de pesquisa.

### Modo Interativo de Pesquisa
Após a conclusão do pipeline, o sistema pergunta ao utilizador se deseja entrar no modo interativo de pesquisa. Caso o utilizador opte por não entrar no modo interativo, o sistema finaliza a execução. Caso contrário, o sistema entra no mesmo, onde o utilizador pode realizar pesquisas em tempo real. Cada query é processada, recebe enhancement automático, utiliza cache quando disponível e apresenta resultados ordenados por relevância (os mais similares).

### Execução de Componentes Individuais

Cada componente do sistema pode ser executado independentemente para desenvolvimento, debugging ou análise específica de uma fase do pipeline.

```bash
python3 <nome_ficheiro>.py
```

## 🏗️ Arquitectura

### Fluxo de Dados Principal

O sistema segue uma arquitectura pipeline onde os dados fluem sequencialmente através de múltiplas fases de processamento. Inicia com a extração de dados XML do RepositoriUM, processa para formato JSON estruturado, aplica validação e limpeza, calcula similaridades com clustering, treina o modelo de embeddings, pré-computa embeddings com cache e finaliza com o sistema de retrieval interativo.

### Arquitectura de Componentes

A arquitectura é organizada em quatro camadas principais: Data Layer (dados brutos e processados), Processing Layer (extração e processamento), ML Layer (treino e embeddings) e Retrieval Layer (pesquisa e avaliação). Esta separação permite modularidade, testabilidade e manutenibilidade do sistema.

## 🧠 Componentes Técnicos

### 📥 **Extração de Dados (data_extraction.py)**

O sistema extrai documentos do RepositoriUM utilizando o protocolo OAI-PMH com múltiplas otimizações para robustez e eficiência.

#### **Estratégias de Robustez:**
- **Rate Limiting Inteligente**: Implementa delay adaptativo entre requests (1-3 segundos) para evitar sobrecarga do servidor e respeitar políticas de uso
- **Retry com Backoff Exponencial**: Sistema de retry com até 3 tentativas e delays crescentes exponencialmente com jitter aleatório para evitar thundering herd
- **Timeout Configurável**: Timeout de 45 segundos por request por defeito, ajustável conforme latência da rede e tamanho dos dados
- **Gestão de Erros Consecutivos**: Para automaticamente após 5 erros consecutivos para evitar loops infinitos e proteger o servidor remoto

#### **Suporte Multi-Coleção:**
O sistema suporta extração simultânea de múltiplas coleções do RepositoriUM, incluindo Mestrados em Informática, outros Mestrados e Doutoramentos. A distribuição é feita de forma inteligente, monitorizando progresso e ajustando dinamicamente o número de registos por coleção.

#### **Otimizações de Performance:**
- **Extração por Lotes**: Utiliza resumption tokens do protocolo OAI-PMH para processar grandes volumes de dados eficientemente
- **Processamento Paralelo**: Metadados são processados em paralelo durante a extração para maximizar throughput
- **Compressão Automática**: XML de saída é comprimido automaticamente para poupar espaço de armazenamento
- **Monitorização em Tempo Real**: Estatísticas detalhadas são apresentadas durante a extração para acompanhamento do progresso

### 🔧 **Processamento de Dados (data_processing.py)**

Converte dados XML para formato JSON estruturado através de um pipeline de limpeza multi-fase que garante qualidade e consistência dos dados.

#### **Pipeline de Limpeza:**

O sistema implementa um pipeline de limpeza em quatro fases principais:

1. **Remoção de Caracteres de Controlo**: Elimina caracteres não imprimíveis que podem corromper o processamento posterior, utilizando categorização Unicode para identificar caracteres problemáticos.

2. **Normalização de Espaços**: Converte múltiplos espaços, tabs e quebras de linha em espaços únicos através de expressões regulares.

3. **Limpeza de Metadados**: Remove tags XML residuais, entidades HTML mal formadas e outros artefactos do processamento XML.

4. **Normalização de Datas**: Extrai anos no formato YYYY através de expressões regulares para garantir consistência temporal nos metadados.

#### **Validação de Qualidade Rigorosa:**
- **Abstracts**: Validação de tamanho mínimo (50 caracteres) e máximo (2000 caracteres) para evitar ruído
- **Títulos**: Verificação de obrigatoriedade e não-vazio para garantir metadados essenciais
- **Metadados**: Validação de estrutura e tipos de dados para consistência
- **Encoding**: Verificação e correção automática de problemas de codificação UTF-8

#### **Estruturação JSON:**
O sistema produz documentos JSON estruturados com campos normalizados incluindo identificador único, título limpo, abstract processado, lista de autores, keywords extraídas, data normalizada, classificações UDC e FoS, e memberships de coleções.

### 🧮 **Cálculo de Similaridades (similarity_calculator.py)**

Implementa uma abordagem híbrida que combina clustering inteligente, TF-IDF otimizado e múltiplas dimensões de similaridade para criar dados de treino de alta qualidade.

#### **1. Estratégia de Clustering Adaptativo**

Para coleções grandes (> 1000 documentos), o sistema utiliza clustering para reduzir drasticamente a complexidade computacional de O(n²) para O(n log n).

**Implementação MiniBatch K-Means:**
O sistema utiliza MiniBatch K-Means com número de clusters adaptativo baseado no tamanho da coleção, processamento em lotes de 1000 documentos e seed fixo para reprodutibilidade.

**Vantagens do Clustering:**
- **Eficiência Computacional**: Redução dramática da complexidade algorítmica
- **Qualidade dos Pairs**: Documentos no mesmo cluster têm alta probabilidade de similaridade semântica
- **Diversidade**: Pairs entre clusters diferentes fornecem exemplos negativos valiosos para treino
- **Escalabilidade**: Funciona eficientemente com dezenas de milhares de documentos

**Estratégia de Sampling Inteligente:**
O sistema gera pairs intra-cluster para alta similaridade (máximo 100 pairs por cluster) e pairs inter-cluster para baixa similaridade (33% de exemplos negativos), aplicando threshold de qualidade de 0.3 para filtrar pairs de baixa qualidade.

#### **2. TF-IDF Híper-Otimizado**

O vectorizador TF-IDF é configurado com parâmetros cientificamente calibrados para maximizar informação semântica enquanto mantém eficiência computacional.

**Configuração Otimizada:**
- **max_features=5000**: Vocabulário limitado aos 5000 termos mais informativos para equilibrar informação vs. eficiência
- **ngram_range=(1,2)**: Unigramas e bigramas para capturar contexto e expressões como "machine learning"
- **min_df=2**: Termos devem aparecer em pelo menos 2 documentos para eliminar typos e termos únicos
- **max_df=0.8**: Remove termos em mais de 80% dos documentos (palavras muito comuns que não discriminam)

#### **3. Similaridade Multi-Dimensional Avançada**

O sistema combina múltiplos sinais de similaridade com pesos cientificamente calibrados para capturar diferentes aspectos da relevância semântica.

**Componentes da Similaridade:**
- **Similaridade de Assuntos UDC/FoS**: 30% do peso total, utiliza índice de Jaccard para conjuntos de classificações
- **Similaridade de Keywords**: 20% do peso total, também com índice de Jaccard para robustez
- **TF-IDF Base**: 70% do peso total, utilizando similaridade coseno para vectores densos

**Justificação da Ponderação:**
A ponderação 70/30 permite que a similaridade semântica TF-IDF domine (captura semântica profunda) enquanto os metadados refinam e ajustam (estrutura e classificação formal).

### 🧩 **Processamento de Queries (query_processor.py)**

Sistema que normaliza e otimiza queries para maximizar a qualidade dos resultados de pesquisa através de um pipeline de processamento completo.

#### **Pipeline de Processamento:**

1. **Limpeza de Texto Avançada**: Remove caracteres de controlo e normaliza espaços múltiplos utilizando as mesmas funções do processamento de documentos para garantir consistência.

2. **Tokenização Inteligente**: Utiliza o tokenizador NLTK punkt que lida corretamente com pontuação, contrações e casos especiais da língua portuguesa e inglesa.

3. **Remoção de Stop Words Multi-idioma**: Sistema adaptativo que tenta português primeiro e faz fallback para inglês, garantindo robustez em ambientes multilíngues.

4. **Extração de Keywords Filtrada**: Filtra tokens alfabéticos com mais de 2 caracteres, excluindo stop words para manter apenas termos semanticamente relevantes.

#### **Classificação Automática de Queries:**
O sistema classifica automaticamente queries em categorias (empty, single_term, short_phrase, long_phrase) para permitir estratégias de pesquisa adaptadas ao tipo de query.

#### **Estratégias de Enhancement:**
Implementa duplicação estratégica de keywords para reforço semântico, aumentando o peso TF-IDF dos termos importantes sem alterar a semântica fundamental da query.

#### **Consistência com Documentos:**
O processamento de queries utiliza exactamente as mesmas funções (clean_text, extract_keywords) que o processamento de documentos, garantindo consistência perfeita na representação textual entre queries e documentos.

### 🤖 **Treino de Modelos (model_trainer.py)**

Implementa fine-tuning avançado de sentence transformers com múltiplas otimizações para eficiência e qualidade, utilizando técnicas de machine learning modernas.

#### **Modelo Base Estrategicamente Escolhido:**
Utiliza o modelo "sentence-transformers/all-MiniLM-L6-v2" que oferece o melhor compromisso entre tamanho (23M parâmetros), velocidade (5x mais rápido que modelos maiores), qualidade (mantém 95% da performance) e suporte multilíngue nativo.

#### **Estratégias de Treino:**

**1. Early Stopping:**
Implementa early stopping com paciência de 2 épocas, guardando checkpoints do melhor modelo e restaurando automaticamente quando a performance de validação para de melhorar.

**2. Split Automático de Dados:**
Quando não são fornecidos dados de validação, o sistema automaticamente reserva 10% dos dados de treino para validação, garantindo avaliação robusta.

**3. Configuração Adaptativa:**
DataLoader configurado com batch size otimizado para GPUs modernas (32), paralelização condicional baseada na disponibilidade de GPU e memory pinning para otimização de transferência de dados.

#### **Loss Function Especializada:**
Utiliza CosineSimilarityLoss que optimiza directamente a métrica usada no retrieval, oferece maior estabilidade que MSE e produz scores directamente interpretáveis como similaridade.

#### **Avaliação Rápida Durante Treino:**
Sistema de avaliação que utiliza apenas 200 exemplos para velocidade, processamento em batches para eficiência, embeddings vectorizados e correlação de Pearson como métrica de qualidade.

### 🚀 **Sistema de Cache (caching_system.py)**

Implementação de cache híbrido que combina memória RAM e armazenamento persistente para máxima performance e eficiência.

#### **Arquitectura do Cache Híbrido:**

**1. Memory Cache (Tier 1 - RAM):**
Cache em memória com acesso O(1), zero I/O e substituição LRU implícita quando atinge o limite configurável de 1000 embeddings.

**2. Disk Cache (Tier 2 - SSD/HDD):**
Cache persistente que sobrevive a reinicializações, com capacidade ilimitada (limitada apenas pelo espaço em disco) e compressão automática via pickle.

#### **Sistema de Chaves Inteligente:**
Utiliza hash MD5 de uma combinação modelo+texto para garantir que embeddings de modelos diferentes não colidem, produzindo chaves de tamanho fixo independente do tamanho do texto e sendo determinística para consistência.

#### **Operações Batch:**
Implementa operações batch para minimizar syscalls, garantir atomicidade de operações em grupo e facilitar monitorização de progresso.

#### **Estratégia de Cache Hierárquico:**
Sistema de dois níveis onde o Tier 1 (memória) é verificado primeiro para máxima velocidade, seguido do Tier 2 (disco) para persistência, com promoção automática de embeddings do disco para memória quando há espaço disponível.

### 🔍 **Sistema de Retrieval (retrieval_system.py)**

Motor de pesquisa semântica que integra todos os componentes numa experiência de pesquisa fluida e eficiente.

#### **Inicialização com Cache Inteligente:**
Sistema inicializado com QueryProcessor para processamento de queries, EmbeddingCache para performance e carregamento automático do modelo treinado.

#### **Pré-computação de Embeddings com Cache:**
Verifica cache em batch para todos os abstracts, carrega instantaneamente se 100% cache hit, calcula apenas embeddings em falta se cache parcial, e reconstrói array completo mantendo ordem dos documentos.

#### **Retrieval com Processamento de Query Integrado:**
Pipeline completo que processa a query, aplica enhancement, verifica cache para embedding da query, calcula similaridades vectorizadas, aplica boost baseado em metadados e retorna resultados ordenados por relevância.

#### **Similaridade Semântica Vectorizada:**
Implementa produto escalar normalizado (similaridade coseno) utilizando vectorização NumPy para operações SIMD, broadcasting para evitar loops explícitos e arrays contíguos para eficiência de cache CPU.

#### **Sistema de Boost Inteligente:**
Aplica boost de 10% por match de keywords exactas, 15% por match no título (mais importante), com cap máximo de 50% para evitar dominação da similaridade semântica e preservação da ordenação relativa base.

### 📊 **Sistema de Avaliação (evaluation_system.py)**

Framework completo de avaliação que implementa métricas padrão de Information Retrieval para validar rigorosamente a qualidade do sistema.

#### **Métricas de Retrieval Implementadas:**

**1. Precision@K:** Mede a proporção de documentos relevantes nos top-K resultados retornados.

**2. Recall@K:** Mede a proporção de documentos relevantes totais que foram recuperados nos top-K resultados.

**3. Mean Average Precision (MAP):** Calcula a média das precisões em cada posição onde um documento relevante é encontrado.

**4. Mean Reciprocal Rank (MRR):** Calcula a média do inverso da posição do primeiro documento relevante encontrado.

### 🛠️ **Validação de Dados (data_validator.py)**

Sistema robusto de validação que garante a qualidade e consistência dos dados através de múltiplas fases de verificação rigorosa.

#### **Validação XML Prévia:**
Verifica integridade do XML antes do processamento, remove duplicados por identifier já na fase XML e produz estatísticas de duplicados encontrados.

#### **Pipeline de Limpeza Multi-Fase:**

**Fase 1 - Remoção de Duplicados:**
Remove duplicados por ID exacto primeiro, depois duplicados por conteúdo utilizando assinatura baseada em título+autores+data normalizada.

**Fase 2 - Validação de Qualidade:**
Verifica obrigatoriedade de títulos, valida tamanho de abstracts (mínimo 50, máximo 2000 caracteres), e remove documentos que não cumprem critérios de qualidade.

## ⚙️ Configuração Avançada

### Parâmetros de Performance

O sistema oferece configuração detalhada de parâmetros para clustering (sample ratio de 5%, clustering para coleções > 1000 docs), cache (1000 embeddings em memória, cache persistente ativo), TF-IDF (vocabulário de 5000 features, min_df=2, max_df=0.8) e extração (timeout de 45s, 3 retries, delay base de 1s).

### Modelo e Treino

Configuração do modelo base all-MiniLM-L6-v2, 2 épocas de treino, batch size de 32, threshold de similaridade de 0.2 para pairs de treino, e validação de abstracts entre 50-2000 caracteres.

## 🛠️ Tecnologias Utilizadas

- **Sentence Transformers**: Framework para embeddings semânticos
- **Scikit-learn**: Biblioteca para machine learning e TF-IDF
- **NLTK**: Toolkit para processamento de linguagem natural
- **NumPy**: Biblioteca para computação científica e vectorização
- **PyTorch**: Framework para deep learning e neural networks

## 👥 Contribuidores

- [João Coelho - PG55954](https://github.com/JoaoCoelho2003)
- [José Rodrigues - PG55969](https://github.com/FilipeR13)
- [Mariana Silva - PG55980](https://github.com/MarianaSilva659)

---