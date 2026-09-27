from .observateur import Observateur


class AfficheurPortfolio(Observateur):
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()

        titres = donnees["titres"]
        prix_actuels = donnees["prix_actuels"]

        valeur_totale = sum(
            prix * titres[ticker]["quantite"]
            for ticker, (prix, ouverture) in prix_actuels.items()
        )

        valeur_ouverture = sum(
            ouverture * titres[ticker]["quantite"]
            for ticker, (prix, ouverture) in prix_actuels.items()
        )

        variation = valeur_totale - valeur_ouverture

        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        self.dashboard.label_valeur.config(
            text=f"Valeur totale : {valeur_totale:.2f} $"
        )

        self.dashboard.label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg=couleur
        )