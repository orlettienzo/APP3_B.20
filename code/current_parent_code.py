# Parent
from microbit import *
import radio
import random
import music
import speech

def call_function():
    def add():
        n = 0
        limite = 7
        add = True
        while add:

            if n > limite:
                n = 0

            if n < 10:
                display.show("{}".format(n))

            if button_b.was_pressed():
                n += 1

            elif button_a.was_pressed():
                if n >= 1:
                    n -= 1
                if n == 0:
                    n = 8
                else:
                    pass

            elif pin_logo.is_touched():
                add = False

        return n

    value = add()
    if value == 0:
        pass
    if value == 1:
        return "get_milk"
    elif value == 2:
        return "ask_temperature"
    elif value == 3:
        return "check_etat"
    elif value == 4:
        return "make_baby_sleep"
    elif value == 5:
        return "talk"
    elif value == 6:
        return "get_baby_direction"
    elif value == 7:
        return "send_btc"

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

def get_hash(string):
    return hashing(string)

def send_packet(key, type, content):
    vig_cont = vigenere(content, key, decryption=False)
    packet = tlv(type, vig_cont)
    radio.send(packet)

def stock_nonce(element, liste):
    if element not in liste:
        liste.append(element)
    else:
        e = int(element)
        liste.append(-e)

def unpack_data(encrypted_packet, key):
    parts = encrypted_packet.split("|")
    m = parts[2].split(":")
    nonce = m[0]
    stock_nonce(nonce, nonce_lst)
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
        challenge = parts[2].split(":")
        graine = vigenere(challenge[1], key, decryption=True)
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

def establish_connexion_Parent(type, key):
    hash_key = hashing(key)
    answer = False
    while not answer:
        m = radio.receive()
        if m:
            parts = m.split("|")
            des_vig = vigenere(parts[2], key, decryption=True)
            if des_vig == hash_key:
                radio.send(tlv(type, vigenere(hash_key, key, decryption=False)))
                return 1
    return 0

def create_nonce(lst):
    if len(lst) == 5000:
        lst = []
    nonce = random.randint(5001, 10000)
    if nonce not in lst:
        lst.append(nonce)
        return nonce
    else:
        create_nonce(lst)

def main():
    return True

key = "H"
hash_pass = hashing(key)
radio.on()
radio.config(channel=20)
connexion = False
racineRandom = None
hash_graine = None
m = radio.receive()

final_key = ""
final_key += key

nonce_lst = []

nonce = create_nonce(nonce_lst)
nonce_str = str(nonce)

while not connexion:
    type = 1
    display.show("?")
    result = calculate_challenge_response(m, key)
    if result != None:
        racineRandom = int(result)
        send_packet(key, type, racineRandom)
        confirmation = False
        while not confirmation:
            m = radio.receive()
            if m:
                confirmation = True
            else:
                sleep(200)
        challenge = next_challenge(racineRandom)
        c = str(challenge)
        hash_c = hashing(c)
        vig_hash = vigenere(hash_c, key, decryption=False)
        message = tlv(type, vig_hash)
        radio.send(message)
        confirmation = False
        while not confirmation:
            m = radio.receive()
            if m:
                display.show(Image.HAPPY)
                music.play(music.POWER_UP)
                sleep(1500)
                final_key += c
                confirmation = True
            else:
                sleep(200)

        connexion = True

    else:
        sleep(200)


def set_amount():
    euros = 0
    add = True
    time_to_stop = 2000
    while add:

        if euros < 10:
            display.show("{} EUR".format(euros))

        if button_b.was_pressed():
            euros += 100

        elif button_a.was_pressed():
            if euros >= 100:
                euros -= 100
            else:
                pass


        elif button_a.is_pressed():
            tempo_initial = running_time()

            while button_a.is_pressed():
                temps_ecoule = running_time() - tempo_initial

                if temps_ecoule >= time_to_stop:
                    euros = 0
                    break

        elif button_b.is_pressed():
            tempo_initial = running_time()
            while button_b.is_pressed():
                temps_ecoule = running_time() - tempo_initial
                if temps_ecoule >= time_to_stop:
                    euros -= 100
                    add = False
                    break

        elif euros >= 10:
            display.scroll("{}".format(euros))

    return euros


def send_btc(devises):
    amount = set_amount()
    current_btc = devises["data"]["EUR"]["value"]
    btc = amount / current_btc
    message = str(amount) + "_" + str(btc) + "_" + "btc"
    send_packet(final_key, 4, message)
    answer = False
    while not answer:
        display.clear()
        message = radio.receive()
        if message:
            check = Image("00000:"
                          "00009:"
                          "00090:"
                          "90900:"
                          "09000:")

            display.show(check)
            music.play(music.BA_DING)
            sleep(1500)
            answer = True
        else:
            sleep(200)


def show_image():
    parent_image = Image("99990:"
                         "90090:"
                         "99990:"
                         "90000:"
                         "90000:")

    display.show(parent_image)


def rassurer_enfant(type=1):
    message = "calm"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


def get_milk_consumed(type=3):
    message = "getMilk"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


def ask_temperature(type=4):
    message = "getTemperature"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


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


def show_croix():
    croix = Image("00900:"
                  "00900:"
                  "99999:"
                  "00900:"
                  "00900:")
    display.show(croix)
    sleep(100)
    display.clear()
    sleep(100)
    display.show(croix)
    sleep(100)
    display.clear()
    sleep(100)
    display.show(croix)
    sleep(100)
    display.clear()
    sleep(100)
    display.show(croix)
    sleep(100)
    display.clear()
    sleep(100)
    display.show(croix)
    sleep(100)
    display.clear()
    sleep(100)
    display.show(croix)
    sleep(100)
    display.clear()
    sleep(100)
    display.show(croix)
    sleep(700)


def send_medicament(type=4):
    message = "medicament"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


def set_milk_dose():
    display.scroll("def dose")
    dose = 0
    add = True

    time_to_stop = 2000

    while add:

        if dose < 10:
            display.show("{}".format(dose))

        if button_b.was_pressed():
            dose += 50

        elif button_a.was_pressed():
            if dose >= 50:
                dose -= 50
            else:
                pass

        elif button_a.is_pressed():
            tempo_initial = running_time()

            while button_a.is_pressed():
                temps_ecoule = running_time() - tempo_initial
                if temps_ecoule >= time_to_stop:
                    dose = 0
                    break

        elif button_b.is_pressed():
            tempo_initial = running_time()
            while button_b.is_pressed():
                temps_ecoule = running_time() - tempo_initial
                if temps_ecoule >= time_to_stop:
                    dose -= 50
                    add = False
                    break

        elif dose >= 10:
            display.scroll("{}".format(dose))

    return dose


def send_milk_dose(dose, type=3):
    message = str(dose)
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


def check_etat_eveil():
    message = "etatEveil"
    send_packet(final_key, 1, message)
    answer1 = False
    while not answer1:
        m = radio.receive()
        if m:
            tupla = unpack_data(m, final_key)
            if tupla != None:
                etat = tupla[2]
                if etat == "sleeping":
                    display.show(Image.ASLEEP)
                    sleep(1000)
                    answer1 = True

                else:
                    display.show(Image.SURPRISED)
                    sleep(1000)
                    answer1 = True

            else:
                sleep(200)
        else:
            sleep(200)
    sleep(1500)
    send_packet(final_key, 1, "next")
    answer2 = False
    while not answer2:
        m = radio.receive()
        if m:
            tupla = unpack_data(m, final_key)
            if tupla != None:
                niveau = tupla[2]
                if niveau == "agitation faible":
                    display.show(Image.ARROW_SE)
                    sleep(1200)
                    answer2 = True
                if niveau == "agitation moyenne":
                    display.show(Image.ARROW_E)
                    sleep(1200)
                    answer2 = True
                if niveau == "agitation elevee":
                    display.show(Image.ARROW_NE)
                    sleep(1200)
                    answer2 = True
            else:
                sleep(200)
        else:
            sleep(200)
    sleep(1500)
    send_packet(final_key, 1, "next")
    answer3 = False
    while not answer3:
        m = radio.receive()
        if m:
            tupla = unpack_data(m, final_key)
            if tupla != None:
                if int(tupla[2]) > 0:
                    display.show(Image.SAD)
                    sleep(1200)
                    display.scroll("It last {} ml".format(tupla[2]))
                    answer3 = True
                elif int(tupla[2]) <= 0:
                    display.show(Image.HAPPY)
                    sleep(1200)
                    answer3 = True
            else:
                sleep(200)
        else:
            sleep(200)


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
cmpt_a = 0
cmpt_b = 0

communication = True
while communication:

    show_image()
    f = ""
    if button_a.was_pressed():
        f = call_function()

    if f == "get_milk":
        get_milk_consumed()
        answer = False
        while not answer:
            m = radio.receive()
            if m:
                tupla = unpack_data(m, final_key)
                if tupla != None:
                    display.scroll("{} ml".format(tupla[2]))
                    dose = set_milk_dose()
                    send_milk_dose(dose)
                    a = False
                    while not a:
                        m = radio.receive()
                        if m:
                            tupla = unpack_data(m, final_key)
                            if tupla != None:
                                if int(tupla[2]) > 0:
                                    display.scroll("{} ml".format(tupla[2]))
                                a = True
                            cmpt_a = 0
                            answer = True
                else:
                    sleep(200)

                    sleep(200)

    if f == "ask_temperature":
        ask_temperature()
        answer = False
        while not answer:
            m = radio.receive()
            if m:
                tupla = unpack_data(m, final_key)
                if tupla != None:
                    temp = int(tupla[2])
                    fever = check_fever(temp)
                    display.scroll("{} C -> {}".format(temp, fever))
                    if fever != "temperature_normale":
                        display.show(Image.SURPRISED)
                        sleep(500)
                        show_croix()
                        send_medicament()
                        answer = True
                    else:
                        display.show(Image.HAPPY)
                        answer = True
            else:
                sleep(200)
        cmpt_b = 0

    if f == "send_btc":
        sleep(2000)
        send_btc(devises)

    if f == "check_etat":
        check_etat_eveil()

    if f == "talk":
        message = "hello"
        speech.say("Hello my son, how are you?")
        send_packet(final_key, 5, message)
        answer = False
        while not answer:
            m = radio.receive()
            if m:
                display.show(Image.HAPPY)
                sleep(1000)
                answer = True
            else:
                sleep(200)

    if f == "make_baby_sleep":
        display.clear()
        message = "sleep"
        speech.say("It is time to go to bed")
        send_packet(final_key, 6, message)
        answer = False
        while not answer:
            m = radio.receive()
            if m:
                answer = True
            else:
                sleep(200)
        asleep = False
        while not asleep:
            m = radio.receive()
            if m:
                asleep = True
            else:
                if button_b.was_pressed():
                    send_packet(final_key, 6, "1")
                elif button_a.was_pressed():
                    send_packet(final_key, 6, "-1")

        start_time = running_time()
        while True:
            m = radio.receive()
            if m:
                display.show(Image.SAD)
                sleep(700)
                break
            else:
                display.show(Image.ALL_CLOCKS)
                total = elapsed_time = (running_time() - start_time) / 1000
                if total >= 8:
                    display.show(Image.HAPPY)
                    music.play(music.POWER_UP)
                    sleep(1000)
                    break

    if f == "get_baby_direction":
        display.clear()
        message = "direction"
        send_packet(final_key, 7, message)
        suivre_enfant = True
        while suivre_enfant:
            if button_a.was_pressed():
                send_packet(final_key, 7, "finish")
                suivre_enfant = False

            m = radio.receive()
            if m:
                tupla = unpack_data(m, final_key)
                if tupla != None:
                    display.show("{}".format(tupla[2]))
                    sleep(100)

    message = radio.receive()
    if message:
        tupla = unpack_data(message, final_key)

        if tupla != None:
            if tupla[2] == "agitation elevee":
                display.show(Image.SURPRISED)
                music.play(music.BA_DING)
                sleep(1000)
                calm = False
                while not calm:
                    m = radio.receive()
                    if m:
                        tupla = unpack_data(m, final_key)
                        if tupla != None:
                            if tupla[2] == "calm":
                                display.show(Image.HAPPY)
                                music.play(music.POWER_UP)
                        calm = True
                    else:
                        sleep(200)

            if tupla[2] == "freefall":
                calm = False
                display.show(Image.SURPRISED)
                sleep(500)
                while not calm:
                    message = radio.receive_full()
                    if message:
                        _, ping, _ = message
                        if ping != None:
                            if ping > -35:
                                send_packet(final_key, 2, "calm")
                                display.show(Image.HAPPY)
                                music.play(music.POWER_UP)
                                sleep(1000)
                                calm = True
                    else:
                        display.show(Image.SAD)

        sleep(1000)

    else:
        sleep(200)

