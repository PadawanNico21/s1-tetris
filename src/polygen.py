"""
Générateur de polynominos de taille n
"""

import matrice


def generer(taille):
    piece = matrice.creer_matrice(taille, taille, 0)
