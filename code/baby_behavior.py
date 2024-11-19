from microbit import *
import radio
import music

# Active le module radio
radio.on()
radio.config(channel=7)

#first comit branchTest

# Classe représentant le portefeuille numérique de l'enfant
class DigitalWallet:
    def __init__(self, titulaire, numero_compte):
        self.titulaire = titulaire
        self.numero_compte = numero_compte
        self.solde = 0.0

    def receive(self, valeur):
        self.solde += valeur


# Initialisation du portefeuille
baby_wallet = DigitalWallet('Micro Enfant', 'BE00 0001')


def rassurer_parent():
    radio.send("calm")


# Fonction pour afficher une image d'enfant
def show_image():
    baby_image = Image("99990:"
                       "90000:"
                       "99900:"
                       "90000:"
                       "99990:")
    display.show(baby_image)


# Fonction pour vérifier le niveau d'agitation
def check_agitation():
    agitation = accelerometer.get_strength()
    if agitation < 1000:
        return "agitation faible"
    elif agitation < 3000:
        return "agitation moyenne"
    else:
        return "agitation elevee"


# Fonction pour envoyer un message sur l'agitation
def send_agitation():
    message = check_agitation()
    radio.send(message)


# Fonction pour afficher la quantité de lait consommée
def show_milk(milk_consumed):
    display.scroll(str((milk_consumed) + " ml"))


# Gestion de la consommation de lait
def drink_milk(milk_consumed, dose):
    milk_consumed += dose
    # display.scroll(str(milk_consumed) + "ml")
    return milk_consumed


# Variables globales
sleeping = True
calm = True
milk_consumed = 0

communication = True
# Boucle principale
while communication:
    # Affiche une image de l'enfant
    show_image()

    # Si le bouton A est pressé, affiche la quantité de lait consommée
    if button_a.was_pressed():
        show_milk(str(milk_consumed))

    # Vérifie les mouvements avec l'accéléromètre
    movement = accelerometer.current_gesture()

    # Vérifie si l'enfant est en chute libre
    if movement == "freefall":
        radio.send("freefall")
        sleeping = False
        calm = False
        display.show(Image.SAD)
        while not calm:
            radio.send("ping")
            message = radio.receive()
            if message:
                if message == "calm":
                    display.show(Image.HAPPY)
                    music.play(music.POWER_UP)
                    calm = True
                else:
                    sleep(1000)
            else:
                sleep(500)
        sleep(3500)
    # Vérifie le niveau d'agitation
    etat_enfant = check_agitation()
    if etat_enfant == "agitation elevee":
        # Envoie le message "awake" si l'appareil dormait et qu'il y a eu un mouvement
        send_agitation()
        sleep(1000)  # Max 1 message/ seconde
        sleeping = False
        calm = False
        while not calm:
            display.show(Image.CONFUSED)
            sleep(1000)
            music.play(music.ODE)
            sleep(1000)
            rassurer_parent()
            display.show(Image.HAPPY)
            sleep(1000)
            calm = True

    # Réception des messages via radio
    message = radio.receive()
    if message:
        message = message.strip()

        # Gérer la demande de lait consommé
        if message == "get_milk":
            radio.send(str(milk_consumed))
            display.scroll('{} ml'.format(milk_consumed))


        # Gérer la demande de température
        elif message == "get_temperature":
            temp = temperature()
            radio.send(str(temp) + " C")
            if temp < 35 or temp > 37:
                happy = False
                while not happy:
                    display.show(Image.SAD)
                    response = radio.receive()
                    if response == "medicament":
                        display.show(Image.HAPPY)
                        music.play(music.POWER_UP)
                        radio.send("merci")
                        happy = True
                    sleep(100)

        # Gérer la consommation de lait
        elif message.isdigit():
            dose = int(message)
            milk_consumed = drink_milk(milk_consumed, dose)
            display.show(Image.HAPPY)
            music.play(music.POWER_UP)
            radio.send(str(milk_consumed))
            display.scroll('{} ml'.format(milk_consumed))

        elif message == 'btc':
            radio.send('send')
            answer = False
            while not answer:
                message = radio.receive()
                if message:
                    baby_wallet.receive(float(message))
                    display.scroll('{} BTC'.format(baby_wallet.solde))
                    answer = True
                else:
                    sleep(1000)

        else:
            sleep(500)