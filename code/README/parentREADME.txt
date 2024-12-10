README - parent_code.py

P.S. : Le code original ne contient pas de commentaires en raison de la capacité mémoire limitée du micro:bit.

####################
# Aspects généraux #
####################

- Tout d'abord, nous avons divisé le code en deux grandes parties. La première correspond à
l'établissement de la connexion entre l'Enfant et le Parent, où se trouve le défi de la cryptographie,
et la deuxième correspond à la séquence de communication entre les deux. Par conséquent, le code contient
deux boucles principales : la boucle "connexion" et la boucle "communication" (ces boucles sont des variables
qui reçoivent une valeur booléenne).

- La fonction **tlv** est implémentée juste entre les fonctions liées à la cryptographie
afin de garantir que celles-ci ne chiffrent et ne déchiffrent que les messages respectant
un certain format.

- La fonction **create_nonce** est une fonction récursive qui génère un nonce. Si le nonce
généré existe déjà, il en génère un nouveau jusqu'à ce qu'il soit unique. Sinon, le nonce est
retourné immédiatement.

################
# Micro Parent #
################

Fonctionnalités :
    (1) Définir une nouvelle dose de lait pour l'Enfant
    (2) Vérifier la température de l'Enfant
    (3) Vérifier l'état d'éveil de l'Enfant + niveau d'agitation actuel + s'il a déjà bu
     la quantité quotidienne de lait prédéfinie : 500 ml)
    (4) Faire dormir l'Enfant
    (5) Parler avec l'Enfant
    (6) Suivre l'orientation de l'Enfant en temps réel
    (7) Effectuer un dépôt de bitcoins sur le compte d'investissement de l'Enfant

Dans la boucle de communication, il existe deux options pour le Parent :
    - Soit il choisit la fonctionnalité qu'il souhaite utiliser en appuyant sur A
    pour ouvrir le menu ;

    - Soit il réagit aux messages reçus de l'Enfant via radio.