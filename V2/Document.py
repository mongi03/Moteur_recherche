class Document:
    """
    La classe Document représente un document générique.
    Elle sert de classe de base pour des documents plus spécifiques
    (RedditDocument, ArxivDocument, etc.).
    """

    def __init__(self, titre, auteur, date, url, texte):
        """
        Constructeur de la classe Document.

        :param titre: Titre du document
        :param auteur: Auteur du document
        :param date: Date de publication
        :param url: Lien vers le document
        :param texte: Contenu textuel du document
        """

        # Informations principales du document
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def afficher_informations(self):
        """
        Affiche de manière lisible les informations du document.
        Le texte est tronqué pour éviter un affichage trop long.
        """

        print("===== Informations du document =====")
        print(f"Titre  : {self.titre}")
        print(f"Auteur : {self.auteur}")
        print(f"Date   : {self.date}")
        print(f"URL    : {self.url}")

        # Affiche uniquement les 200 premiers caractères du texte
        extrait = self.texte[:200]
        if len(self.texte) > 200:
            extrait += "..."
        print(f"Texte  : {extrait}")

        print("===================================")

    def __str__(self):
        """
        Représentation textuelle simple du document.
        Utile pour l'affichage ou le débogage.
        """
        return f"Document : {self.titre}"

    def getType(self):
        """
        Retourne le type du document.
        Cette méthode est redéfinie dans les classes filles.
        """
        return "Document"
