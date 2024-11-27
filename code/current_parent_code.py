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
    lenght = len(message)
    message = message.strip()
    _tlv = "{}|{}|{}".format(type, lenght, message)
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

    encrypted_packet = radio.receive()
    if encrypted_packet:
        parts = encrypted_packet.split("|")
        type = parts[0]
        lenght = parts[1]
        message = vigenere(parts[2], key, decryption=True)
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

    # return (type, lenght, message)


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
        challenge = parts[2]
        graine = vigenere(challenge, key, decryption=True)
        random.seed(int(graine))
        reponse = random.randint(1, 100)
        return str(reponse)
    else:
        sleep(200)


# Ask for a new connection with a micro:bit of the same group
def establish_connexion_Parent(type, key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
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
graine = None
hash_graine = None
m = radio.receive()

final_key = ""
final_key += key

# Recuperer nonce + set seed
while not connexion:
    type = 1
    display.show("?")
    result = calculate_challenge_response(m, key)
    if result != None:
        # Configuration de la graine locale
        graine = int(result)
        hash_graine = hashing(result)
        vig_graine = vigenere(result, key, decryption=False)
        final_key += result
        # Configuration de la graine a distance
        message = vig_graine + "_" + hash_graine
        radio.send(tlv(type, message))
        # Etablissement de la connexion
        status = establish_connexion_Parent(type, final_key)
        if status == 1:
            display.show(Image.HAPPY)
            music.play(music.POWER_UP)
            sleep(1500)
            connexion = True
        else:
            sleep(200)

    else:
        sleep(200)

# Test
# radio.send(final_key)

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
    message = "get_milk"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


def ask_temperature(type=4):
    message = "get_temperature"
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


communication = True
while communication:
    show_image()

