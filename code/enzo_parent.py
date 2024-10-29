from microbit import *
import radio

#Can be used to filter the communication, only the ones with the same parameters will receive messages
#radio.config(group=23, channel=2, address=0x11111111)
#default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)

#1. Definition de l'image initiale pour le be:bi parent
parent_image = Image("99990:"
                "90090:"
                "99990:"
                "90000:"
                "90000:")


display.show(parent_image) # image initale = lettre "P"

def get_milk_consumed():
    for i in range(1):
        radio.send("get_milk")
    
        
        

# Inicia o rádio
radio.on()
# Configura um canal para evitar interferência com outros micro:bits próximos (opcional)
radio.config(channel=7)

#Boucle pour la communication entre les micros
communication = True

while communication:
    # Recebe a mensagem se houver uma disponível
    mensagem = radio.receive()
    m = ''
    
    if mensagem:
        m = mensagem.strip()

    
    
    # Verifica se recebeu uma nova mensagem
    if m == "awake":
        # Reage à mensagem recebida (mostra um coração)
        display.show(Image.SURPRISED)
        sleep(1000)  # Exibe o coração por 1 segundo
        display.clear()  # Limpa a tela para que possa exibir de novo na próxima mensagem

    if button_a.was_pressed():
        get_milk_consumed()

    if m.isdigit():
        display.scroll("{} ml".format(m))
        
    else:
        # Pequeno delay para não sobrecarregar o loop
        sleep(100)


