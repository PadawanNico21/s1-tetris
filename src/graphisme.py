"""
Fonctions pour la partie graphique
"""

import fltk
import constantes
import modeles


def dessiner_grille(lignes, colonnes, decalage_x, decalage_y):
    """
    Dessine la grille du tetris
    """
    largeur = colonnes * constantes.COTE_PIXEL_PIECE
    hauteur = lignes * constantes.COTE_PIXEL_PIECE

    for i in range(colonnes + 1):
        y = i * constantes.COTE_PIXEL_PIECE + decalage_x
        fltk.ligne(y, decalage_y, y, hauteur + decalage_y, "grey")
    for i in range(lignes + 1):
        y = i * constantes.COTE_PIXEL_PIECE + decalage_y
        fltk.ligne(decalage_x, y, largeur + decalage_x, y, "grey")


def dessiner_plateau(jeu, pieces, offset=0):
    """
    Dessine les pièces présent sur la grille
    """
    dx = 100 + offset
    dy = 100
    dessiner_grille(len(jeu), len(jeu[0]), dx, dy)

    for i in range(len(jeu)):
        for j in range(len(jeu[0])):
            if jeu[i][j] != -1:
                piece = modeles.chercher_piece_par_id(pieces, jeu[i][j])
                couleur = modeles.couleur_piece(piece)

                fltk.rectangle(
                    dx + j * constantes.COTE_PIXEL_PIECE,
                    dy + i * constantes.COTE_PIXEL_PIECE,
                    dx + (j + 1) * constantes.COTE_PIXEL_PIECE,
                    dy + (i + 1) * constantes.COTE_PIXEL_PIECE,
                    None,
                    couleur,
                )


def afficher_score(score, decalage_x):
    """
    Dessine le score
    """
    fltk.rectangle(400 + decalage_x, 210, 500 + decalage_x, 280, "white")
    fltk.texte(410 + decalage_x, 220, "Score:", "white", "nw", "Arial", 16)
    fltk.texte(490 + decalage_x, 250, str(score), "white", "ne", "Arial", 14)


def afficher_niveau(niveau, decalage_x):
    """
    Dessine le niveau
    """
    fltk.rectangle(400 + decalage_x, 290, 500 + decalage_x, 360, "white")
    fltk.texte(450 + decalage_x, 310, "Niveau", "white", "center", "Arial", 16)
    fltk.texte(450 + decalage_x, 340, str(niveau), "white", "center", "Arial", 14)


def dessiner_prochaine_piece(piece, decalage_x):
    """
    Dessine la prochaine pièce
    """
    couleur = modeles.couleur_piece(piece)
    forme = modeles.forme_piece(piece)
    cote = 100 / (len(forme) + 2)
    dx = 400 + cote + decalage_x
    dy = 100 + cote

    fltk.rectangle(400 + decalage_x, 100, 500 + decalage_x, 200, "white")
    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if not forme[i][j]:
                continue
            fltk.rectangle(
                dx + j * cote,
                dy + i * cote,
                dx + (j + 1) * cote,
                dy + (i + 1) * cote,
                None,
                couleur,
            )
