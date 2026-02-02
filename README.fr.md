# RAG avec NLI et Décomposition en Sous-Revendications

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Deployed-FF9900)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[English](README.md)

Système RAG prêt pour la production qui filtre les informations non pertinentes avant la génération de réponses, offrant des réponses IA plus précises et fiables.

**Cas d’usage :** Support client, analyse de documents juridiques, recherche dans la documentation technique, vérification de conformité

---

## Enjeux

Les chatbots et systèmes de questions-réponses standards souffrent souvent de problèmes critiques :

- ❌ **Hallucinations** - Donnent des réponses confiantes mais incorrectes
- ❌ **Bruit informationnel** - Mélangent contenu pertinent et non pertinent
- ❌ **Échecs sur questions complexes** - Peinent avec les questions à plusieurs parties

**Ce système résout ces problèmes en :**

- ✅ Filtrant le bruit avant de générer les réponses (améliorations démontrées de la précision)
- ✅ Validant chaque élément d'information indépendamment
- ✅ Gérant les questions complexes nécessitant plusieurs sources

**Impact concret :**
- Réduction des erreurs et du temps de réponse du support client
- Examen plus rapide des documents pour les équipes juridiques et de conformité
- Recherche plus fiable dans les bases de connaissances
- Coûts opérationnels réduits grâce à moins de réponses incorrectes

---

## Applications Clés

| Domaine | Impact Principal |
|---------|------------------|
| 📞 Support Client | Résolution plus rapide des tickets, réponses plus fiables |
| ⚖️ Juridique & Conformité | Analyse de documents plus rapide, risque juridique réduit |
| 📚 Documentation Technique | Meilleure expérience développeur, charge de support réduite |
| 🏥 Information Santé | Information plus sûre et plus fiable |


## Aperçu de l'Approche

Trois pipelines sont implémentés et comparés :

**Baseline RAG :** Récupération dense (FAISS) + génération basée sur prompts

**RAG + NLI :** Filtre les passages récupérés en utilisant NLI pour ne garder que ceux qui impliquent la revendication ([détails](docs/rag_nli.md))

**RAG + NLI + Sous-Revendications :** Décompose les revendications complexes en sous-revendications, valide chacune indépendamment ([détails](docs/rag_nli_subclaim.md))

## Architecture du Système

Le diagramme ci-dessous illustre le pipeline principal (**RAG + NLI + Sous-Revendications**). Il détaille comment les requêtes complexes sont décomposées et comment le modèle NLI agit comme un gardien sémantique pour filtrer le bruit avant la génération.

<p align="center">
  <img src="docs/images/Graph_rag_nli_sub.png" alt="Architecture RAG avec NLI" width="600">
  <br>
  <em>(Figure : Flux de travail de la Décomposition en Sous-Revendications et du Filtrage par Implication NLI)</em>
</p>

## Évaluation

Les expériences ont été menées sur HotpotQA (configuration avec distracteurs).

**Métriques utilisées :**

- Exact Match
- F1
- BERTScore (Précision / Rappel / F1)

| Métrique | Amélioration vs Baseline |
|----------|--------------------------|
| **Précision des Réponses (Exact Match)** | **+16%** |
| **Qualité des Réponses (Score F1)** | **+10%** |

**Résultats clés :**  
Avec notre pipeline le plus avancé (**RAG + NLI + Sous-Revendications**), nous avons observé jusqu'à **+16% d'amélioration en Exact Match** et **+10% en F1** par rapport à une baseline RAG standard, selon le modèle et la configuration Top-K.


📈 [Voir les résultats d'évaluation détaillés](docs/evaluations.md)

---

## Agent d'Analyse

Agent de débogage intégré propulsé par Gemini qui explique les décisions du pipeline en langage clair.

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

L'agent explique que le module NLI a filtré avec succès le passage "distracteur" sur Rihanna car il n'impliquait pas la revendication sur l'album "Confessions" d'Usher.

*Cet agent aide pendant le développement à analyser les décisions du pipeline, comparer les sorties baseline vs filtrées, et fournit des informations exploitables pour l'ajustement du système.*

---

## Structure du Projet

```
rag-nli/
│
├── rag/                 # Récupération & génération
├── nli/                 # Modèle NLI et logique de filtrage
├── pipelines/           # RAG / RAG+NLI / RAG+NLI+Subclaim
├── evaluation/          # Métriques et expériences
├── agents/              # Agent d'analyse
├── api/                 # Service FastAPI
├── scripts/             # Exécuteurs d'expériences
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

### 2. Exécuter les expériences

```bash
python -m scripts.run_experiments
```

Cela exécutera tous les pipelines sur un sous-ensemble de HotpotQA et affichera les métriques d'évaluation.

### 3. Exécuter l'API

Le projet expose un service FastAPI pour les questions-réponses.

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
   GOOGLE_API_KEY=votre_clé_api_ici
   


## Optionnel : Déploiement Docker

Le projet peut également être conteneurisé en utilisant Docker pour faciliter le déploiement et la reproductibilité.

Un Dockerfile est fourni pour :

- installer les dépendances,
- exposer le service FastAPI,
- exécuter l'application dans un environnement reproductible.

**Exemples de commandes :**

```bash
docker build -t rag-nli-app .
docker run -p 8001:8001 rag-nli-app
```

Cette configuration a été testée localement et déployée sur une instance AWS EC2 (Ubuntu).

## Limitations

- La décomposition en sous-revendications est basée sur des règles et heuristique
- Toutes les revendications dans HotpotQA ne sont pas décomposables
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

[2] Ori Yoran, et al. "Making Retrieval-Augmented Language Models Robust to Irrelevant Context." ICLR, 2024. (Travail fondamental sur la filtration du bruit dans RAG).

[3] Akari Asai, et al. "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." ICLR, 2024. (Contexte concernant l'auto-correction et le support des revendications).

[4] Shahul Es, et al. "RAGAS: Automated Evaluation of Retrieval Augmented Generation." EACL, 2024. (Framework utilisé pour définir les métriques de Fidélité via NLI).

[5] Nelson F. Liu, et al. "Lost in the Middle: How Language Models Use Long Contexts." TACL, 2024. (Souligne la nécessité du filtrage pour éviter la dégradation des performances dans les contextes longs).
