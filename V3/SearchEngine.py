import numpy as np
import math
from scipy import sparse


class SearchEngine:
    """
    La classe SearchEngine implémente un moteur de recherche basé sur :
    - TF (Term Frequency)
    - IDF (Inverse Document Frequency)
    - TF-IDF
    - Similarité cosinus entre requête et documents
    """

    def __init__(self, corpus):
        """
        Initialise le moteur de recherche à partir d'un corpus.

        :param corpus: Objet Corpus contenant les documents
        """
        self.corpus = corpus

        # Liste des documents du corpus
        self.documents = list(corpus.documents.values())

        # Construction du vocabulaire
        self.vocab = self._build_vocab()

        # Matrice TF (documents x mots)
        self.mat_TF = self._build_TF_matrix()

        # Mise à jour des statistiques du vocabulaire (TF total et DF)
        self._update_vocab_stats()

        # Matrice TF-IDF
        self.mat_TFIDF = self._build_TFIDF_matrix(self.mat_TF)

    def _build_vocab(self):
        """
        Construit le vocabulaire du corpus.
        Chaque mot est associé à :
        - un identifiant unique
        - sa fréquence totale
        - sa fréquence documentaire (DF)
        """

        vocab = {}
        next_id = 0

        for doc in self.documents:
            for m in doc.texte.lower().split():
                if m not in vocab:
                    vocab[m] = {
                        "id": next_id,
                        "total_freq": 0,
                        "df": 0
                    }
                    next_id += 1

        return vocab

    def _build_TF_matrix(self):
        """
        Construit la matrice TF sous forme sparse (CSR).
        Chaque case (i, j) représente le nombre d'occurrences
        du mot j dans le document i.
        """

        rows, cols, data = [], [], []

        for i, doc in enumerate(self.documents):
            for m in doc.texte.lower().split():
                if m in self.vocab:
                    j = self.vocab[m]["id"]
                    rows.append(i)
                    cols.append(j)
                    data.append(1)

        N = len(self.documents)
        V = len(self.vocab)

        return sparse.csr_matrix((data, (rows, cols)), shape=(N, V))

    def _update_vocab_stats(self):
        """
        Met à jour :
        - DF (document frequency)
        - fréquence totale de chaque mot
        """

        TF = self.mat_TF

        for mot, info in self.vocab.items():
            j = info["id"]
            col = TF[:, j]

            info["df"] = int(col.count_nonzero())
            info["total_freq"] = int(col.sum())

    def _build_TFIDF_matrix(self, TF):
        """
        Construit la matrice TF-IDF à partir de TF.
        TF-IDF = TF × IDF
        """

        N, V = TF.shape
        idf = np.zeros(V)

        for mot, info in self.vocab.items():
            j = info["id"]
            df = info["df"]
            idf[j] = math.log(N / df) if df > 0 else 0

        return TF.multiply(idf).tocsr()

    def _build_query_vector(self, query):
        """
        Transforme une requête utilisateur en vecteur TF-IDF.
        """

        N = len(self.documents)
        V = len(self.vocab)
        vec = np.zeros(V)

        for m in query.lower().split():
            if m in self.vocab:
                j = self.vocab[m]["id"]
                df = self.vocab[m]["df"]
                idf = math.log(N / df) if df > 0 else 0
                vec[j] += idf

        return vec

    def search(self, query, k=5):
        """
        Recherche les k documents les plus pertinents pour une requête.
        La pertinence est calculée avec la similarité cosinus.
        """

        q_vec = self._build_query_vector(query)
        scores = []

        for i in range(self.mat_TFIDF.shape[0]):
            doc_vec = self.mat_TFIDF[i].toarray().flatten()

            # Similarité cosinus
            num = np.dot(q_vec, doc_vec)
            den = math.sqrt(np.dot(q_vec, q_vec)) * math.sqrt(np.dot(doc_vec, doc_vec))
            score = num / den if den != 0 else 0

            scores.append(score)

        # Sélection des meilleurs documents
        best = np.argsort(scores)[::-1][:k]

        results = []
        for i in best:
            d = self.documents[i]
            results.append({
                "score": scores[i],
                "titre": d.titre,
                "auteur": d.auteur,
                "date": d.date,
                "url": d.url,
            })

        return results
