README - baby_code.py

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

##################
# Micro Enfant   #
##################

1. La classe **DigitalWallet** est utilisée pour la fonctionnalité 7 : l'envoi de bitcoins
du Parent vers l'Enfant. Ses méthodes permettent à l'Enfant de recevoir un montant et de l'en
retirer pour lui-même.

2. La fonction **show_image()** affiche sur les LEDs l'image initiale correspondant à l'Enfant : la lettre "E".

3. La fonction **check_agitation()** est utilisée dans la fonctionnalité 3. Elle utilise
l'accéléromètre du micro:bit et, en fonction de la force de l'agitation, elle retourne un type
d'agitation. Si la valeur retournée est "agitation élevée", une notification sera automatiquement
envoyée au Parent.

4. La fonction **get_temperature()** est utilisée dans la fonctionnalité 2, où le Parent demande
à l'Enfant quelle est sa température.

5. La fonction **show_milk()** affiche sur les LEDs la quantité de lait consommée par l'Enfant
jusqu'à ce moment.

6. Nous calibrons la boussole du micro:bit pour l'utiliser dans la fonctionnalité 6, où le Parent
suit l'orientation de l'Enfant.

7. Dans la boucle de communication, il y a trois options pour l'Enfant :
    - Soit il envoie des notifications automatiques au Parent, par exemple lorsqu'il est très
    agité ou en chute libre ;

    - Soit il réagit aux messages envoyés par le Parent via radio
    (ce qui englobe un total de 7 possibilités) ;

    - Soit il affiche sur les LEDs la quantité de lait consommée, si le bouton A est pressé ;
    sa température, si le bouton B est pressé ; la valorisation de ses investissements,
    si le logo est pressé.






