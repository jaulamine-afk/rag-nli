# RAG avec NLI et Décomposition en Sous-Affirmations

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Deployed-FF9900)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[English](README.md)

Mon projet explore comment l'inférence en langage naturel (NLI) et la décomposition d'affirmations peuvent être intégrées dans un pipeline de génération augmentée par récupération (RAG) pour réduire le bruit de récupération et améliorer les réponses.



## Motivation

Les systèmes RAG standards récupèrent souvent des passages qui sont :

- vaguement liés à la question,
- partiellement contradictoires,
- ou non pertinents mais sémantiquement similaires.

Ce bruit peut perturber le générateur et dégrader la qualité des réponses.

Ce projet propose :

- d'utiliser un filtrage NLI basé sur l'implication pour ne conserver que les passages qui soutiennent logiquement une affirmation,
- et une extension basée sur la décomposition en sous-affirmations pour les questions comparatives ou multi-entités.

## Aperçu de l'Approche

Trois pipelines sont implémentés et comparés :

### RAG de Base

- Récupération dense (FAISS)
- Génération basée sur des prompts

### RAG + NLI

- Les passages récupérés sont filtrés à l'aide d'un modèle NLI
- Seuls les passages qui impliquent l'affirmation sont conservés 
- Une explication détaillée de la méthode est disponible ici [RAG + NLI](docs/rag_nli.md).

### RAG + NLI + Sous-Affirmations

- Les affirmations complexes sont décomposées en sous-affirmations plus simples
- Chaque sous-affirmation est validée indépendamment avec NLI
- Les passages ne sont conservés que s'ils soutiennent au moins une sous-affirmation
- Une explication détaillée de la méthode est disponible ici [RAG + NLI + Sub-Claims](docs/rag_nli_subclaim.md).

Cela permet un filtrage plus fin, en particulier pour les questions comparatives ou compositionnelles.

## Architecture du Système

Le diagramme ci-dessous illustre le pipeline principal (**RAG + NLI + Sous-Affirmations**). Il détaille comment les requêtes complexes sont décomposées et comment le modèle NLI agit comme un filtre sémantique (*gatekeeper*) pour éliminer le bruit avant la génération.

<p align="center">
  <img src="docs/images/Graph_rag_nli_sub.png" alt="Architecture RAG avec NLI" width="600">
  <br>
  <em>(Figure : Flux de travail de la décomposition en sous-affirmations et du filtrage par implication NLI)</em>
</p>

## Évaluation

Les expériences ont été menées sur HotpotQA (configuration avec distracteurs).

**Métriques utilisées :**

- Exact Match
- F1
- BERTScore (Précision / Rappel / F1)

   **Résultats clés :**  
Avec notre pipeline le plus avancé (**RAG + NLI + Subclaims**) on observe jusqu’à **+16 % d’amélioration en Exact Match** et **+10 % en F1** par rapport au RAG de base, selon le modèle et la configuration Top-K.

Ces gains proviennent principalement de la **réduction du bruit de retrieval**, grâce au filtrage par inférence logique (NLI) et à la décomposition en sous-claims, plutôt que d’une simple augmentation de la capacité du générateur.

Les résultats montrent des améliorations constantes par rapport au RAG de base, avec :

- réduction des passages non pertinents ou hors sujet,
- amélioration de l’ancrage factuel des réponses,
- gains plus nets pour les questions compositionnelles ou comparatives.

Les résultats détaillés (par modèle et par Top-K) sont disponibles dans :  
[`docs/evaluations.md`](docs/evaluations.md)


## Agent d'Analyse (Démonstration)

Le projet inclut un agent d'analyse propulsé par Gemini qui inspecte les décisions du pipeline.

**1. Comparaison des Résultats :**
L'agent affiche d'abord l'affirmation générée et compare les réponses. La baseline échoue (hallucination) tandis que notre système réussit.

<p align="center">
  <img src="docs/images/Agent_compare.png" alt="Comparaison RAG vs NLI" width="600">
</p>

**2. Raisonnement & Filtrage :**
Ensuite, il explique *pourquoi* la correction a eu lieu : le module NLI a rejeté le passage "piège" sur Rihanna car il ne validait pas l'affirmation concernant l'album "Confessions".

<p align="center">
  <img src="docs/images/Agent_analysis.png" alt="Analyse Logique Agent" width="600">
</p>

Ce composant est conçu comme un outil pédagogique et d'interprétabilité, et non comme partie intégrante de la boucle d'évaluation principale.

## Structure du Projet

```
rag-nli-subclaim/
│
├── rag/                 # Récupération et génération
├── nli/                 # Modèle NLI et logique de filtrage
├── pipelines/           # RAG / RAG+NLI / RAG+NLI+Subclaim
├── evaluation/          # Métriques et expériences
├── agents/              # Agent d'analyse
├── api/                 # Service FastAPI
├── scripts/             # Lanceurs d'expériences
├── data/
├── docs/
└── Dockerfile              
└── README.md
```

## Exécution du Projet

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

Le projet expose un service FastAPI pour la réponse aux questions.

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001
```

## Configuration de la Clé API (Gemini)

Certains composants (notamment l'agent d'analyse) utilisent Gemini 2.5 Flash.

1. Générez une clé API ici :
   [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. Créez un fichier nommé `.env` à la racine du projet.

3. Ajoutez votre clé dans le fichier `.env` :
   ```env
   GOOGLE_API_KEY=votre_cle_ici
   
## Optionnel : Déploiement Docker

Le projet peut également être conteneurisé avec Docker pour faciliter le déploiement et la reproductibilité.

Un Dockerfile est fourni pour :

- installer les dépendances,
- exposer le service FastAPI,
- exécuter l'application dans un environnement reproductible.

**Commandes d'exemple :**

```bash
docker build -t rag-nli-app .
docker run -p 8001:8001 rag-nli-app
```

Cette configuration a été testée localement et déployée sur une instance AWS EC2 (Ubuntu).

## Limitations

- La décomposition en sous-affirmations est basée sur des règles et heuristique
- Toutes les affirmations dans HotpotQA ne sont pas décomposables
- Pas de tests de significativité statistique (configuration CPU uniquement)
- L'accent est mis sur la réduction du bruit de récupération, pas sur la prévention complète des hallucinations

Ces limitations sont discutées de manière transparente pour souligner le réalisme et la reproductibilité.

## Technologies

- Python
- Hugging Face
- FAISS
- FastAPI
- LangChain / LangGraph
- Docker
- AWS
- Gemini (Google GenAI)

## Références

[1] Lu Dai, Hao Liu, Hui Xiong. "Improve Dense Passage Retrieval with Entailment Tuning." The Hong Kong University of Science and Technology, 2024.

[2] Ori Yoran, et al. "Making Retrieval-Augmented Language Models Robust to Irrelevant Context." ICLR, 2024. (Foundational work on noise filtration in RAG).

[3] Akari Asai, et al. "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." ICLR, 2024. (Context regarding self-correction and claim support).

[4] Shahul Es, et al. "RAGAS: Automated Evaluation of Retrieval Augmented Generation." EACL, 2024. (Framework used for defining Faithfulness metrics via NLI).

[5] Nelson F. Liu, et al. "Lost in the Middle: How Language Models Use Long Contexts." TACL, 2024. (Highlights the necessity of filtering to avoid performance degradation in long contexts).
