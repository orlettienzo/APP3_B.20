from microbit import *
import radio


# Fonction de hachage existante
def hashing(string):
    """
    Calcule le hachage d'une chaîne donnée.

    :param string: chaîne à hacher
    :return: hachage de la chaîne
    """

    def to_32(value):
        """
        Convertit une valeur en entier signé 32 bits.

        :param value: valeur à convertir
        :return: entier signé 32 bits
        """
        value = value % (2 ** 32)
        if value >= 2 ** 31:
            value = value - 2 ** 32
        return int(value)

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


# Fonction pour générer un format TLV (Type, Length, Value)
def generate_tlv(type, message):
    """
    Génère une chaîne au format TLV.

    :param type: type de la donnée
    :param message: contenu de la donnée
    :return: chaîne au format TLV
    """
    length = len(message)
    message = message.strip().lower()
    m_tlv = "{}|{}|{}".format(type, length, message)
    return m_tlv


# Fonction de chiffrement/déchiffrement Vigenère
def vigenere(message, key, decrypt=False):
    """
    Chiffre ou déchiffre un message avec l'algorithme de Vigenère.

    :param message: message à chiffrer/déchiffrer
    :param key: clé utilisée pour le chiffrement/déchiffrement
    :param decrypt: True pour déchiffrer, False pour chiffrer
    :return: message chiffré ou déchiffré
    """
    result = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)):
        key_index = i % key_length
        if char.isalpha():
            if decrypt:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else:
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            if char.islower():
                modified_char = modified_char.lower()
            result += modified_char
        elif char.isdigit():
            if decrypt:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            result += modified_char
        else:
            result += char
    return result


# Décodage Vigenère
def decode_vigenere(encrypted_message, key):
    """
    Déchiffre un message chiffré avec l'algorithme de Vigenère.

    :param encrypted_message: message chiffré
    :param key: clé utilisée pour le chiffrement
    :return: message déchiffré
    """
    return vigenere(encrypted_message, key, decrypt=True)


# Décodage complet
def decode_final(encrypted_message, key):
    """
    Effectue le processus complet de décodage.

    :param encrypted_message: message chiffré
    :param key: clé utilisée pour le chiffrement
    :param original_message: message original au format TLV
    :return: message original si le hachage est valide
    :raises ValueError: si le hachage déchiffré ne correspond pas à l'original
    """
    # Étape 1 : Déchiffrement Vigenère
    decoded_hash = decode_vigenere(encrypted_message, key)
    print("Hachage déchiffré:", decoded_hash)

    return decoded_hash


def check_value(a, b):
    if a == b:
        return True
    else:
        return False


communication = True
while communication:

    message = radio.receive()
    if message:
        if message.isdigit():
            radio.send('ok')
            hash = message
            answer = False
            while not answer:
                vig = radio.receive()
                if vig:
                    m = decode_final(vig, "KEYWORD")
                    condition = check_value(m, hash)
                    if condition:
                        radio.send('ok')
                    else:
                        radio.send('not ok')

                    a = False
                    while not a:
                        message = radio.receive()
                        if message:
                            parts = message.split("|")
                            if parts[2] == "hello":
                                display.show(Image.HAPPY)
                                sleep(2000)
                                a = True

                    answer = True
                sleep(1000)

    sleep(1000)