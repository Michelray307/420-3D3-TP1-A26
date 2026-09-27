from modeles.portefeuille import Portefeuille

from observateurs.afficheur_prix import AfficheurPrix
from observateurs.afficheur_portfolio import AfficheurPortfolio
from observateurs.gestionnaire_alertes import GestionnaireAlerte
from observateurs.journal_csv import JournalCsv

from views.dashboard import Dashboard


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


def main():

    # Création du sujet
    portefeuille = Portefeuille(TITRES)

    # Création de l'interface
    dashboard = Dashboard(portefeuille)

    # Création des observateurs
    afficheur_prix = AfficheurPrix(dashboard)
    afficheur_portfolio = AfficheurPortfolio(dashboard)
    gestionnaire_alerte = GestionnaireAlerte(dashboard)
    journal_csv = JournalCsv()

    # Abonnement des observateurs
    portefeuille.abonner(afficheur_prix)
    portefeuille.abonner(afficheur_portfolio)
    portefeuille.abonner(gestionnaire_alerte)
    portefeuille.abonner(journal_csv)

    # Lancer l'application
    dashboard.demarrer()


if __name__ == "__main__":
    main()