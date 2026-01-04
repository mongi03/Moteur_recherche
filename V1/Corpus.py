# Corpus.py
import pandas as pd
from datetime import datetime, timezone
import re


class Corpus:
    """
    La classe Corpus représente un ensemble de documents.
    Elle permet de :
    - stocker des documents et des auteurs
    - trier et afficher les documents
    - sauvegarder / charger le corpus
    - effectuer des recherches textuelles (search, concordance)
    - calculer des statistiques lexicales
    """

    def __init__(self, nom):
        """
        Constructeur du corpus.

        :param nom: Nom du corpus
        """
        self.nom = nom

        # Dictionnaire des documents : {id_doc: Document}
        self.documents = {}

        # Identifiant auto-incrémenté pour les documents
        self.id_doc = 1

        # Dictionnaire des auteurs : {nom_auteur: Author}
        self.authors = {}

        # Cache pour accélérer les recherches textuelles
        self._full_text = None      # texte concaténé de tous les documents
        self._text_mapping = []     # mapping positions → documents

    def add_document(self, doc):
        """
        Ajoute un document au corpus et met à jour les auteurs.
        """

        # Ajout du document avec un identifiant unique
        self.documents[self.id_doc] = doc

        # Création de l'auteur s'il n'existe pas encore
        if doc.auteur not in self.authors:
            from Author import Author
            self.authors[doc.auteur] = Author(doc.auteur)

        # Ajout du document à la production de l'auteur
        self.authors[doc.auteur].add(doc.titre, doc)

        # Incrément de l'identifiant
        self.id_doc += 1

        # Invalidation du cache de recherche
        self._full_text = None

    def afficher_par_date(self, n=5):
        """
        Affiche les n documents les plus récents du corpus.
        """

        # Fonction interne pour parser les dates
        def parse_date(doc):
            dt = doc.date

            # Conversion depuis une chaîne de caractères si nécessaire
            if isinstance(dt, str):
                try:
                    dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                except ValueError:
                    dt = datetime.strptime(dt[:10], '%Y-%m-%d')

            # Normalisation en UTC sans timezone
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)

            return dt

        # Tri des documents par date décroissante
        docs_tries = sorted(self.documents.values(), key=parse_date, reverse=True)

        print(f"\n--- {n} documents les plus récents ---")
        for doc in docs_tries[:n]:
            print(f"{doc.titre} ({doc.date}) - Source : {doc.getType()}")

    def afficher_par_titre(self, n=5):
        """
        Affiche les n premiers documents triés par ordre alphabétique du titre.
        """
        docs_tries = sorted(self.documents.values(), key=lambda d: d.titre)

        print(f"\n--- {n} documents triés par titre ---")
        for doc in docs_tries[:n]:
            print(f"{doc.titre} ({doc.date}) - Source : {doc.getType()}")

    def __repr__(self):
        """
        Représentation courte du corpus.
        """
        return f"Corpus '{self.nom}' avec {len(self.documents)} documents et {len(self.authors)} auteurs"

    def save(self, filename):
        """
        Sauvegarde le corpus dans un fichier CSV (séparateur tabulation).
        """

        df = pd.DataFrame([
            {
                'id_doc': i,
                'titre': doc.titre,
                'auteur': doc.auteur,
                'date': doc.date,
                'url': doc.url,
                'texte': doc.texte,
                'type_doc': doc.getType()
            }
            for i, doc in self.documents.items()
        ])

        df.to_csv(filename, sep='\t', index=False)
        print(f"\n✅ Corpus sauvegardé dans '{filename}'")

    def load(self, filename):
        """
        Recharge un corpus depuis un fichier CSV.
        """

        df = pd.read_csv(filename, sep='\t')

        from Document import Document
        from RedditDocument import RedditDocument
        from ArxivDocument import ArxivDocument

        # Réinitialisation du corpus
        self.documents = {}
        self.authors = {}
        self.id_doc = 1
        self._full_text = None

        # Reconstruction des documents selon leur type
        for _, row in df.iterrows():
            if row['type_doc'] == "Reddit":
                doc = RedditDocument(
                    row['titre'], row['auteur'], row['date'],
                    row['url'], row['texte'], nb_comments=0
                )
            elif row['type_doc'] == "Arxiv":
                doc = ArxivDocument(
                    row['titre'], row['auteur'], row['date'],
                    row['url'], row['texte'], coauthors=[]
                )
            else:
                doc = Document(
                    row['titre'], row['auteur'], row['date'],
                    row['url'], row['texte']
                )

            self.add_document(doc)

    def search(self, mot_clef, contexte=40):
        """
        Recherche un mot-clé exact dans le corpus avec affichage du contexte.
        """

        # Construction du cache si nécessaire
        if self._full_text is None:
            self._text_mapping = []
            self._full_text = ""

            for doc in self.documents.values():
                start = len(self._full_text)
                self._full_text += doc.texte + "\n"
                end = len(self._full_text)
                self._text_mapping.append((start, end, doc))

        # Expression régulière pour recherche du mot entier
        pattern = re.compile(rf"\b{re.escape(mot_clef)}\b", re.IGNORECASE)

        results = []

        for match in pattern.finditer(self._full_text):
            start, end = match.span()
            extrait = self._full_text[
                max(0, start - contexte):min(len(self._full_text), end + contexte)
            ]

            # Identification du document correspondant
            for s, e, doc in self._text_mapping:
                if s <= start < e:
                    results.append((doc.titre, extrait.strip()))
                    break

        # Affichage des résultats
        if results:
            print(f"\n--- Résultats pour '{mot_clef}' ---")
            for titre, extrait in results:
                print(f"\n📄 {titre} :\n...{extrait}...")
        else:
            print(f"\nAucun résultat pour '{mot_clef}'.")

        return results

    def concorde(self, motif, contexte=40):
        """
        Génère un concordancier (KWIC) à partir d'une expression régulière.
        """

        # Construction du cache si nécessaire
        if self._full_text is None:
            self._text_mapping = []
            self._full_text = ""

            for doc in self.documents.values():
                start = len(self._full_text)
                self._full_text += doc.texte + "\n"
                end = len(self._full_text)
                self._text_mapping.append((start, end, doc))

        pattern = re.compile(motif, re.IGNORECASE)
        lignes = []

        for match in pattern.finditer(self._full_text):
            start, end = match.span()

            gauche = self._full_text[max(0, start - contexte):start]
            centre = match.group()
            droite = self._full_text[end:end + contexte]

            doc_titre = None
            for s, e, doc in self._text_mapping:
                if s <= start < e:
                    doc_titre = doc.titre
                    break

            lignes.append({
                "document": doc_titre,
                "contexte gauche": "..." + gauche.strip(),
                "motif trouvé": centre,
                "contexte droit": droite.strip() + "..."
            })

        df = pd.DataFrame(lignes)

        if df.empty:
            print(f"\nAucun résultat pour '{motif}'.")
        else:
            print(f"\n--- Concordancier pour '{motif}' ---")
            print(df.head(10))

        return df