#Table de Vigenère
import string
import random as r

#Esta variavel armazena o alfabeto em uma só string = 'abcdefghijklmnopqrstuvwxyz'
alphabet = string.ascii_lowercase

#Esta lista armazena EM ORDEM os dicionários que correspondem à cada coluna da Tabele de Vigenère;
vigenere_table = []

for letter in range(26):  # 26 deslocamentos, incluindo o original
    shifted_alphabet = alphabet[letter:] + alphabet[:letter]  # Realizar o deslocamento
    vigenere_table.append({alphabet[i]: shifted_alphabet[i] for i in range(26)}) # Criar e adicionar o dicionário na lista

#Dicionario onde key=letter e value=number | a:1, b:2, ..., z:26
letter_to_number = {letter: index + 1 for index, letter in enumerate(alphabet)}
#Dicionario onde key=number e value=letter | 1:a, 2:b, ..., 26:z
number_to_letter = {index + 1: letter for index, letter in enumerate(alphabet)}


password = "" #essa variável vai armazenar a nossa senha original
chiffrement = "" #essa variável vai armezenar uma string do mesmo comprimento que a nossa senha;
# ela será usada para gerar as combinações e poder buscar a letra correspondente na Tabela de Vigenère

for _ in range(1, 10):
    number = r.randint(1, 26)
    if number in number_to_letter:
        password += number_to_letter[number] #criação da nossa senha aleatória

for _ in range(1, 10):
    number = r.randint(1, 26)
    if number in number_to_letter:
        chiffrement += number_to_letter[number] #criação do nosso chiffrement aleatorio

result = '' #essa variável vai armazenar o resultado obtido através da Tablea de Viginère
index = 0
while index <= len(password) - 1: #iremos percorrer todos os indices presentes na nossa senha
    letter = password[index]
    letter_chiffree = chiffrement[index]

    number = None
    if letter_chiffree in letter_to_number:
        for key, value in letter_to_number.items():
            if key == letter_chiffree:
                number = value
    def get_decalage(number, liste):
        """
        Retorna o dicionário correspondente ao deslocamento especificado.
        :param number: Número do deslocamento (1 a 26).
        :param liste: Lista contendo os dicionários de deslocamentos.
        :return: O dicionário correspondente ao deslocamento.
        """
        if 1 <= number <= 26:  # Verificar se o número está no intervalo válido
            return liste[number - 1]  # Retornar o dicionário correspondente
        else:
            raise ValueError("O número deve estar entre 1 e 26.")  # Erro para valores fora do intervalo


    line = get_decalage(number, vigenere_table)


    letter_to_add = None
    for key, value in line.items():
        if key == letter:
            letter_to_add = value

    result += letter_to_add
    index += 1

#test
print(password +": password")
print(chiffrement + ": chiffrement")
print("----")
print(result + ": result")