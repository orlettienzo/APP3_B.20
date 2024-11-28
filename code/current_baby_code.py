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
        challenge = parts[2]
        graine = vigenere(challenge, key, decryption=True)
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
def establish_connexion_Enfant(type, key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
    """
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


def send_confirmation():
    message = "ok"
    m = hashing(message)
    vig_m = vigenere(m, key, decryption=False)
    to_send = tlv(type, vig_m)
    radio.send(to_send)


def main():
    return True


##########
# ENFANT #
##########

# Initialisation des variables
key = "HEISENBERG"
hash_pass = hashing(key)
radio.on()
radio.config(channel=20)
racineRandom = None
connexion = False
m = radio.receive()

final_key = ""
final_key += key

# Liste pour stocker les nonces
nonce_lst = []

# Envoi du nonce chiffre au Parent
while not connexion:
    #break
    # Nonce aleatoire
    nonce = random.randint(1, 1000)
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
                racineRandom = int(u[2])  # racine random configuree
                # radio.send(str(racineRandom))

                # Prochain challenge
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

# Variables globales
sleeping = True
calm = True
milk_consumed = 0


# Fonctions Enfant

# Classe représentant le portefeuille numérique de l'enfant
class DigitalWallet:
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


# Initialisation du portefeuille
baby_wallet = DigitalWallet('Micro Enfant', 'BE00 0001')


def show_image():
    baby_image = Image("99990:"
                       "90000:"
                       "99900:"
                       "90000:"
                       "99990:")
    display.show(baby_image)


# Fonction pour rassurer le parent
def rassurer_parent():
    message = "calm"
    vig_m = vigenere(message, final_key, decryption=False)
    radio.send(tlv(2, vig_m))  # CHIFFREE


# Fonction pour vérifier le niveau d'agitation
def check_agitation():
    agitation = accelerometer.get_strength()
    if agitation < 1000:
        return "agitation faible"
    elif agitation < 3000:
        return "agitation moyenne"
    else:
        return "agitation elevee"


# Fonction pour envoyer un message sur l'agitation
def send_agitation(type=2, agitation=None):
    vig_m = vigenere(agitation, final_key, decryption=False)
    radio.send(tlv(type, vig_m))  # CHIFFREE


# Fonction pour envoyer un message si l'enfant est en chute libre
def send_freefall(type=2, mouvement="freefall"):
    vig_m = vigenere(mouvement, final_key, decryption=False)
    radio.send(tlv(type, vig_m))


# Fonction pour verifier la temperature
def get_temperature():
    temp = str(temperature())
    return temp


# Fonction pour envoyer un message sur la temperature
def send_temperature(temp, type=4):
    vig_temp = vigenere(str(temp), final_key, decryption=False)
    radio.send(tlv(type, vig_temp))  # CHIFFREE


# Fonction pour afficher la quantité de lait consommée
def show_milk(milk_consumed):
    display.scroll(str((milk_consumed) + " ml"))


# Gestion de la consommation de lait
def drink_milk(milk_consumed, dose):
    milk_consumed += dose
    return milk_consumed


# Boucle reservée à la communication entre les micros
communication = True
while communication:
    show_image()

    # Si le bouton A est pressé, affiche la quantité
    # de lait consommée
    if button_a.was_pressed():
        show_milk(str(milk_consumed))

        # Vérifie les mouvements avec l'accéléromètre
        movement = accelerometer.current_gesture()

        # Vérifie si l'enfant est en chute libre
        if movement == "freefall":
            send_freefall()
            sleeping = False
            calm = False
            display.show(Image.SAD)
            # ci-dessous on va verifier si les parents se rapprochent de lui (version 1.0)
            while not calm:
                message = "ping"
                vig_m = vigenere(message, final_key, decryption=False)
                radio.send(tlv(2, vig_m))
                m = radio.receive()
                if message:
                    pass

    # verification du niveau d'agitation (verison 1.0)
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

    # Réception des messages via radio (version 1.0)
    message = radio.receive()
    if message:
        tupla = unpack_data(message, final_key)
        if tupla != None:
            if tupla[2] == "btc":
                send_packet(final_key, 4, "send")
                value = baby_wallet.get_transfer()
                baby_wallet.receive(value)
                display.scroll("{} BTC".format(baby_wallet.solde))
        else:
            sleep(200)


    else:
        sleep(200)



