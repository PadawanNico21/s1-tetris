"""
Permet de lire et d'écrire dans un fichier de forme
"""

import pathlib
import matrice
from piece import affiche_forme_debug
import constantes


def fichier_existe(chemin):
    """
    Renvoie True si le fichier 'chemin' existe
    """
    return pathlib.Path(chemin).exists()


def lire_fichier(chemin):
    """
    Lis le fichier en fonction du chemin passé en paramètre
    """
    return pathlib.Path(chemin).read_text("utf-8")


def ecrire_fichier(chemin, contenu):
    """
    Ecris dans le fichier
    ! Attention: cette fonction écrase le contenu présent
    """
    pathlib.Path(chemin).write_text(contenu, "utf-8")


def est_ligne_commentaire(ligne):
    """
    Renvoie True si la ligne commence par un #
    """
    return ligne.startswith("#")


def est_ligne_vide(ligne):
    """
    Renvoie True si la ligne est vide ou ne contient que des espaces
    """
    if len(ligne) == 0:
        return True

    for c in ligne:
        if c not in [" ", "\t", "\r"]:
            return False
    return True


def ligne_vers_tableau(ligne):
    """
    Transforme une ligne du fichier de forme
    en ligne de 0 et de 1
    """
    sortie = []
    for char in ligne:
        if char == " ":
            sortie.append(0)
        else:
            sortie.append(1)
    return sortie


def extraire_pieces(contenu):
    """
    Extrait les formes du contenu et les renvoie
    """
    pieces = []

    lignes = contenu.splitlines()
    i = 0
    while i < len(lignes):
        piece = []
        largeur = 0
        hauteur = 0
        while i < len(lignes) and not est_ligne_vide(lignes[i]):
            ligne = lignes[i]
            if est_ligne_commentaire(ligne):
                i += 1
                continue

            longueur_ligne = len(ligne)
            hauteur += 1
            if longueur_ligne > largeur:
                largeur = longueur_ligne

            piece.append(ligne_vers_tableau(ligne))
            i += 1
        cote = hauteur
        if largeur > hauteur:
            cote = largeur

        matrice.rendre_matrice_carree(piece, cote)

        if len(piece) > 0:
            pieces.append(piece)

        i += 1

    return pieces


def generer_contenu_fichier_forme(formes):
    """
    Génere le contenu d'un fichier forme
    """

    contenu = "# Fichier généré automatiquement\n"
    for forme in formes:
        contenu += "\n"
        for ligne in forme:
            for c in ligne:
                if c:
                    contenu += "+"
                else:
                    contenu += " "
            contenu += "\n"
    return contenu


def afficher_pieces_disponibles(formes, couleurs):
    """
    Affiche les pièces qui seront utilisée lors du jeu
    dans le terminal
    """
    i = 0

    print("Les pièces utilisées seront: ")

    for piece in formes:
        couleur_piece = couleurs[i]
        i = (i + 1) % len(couleurs)
        piece_toutes_rotations = []

        for l in piece:
            piece_toutes_rotations.append(list(l))

        piece_tournee = piece

        for _ in range(3):
            piece_tournee = matrice.rotation_droite(piece_tournee)
            for j in range(len(piece_tournee)):
                piece_toutes_rotations[j].append(0)
                piece_toutes_rotations[j].extend(piece_tournee[j])

        affiche_forme_debug(piece_toutes_rotations, couleur_piece, False)


def forme_init():
    """
    Tente de lire le fichier FICHIER_PIECE si il n'existe pas utilise les formes de bases
    """
    if fichier_existe(constantes.FICHIER_PIECE):
        formes = extraire_pieces(lire_fichier(constantes.FICHIER_PIECE))
        afficher_pieces_disponibles(formes, constantes.COULEURS_TERMINAL)

        return formes

    contenu = generer_contenu_fichier_forme(constantes.FORMES_BASE)
    ecrire_fichier(constantes.FICHIER_PIECE, contenu)

    afficher_pieces_disponibles(constantes.FORMES_BASE, constantes.COULEURS_TERMINAL)

    return constantes.FORMES_BASE
