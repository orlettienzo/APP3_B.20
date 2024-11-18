from microbit import *
import radio
import random
import music

# Active le module radio
radio.on()
radio.config(channel=7)


class DigitalWallet:
    def __init__(self, titulaire, numero_compte):
        self.titulaire = titulaire
        self.numero_compte = numero_compte
        self.solde = 0.0

    def receive(self, valeur):
        self.solde += valeur


# Cette fonction sera utiliser plus tard
# def calculer_appreciation(valeur_ancienne, valeur_nouvelle):
# if valeur_ancienne == 0:
# raise ValueError("La valeur ancienne ne peut pas être zéro pour calculer l'appréciation en pourcentage.")

# appreciation = ((valeur_nouvelle - valeur_ancienne) / valeur_ancienne) * 100
# return appreciation

baby_wallet = DigitalWallet('Micro Enfant', 'BE00 0001')

getting_btc = False
while not getting_btc:
    message = radio.receive()
    if message:
        amount = float(message)

        baby_wallet.receive(amount)

        display.scroll('{} BTC'.format(baby_wallet.solde))

        getting_btc = True

    else:
        sleep(1000)


def show_image():
    # 1. Définition de l'image initiale pour le bébé enfant
    baby_image = Image("99990:"
                       "90000:"
                       "99900:"
                       "90000:"
                       "99990:")

    display.show(baby_image)  # image initiale = lettre "E"


def check_agitation():
    # Capture les valeurs de l'accéléromètre sur les axes X, Y et Z
    agitation = accelerometer.get_strength()
    limite = 3000

    # Définir les niveaux d'agitation (ajuster si nécessaire)
    if agitation < 1000:
        return "agitation faible"
    elif agitation < 2999:
        return "agitation moyenne"
    elif agitation >= limite:
        return "agitation elevee"


def send_agitation():
    message = check_agitation()
    radio.send(str(message))


# Active le module radio
radio.on()

# Configure le canal radio sur 7 (vous pouvez choisir un autre si nécessaire)
radio.config(channel=7)

# Variable pour stocker l'état précédent
sleeping = True
calm = True
radio.send("sleeping")

# Variable pour la quantité de lait consommée
milk_consumed = 0


def drink_milk(milk_consumed, dose):
    milk_consumed += dose


communication = True
while communication:
    # display.scroll(password)
    show_image()

    # Vérifie le mouvement à l'aide de l'accéléromètre
    movement = accelerometer.current_gesture()
    message = radio.receive()
    m = ''

    etat_enfant = check_agitation()

    #Verification si l'enfant tombe
    if movement == "freefall":
        radio.send("agitation elevee")
        sleep(1000)  # Max 1 message/ seconde
        sleeping = False
        calm = False
        while not calm:
            display.show(Image.CONFUSED)
            message = radio.receive()
            if message:
                if message == "calm":
                    display.show(Image.HAPPY)
                    music.play(music.POWER_UP)
                    calm = True
            sleep(1000)

    if etat_enfant == "agitation elevee":
        # Envoie le message "awake" si l'appareil dormait et qu'il y a eu un mouvement
        send_agitation()
        sleep(1000)  # Max 1 message/ seconde
        sleeping = False
        calm = False
        while not calm:
            display.show(Image.CONFUSED)
            message = radio.receive()
            if message:
                if message == "calm":
                    display.show(Image.HAPPY)
                    music.play(music.POWER_UP)
                    calm = True
            sleep(1000)

    if message:
        m = message.strip()

    if m == 'get_milk':
        radio.send(str(milk_consumed))
        display.scroll("{} ml".format(milk_consumed))

    if m == 'get_temperature':
        temp = temperature()
        radio.send(str(temp) + " C")
        if temp < 35 or temp > 37:
            happy = False
            while not happy:
                display.show(Image.SAD)
                message = radio.receive()
                if message == 'medicament':
                    display.show(Image.HAPPY)
                    music.play(music.POWER_UP)
                    radio.send('merci')
                    happy = True
                else:
                    sleep(1000)


    elif m.isdigit():
        dose = int(m)
        milk_consumed += dose  # L'enfant est en train de boire la dose de lait
        display.show(Image.HAPPY)  # :)
        music.play(music.POWER_UP)
        radio.send("{}".format(milk_consumed))
        display.scroll("{} ml".format(milk_consumed))

    else:
        sleep(500)