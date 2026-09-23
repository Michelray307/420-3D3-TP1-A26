from .observateur  import Observateur

class AfficheurPrix(Observateur):
    def __init__(self,label):
        self.label = label

    def actualiser(self, sujet) -> None:
        donnes = sujet.get_donnes()
        prix_actuels = donnes.get("prix_actuels")

        for ticker, (prix,ouverture) in prix_actuels.items():
            variation = (prix - ouverture) / ouverture * 100

            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"

            texte = f"{prix:.2f} $  {symbole} {abs(variation):.2f}%"

            self.dashboard.labels_prix[ticker].config(text=texte,fg=couleur)

            