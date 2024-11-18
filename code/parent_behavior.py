from microbit import *
import radio
import random
import music

# Active le module radio
radio.on()
radio.config(channel=7)

# Dictionnaire des taux de change des devises - 08/11
# Dictionnaire généré par l'API:
# "Currencyapi"

devises = {
    "meta": {
        "last_updated_at": "2024-11-07T23:59:59Z"
    },
    "data": {
        "CAD": {
            "code": "CAD",
            "value": 105168.1281341745
        },
        "EUR": {
            "code": "EUR",
            "value": 70239.7648075961
        },
        "USD": {
            "code": "USD",
            "value": 75847.1329232132
        }
    }
}

# devises_new_values = {À REMPLIR} *À consulter nouvellement l'API en decembre pour pouvoir calculer l'appreciation du BTC

allocation_familiale = 1000


def send_money(devises, amount):
    current_btc = devises["data"]["EUR"]["value"]
    btc = amount / current_btc
    radio.send("btc")
    answer = False
    while not answer:
        message = radio.receive()
        if message:
            if message == "send":
                radio.send(str(btc))





def show_image():
    # 1. Définition de l'image initiale pour le micro:bit parent
    parent_image = Image("99990:"
                         "90090:"
                         "99990:"
                         "90000:"
                         "90000:")

    display.show(parent_image)  # image initiale = lettre "P"


def rassurer_enfant():
    music.play(music.ODE)
    radio.send("calm")


def get_milk_consumed():
    radio.send("get_milk")


def get_temperature():
    radio.send("get_temperature")


def check_fever(temp):
    if temp < 35:
        return "hypothermie"
    elif 37 < temp < 38:
        return "fievre_legere"
    elif 38 < temp < 39:
        return "fievre_moderee"
    elif 39 < temp < 40:
        return "fievre_elevee"
    elif temp > 40:
        return "fievre_tres_elevee"
    else:
        return "temperature_normale"


def send_medicament():
    radio.send('medicament')


def set_milk_dose():
    display.scroll("set dose")
    dose = 0
    add = True

    time_to_stop = 2000

    while add:

        if dose < 10:
            display.show("{}".format(dose))

        if button_b.was_pressed():
            dose += 50

        # Supprimer une dose erro
        elif button_a.was_pressed():
            if dose >= 50:
                dose -= 50
            else:
                pass  # Il existe pas de dose negative´

        # Reinitialiser a zero
        elif button_a.is_pressed():
            tempo_initial = running_time()  # Capture le temps initial

            # Tant que le bouton B est pressé, continue de vérifier
            while button_a.is_pressed():
                temps_ecoule = running_time() - tempo_initial  # Temps pendant lequel le bouton a été pressé

                # Si le temps écoulé est supérieur ou égal à 2000ms, arrête d'ajouter
                if temps_ecoule >= time_to_stop:
                    dose = 0
                    break  # Sort de la boucle si le bouton est pressé plus de 2 secondes


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

    if pin_logo.is_touched():
        send_money(devises, allocation_familiale)

    # Reçoit un message s'il y en a un de disponible
    message = radio.receive()
    m = ''

    if message:
        m = message.strip()
        m = str(m)

    # Vérifie si un nouveau message a été reçu
    if m == "agitation elevee":
        calm = False
        display.show(Image.SURPRISED)
        while not calm:
            message = radio.receive()
            if message:
                if message == "calm":
                    display.show(Image.HAPPY)
                    music.play(music.BA_DING)
            else:
                sleep(1000)

    if button_a.was_pressed():
        get_milk_consumed()

    if button_b.was_pressed():
        get_temperature()
        found = False
        while not found:
            message = radio.receive()
            if message:
                m = message.strip()
                parts = m.split()
                temp = parts[0]
                celsius = parts[1]
                if temp.isdigit() and celsius == 'C':
                    display.scroll('{} C'.format(temp))
                    sleep(500)
                    baby_temp = check_fever(int(temp))
                    display.scroll("{}".format(baby_temp))
                    if baby_temp != "temperature_normale":
                        display.show(Image.SURPRISED)
                        sleep(1000)
                        send_medicament()
                        answer = False
                        while not answer:
                            display.show(Image.SURPRISED)
                            message = radio.receive()
                            if message == 'merci':
                                display.show(Image.HAPPY)
                                sleep(1000)
                                answer = True
                            else:
                                sleep(200)
                        found = True
                else:
                    sleep(1000)

    if m.isdigit():
        dose_given = False
        while not dose_given:
            display.scroll("{} ml".format(m))
            sleep(1000)
            button_b.was_pressed()  # Nous utilisons
            # cette ligne pour ignorer les pressions précédentes sur le bouton B,
            # permettant de définir chaque nouvelle dose à 0.
            dose = set_milk_dose()
            if dose > 0:
                send_milk_dose(dose)
            dose_given = True

    else:
        # Petit délai pour éviter de surcharger la boucle
        sleep(500)