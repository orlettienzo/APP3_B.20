from cryptographie.TLV import baby_functions as b

#Exemple de transformation de message en TLV

"""
TLV = Type Lenght Value
"""
import random

message = "Hello"
m = message.strip().lower()

def tlv_simple(message):
    type = random.randint(1, 10)
    length = len(message)
    message = message

    return (type, length, message)

new = tlv_simple(message)
print(new)

def tlv_en_bits(tupla):
    """
    tupla == (type = int, length = int, message = str)
    """
    if not isinstance(tupla[0], int) or not isinstance(tupla[1], int) or not isinstance(tupla[2], str):
        return False

    to_send = ''
    to_send += str(tupla[0]) + "|"
    to_send += str(tupla[1]) + "|"
    to_send += b.hashing(tupla[2])

    return to_send

to_send = tlv_en_bits(new)
print(to_send)
