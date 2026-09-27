from app import App

from modeles.portefeuille import Portefeuille

from observateurs.afficheur_prix import AfficheurPrix
from observateurs.afficheur_portfolio import AfficheurPortfolio
from observateurs.gestionnaire_alertes import GestionnaireAlertes
from observateurs.journal_csv import JournalCSV


TITRES = {
    "AAPL": {
        "quantite": 10,
        "seuil_haut": 200.0,
        "seuil_bas": 150.0
    },
    "GOOGL": {
        "quantite": 5,
        "seuil_haut": 160.0,
        "seuil_bas": 120.0
    },
    "MSFT": {
        "quantite": 8,
        "seuil_haut": 430.0,
        "seuil_bas": 380.0
    }
}


if __name__ == "__main__":
    # Création du portefeuille
    portefeuille = Portefeuille(TITRES)

    # Création du dashboard
    app = App(portefeuille)

    # Création des observateurs
    afficheur_prix = AfficheurPrix(app)
    afficheur_portfolio = AfficheurPortfolio(app)
    gestionnaire_alertes = GestionnaireAlertes(app)
    journal_csv = JournalCSV("portfolio.csv")

    # Abonnement au portefeuille
    portefeuille.abonner(afficheur_prix)
    portefeuille.abonner(afficheur_portfolio)
    portefeuille.abonner(gestionnaire_alertes)
    portefeuille.abonner(journal_csv)

    # Démarrage de l'application
    dashboard.demarrer()

    #TODO:
    #import de dashboard dans main

    #__init__ de dashboard initialise toutes les fenetres

    #dans dashboard -> methodes pour construites tout les frames et label pour: prix, portfolio, alertes et gestion/portefeuille

    #methode demarrer() dans dashboard qui sert a lancer:
    #def demarrer(self):
    #    self.rafraichir()
    #    self.fenetre.mainloop()

    #methode rafraichir() de dashboard qui lance la methode rafraichir() de portefeuille (avec un try,exept ??) ET rappelle sa methode
    #self.rafraichir apres 30 secondes
