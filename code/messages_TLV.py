import struct


def encode_tlv(tag, value):
    """
    Encode un message en format TLV (Tag-Length-Value).

    tag : Identifiant du tag (entier).
    value : Données à envoyer (en bytes ou string).
    """
    length = len(value)  # Calcul de la longueur de la valeur
    # Utilisation de struct pour encoder le Tag, Length et Value
    tlv_message = struct.pack(f"!B B {len(value)}s", tag, length, value.encode('utf-8'))
    return tlv_message


def send_tlv_to_file(tag, value, file_name):
    """
    Encode un message TLV et l'écrit dans un fichier.

    tag : Identifiant du tag.
    value : Données à envoyer.
    file_name : Le nom du fichier où envoyer le message.
    """
    tlv_message = encode_tlv(tag, value)
    with open(file_name, 'wb') as file:
        file.write(tlv_message)
    print(f"Message envoyé dans le fichier - Tag: {tag}, Value: {value}")


# Exemple d'utilisation
send_tlv_to_file(1, "Hello, File!", 'message.tlv')

def decode_tlv(tlv_data):
    """
    Décode un message TLV (Tag-Length-Value).

    tlv_data : Les données TLV sous forme de bytes.
    """
    # Décodage du tag et de la longueur
    tag, length = struct.unpack("!B B", tlv_data[:2])
    value = tlv_data[2:2 + length].decode('utf-8')
    return tag, value


def receive_tlv_from_file(file_name):
    """
    Lit un fichier contenant un message TLV et le décode.

    file_name : Le nom du fichier contenant le message TLV.
    """
    with open(file_name, 'rb') as file:
        tlv_data = file.read()
    tag, value = decode_tlv(tlv_data)
    print(f"Message reçu du fichier - Tag: {tag}, Value: {value}")
    return tag, value


# Exemple d'utilisation
receive_tlv_from_file('message.tlv')

