from microbit import *
import radio
import music


# Can be used to filter the communication, only the ones with the same parameters will receive messages
# radio.config(group=23, channel=2, address=0x11111111)
# default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)

def show_image():
    # 1. Definition de l'image initiale pour le be:bi parent
    parent_image = Image("99990:"
                         "90090:"
                         "99990:"
                         "90000:"
                         "90000:")

    display.show(parent_image)  # image initale = lettre "P"


def get_milk_consumed():
    radio.send("get_milk")


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

        # Verifica se o botão B está pressionado
        elif button_b.is_pressed():
            tempo_inicial = running_time()  # Captura o tempo inicial

            # Enquanto o botão B estiver pressionado, continua verificando
            while button_b.is_pressed():
                tempo_decorrido = running_time() - tempo_inicial  # Tempo que o botão foi pressionado

                # Se o tempo decorrido for maior ou igual a 2000ms, para de adicionar
                if tempo_decorrido >= time_to_stop:
                    dose -= 50
                    add = False
                    break  # Sai do loop se o botão for pressionado por mais de 2 segundos

        elif dose >= 10:
            display.scroll("{}".format(dose))

        # display.scroll("{}".format(dose))

    return dose


def send_milk_dose(dose):
    radio.send("{}".format(dose))


# Inicia o rádio
radio.on()
# Configura um canal para evitar interferência com outros micro:bits próximos (opcional)
radio.config(channel=7)

# Boucle pour la communication entre les micros
communication = True

while communication:
    show_image()

    # Recebe a mensagem se houver uma disponível
    mensagem = radio.receive()
    m = ''

    if mensagem:
        m = mensagem.strip()

    # Verifica se recebeu uma nova mensagem
    if m == "awake":
        # Reage à mensagem recebida (mostra um coração)
        display.show(Image.SURPRISED)
        music.play(music.BA_DING)
        sleep(1000)  # Exibe o coração por 1 segundo
        display.clear()  # Limpa a tela para que possa exibir de novo na próxima mensagem

    if button_a.was_pressed():
        get_milk_consumed()

    if m.isdigit():
        display.scroll("{} ml".format(m))
        sleep(1000)
        dose = set_milk_dose()
        if dose > 0:
            send_milk_dose(dose)

    else:
        # Pequeno delay para não sobrecarregar o loop
        sleep(500)

