import re
mot = "585"
regex = re.compile(r"[0-9]*[a-zA-Z]+[0-9]*")
if regex.match(mot) is not None:
    #Le nombre n'est pas entier
    print ("Vrai")
else:
    #Le nbre est entier
    print ("Faux")