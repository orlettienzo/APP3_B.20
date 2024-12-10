#Ce fichier va contenir les tests de notre programme
import random

def test_nonces(racine):
    pre_condition = False
    if isinstance(racine, int):
        pre_condition = True

    assert pre_condition == True

    random.seed(racine)
    n1 = []
    n2 = []
    for _ in range(20):
        nonce = random.randint(1, 2000)
        n1.append(nonce)
    for _ in range(20):
        nonce = random.randint(2001, 4000)
        n2.append(nonce)

    #1: un element ne peut pas se trouver dans les 2 listes
    condition1 = True
    for element in n1:
        if element in n2:
            condition1 = False

    for element in n2:
        if element in n1:
            condition1 = False

    assert condition1 == True

    #2: un element doit apparaitre seulement une fois dans la liste
    condition2 = True
    new_n1 = []
    new_n2 = []
    while condition2:
        for element in n1:
            if element not in new_n1:
                new_n1.append(element)
            else:
                condition2 = False

        for element in n2:
            if element not in new_n2:
                new_n2.append(element)
            else:
                condition2 = False

        #print(new_n1, len(new_n1))
        #print(new_n2, len(new_n2))
        break

    assert condition2 == True

    #2.1: Donc, new_n1, new_n2 doivent etre egale à n1, n2
    assert new_n1 == n1
    assert new_n2 == n2

test_nonces(42)
