# Pipeline RAG Intelligent - Amélioration de la Précision des Réponses par Filtrage Intelligent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Deployed-FF9900)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[English](README.md)

Système de génération augmentée par récupération (RAG) production-ready qui filtre les informations non pertinentes avant la génération de réponses, offrant des résultats IA plus précis et fiables.

**Parfait pour :** Support client, analyse de documents juridiques, recherche dans la documentation technique, vérification de conformité

---

## Impact

Les chatbots et systèmes de Q&A standards souffrent souvent de problèmes critiques :

- ❌ **Hallucinations** - Donnent des réponses confiantes mais incorrectes
- ❌ **Bruit informationnel** - Mélangent informations pertinentes et non pertinentes
- ❌ **Échecs sur questions complexes** - Peinent avec les questions multi-parties

**Ce système résout ces problèmes en :**

- ✅ Filtrant le bruit avant de générer les réponses (améliorations démontrées de la précision)
- ✅ Validant chaque information indépendamment
- ✅ Gérant les questions complexes nécessitant plusieurs sources

**Impact réel :**
- Réduction des erreurs et du temps de réponse du support client
- Révision de documents plus rapide pour les équipes juridiques et de conformité
- Recherche dans les bases de connaissances plus fiable
- Réduction des coûts opérationnels grâce à moins de réponses incorrectes

---
## Fonctionnement

### Vue d'Ensemble Simple

Le système utilise une approche de filtrage intelligent en trois étapes :

1. **Récupération** - Recherche de documents potentiellement pertinents via recherche vectorielle dense (FAISS)
2. **Vérification** - L'IA valide chaque document : *"Cette information supporte-t-elle réellement la réponse à la question ?"*
3. **Filtrage** - Ne conserve que les informations vérifiées et pertinentes
4. **Génération** - Crée une réponse à partir de données propres et validées uniquement

### Trois Variantes de Pipeline

| Pipeline | Description | Idéal Pour |
|----------|-------------|------------|
| **RAG Baseline** | Récupération + génération standard | Questions factuelles simples |
| **RAG + NLI** | Ajoute un filtrage intelligent via inférence en langage naturel | Q&A général avec réduction du bruit |
| **RAG + NLI + Sous-Affirmations** | Décompose les questions complexes en parties plus simples | Questions multi-parties, comparatives |

### Architecture 

<p align="center">
  <img src="docs/images/Graph_rag_nli_sub.png" alt="Architecture RAG avec NLI" width="600">
  <br>
  <em>Workflow de Décomposition en Sous-Affirmations et Filtrage par Implication NLI</em>
</p>

📖 **Explications techniques détaillées :**
- [Explication détaillée RAG + NLI](docs/rag_nli.md)
- [Explication détaillée RAG + NLI + Sous-Affirmations](docs/rag_nli_subclaim.md)

---

## Métriques

**Évaluation sur le benchmark de référence HotpotQA :**

| Métrique | Amélioration vs Baseline |
|----------|--------------------------|
| **Précision des Réponses (Exact Match)** | **+16%** |
| **Qualité des Réponses (Score F1)** | **+10%** |

Ces améliorations proviennent de la **réduction intelligente du bruit de récupération**, pas simplement de plus de puissance de calcul.

📈 [Voir les résultats d'évaluation détaillés](docs/evaluations.md)

---
## Agent d'Analyse

Agent de débogage intégré propulsé par Gemini qui explique les décisions du pipeline en langage naturel.

**Exemple d'Analyse :**

**1. Comparaison des Résultats :**

<p align="center">
  <img src="docs/images/Agent_compare.png" alt="Comparaison RAG vs NLI" width="600">
</p>

L'agent montre comment la baseline échoue (hallucination) tandis que le système filtré réussit.

**2. Comprendre Pourquoi :**

<p align="center">
  <img src="docs/images/Agent_analysis.png" alt="Analyse Logique Agent" width="600">
</p>

L'agent explique que le module NLI a filtré avec succès le passage "distracteur" sur Rihanna car il ne validait pas l'affirmation sur l'album "Confessions" d'Usher.

*Cet agent aide pendant le développement à analyser les décisions du pipeline, comparer les sorties baseline vs filtrées, et fournit des insights actionnables pour l'optimisation du système.*

---

## Démarrage Rapide

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer les expériences

```bash
python -m scripts.run_experiments
```

Cela exécutera tous les pipelines sur un sous-ensemble de HotpotQA et affichera les métriques d'évaluation.

### 3. Lancer l'API

Le projet expose un service FastAPI qui donne accès à un agent d'analyse.

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001
```

## Configuration de la Clé API (Gemini)

Certains composants (agent d'analyse) utilisent Gemini 2.5 Flash.

1. Générez une clé API ici :
   [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. Créez un fichier nommé `.env` à la racine du projet.

3. Ajoutez votre clé dans le fichier `.env` :
   ```env
   GOOGLE_API_KEY=votre_cle_api_ici
   ```

---
## Déploiement Docker

Déploiement conteneurisé prêt pour la production :

```bash
# Construire l'image Docker
docker build -t rag-nli-app .

# Lancer le conteneur
docker run -p 8001:8001 rag-nli-app

# Accéder à l'API
curl http://localhost:8001/health
```

**Déploiement testé sur :**
- Développement local (Linux/macOS/Windows)
- AWS EC2 (Ubuntu)
- Services de conteneurs cloud (compatible ECS, Cloud Run)

---

## Applications Concrètes

| Domaine |
|---------|
| **Support Client** |
| **Juridique & Conformité** |
| **Documentation Technique** |
| **Information Médicale** |


## Structure du Projet

```
rag-nli/
│
├── rag/                 # Modules de récupération & génération
├── nli/                 # Modèle NLI et logique de filtrage
├── pipelines/           # Implémentations des pipelines
│   ├── baseline.py      # RAG standard
│   ├── nli.py           # RAG + filtrage NLI
│   └── subclaim.py      # RAG + NLI + Sous-affirmations
├── evaluation/          # Métriques et lanceurs d'expériences
├── agents/              # Agent d'analyse pour le débogage
├── api/                 # Service FastAPI
├── scripts/             # Scripts d'exécution d'expériences
├── data/                # Stockage des datasets
├── docs/                # Documentation détaillée
├── Dockerfile           # Configuration du conteneur
└── README.md
```

## Limitations & Améliorations

**Limitations actuelles :**
- La décomposition en sous-affirmations utilise des heuristiques basées sur des règles (peut être améliorée avec décomposition apprise)
- Tous les types de questions dans HotpotQA ne bénéficient pas également de la décomposition
- Évaluation réalisée sur CPU uniquement (pas encore de tests de significativité statistique)
- Évaluation à échelle proof-of-concept (démontre la méthodologie sur un sous-ensemble du benchmark)
- Focus sur la réduction du bruit de récupération, pas la prévention complète des hallucinations

**Améliorations futures :**
- Génération de sous-affirmations apprise utilisant des LLMs
- Évaluation accélérée par GPU pour tests statistiques
- Couverture de datasets élargie au-delà de HotpotQA
- Modèles NLI fine-tunés pour des cas d'usage spécifiques au domaine

Ces limitations sont reconnues pour souligner le réalisme et guider le développement futur.

---

## Technologies 

**Technologies Principales :**
- **Python 3.10+** - Langage de programmation principal
- **FastAPI** - Framework API de production
- **Docker** - Conteneurisation

**Stack IA/ML :**
- **Hugging Face Transformers** - Modèles NLI et génération de texte
- **FAISS** - Recherche rapide de similarité vectorielle
- **LangChain / LangGraph** - Orchestration de pipelines

**Déploiement :**
- **AWS EC2** - Déploiement cloud testé
- **Google Gemini** - Agent d'analyse

---

## Références

[1] Lu Dai, Hao Liu, Hui Xiong. "Improve Dense Passage Retrieval with Entailment Tuning." The Hong Kong University of Science and Technology, 2024.

[2] Ori Yoran, et al. "Making Retrieval-Augmented Language Models Robust to Irrelevant Context." ICLR, 2024. (Foundational work on noise filtration in RAG).

[3] Akari Asai, et al. "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." ICLR, 2024. (Context regarding self-correction and claim support).

[4] Shahul Es, et al. "RAGAS: Automated Evaluation of Retrieval Augmented Generation." EACL, 2024. (Framework used for defining Faithfulness metrics via NLI).

[5] Nelson F. Liu, et al. "Lost in the Middle: How Language Models Use Long Contexts." TACL, 2024. (Highlights the necessity of filtering to avoid performance degradation in long contexts).

---
