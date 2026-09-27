from .sujet import Sujet
import yfinance as yf

class Portefeuille(Sujet):
    def __init__(self, titres: dict):
        super().__init__()
        self.titres = titres
        self.prix_actuels = {}
<<<<<<< HEAD
    
=======

>>>>>>> c25dbb6facf7024f57c66b18b51f43eafb9bdd5e
    def recuperer_prix(self, ticker):
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]

        if prix is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas.")

        return prix, info["open"]

    def rafraichir(self):
        self.prix_actuels = {
            ticker: self.recuperer_prix(ticker)
            for ticker in self.titres
        }

        self.notifier()

    def ajouter_titre(self, ticker, quantite, seuil_bas, seuil_haut):
        self.titres[ticker] = {
            "quantite": quantite,
            "seuil_bas": seuil_bas,
            "seuil_haut": seuil_haut
        }

    def retirer_titre(self, ticker):
        del self.titres[ticker]

    def modifier_titre(self, ticker, **changements):
        self.titres[ticker].update(changements)

    def get_donnees(self):
        return {
            "titres": self.titres,
            "prix_actuels": self.prix_actuels
        }