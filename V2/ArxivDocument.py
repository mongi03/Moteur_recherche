from Document import Document

# La classe ArxivDocument hérite de la classe Document.
# Elle représente un document scientifique provenant d'ArXiv,
# avec la gestion spécifique des co-auteurs.
class ArxivDocument(Document):

    def __init__(self, titre, auteur, date, url, texte, coauthors=None):
        """
        Constructeur de la classe ArxivDocument.

        :param titre: Titre du document
        :param auteur: Auteur principal
        :param date: Date de publication
        :param url: Lien vers le document
        :param texte: Contenu textuel du document
        :param coauthors: Liste des co-auteurs (optionnelle)
        """

        # Appel du constructeur de la classe parente Document
        super().__init__(titre, auteur, date, url, texte)

        # Initialisation des co-auteurs
        # Si aucun co-auteur n'est fourni, on initialise une liste vide
        self.coauthors = coauthors if coauthors is not None else []

    def get_coauthors(self):
        """
        Retourne la liste des co-auteurs du document.
        """
        return self.coauthors

    def set_coauthors(self, coauthors):
        """
        Modifie la liste des co-auteurs.

        :param coauthors: Nouvelle liste de co-auteurs
        """
        self.coauthors = coauthors

    def add_coauthor(self, coauthor):
        """
        Ajoute un co-auteur à la liste s'il n'est pas déjà présent.
        Cela évite les doublons.
        
        :param coauthor: Nom du co-auteur à ajouter
        """
        if coauthor not in self.coauthors:
            self.coauthors.append(coauthor)

    def getType(self):
        """
        Retourne le type du document.
        Méthode utile pour identifier dynamiquement le type d'objet.
        """
        return "Arxiv"

    def __str__(self):
        """
        Redéfinition de la méthode __str__ pour fournir
        une représentation textuelle lisible de l'objet.
        """

        # Création d'une chaîne de caractères pour les co-auteurs
        coauthors_str = ", ".join(self.coauthors) if self.coauthors else "Aucun co-auteur"

        # Retourne une description complète du document
        return (
            f"{self.type_doc}: '{self.titre}' par {self.auteur} "
            f"({self.date}) - Co-auteurs: {coauthors_str}"
        )
