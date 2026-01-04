text
# 📄 Moteur de Recherche Documentaire (Reddit & ArXiv)

## 🧠 Description

Ce projet consiste à développer un **moteur de recherche documentaire en Python** basé sur un corpus de documents textuels provenant de **Reddit** et **ArXiv**. L’objectif est de permettre à l’utilisateur de formuler des **requêtes par mots-clés** et d’obtenir une **liste de documents classés par pertinence**, à l’aide de méthodes classiques de **recherche d’information** : fréquence des termes (TF), pondération TF-IDF et similarité cosinus.

Le projet inclut également une **interface graphique interactive** (via `ipywidgets`), afin de proposer une utilisation conviviale sans nécessiter de connaissances en programmation.

---

## 🎯 Fonctionnalités

- Constitution et gestion d’un **corpus de documents textuels**
- **Moteur de recherche** basé sur :
  - Fréquence des termes (**TF**)
  - Pondération **TF-IDF**
  - **Similarité cosinus**
- **Recherche par mots-clés** et classement des documents par pertinence
- **Interface graphique interactive** avec `ipywidgets`
- **Filtres de recherche** :
  - Source (Reddit / ArXiv)
  - Auteur
  - Période temporelle
- **Analyse de l’évolution temporelle** d’un mot-clé
- **Comparaison des résultats** entre Reddit et ArXiv

---

## 🧱 Structure du projet

```bash
├── Corpus.py
├── Document.py
├── RedditDocument.py
├── ArxivDocument.py
├── SearchEngine.py
├── Author.py
├── ui.ipynb / main.py
├── README.md
🛠️ Environnement et installation
Prérequis
Python ≥ 3.9

Installation des dépendances
bash
pip install numpy pandas scipy matplotlib ipywidgets praw xmltodict certifi


🧠 Méthodes de recherche d’information
Le moteur repose sur un modèle vectoriel de documents, avec les étapes suivantes :

Normalisation du texte (nettoyage, préparation)

Calcul des vecteurs de documents avec TF-IDF

Calcul de la similarité cosinus entre la requête et chaque document

Filtrage par métadonnées (source, auteur, période temporelle)

Ces méthodes permettent de classer les documents en fonction de leur pertinence par rapport à la requête de l’utilisateur.


🚀 Évolutions possibles
Plusieurs pistes d’amélioration sont envisagées :

Intégration du modèle BM25

Amélioration du prétraitement linguistique :

Lemmatisation

Gestion avancée des stop-words

Intégration de nouvelles sources documentaires

Déploiement du moteur de recherche sous forme d’application web

📚 Références et utilisation de l’IA
Le projet s’appuie sur :

La documentation officielle des bibliothèques Python utilisées (numpy, pandas, scipy, matplotlib, ipywidgets, praw, xmltodict, certifi)

Les supports de cours

Les documentations des API Reddit et ArXiv

Un outil d’intelligence artificielle (ChatGPT) a été utilisé comme assistant pédagogique, notamment pour :

Clarifier certains concepts théoriques

Aider à la résolution d’erreurs

Améliorer la structuration du projet et la rédaction de la documentation

L’ensemble du code et des choix de conception a été implémenté et validé par l’étudiant.

👤 Auteur
Projet réalisé individuellement dans le cadre d’une formation universitaire.

