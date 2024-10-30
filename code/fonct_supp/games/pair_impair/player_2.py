# Imports go at the top | PLAYER 2
from microbit import *
import random as r
import radio


radio.on()
radio.config(channel=7) #Igualamos os 2 micros no mesmo canal

choix = 'None'
chosen_number = r.randint(0, 9) #Numero que sera lançado

#get choice
def get_choice():
    message = radio.receive()
    if message:
        return message
    else:
        sleep(500)

searching = True
while searching:
    #sleep(3000)
    choix = get_choice()
    if choix != None:
        searching = False

#Escolha desse micro afichada no LED
if choix == 'pair': 
    display.show("P")
    sleep(1000)
if choix == 'impair':
    display.show("I")
    sleep(1000)

sleep(1000)
challenge = True
while challenge:
    display.clear()
    sleep(1000)
    display.show("3")
    sleep(1000)
    display.show("2")
    sleep(1000)
    display.show("1")
    sleep(1000)
    display.clear()
    sleep(1000)
    radio.send('{}'.format(chosen_number))
    display.show('{}'.format(chosen_number))
    sleep(3000)
    challenge = False

sleep(1000)
comparing = True
while comparing:
    message = radio.receive()
    if message:
        if message.isdigit():
            opp_number = int(message)
            
            somme = chosen_number + opp_number

            if somme % 2 == 0 and choix == 'pair':
                display.show(Image.HAPPY)
                sleep(1000)
                display.scroll("You won!")
                comparing = False

            elif somme % 2 != 0 and choix == 'impair':
                display.show(Image.HAPPY)
                sleep(1000)
                display.scroll("You won!")
                comparing = False

            elif somme % 2 != 0 and choix == 'pair':
                display.show(Image.SAD)
                sleep(1000)
                display.scroll("You lost!")
                comparing = False

            elif somme % 2 == 0 and choix == 'impair':
                display.show(Image.SAD)
                sleep(1000)
                display.scroll("You lost!")
                comparing = False


    


    