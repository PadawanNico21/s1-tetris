"""
Générateur de polynominos de taille n
"""

import matrice
import piece


def generer_positions(taille):
    """
    Genère les set de positions de toutes les pièces de taille taille
    """
    return generer_positions_rec(taille, set([(0, 0)]))


def generer_positions_rec(taille, piece):
    """
    Genère les set de positions de toutes les pièces de taille taille
    """
    if len(piece) >= taille:
        return set([frozenset(piece)])
    pieces = set()
    for x, y in piece:
        if x > 0 and (x - 1, y) not in piece:
            nouvelle_piece = set(piece)
            nouvelle_piece.add((x - 1, y))
            pieces |= generer_positions_rec(taille, nouvelle_piece)

        if x < taille - 1 and (x + 1, y) not in piece:
            nouvelle_piece = set(piece)
            nouvelle_piece.add((x + 1, y))
            pieces |= generer_positions_rec(taille, nouvelle_piece)

        if y > 0 and (x, y - 1) not in piece:
            nouvelle_piece = set(piece)
            nouvelle_piece.add((x, y - 1))
            pieces |= generer_positions_rec(taille, nouvelle_piece)

        if y < taille - 1 and (x, y + 1) not in piece:
            nouvelle_piece = set(piece)
            nouvelle_piece.add((x, y + 1))
            pieces |= generer_positions_rec(taille, nouvelle_piece)

    return pieces


def positions_vers_formes(positions):
    """
    Convertis le set de positions
    """
    max_x = max(positions, key=lambda t: t[0])[0]
    max_y = max(positions, key=lambda t: t[1])[1]

    forme = matrice.creer_matrice(max_x + 1, max_y + 1, 0)

    for x, y in positions:
        forme[x][y] = 1

    formes = set()
    for _ in range(4):
        formes.add(tuple([tuple(ligne) for ligne in forme]))
        forme = matrice.rotation_droite(forme)

    return frozenset(formes)


def generer_polynominos(taille):
    """
    Génère les polynominos de taille <= taille
    """
    polynominos_toute_rotation = set()
    for i in range(1, taille + 1):
        positions = generer_positions(i)
        for position in positions:
            polynominos_toute_rotation.add(positions_vers_formes(position))
    polynominos = []
    for poly in polynominos_toute_rotation:
        forme = list(poly)[0]
        forme_mut = [list(ligne) for ligne in forme]
        matrice.rendre_matrice_carree(forme_mut, max(len(forme_mut), len(forme_mut[0])))

        polynominos.append(forme_mut)
    return polynominos
