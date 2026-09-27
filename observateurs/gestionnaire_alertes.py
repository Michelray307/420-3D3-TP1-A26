from .observateur  import Observateur

class GestionnaireAlerte(Observateur):
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def actualiser(self, sujet) -> None:
        donnes = sujet.get_donnees()

        titres = donnes["titres"]
        prix_actuels = donnes["prix_actuels"]

        alertes = []

        for ticker, (prix, ouverture) in prix_actuels.items():

            seuil_bas = titres[ticker]["seuil_bas"]
            seuil_haut = titres[ticker]["seuil_haut"]

            if prix >= seuil_haut:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )

            elif prix <= seuil_bas:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )
        if alertes:
            self.dashboard.label_alertes.config(text="\n".join(alertes), fg="red")
        else:
            self.dashboard.label_alertes.config(text="Aucune alerte", fg="gray")
