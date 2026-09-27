from datetime import datetime
from .observateur import Observateur


class JournalCSV(Observateur):
    def __init__(self, chemin):
        self.chemin = chemin

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]

        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.chemin, "a") as fichier:
            for ticker, (prix, ouverture) in prix_actuels.items():
                fichier.write(
                    f"{horodatage},{ticker},{prix:.2f},{ouverture:.2f}\n"
                )