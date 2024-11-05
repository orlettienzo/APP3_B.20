from microbit import *
import radio
import music
import random

# Peut être utilisé pour filtrer la communication, seuls ceux ayant les mêmes paramètres recevront les messages
# radio.config(group=23, channel=2, address=0x11111111)
# paramètres par défaut : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)

# Simulation de partage de mot de passe
password = None
def set_password():
    lettres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    d = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
        'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15,
        'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22,
        'w': 23, 'x': 24, 'y': 25, 'z': 26
    }

    password = ''
    for i in range(5):
        index = random.randint(0, len(lettres) - 1)
        password += lettres[index]

    password_chiffre = ''
    for lettre in password:
        if lettre in d:
            password_chiffre += str(d[lettre]) + ' '

    # radio.send(password)
    radio.send(password_chiffre)
    return password


password = set_password()


def show_image():
    # 1. Définition de l'image initiale pour le micro:bit parent
    parent_image = Image("99990:"
                         "90090:"
                         "99990:"
                         "90000:"
                         "90000:")

    display.show(parent_image)  # image initiale = lettre "P"


def get_milk_consumed():
    radio.send("get_milk")


def set_milk_dose():
    display.scroll("définir dose")
    dose = 0
    add = True

    time_to_stop = 2000

    while add:

        if dose < 10:
            display.show("{}".format(dose))

        if button_b.was_pressed():
            dose += 50

        # Vérifie si le bouton B est pressé
        elif button_b.is_pressed():
            tempo_initial = running_time()  # Capture le temps initial

            # Tant que le bouton B est pressé, continue de vérifier
            while button_b.is_pressed():
                temps_ecoule = running_time() - tempo_initial  # Temps pendant lequel le bouton a été pressé

                # Si le temps écoulé est supérieur ou égal à 2000ms, arrête d'ajouter
                if temps_ecoule >= time_to_stop:
                    dose -= 50
                    add = False
                    break  # Sort de la boucle si le bouton est pressé plus de 2 secondes

        elif dose >= 10:
            display.scroll("{}".format(dose))

    return dose


def send_milk_dose(dose):
    radio.send("{}".format(dose))


# Active le module radio
radio.on()
# Configure un canal pour éviter les interférences avec d'autres micro:bits à proximité (optionnel)
radio.config(channel=7)

# Boucle pour la communication entre les micro:bits
communication = True

while communication:
    show_image()

    # Reçoit un message s'il y en a un de disponible
    message = radio.receive()
    m = ''

    if message:
        m = message.strip()

    # Vérifie si un nouveau message a été reçu
    if m == "awake":
        # Réagit au message reçu (affiche un visage surpris)
        display.show(Image.SURPRISED)
        music.play(music.BA_DING)
        sleep(1000)  # Affiche le visage surpris pendant 1 seconde
        display.clear()  # Efface l'écran pour afficher à nouveau lors du prochain message

        # Ici, nous allons rassurer l'enfant
        radio.send("calm")
        music.play(music.ODE)

    if button_a.was_pressed():
        get_milk_consumed()

    if m.isdigit():
        display.scroll("{} ml".format(m))
        sleep(1000)
        button_b.was_pressed()  # Nous utilisons
        # cette ligne pour ignorer les pressions précédentes sur le bouton B,
        # permettant de définir chaque nouvelle dose à 0.
        dose = set_milk_dose()
        if dose > 0:
            send_milk_dose(dose)

    else:
        # Petit délai pour éviter de surcharger la boucle
        sleep(500)

