"""
Fonctions pour la manipulation des matrices
"""


def rotation_droite(matrice):
    """
    Renvoie une nouvelle matrice tournée de 90° vers la droite
    """
    hauteur = len(matrice)
    largeur = len(matrice[0])

    nouvelle_matrice = []
    for i in range(largeur):
        ligne = []
        for j in range(hauteur):
            ligne.append(matrice[hauteur - j - 1][i])
        nouvelle_matrice.append(ligne)
    return nouvelle_matrice


def rotation_gauche(matrice):
    """
    Renvoie une nouvelle matrice tournée de 90° vers la gauche
    """
    hauteur = len(matrice)
    largeur = len(matrice[0])

    nouvelle_matrice = []
    for i in range(largeur):
        ligne = []
        for j in range(hauteur):
            ligne.append(matrice[j][largeur - i - 1])
        nouvelle_matrice.append(ligne)
    return nouvelle_matrice


def decalage_bas(matrice, a, b, remplace_par=None):
    """
    Decale les lignes comprise entre a et b de 1 rang vers le bas.
    """
    lignes = []

    for i in range(len(matrice)):
        if len(lignes) >= len(matrice):
            # La nouvelle matrice ne doit pas être plus grande
            break
        if i < a:
            lignes.append(matrice[i])
            continue
        if i == b:
            continue
        if i > b:
            lignes.append(matrice[i])
            continue

        if i == a:
            lignes.append([remplace_par] * len(matrice[i]))
        if i >= a:
            lignes.append(matrice[i])

    return lignes


def rendre_matrice_carree(matrice, cote):
    """
    Prend une matrice en entrée en transforme la pour quelle devienne
    carrée de cote 'cote'
    """
    for x in range(cote):
        if x >= len(matrice):
            matrice.append([0] * cote)
            continue
        for y in range(cote):
            if y >= len(matrice[x]):
                matrice[x].append(0)


def cloner_matrice(matrice):
    """
    Renvoie une matrice identique mais dissociée au niveau des modifications
    """
    matrice_indep = []
    for ligne in matrice:
        matrice_indep.append(list(ligne))

    return matrice_indep


def creer_matrice(lignes, colonnes, valeur):
    """
    Créer une matrice de dimension lignes et colonnes
    """
    matrice = []
    for _ in range(lignes):
        matrice.append([valeur] * colonnes)
    return matrice
