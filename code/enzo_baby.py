from microbit import *

#1. Definition de l'image initiale pour le be:bi enfant
baby_image = Image("99990:"     
                "90000:"        
                "99900:"        
                "90000:"        
                "99990:")


display.show(baby_image) # image initale = lettre "E"

from microbit import *
import radio

# Active le module radio
radio.on()

# Configure le canal radio sur 7 (vous pouvez choisir un autre si nécessaire)
radio.config(channel=7)

# Variable pour stocker l'état précédent
sleeping = True
radio.send("sleeping")

while True:
    # Vérifie le mouvement à l'aide de l'accéléromètre
    movement = accelerometer.current_gesture()
    
    if movement == "shake" or movement == "freefall" or movement == "move":
        if sleeping:
            # Envoie le message "awake" si l'appareil dormait et qu'il y a eu un mouvement
            radio.send("awake")
            sleeping = False
    
        
    
    # Pause pour réduire la fréquence de vérification
    sleep(500)

