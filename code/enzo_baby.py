from microbit import *
import radio

# 1. Définition de l'image initiale pour le bébé enfant
baby_image = Image("99990:"
                   "90000:"
                   "99900:"
                   "90000:"
                   "99990:")

display.show(baby_image)  # image initiale = lettre "E"

# Active le module radio
radio.on()

# Configure le canal radio sur 7 (vous pouvez choisir un autre si nécessaire)
radio.config(channel=7)

# Variable pour stocker l'état précédent
sleeping = True
radio.send("sleeping")

# Variable pour la quantité de lait consommée
milk_consumed = 0

# Envoie la quantité de lait consommée via radio
radio.send("milk consumed: {} ml".format(milk_consumed))

while True:
    # Vérifie le mouvement à l'aide de l'accéléromètre
    movement = accelerometer.current_gesture()

    if movement == "shake" or movement == "freefall" or movement == "move":
        if sleeping:
            # Envoie le message "awake" si l'appareil dormait et qu'il y a eu un mouvement
            radio.send("awake")
            sleeping = False

    # Vérifie si le bouton A est pressé pour afficher la quantité de lait
    if button_a.is_pressed():
        display.scroll("Milk: {} ml".format(milk_consumed))

    # Pause pour réduire la fréquence de vérification
    sleep(500)

