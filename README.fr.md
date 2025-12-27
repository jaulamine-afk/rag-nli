# RAG avec NLI et Décomposition en Sous-Affirmations

[English](README.md)

Ce projet explore comment l'inférence en langage naturel (NLI) et la décomposition d'affirmations peuvent être intégrées dans un pipeline de génération augmentée par récupération (RAG) pour réduire le bruit de récupération et améliorer les réponses.



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

### RAG + NLI + Sous-Affirmations

- Les affirmations complexes sont décomposées en sous-affirmations plus simples
- Chaque sous-affirmation est validée indépendamment avec NLI
- Les passages ne sont conservés que s'ils soutiennent au moins une sous-affirmation

Cela permet un filtrage plus fin, en particulier pour les questions comparatives ou compositionnelles.

## Évaluation

Les expériences ont été menées sur HotpotQA (configuration avec distracteurs).

**Métriques utilisées :**

- Exact Match
- F1
- BERTScore (Précision / Rappel / F1)

Les résultats montrent des améliorations constantes par rapport au RAG de base, avec :

- réduction des passages non pertinents,
- amélioration de l'ancrage des réponses,
- et gains plus nets pour les questions à forte composition.

## Agent d'Analyse (Démonstration)

En plus de l'évaluation quantitative, le projet inclut un agent d'analyse propulsé par Gemini.

Cet agent :

- compare les réponses de RAG vs RAG + NLI Sous-Affirmations,
- inspecte les passages récupérés avant et après filtrage,
- explique pourquoi un pipeline produit une réponse plus fiable.

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
├── config/
├── data/
└── README.md
```

## Exécution du Projet

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer les expériences

```bash
python scripts/run_experiments.py
```

Cela exécutera tous les pipelines sur un sous-ensemble de HotpotQA et affichera les métriques d'évaluation.

### 3. Lancer l'API

Le projet expose un service FastAPI pour la réponse aux questions.

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001
```

## Configuration de la Clé API (Gemini)

Certains composants (agent d'analyse) utilisent Gemini 2.5 Flash.

Vous devez générer une clé API ici :  
👉 https://aistudio.google.com/app/apikey

Collez votre clé API dans le fichier `code_api.txt` à la racine du projet.

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
