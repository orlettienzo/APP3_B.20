from microbit import *
import radio
import random
import music


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
    agitation = accelerometer.get_x() ** 2 + accelerometer.get_y() ** 2 + accelerometer.get_z() ** 2

    # Définir les niveaux d'agitation (ajuster si nécessaire)
    if agitation < 1000:
        return "agitation faible"
    elif agitation < 15000:
        return "agitation moyenne"
    else:
        return "agitation elevee"


def send_agitation():
    message = check_agitation()
    radio.send(message)


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

    elif m.isdigit():
        dose = int(m)
        milk_consumed += dose  # L'enfant est en train de boire la dose de lait
        display.show(Image.HAPPY)  # :)
        music.play(music.POWER_UP)
        radio.send("{}".format(milk_consumed))
        display.scroll("{} ml".format(milk_consumed))

    else:
        sleep(500)