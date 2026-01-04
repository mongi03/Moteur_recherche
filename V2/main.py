# main.py

# ================================
# IMPORT DES LIBRAIRIES
# ================================
import praw  # Pour interagir avec l'API Reddit
import urllib.request  # Pour récupérer des données depuis ArXiv
import certifi, ssl  # Pour gérer les certificats SSL de manière sécurisée
import xmltodict  # Pour parser les flux XML (ArXiv)
from datetime import datetime  # Pour manipuler les dates
from Corpus import Corpus  # Classe pour gérer un corpus de documents
from RedditDocument import RedditDocument  # Classe représentant un post Reddit
from ArxivDocument import ArxivDocument  # Classe représentant un document ArXiv
from SearchEngine import SearchEngine  # Classe pour rechercher dans le corpus
import pandas as pd  # Pour manipuler des tableaux de données
import re  # Pour le traitement de texte (regex)
from Document import Document  # Classe générique pour un document

# ================================
# INITIALISATION DU CORPUS
# ================================
corpus = Corpus("Corpus_Reddit_Arxiv")  # Création d'un corpus vide nommé "Corpus_Reddit_Arxiv"

# ================================
# CONNEXION À REDDIT
# ================================
reddit = praw.Reddit(
    client_id='vc2Hro3ys8p9rqCG6bHeAg',  # ID client Reddit
    client_secret='gedHKB0SBBkm9H2vEwhnsCPw5UykVg',  # Secret client
    user_agent='WebScraping'  # Nom de l'application pour Reddit
)

print("\n--- Récupération des posts Reddit ---")
ml_subreddit = reddit.subreddit('MachineLearning')  # Accès au subreddit MachineLearning

# Parcours des 50 posts les plus populaires
for post in ml_subreddit.hot(limit=50):
    titre = post.title.replace("\n", " ")  # Nettoyage du titre
    auteur = str(post.author) if post.author else "Inconnu"  # Gestion auteur inconnu
    date_pub = datetime.fromtimestamp(post.created_utc)  # Conversion timestamp en date
    url = f"https://www.reddit.com{post.permalink}"  # URL du post
    texte = post.selftext if post.selftext else post.title  # Texte du post
    nb_comments = post.num_comments  # Nombre de commentaires

    # Création d'un objet RedditDocument et ajout au corpus
    doc = RedditDocument(titre, auteur, date_pub, url, texte, nb_comments)
    corpus.add_document(doc)

# ================================
# RÉCUPÉRATION DES PUBLICATIONS ARXIV
# ================================
print("\n--- Récupération des publications ArXiv ---")
context = ssl.create_default_context(cafile=certifi.where())  # Contexte SSL sécurisé
url = 'http://export.arxiv.org/api/query?search_query=all:Machine&start=0&max_results=50'

# Récupération et parsing du flux XML
data = urllib.request.urlopen(url, context=context).read().decode('utf-8')
dict_data = xmltodict.parse(data)
entries = dict_data['feed']['entry']

# Parcours des publications
for entry in entries:
    titre = entry['title'].replace("\n", " ")  # Nettoyage du titre

    # Gestion d'un ou plusieurs auteurs
    if isinstance(entry['author'], list):
        auteur = entry['author'][0]['name']  # Auteur principal
        coauthors = [a['name'] for a in entry['author'][1:]]  # Co-auteurs
    else:
        auteur = entry['author']['name']
        coauthors = []

    date_pub = datetime.fromisoformat(entry['published'].replace('Z', '+00:00'))  # Conversion date
    url = entry['id']  # URL du document
    texte = entry['summary'].replace("\n", " ")  # Résumé nettoyé

    # Création d'un objet ArxivDocument et ajout au corpus
    doc = ArxivDocument(titre, auteur, date_pub, url, texte, coauthors)
    corpus.add_document(doc)

# ================================
# AFFICHAGE DU CORPUS
# ================================
print("\n=== Aperçu du corpus ===")
print(corpus)  # Affiche un résumé du corpus
corpus.afficher_par_date(20)  # Affiche les 20 documents les plus récents
corpus.afficher_par_titre(20)  # Affiche les 20 premiers titres

# ================================
# SAUVEGARDE ET RECHARGEMENT
# ================================
corpus.save("corpus.csv")  # Sauvegarde du corpus
nouveau_corpus = Corpus("Corpus_Recharge")  # Création d'un nouveau corpus vide
nouveau_corpus.load("corpus.csv")  # Recharge le corpus sauvegardé

print("\n✅ Corpus rechargé :")
print(nouveau_corpus)

# ================================
# RECHERCHE PAR AUTEUR
# ================================
nom_recherche = input("\nEntrez le nom d'un auteur : ")

if nom_recherche in nouveau_corpus.authors:
    auteur_obj = nouveau_corpus.authors[nom_recherche]
    print(f"\nAuteur trouvé : {auteur_obj.name}")
    print(f"Nombre de documents : {auteur_obj.nb_docs}")

    # Calcul de la taille moyenne des documents
    longueurs = [len(doc.texte.split()) for doc in auteur_obj.production.values()]
    moyenne = sum(longueurs) / len(longueurs) if longueurs else 0
    print(f"Taille moyenne des documents : {moyenne:.2f} mots")
else:
    print(f"Auteur '{nom_recherche}' non trouvé dans le corpus.")

# ================================
# RECHERCHE DE MOTS-CLÉS DANS LE CORPUS
# ================================
mot_test = input("\n🔍 Entrez un mot-clé à rechercher dans le corpus : ")

print("\n--- Test de la méthode search() ---")
resultats_search = nouveau_corpus.search(mot_test, contexte=60)  # Recherche avec contexte de 60 caractères
print(f"\nNombre de passages trouvés : {len(resultats_search)}")

print("\n--- Test de la méthode concorde() ---")
df_concorde = nouveau_corpus.concorde(mot_test, contexte=60)  # Concordancier
print(f"\nNombre de concordances trouvées : {len(df_concorde)}")

if not df_concorde.empty:
    df_concorde.to_csv("concordancier.csv", sep='\t', index=False)  # Sauvegarde du concordancier
    print("\n✅ Concordancier sauvegardé dans 'concordancier.csv'")

# ================================
# STATISTIQUES DU CORPUS
# ================================
print("\n=== Statistiques sur le corpus ===")
freq = nouveau_corpus.stats(20)  # Top 20 mots les plus fréquents
freq.to_csv("stats_vocab.csv", sep='\t', index=False)
print("\n✅ Statistiques sauvegardées dans 'stats_vocab.csv'")

# ================================
# MOTEUR DE RECHERCHE TF + TF-IDF
# ================================
print("\n=== Construction du moteur de recherche (TF + TF-IDF) ===")
engine = SearchEngine(nouveau_corpus)
print("✅ Moteur de recherche créé.")

query = input("\n🔎 Entrez des mots-clés pour le moteur TF-IDF : ")
df_results = engine.search(query, k=10)  # Recherche top 10
print("\n=== Résultats du moteur de recherche ===")
print(df_results)

