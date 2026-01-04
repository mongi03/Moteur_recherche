📄 Moteur de recherche documentaire (Reddit & ArXiv)
📌 Description

Ce projet consiste à développer un moteur de recherche documentaire en Python, basé sur un ensemble de documents textuels issus de différentes sources, notamment Reddit et ArXiv.

L’objectif principal est de permettre à un utilisateur de formuler des requêtes par mots-clés et d’obtenir une liste de documents classés par pertinence, à l’aide de méthodes statistiques classiques de recherche d’information (TF, TF-IDF, similarité cosinus).

Le projet inclut également une interface graphique interactive permettant une utilisation conviviale du moteur de recherche, sans nécessiter de connaissances en programmation.

🎯 Fonctionnalités principales

Constitution et gestion d’un corpus de documents textuels

Moteur de recherche basé sur :

fréquence des termes (TF),

pondération TF-IDF,

similarité cosinus

Recherche par mots-clés

Classement des documents par pertinence

Interface graphique interactive avec ipywidgets

Filtres de recherche :

source (Reddit / ArXiv),

auteur,

période temporelle

Analyse de l’évolution temporelle d’un mot-clé

Comparaison des résultats entre Reddit et ArXiv

🧱 Structure du projet
├── Corpus.py
├── Document.py
├── RedditDocument.py
├── ArxivDocument.py
├── SearchEngine.py
├── Author.py
├── main.ipynb / main.py
├── data/
│   └── corpus.csv
├── README.md

🛠️ Environnement et dépendances

Python ≥ 3.9

Environnement virtuel recommandé (venv)

Bibliothèques principales :

numpy

pandas

scipy

matplotlib

ipywidgets

praw

xmltodict

certifi

Installation des dépendances :

pip install numpy pandas scipy matplotlib ipywidgets praw xmltodict certifi

▶️ Lancer le projet

Cloner le dépôt :

git clone <url_du_repo>
cd <nom_du_repo>


Créer et activer un environnement virtuel :

python3 -m venv .venv
source .venv/bin/activate


Lancer Jupyter Notebook :

jupyter notebook


Ouvrir le notebook principal et exécuter les cellules pour :

charger le corpus,

lancer l’interface graphique,

effectuer des recherches.

🧠 Méthodes utilisées

Modèle vectoriel de documents

Pondération TF-IDF

Similarité cosinus

Normalisation du texte

Filtrage des résultats par métadonnées

🧪 Tests

Les tests ont été réalisés de manière incrémentale :

tests unitaires des méthodes principales (corpus, moteur de recherche),

tests globaux via l’interface graphique,

vérification des cas particuliers (requêtes vides, absence de résultats, documents sans date).

🚀 Évolutions possibles

Ajout du modèle BM25

Amélioration du prétraitement linguistique (lemmatisation, stop-words)

Intégration de nouvelles sources documentaires

Déploiement sous forme d’application web

📚 Sources et utilisation de l’IA

Le projet s’appuie sur :

la documentation officielle des bibliothèques Python utilisées,

les supports de cours,

les documentations des API Reddit et ArXiv.

Un outil d’intelligence artificielle (ChatGPT) a été utilisé comme assistant pédagogique, notamment pour :

clarifier certains concepts théoriques,

aider à la résolution d’erreurs,

améliorer la structuration du projet et de la documentation.

L’ensemble du code et des choix de conception a été implémenté et validé par l’étudiant.

👤 Auteur

Projet réalisé individuellement dans un cadre universitaire.