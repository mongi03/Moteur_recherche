class Author:
    """
    La classe Author représente un auteur scientifique.
    Elle permet de stocker son nom, le nombre de documents qu'il a produits
    et la liste de ses productions (documents associés à leurs titres).
    """

    def __init__(self, name: str):
        """
        Constructeur de la classe Author.

        :param name: Nom de l'auteur
        """

        # Nom de l'auteur
        self.name = name

        # Nombre total de documents produits par l'auteur
        self.nb_docs = 0

        # Dictionnaire contenant les documents de l'auteur
        # La clé est le titre du document et la valeur est l'objet document correspondant
        self.production = {}

    def add(self, title, document):
        """
        Ajoute un document à la production de l'auteur.

        :param title: Titre du document
        :param document: Objet document associé au titre
        """

        # Vérifie si le document n'est pas déjà enregistré
        if title not in self.production:
            self.production[title] = document
            self.nb_docs += 1
        else:
            # Message d'avertissement en cas de doublon
            print(f"⚠️ Le document '{title}' est déjà enregistré pour {self.name}.")

    def __str__(self):
        """
        Retourne une représentation textuelle lisible de l'auteur.
        Affiche son nom, le nombre de documents et la liste de ses productions.
        """

        # Liste des titres des documents, ou message par défaut si vide
        doc_list = ", ".join(self.production.keys()) if self.production else "Aucun document"

        return (
            f"Auteur : {self.name}\n"
            f"Nombre de documents : {self.nb_docs}\n"
            f"Production : {doc_list}"
        )
