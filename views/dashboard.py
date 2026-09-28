import tkinter as tk
from datetime import datetime


INTERVALLE_MS = 30000

POLICE = ("Segoe UI", 10)
POLICE_TITRE = ("Segoe UI", 16, "bold")
POLICE_VALEUR = ("Segoe UI", 13, "bold")


class Dashboard:

    def __init__(self, portefeuille):
        self.portefeuille = portefeuille

        self.fenetre = tk.Tk()
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.resizable(False, False)
        self.fenetre.option_add("*Font", POLICE)

        self.labels_prix = {}
        self.frames_prix = {}

        self._construire_interface()


    # --------------------------------------------------------- INTERFACE

    def _construire_interface(self):

        tk.Label(
            self.fenetre,
            text="Portfolio Tracker",
            font=POLICE_TITRE
        ).pack(pady=10)

        # ---------------- Prix en temps réel ----------------

        self.frame_prix = tk.LabelFrame(self.fenetre, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        donnees = self.portefeuille.get_donnees()

        for ticker in donnees["titres"]:
            self._creer_ligne_prix(ticker)

        # ---------------- Gestion des titres ----------------

        self._construire_gestion()

        # ---------------- Portfolio ----------------

        frame_portfolio = tk.LabelFrame(self.fenetre, text="Mon portfolio", padx=10, pady=10)
        frame_portfolio.pack(fill=tk.X, padx=10, pady=5)

        self.label_valeur = tk.Label(
            frame_portfolio,
            text="Valeur totale : calcul en cours...",
            font=POLICE_VALEUR
        )
        self.label_valeur.pack()

        self.label_variation = tk.Label(
            frame_portfolio,
            text=""
        )
        self.label_variation.pack()

        # ---------------- Alertes ----------------

        frame_alertes = tk.LabelFrame(self.fenetre, text="Alertes", padx=10, pady=10)
        frame_alertes.pack(fill=tk.X, padx=10, pady=5)

        self.label_alertes = tk.Label(
            frame_alertes,
            text="Aucune alerte",
            fg="gray",
            justify=tk.LEFT,
            wraplength=380
        )
        self.label_alertes.pack(anchor="w")

        # ---------------- Dernière mise à jour ----------------

        self.label_maj = tk.Label(
            self.fenetre,
            text="",
            fg="gray"
        )
        self.label_maj.pack(pady=5)


    # --------------------------------------------------------- PRIX

    def _creer_ligne_prix(self, ticker):

        frame = tk.Frame(self.frame_prix)
        frame.pack(fill=tk.X, pady=2)

        tk.Label(
            frame,
            text=f"{ticker}:",
            width=8,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(side=tk.LEFT)

        label = tk.Label(
            frame,
            text="Chargement..."
        )
        label.pack(side=tk.LEFT)

        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame


    # --------------------------------------------------------- GESTION

    def _construire_gestion(self):

        frame = tk.LabelFrame(self.fenetre, text="Gérer les titres", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)

        # ---------------- Ajouter ----------------

        ligne_ajout = tk.Frame(frame)
        ligne_ajout.pack(fill=tk.X)

        self.entry_ticker = self._champ(
            ligne_ajout,
            "Ticker",
            8
        )

        self.entry_quantite = self._champ(
            ligne_ajout,
            "Qté",
            5,
            "1"
        )

        self.entry_seuil_bas_ajout = self._champ(
            ligne_ajout,
            "Alerte basse",
            7
        )

        self.entry_seuil_haut_ajout = self._champ(
            ligne_ajout,
            "Alerte haute",
            7
        )

        tk.Button(
            ligne_ajout,
            text="Ajouter",
            command=self.ajouter_titre
        ).pack(side=tk.LEFT)

        # ---------------- Liste ----------------

        ligne_liste = tk.Frame(frame)
        ligne_liste.pack(fill=tk.X, pady=5)

        self.listbox_titres = tk.Listbox(
            ligne_liste,
            height=4,
            exportselection=False
        )
        self.listbox_titres.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        titres = self.portefeuille.get_donnees()["titres"]

        for ticker in titres:
            self.listbox_titres.insert(
                tk.END,
                self._texte_listbox(ticker)
            )

        tk.Button(
            ligne_liste,
            text="Retirer",
            command=self.retirer_titre
        ).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        # ---------------- Modifier ----------------

        ligne_modif = tk.Frame(frame)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))

        tk.Label(
            ligne_modif,
            text="Sélection →"
        ).pack(side=tk.LEFT)

        self.entry_nouvelle_quantite = self._champ(
            ligne_modif,
            "Qté",
            5
        )

        self.entry_nouveau_seuil_bas = self._champ(
            ligne_modif,
            "Alerte basse",
            7
        )

        self.entry_nouveau_seuil_haut = self._champ(
            ligne_modif,
            "Alerte haute",
            7
        )

        tk.Button(
            ligne_modif,
            text="Modifier sélection",
            command=self.modifier_selection
        ).pack(side=tk.LEFT)

        # ---------------- Statut ----------------

        self.label_statut_titres = tk.Label(
            frame,
            text="",
            fg="gray"
        )
        self.label_statut_titres.pack(anchor="w", pady=(5, 0))


    def _champ(self, parent, texte, width, valeur_defaut=""):

        tk.Label(
            parent,
            text=f"{texte}:"
        ).pack(side=tk.LEFT)

        entry = tk.Entry(
            parent,
            width=width
        )

        if valeur_defaut:
            entry.insert(0, valeur_defaut)

        entry.pack(side=tk.LEFT, padx=(2, 8))

        return entry


    # --------------------------------------------------------- LISTBOX

    def _texte_listbox(self, ticker):

        titres = self.portefeuille.get_donnees()["titres"]
        infos = titres[ticker]

        return (
            f"{ticker} — {infos['quantite']} action(s) "
            f"(alerte : {infos['seuil_bas']:.2f} $ / "
            f"{infos['seuil_haut']:.2f} $)"
        )


    def _ticker_selectionne(self):

        selection = self.listbox_titres.curselection()

        if not selection:
            return None

        index = selection[0]

        texte = self.listbox_titres.get(index)

        ticker = texte.split(" — ")[0]

        return index, ticker


    def _statut(self, texte, couleur):

        self.label_statut_titres.config(
            text=texte,
            fg=couleur
        )


    # --------------------------------------------------------- AJOUTER

    def ajouter_titre(self):

        ticker = self.entry_ticker.get().strip().upper()

        if not ticker:
            self._statut(
                "Entrez un ticker.",
                "orange"
            )
            return

        titres = self.portefeuille.get_donnees()["titres"]

        if ticker in titres:
            self._statut(
                f"{ticker} est déjà dans le portfolio.",
                "orange"
            )
            return

        try:
            quantite = int(
                self.entry_quantite.get().strip()
            )

            seuil_bas = float(
                self.entry_seuil_bas_ajout.get().strip()
            )

            seuil_haut = float(
                self.entry_seuil_haut_ajout.get().strip()
            )

            if quantite <= 0:
                raise ValueError

            if seuil_bas <= 0 or seuil_haut <= 0:
                raise ValueError

            if seuil_bas >= seuil_haut:
                self._statut(
                    "L'alerte basse doit être inférieure à l'alerte haute.",
                    "red"
                )
                return

        except ValueError:

            self._statut(
                "La quantité et les alertes doivent être des nombres positifs.",
                "red"
            )
            return

        self.portefeuille.ajouter_titre(
            ticker,
            quantite,
            seuil_bas,
            seuil_haut
        )

        self._creer_ligne_prix(ticker)

        self.listbox_titres.insert(
            tk.END,
            self._texte_listbox(ticker)
        )

        self.entry_ticker.delete(0, tk.END)

        self.entry_quantite.delete(0, tk.END)
        self.entry_quantite.insert(0, "1")

        self.entry_seuil_bas_ajout.delete(0, tk.END)
        self.entry_seuil_haut_ajout.delete(0, tk.END)

        self._statut(
            f"{ticker} ajouté au portfolio.",
            "green"
        )

        self.mettre_a_jour()


    # --------------------------------------------------------- RETIRER

    def retirer_titre(self):

        selection = self._ticker_selectionne()

        if selection is None:
            self._statut(
                "Sélectionnez un titre à retirer.",
                "orange"
            )
            return

        index, ticker = selection

        self.portefeuille.retirer_titre(ticker)

        self.listbox_titres.delete(index)

        self.labels_prix.pop(
            ticker,
            None
        )

        frame = self.frames_prix.pop(
            ticker,
            None
        )

        if frame:
            frame.destroy()

        self._statut(
            f"{ticker} retiré du portfolio.",
            "gray"
        )

        self.mettre_a_jour()


    # --------------------------------------------------------- MODIFIER

    def modifier_selection(self):

        selection = self._ticker_selectionne()

        if selection is None:
            self._statut(
                "Sélectionnez un titre à modifier.",
                "orange"
            )
            return

        index, ticker = selection

        texte_quantite = self.entry_nouvelle_quantite.get().strip()
        texte_bas = self.entry_nouveau_seuil_bas.get().strip()
        texte_haut = self.entry_nouveau_seuil_haut.get().strip()

        if not texte_quantite and not texte_bas and not texte_haut:
            self._statut(
                "Entrez une nouvelle valeur.",
                "orange"
            )
            return

        changements = {}

        try:

            if texte_quantite:

                quantite = int(texte_quantite)

                if quantite <= 0:
                    raise ValueError

                changements["quantite"] = quantite

            if texte_bas or texte_haut:

                if not texte_bas or not texte_haut:
                    self._statut(
                        "Les deux alertes doivent être fournies.",
                        "red"
                    )
                    return

                seuil_bas = float(texte_bas)
                seuil_haut = float(texte_haut)

                if seuil_bas <= 0 or seuil_haut <= 0:
                    raise ValueError

                if seuil_bas >= seuil_haut:
                    self._statut(
                        "L'alerte basse doit être inférieure à l'alerte haute.",
                        "red"
                    )
                    return

                changements["seuil_bas"] = seuil_bas
                changements["seuil_haut"] = seuil_haut

        except ValueError:

            self._statut(
                "La quantité et les alertes doivent être des nombres positifs.",
                "red"
            )
            return

        self.portefeuille.modifier_titre(
            ticker,
            **changements
        )

        self.listbox_titres.delete(index)

        self.listbox_titres.insert(
            index,
            self._texte_listbox(ticker)
        )

        self.listbox_titres.selection_set(index)

        self.entry_nouvelle_quantite.delete(0, tk.END)
        self.entry_nouveau_seuil_bas.delete(0, tk.END)
        self.entry_nouveau_seuil_haut.delete(0, tk.END)

        self._statut(
            f"{ticker} mis à jour.",
            "green"
        )

        self.mettre_a_jour()


    # --------------------------------------------------------- RAFRAICHIR

    def mettre_a_jour(self):

        try:
            self.portefeuille.rafraichir()

            horodatage = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.label_maj.config(
                text=f"Dernière mise à jour : {horodatage}",
                fg="gray"
            )

        except Exception as e:

            self.label_maj.config(
                text=f"Erreur : {e}",
                fg="red"
            )


    def rafraichir(self):

        self.mettre_a_jour()

        self.fenetre.after(
            INTERVALLE_MS,
            self.rafraichir
        )


    # --------------------------------------------------------- DEMARRER

    def demarrer(self):

        self.rafraichir()

        self.fenetre.mainloop()