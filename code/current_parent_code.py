from microbit import *
import radio
import random
import music


# Can be used to filter the communication, only the ones with the same parameters will receive messages
# radio.config(group=23, channel=2, address=0x11111111)
# default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)
def hashing(string):
    """
    Hachage d'une chaîne de caractères fournie en paramètre.
    Le résultat est une chaîne de caractères.
    Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

    :param (str) string: la chaîne de caractères à hacher
    :return (str): le résultat du hachage
    """

    def to_32(value):
        """
        Fonction interne utilisée par hashing.
        Convertit une valeur en un entier signé de 32 bits.
        Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

        :param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
        :return (int): entier signé de 32 bits représentant 'value'
        """
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
        # Letters encryption/decryption
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else:
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            # Put back in lower case if it was
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        # Digits encryption/decryption
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
    nonce = random.randint(1, 1000)
    contenu = "{}:{}".format(nonce, message)
    lenght = len(contenu)
    _tlv = "{}|{}|{}".format(type, lenght, contenu)
    return _tlv


def get_hash(string):
    return hashing(string)


def send_packet(key, type, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
	:return none
    """
    vig_cont = vigenere(content, key, decryption=False)
    packet = tlv(type, vig_cont)
    radio.send(packet)


# Fonction pour stocker les nonces dans la liste
# (Liée à la fonction unpack_data() )
def stock_nonce(element, liste):
    if element not in liste:
        liste.append(element)
    else:
        display.scroll("Duplicata")


# Decrypt and unpack the packet received and return the fields value
def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractères
            (str) message:         Données reçues
    """

    parts = encrypted_packet.split("|")
    m = parts[2].split(":")
    nonce = m[0]
    stock_nonce(nonce, nonce_lst)
    type = parts[0]
    lenght = parts[1]
    message = vigenere(m[1], key, decryption=True)
    _unpacked = (type, int(lenght), message)
    return _unpacked


# Unpack the packet, check the validity and return the type, length and content
def receive_packet(packet_received, key):
    """
    Traite les paquets reçue via l'interface radio du micro:bit
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit
    Si une erreur survient, les 3 champs sont retournés vides

    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
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


# Calculate the challenge response
def calculate_challenge_response(challenge, key):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
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
    """
    Cette fonction sert a calculer le resultat de la
    fonction random avec la racine reçue
    """
    seed = int(seed)
    random.seed(seed)
    value = random.randint(1, 1000)
    return value


# Ask for a new connection with a micro:bit of the same group
def establish_connexion_Parent(type, key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide
	return (srt)challenge_response:   Réponse au challenge
	"""
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


def main():
    return True


##########
# PARENT #
##########


# Initialisation des variables
key = "HEISENBERG"
hash_pass = hashing(key)
radio.on()
radio.config(channel=20)
connexion = False
racineRandom = None
hash_graine = None
m = radio.receive()

final_key = ""
final_key += key

# Nonce aleatoire
nonce = random.randint(2001, 4000)
nonce_str = str(nonce)

# Liste pour stocker les nonces
nonce_lst = []

# Recuperer nonce + set seed
while not connexion:
    # break
    type = 1
    display.show("?")
    result = calculate_challenge_response(m, key)
    if result != None:
        racineRandom = int(result)  # configuration de la racine de la fonction random
        # radio.send(str(racineRandom))
        send_packet(key, type, racineRandom)  # configuration a distance

        confirmation = False
        while not confirmation:
            m = radio.receive()
            if m:
                confirmation = True
            else:
                sleep(200)

        # Prochain challenge
        challenge = next_challenge(racineRandom)

        # Calcul hash
        c = str(challenge)
        hash_c = hashing(c)
        vig_hash = vigenere(hash_c, key, decryption=False)

        # Envoi hash calcule
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

euros = 1000


def send_money(devises, amount):
    current_btc = devises["data"]["EUR"]["value"]
    btc = amount / current_btc
    vig_btc = vigenere("btc", final_key, decryption=False)
    radio.send(tlv(4, vig_btc))
    answer = False
    while not answer:
        message = radio.receive()
        if message:
            tupla = unpack_data(message, final_key)
            if tupla != None:
                if tupla[2] == "send":
                    send_packet(final_key, 4, str(btc))
                    answer = True


def show_image():
    # 1. Définition de l'image initiale pour le micro:bit parent
    parent_image = Image("99990:"
                         "90090:"
                         "99990:"
                         "90000:"
                         "90000:")

    display.show(parent_image)  # image initiale = lettre "P"


def rassurer_enfant(type=1):
    message = "calm"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


def get_milk_consumed(type=3):
    message = "getMilk"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


def ask_temperature(type=4):
    message = "getTemperature"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


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


def send_milk_dose(dose, type=3):
    message = str(dose)
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


def check_etat_eveil():
    message = "etatEveil"
    send_packet(final_key, 1, message)
    answer = False
    while not answer:
        m = radio.receive()
        if m:
            tupla = unpack_data(m, final_key)
            if tupla != None:
                etat = tupla[2]
                display.scroll("{}".format(etat))
                answer = True
            else:
                sleep(200)
        else:
            sleep(200)


cmpt_a = 0
cmpt_b = 0
communication = True
while communication:

    show_image()
    # on va demander la Q de lait consommée par l'enfant (version 1.0)
    if button_a.is_pressed() and button_b.is_pressed() == False:
        cmpt_a += 1
        if cmpt_a >= 1:
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
                                    display.scroll("{} ml".format(tupla[2]))
                                    a = True
                        answer = True
                    else:
                        sleep(200)
            cmpt_a = 0

    # on va demander la temperature de l'Enfant (version 1.1)
    if button_b.is_pressed() and button_a.is_pressed() == False:
        cmpt_b += 1
        if cmpt_b >= 1:
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

    if button_a.is_pressed() and button_b.is_pressed():
        sleep(2000)
        send_money(devises, euros)

    if pin_logo.is_touched():
        check_etat_eveil()

    # Réception des messages via radio (version 1.0)
    message = radio.receive()
    if message:
        tupla = unpack_data(message, final_key)

        if tupla != None:
            # Reaction face a l'agitation de l'enfant (version 1.0)
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

