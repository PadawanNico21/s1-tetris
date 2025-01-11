"""
Générateur de polynominos de taille n
"""

import matrice
import piece


def generer_positions(taille):
    return generer_positions_rec(taille, set([(0, 0)]))


def generer_positions_rec(taille, piece):
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
    polynomionos = set()
    for i in range(1, taille + 1):
        positions = generer_positions(i)
        for position in positions:
            polynomionos.add(positions_vers_formes(position))
    return polynomionos


n = 10
print("Polynominos unique de taille <=", n)
for formes in generer_polynominos(n):
    piece.affiche_forme_debug(list(formes)[0], affiche_espaces=True)
