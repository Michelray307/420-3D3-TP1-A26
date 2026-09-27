from .observateur import Observateur

class GestionnaireAlertes(Observateur):
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()

        titres = donnees["titres"]
        prix_actuels = donnees["prix_actuels"]

        alertes = []

        for ticker, (prix, _) in prix_actuels.items():
            if prix >= titres[ticker]["seuil_haut"]:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {titres[ticker]['seuil_haut']:.2f} $)"
                )

            elif prix <= titres[ticker]["seuil_bas"]:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {titres[ticker]['seuil_bas']:.2f} $)"
                )

        self.dashboard.label_alertes.config(
            text="\n".join(alertes) if alertes else "Aucune alerte",
            fg="red" if alertes else "gray"
        )