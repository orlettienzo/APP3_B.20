# Enfant
from microbit import *
import radio
import random
import music
import speech


def hashing(string):
    def to_32(value):
        value = value % (2 ** 32)
        if value >= 2 ** 31:
            value = value - 2 ** 32
        value = int(value)
        return value

    if string:
        x = ord(string[0]) << 7
        m = 1000003
        for c in string:
            x = to_32((x * m) ^ ord(c))
        x ^= len(string)
        if x == -1:
            x = -2
        return str(x)
    return ""


def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)):
        key_index = i % key_length
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else:
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text


def tlv(type, message):
    message = message.strip()
    nonce = create_nonce(nonce_lst)
    if nonce not in nonce_lst:
        nonce_lst.append(nonce)
    contenu = "{}:{}".format(nonce, message)
    lenght = len(contenu)
    _tlv = "{}|{}|{}".format(type, lenght, contenu)
    return _tlv


def send_packet(key, type, content):
    vig_cont = vigenere(content, key, decryption=False)
    packet = tlv(type, vig_cont)
    radio.send(packet)


def stock_nonce(element, liste):
    if element not in liste:
        liste.append(element)
    else:
        display.scroll("Duplicata")


def unpack_data(encrypted_packet, key):
    if encrypted_packet != None:
        parts = encrypted_packet.split("|")
        m = parts[2].split(":")
        type = parts[0]
        lenght = parts[1]
        message = vigenere(m[1], key, decryption=True)
        _unpacked = (type, int(lenght), message)
        return _unpacked


def receive_packet(packet_received, key):
    if packet_received == None:
        type = None
        lenght = None
        message = None
        return (type, lenght, message)

    type = packet_received[0]
    lenght = packet_received[1]
    message = packet_received[2]

    m = hashing(message)
    to_send = tlv(type, vigenere(m, key, decryption=False))
    radio.send(to_send)

    return (type, lenght, message)


def calculate_challenge_response(challenge, key):
    m = radio.receive()
    if m:
        parts = m.split("|")
        challenge = parts[2]
        graine = vigenere(challenge, key, decryption=True)
        random.seed(int(graine))
        reponse = random.randint(1, 100)
        return str(reponse)
    else:
        sleep(200)


def next_challenge(seed):
    seed = int(seed)
    random.seed(seed)
    value = random.randint(1, 1000)
    return value


def establish_connexion_Enfant(type, key):
    hash_key = hashing(key)
    vig_hash_key = vigenere(hash_key, key, decryption=False)
    radio.send(tlv(type, vig_hash_key))
    answer = False
    while not answer:
        m = radio.receive()
        if m:
            parts = m.split("|")
            des_vig = vigenere(parts[2], key, decryption=True)
            if des_vig == hash_key:
                return 1

        sleep(200)

    return 0


def create_nonce(lst):
    if len(lst) == 5000:
        lst = []
    nonce = random.randint(1, 5000)
    if nonce not in lst:
        lst.append(nonce)
        return nonce
    else:
        create_nonce(lst)


def send_confirmation():
    message = "ok"
    m = hashing(message)
    vig_m = vigenere(m, key, decryption=False)
    to_send = tlv(1, vig_m)
    radio.send(to_send)


def main():
    return True


key = "H"
hash_pass = hashing(key)
radio.on()
radio.config(channel=20)
racineRandom = None
connexion = False
m = radio.receive()

final_key = ""
final_key += key

nonce_lst = []

while not connexion:
    break
    nonce = create_nonce(nonce_lst)
    nonce_str = str(nonce)
    display.show("?")
    type = 1
    send_packet(key, type, nonce_str)
    answer = False
    while not answer:
        m = radio.receive()
        if m:
            send_confirmation()
            u = unpack_data(m, key)
            if u != None:
                racineRandom = int(u[2])
                challenge = next_challenge(racineRandom)
                c = str(challenge)
                hash_c = hashing(c)
                answer = False
                while not answer:
                    m = radio.receive()
                    if m:
                        u = unpack_data(m, key)
                        if u != None:
                            if u[2] == hash_c:
                                send_confirmation()
                                sleep(100)
                                display.show(Image.HAPPY)
                                music.play(music.POWER_UP)
                                final_key += c
                                sleep(1500)
                                answer = True
                connexion = True
        else:
            sleep(200)


class DigitalWallet:
    ancienne_cotation = {
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

    cotation_actuelle = {
        "meta": {
            "last_updated_at": "2024-11-28T23:59:59Z"
        },
        "data": {
            "CAD": {
                "code": "CAD",
                "value": 134004.6817822797
            },
            "EUR": {
                "code": "EUR",
                "value": 90575.5390184203
            },
            "USD": {
                "code": "USD",
                "value": 95682.0736956224
            }
        }
    }

    def __init__(self, titulaire, numero_compte):
        self.__titulaire = titulaire
        self.__numero_compte = numero_compte
        self.solde = 0.0

    def receive(self, valeur):
        if valeur != None:
            self.solde += float(valeur)

    def get_transfer(self):
        answer = False
        while not answer:
            m = radio.receive()
            if m:
                tupla = unpack_data(m, final_key)
                if tupla != None:
                    value = tupla[2]
                    answer = True
                    return float(value)

                else:
                    sleep(100)
            else:
                sleep(100)

    def cash_out_btc(self):
        euros = self.solde * DigitalWallet.cotation_actuelle["data"]["EUR"]["value"]
        currentbtc = euros / DigitalWallet.cotation_actuelle["data"]["EUR"]["value"]
        return (euros, currentbtc)

    def show_valorisation(self):
        valeur_initiale = self.solde * DigitalWallet.ancienne_cotation["data"]["EUR"]["value"]
        valeur_finale = self.solde * DigitalWallet.cotation_actuelle["data"]["EUR"]["value"]
        if valeur_initiale != 0:
            pourcentage = ((valeur_finale - valeur_initiale) / valeur_initiale) * 100
            p = round(pourcentage, 1)
        else:
            pourcentage = 0
            p = 0.0

        currentbtc = valeur_finale / DigitalWallet.cotation_actuelle["data"]["EUR"]["value"]

        display.scroll("Val : ")
        euros = valeur_finale - valeur_initiale
        if euros > 0:
            display.scroll("+ {} EUR".format(round(euros, 2)))
        else:
            display.scroll("- {} EUR".format(round(abs(euros), 2)))

        sleep(300)
        display.scroll("{} BTC".format(round(currentbtc, 7)))
        sleep(300)
        if int(p) > 0:
            sleep(100)
            display.show(Image.ARROW_NE)
            sleep(100)
            display.show(Image.ARROW_NE)
            sleep(100)
            display.show(Image.ARROW_NE)
            sleep(100)
            display.show(Image.ARROW_NE)
            sleep(700)
            music.play(music.POWER_UP)
            display.show(Image.HAPPY)
            sleep(1000)

        elif int(p) == 0:
            sleep(100)
            display.show("=")
            sleep(500)

        elif int(p) < 0:
            sleep(100)
            display.show(Image.ARROW_SE)
            sleep(100)
            display.show(Image.ARROW_SE)
            sleep(100)
            display.show(Image.ARROW_SE)
            sleep(100)
            display.show(Image.ARROW_SE)
            sleep(700)
            music.play(music.POWER_DOWN)
            display.show(Image.SAD)
            sleep(1000)


baby_wallet = DigitalWallet('Micro Enfant', 'BE00 0001')


def show_image():
    baby_image = Image("99990:"
                       "90000:"
                       "99900:"
                       "90000:"
                       "99990:")
    display.show(baby_image)


def rassurer_parent():
    message = "calm"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(2, vig_m))


def check_agitation():
    agitation = accelerometer.get_strength()
    if agitation < 1000:
        return "agitation faible"
    elif agitation < 3000:
        return "agitation moyenne"
    else:
        return "agitation elevee"


def send_agitation(type=2, agitation=None):
    vig_m = vigenere(agitation, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


def send_freefall(type=2, mouvement="freefall"):
    vig_m = vigenere(mouvement, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


def get_temperature():
    temp = str(temperature())
    return temp


def show_temperature():
    display.scroll("{} C".format(temperature()))


def send_temperature(temp, type=4):
    vig_temp = vigenere(str(temp), final_key, decryption=False)
    radio.send(tlv(type, vig_temp))


def show_milk(milk_consumed):
    display.scroll(str(milk_consumed) + " ml")


def drink_milk(milk_consumed, dose):
    milk_consumed += dose


if not compass.is_calibrated():
    compass.calibrate()

sleeping = True
calm = True
milk_consumed = 0

valeur_initiale = 0
valeur_finale = 0
cmpt_a = 0
cmpt_b = 0

communication = True

while communication:
    show_image()
    if button_a.is_pressed() and button_b.is_pressed() == False:
        cmpt_a += 1
        if cmpt_a >= 1:
            show_milk(str(milk_consumed))
            cmpt_a = 0
        else:
            sleep(200)

    movement = accelerometer.current_gesture()
    if movement == "freefall":
        send_freefall()
        sleeping = False
        calm = False
        display.show(Image.SAD)
        while not calm:
            message = "ping"
            send_packet(final_key, 2, message)
            sleep(700)
            m = radio.receive()
            if message:
                tupla = unpack_data(m, final_key)
                if tupla != None:
                    if tupla[2] == "calm":
                        display.show(Image.HAPPY)
                        music.play(music.POWER_UP)
                        sleep(1000)
                        calm = True
            else:
                display.show(Image.SAD)

    if button_b.is_pressed() and button_a.is_pressed() == False:
        cmpt_b += 1
        if cmpt_b >= 1:
            show_temperature()
            cmpt_b = 0
        else:
            sleep(200)

    if button_a.is_pressed() and button_b.is_pressed():
        sleep(1000)
        tupla = baby_wallet.cash_out_btc()
        if tupla != None:
            euros = tupla[0]
            btc = tupla[1]
            display.show(Image.ALL_CLOCKS)
            sleep(100)
            display.scroll("Today : ")
            display.scroll("{} BTC".format(round(btc, 7)))
            sleep(100)
            music.play(music.BA_DING)
            display.scroll("{} EUR".format(round(euros, 2)))
            sleep(100)
            baby_wallet.show_valorisation()
        else:
            sleep(200)

    niveau = check_agitation()
    if niveau == "agitation elevee":
        send_agitation(2, niveau)
        sleeping = False
        calm = False
        while not calm:
            display.show(Image.CONFUSED)
            music.play(music.BA_DING)
            sleep(1000)
            music.play(music.ODE)
            sleep(1000)
            rassurer_parent()
            sleep(200)
            display.show(Image.HAPPY)
            music.play(music.POWER_UP)
            sleep(1000)
            calm = True

    message = radio.receive()
    if message:
        tupla = unpack_data(message, final_key)
        if tupla != None:
            if tupla[2] == "getTemperature":
                temp = get_temperature()
                send_packet(final_key, 3, temp)
                display.scroll("{} C".format(str(temp)))
                answer = False
                while not answer:
                    m = radio.receive()
                    if m:
                        tupla = unpack_data(m, final_key)
                        if tupla != None:
                            if tupla[2] == "medicament":
                                display.show(Image.HAPPY)
                                music.play(music.POWER_UP)
                                sleep(1000)
                                answer = True
                        else:
                            sleep(200)
                    else:
                        sleep(200)

            if tupla[2] == "getMilk":
                send_packet(final_key, 3, milk_consumed)
                show_milk(milk_consumed)
                answer = False
                while not answer:
                    m = radio.receive()
                    if m:
                        tupla = unpack_data(m, final_key)
                        if tupla != None:
                            dose = int(tupla[2])
                            if dose > 0:
                                milk_consumed += dose
                                display.show(Image.HAPPY)
                                music.play(music.POWER_UP)
                                sleep(1000)
                                send_packet(final_key, 3, milk_consumed)
                                show_milk(str(milk_consumed))
                                answer = True
                            else:
                                send_confirmation()
                                answer = True

            if tupla[2] == "etatEveil":
                etat = check_agitation()
                send_packet(final_key, 1, etat)

            if tupla[2] == "hello":
                display.show(Image.HAPPY)
                speech.say("I am good")
                sleep(2000)
                send_confirmation()

            if tupla[2] == "sleep":
                brightness = 7
                for x in range(5):
                    for y in range(5):
                        display.set_pixel(x, y, brightness)
                asleep = False
                c = 0
                while not asleep:
                    c += 1
                    if c == 1:
                        send_packet(final_key, 6, "set_light")

                    m = radio.receive()
                    if m:
                        tupla = unpack_data(m, final_key)
                        if tupla is not None:
                            try:
                                value = int(tupla[2])
                                if value > 0:
                                    brightness = min(brightness + value, 9)
                                elif value < 0:
                                    brightness = max(brightness + value, 0)

                                for x in range(5):
                                    for y in range(5):
                                        display.set_pixel(x, y, brightness)

                                if brightness == 0:
                                    asleep = True
                                    display.show(Image.ASLEEP)
                                    sleep(1200)
                                    display.scroll(" zZzZ")
                                    send_confirmation()
                            except ValueError:
                                pass

            if tupla[2] == "direction":
                sending_drection = True
                while sending_drection:
                    display.clear()
                    direction = compass.heading()
                    m = radio.receive()

                    if m:
                        sending_drection = False

                    else:

                        if direction < 45 or direction >= 315:
                            send_packet(final_key, 7, "N")
                        elif direction < 135:
                            send_packet(final_key, 7, "E")  # Leste
                        elif direction < 225:
                            send_packet(final_key, 7, "S")  # Sul
                        else:
                            send_packet(final_key, 7, "O")  # Oeste

                    sleep(300)

            if tupla[2][-3:] == "btc":
                parts = tupla[2].split("_")
                valeur_initiale = parts[0]
                btc = float(parts[1])
                if btc > 0.0:
                    baby_wallet.receive(btc)
                    display.scroll("{} BTC".format(round(baby_wallet.solde, 7)))
                send_confirmation()
                check = Image("00000:"
                              "00009:"
                              "00090:"
                              "90900:"
                              "09000:")

                display.show(check)
                music.play(music.BA_DING)
                sleep(1500)


        else:
            sleep(200)


    else:
        sleep(200)