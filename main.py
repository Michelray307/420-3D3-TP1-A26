from modeles.portefeuille import Portefeuille

from observateurs.afficheur_prix import AfficheurPrix
from observateurs.afficheur_portfolio import AfficheurPortfolio
from observateurs.gestionnaire_alerte import GestionnaireAlerte
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

    # 1. Création du portefeuille
    portefeuille = Portefeuille(TITRES)

    # 2. Création du dashboard
    dashboard = Dashboard(portefeuille)

    # 3. Création des observateurs
    afficheur_prix = AfficheurPrix(dashboard)
    afficheur_portfolio = AfficheurPortfolio(dashboard)
    gestionnaire_alerte = GestionnaireAlerte(dashboard)
    journal_csv = JournalCsv()

    # 4. Abonnement des observateurs
    portefeuille.abonner(afficheur_prix)
    portefeuille.abonner(afficheur_portfolio)
    portefeuille.abonner(gestionnaire_alerte)
    portefeuille.abonner(journal_csv)

    # 5. Démarrage de l'application
    dashboard.demarrer()


if __name__ == "__main__":
    main()