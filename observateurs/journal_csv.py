from datetime import datetime
from .observateur import Observateur


class JournalCsv(Observateur):

    def __init__(self, fichier="portfolio.csv"):
        self.fichier = fichier

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]

        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.fichier, "a") as f:
            for ticker, (prix, ouverture) in prix_actuels.items():
                f.write(
                    f"{horodatage},{ticker},{prix:.2f},{ouverture:.2f}\n"
                )