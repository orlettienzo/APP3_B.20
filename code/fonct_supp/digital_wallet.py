class DigitalWallet:
    def __init__(self, titulaire, numero_compte):
        self.titulaire = titulaire
        self.numero_compte = numero_compte
        self.solde = 0.0

    def receive(self, valeur):
        self.solde += valeur

