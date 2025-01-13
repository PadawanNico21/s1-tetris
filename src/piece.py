"""
Toutes les fonctions permettant de manipuler les pièces
"""

import modeles
import matrice


def deplacer_piece(jeu, piece, vecteur_deplacement):
    """
    Deplace la piece sur le plateau de jeu
    """
    position = modeles.position_piece(piece)
    forme = modeles.forme_piece(piece)
    identifiant = modeles.identifier(piece)

    x, y = position
    dx, dy = vecteur_deplacement

    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if forme[i][j]:
                jeu[i + y][j + x] = -1

    # Todo améliorer le systeme de nettoyage pour éviter la répétition de code.

    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if forme[i][j]:
                jeu[i + y + dy][j + x + dx] = identifiant

    modeles.ajouter_vecteur(position, vecteur_deplacement)


def rotation_piece(jeu, piece, sens):
    """
    Tourne la pièce
    """
    identifiant = modeles.identifier(piece)
    x, y = modeles.position_piece(piece)
    forme = modeles.forme_piece(piece)
    forme_tournee = None
    if sens == "droite":
        forme_tournee = matrice.rotation_droite(forme)
    else:
        forme_tournee = matrice.rotation_gauche(forme)

    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if forme_tournee[i][j] and not forme[i][j]:
                jeu[i + y][j + x] = identifiant
            elif not forme_tournee[i][j] and forme[i][j]:
                jeu[i + y][j + x] = -1

    modeles.modifier_forme_piece(piece, forme_tournee)


def tomber_piece(jeu, piece):
    """
    Fait desendre la pièce du maximum quelle peut.
    """
    while not est_piece_au_sol(jeu, piece):
        deplacer_piece(jeu, piece, modeles.creer_vecteur(0, 1))


def est_piece_au_sol(jeu, piece):
    """
    Vérifie si la pièce passée en paramètre est au sol
    """
    identifiant = modeles.identifier(piece)
    x, y = modeles.position_piece(piece)
    forme = modeles.forme_piece(piece)

    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if forme[i][j] and (
                y + i + 1 >= len(jeu)
                or (jeu[y + i + 1][x + j] not in [-1, identifiant])
            ):
                return True
    return False


def est_rotation_piece_valide(jeu, piece, sens):
    """
    Vérifie que la pièce a la place pour la rotation demandée
    """
    identifiant = modeles.identifier(piece)
    x, y = modeles.position_piece(piece)
    forme = modeles.forme_piece(piece)
    forme_tournee = None
    if sens == "droite":
        forme_tournee = matrice.rotation_droite(forme)
    else:
        forme_tournee = matrice.rotation_gauche(forme)

    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if forme_tournee[i][j]:
                pos_x = j + x
                pos_y = i + y
                if pos_x < 0 or pos_y < 0 or pos_y >= len(jeu) or pos_x >= len(jeu[0]):
                    return False
                if jeu[pos_y][pos_x] != -1 and jeu[pos_y][pos_x] != identifiant:
                    return False

    return True


def est_deplacement_piece_valide(jeu, piece, vecteur_deplacement):
    """
    Renvoie True si le déplacement de la pièce est contenu dans le plateau
    et n'écrase pas une autre pièce
    """
    identifiant = modeles.identifier(piece)
    x, y = modeles.position_piece(piece)
    forme = modeles.forme_piece(piece)
    vx, vy = vecteur_deplacement

    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if forme[i][j]:
                pos_x = j + x + vx
                pos_y = i + y + vy
                if pos_x < 0 or pos_y < 0 or pos_y >= len(jeu) or pos_x >= len(jeu[0]):
                    return False
                if jeu[pos_y][pos_x] != -1 and jeu[pos_y][pos_x] != identifiant:
                    return False

    return True


def deplacement_piece_si_valide(jeu, piece, vecteur_deplacement):
    """
    Renvoie True si le deplacement par vecteur_deplacement de la piece est valide
    """
    if est_deplacement_piece_valide(jeu, piece, vecteur_deplacement):
        deplacer_piece(jeu, piece, vecteur_deplacement)
        return True
    return False


def rotation_piece_si_valide(jeu, piece, sens):
    """
    Renvoie True si la rotation dans le sens sens de la piece est valide
    """
    if est_rotation_piece_valide(jeu, piece, sens):
        rotation_piece(jeu, piece, sens)
        return True
    return False


def est_piece_vide(piece):
    """
    Renvoie True si la forme de la pièce ne contient que des 0
    """
    forme = modeles.forme_piece(piece)
    for ligne in forme:
        if 1 in ligne:
            return False
    return True


def nettoyage_pieces_vides(pieces):
    """
    Supprime toutes les pièce vides
    """
    pieces_non_vide = []
    for piece in pieces:
        if not est_piece_vide(piece):
            pieces_non_vide.append(piece)
    pieces[:] = pieces_non_vide


def detruire_ligne(jeu, pieces, ligne):
    """
    Cette fonction supprime la ligne passée en paramètre
    et propage les modifications sur les pièce affectée
    """
    piece_dans_ligne = []
    piece_dessus_ligne = []

    # Filtre les pièces en 2 catégories:
    # - Celles qui sont concernées par la ligne à supprimée
    # - Celles qui sont au dessus
    for piece in pieces:
        id_piece = modeles.identifier(piece)
        position = modeles.position_piece(piece)
        forme = modeles.forme_piece(piece)

        if (
            id_piece in jeu[ligne]
            or position[1] < ligne
            and ligne < (position[1] + len(forme))
        ):
            piece_dans_ligne.append(piece)
        elif position[1] < ligne:
            piece_dessus_ligne.append(piece)

    # Suppression de la ligne concernée pour les pièces concernées

    for piece in piece_dans_ligne:
        position = modeles.position_piece(piece)
        y = ligne - position[1]
        forme = modeles.forme_piece(piece)
        nouvelle_forme = None

        if y > 0:
            nouvelle_forme = matrice.decalage_bas(forme, 0, y, 0)
        else:
            nouvelle_forme = []
            for i in range(len(forme)):
                if i == 0:
                    nouvelle_forme.append([0] * len(forme[0]))
                else:
                    nouvelle_forme.append(forme[i])

        for j in range(len(nouvelle_forme)):
            if j + position[1] > len(jeu):
                nouvelle_forme[j] = [0] * len(nouvelle_forme)

        modeles.modifier_forme_piece(piece, nouvelle_forme)

    # Décalage des pièces au-dessus de la ligne à supprimée
    for piece in piece_dessus_ligne:
        deplacer_piece(jeu, piece, modeles.creer_vecteur(0, 1))

    nettoyage_pieces_vides(pieces)

    # Regénération du plateau intégral
    # Cela pourras être améliorié dans le futur

    nouv_plat = modeles.creer_plateau_jeu(len(jeu), len(jeu[0]))
    for p in pieces:
        deplacer_piece(nouv_plat, p, modeles.creer_vecteur(0, 0))

    for i in range(len(nouv_plat)):
        jeu[i][:] = nouv_plat[i]


# Partie debug
# Ces fonctions ne sont pas utilisé dans le jeu mais sont utiles en cas de problèmes


def affiche_forme_debug(forme, couleur="\x1B[48;2;255;255;255m", affiche_espaces=False):
    """
    Fonction permettant d'afficher de manière visuelle
    une forme
    """
    for ligne in forme:
        for c in ligne:
            if c:
                print(couleur + "  \x1B[0m", end="")
            elif affiche_espaces:
                print("░░", end="")
            else:
                print("  ", end="")
        print("")
    print("")
