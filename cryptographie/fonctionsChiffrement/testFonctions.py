import fonctions as f
def test_hashing():
    message = "hello"
    hash_m = f.hashing(message)

    assert hash_m == "-1267296259"
    assert f.hashing("hello") == "-1267296259"

def test_tlv():
    type = "0x01"
    message = "hello"

    _tlv = f.tlv(type, message)
    #print(_tlv)
    parts = _tlv.split("|")
    assert parts[0] == type
    assert int(parts[1]) == len(parts[2])

    p = parts[2].split(":")

    condition1 = False
    if p[0].isdigit():
        condition1 = True
    assert condition1 == True

    condition2 = False
    if isinstance(p[1], str):
        condition2 = True
    assert condition2 == True

def test_vigenere():
    key = "keyword"
    message = "hello"
    vig_m = f.vigenere(message, key, decryption=False)
    des_vig = f.vigenere(vig_m, key, decryption=True)

    assert vig_m == "xopni"
    assert des_vig == message

test_hashing()
test_tlv()
test_vigenere()