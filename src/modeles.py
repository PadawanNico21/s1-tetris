"""
Fonctions facilitant la manipulation des tuples
"""

import matrice
import time
import constantes
from jeu import calculer_score_ajout

dernier_identifiant = 0


def generer_identifiant():
    """
    Créer un identifiant unique
    """
    global dernier_identifiant
    dernier_identifiant += 1
    return dernier_identifiant


def definir_dernier_identifiant(id):
    """
    Definis l'identifiant
    """
    global dernier_identifiant
    dernier_identifiant = id


def creer_vecteur(x, y):
    """
    Créer un vecteur
    (une liste avec deux éléments)
    """
    return [x, y]


def modifier_vecteur(vecteur, x, y):
    """
    Ecrase les valeurs du vecteur passé en paramètres
    """
    vecteur[0] = x
    vecteur[1] = y


def ajouter_vecteur(vecteur_a, vecteur_b):
    """
    Ajoute les valeurs du vecteur_b au vecteur_a
    """
    vecteur_a[0] += vecteur_b[0]
    vecteur_a[1] += vecteur_b[1]


def creer_piece(forme, couleur):
    """
    Creer une piece

    `0` identifiant
    `1` forme de la pièce
    `2` couleur de la pièce
    `3` position de la pièce
    """
    return (
        generer_identifiant(),
        matrice.cloner_matrice(forme),
        couleur,
        creer_vecteur(0, 0),
    )


def cloner_piece(piece):
    """
    Clone une pièce
    """
    return [piece[0], matrice.cloner_matrice(piece[1]), piece[2], list(piece[3])]


def forme_piece(piece):
    """
    Renvoie la forme de la pièce
    """
    return piece[1]


def modifier_forme_piece(piece, forme):
    """
    Modifie la forme de la pièce
    """
    piece[1][:] = forme


def couleur_piece(piece):
    """
    Renvoie la couleur de la pièce
    """
    return piece[2]


def position_piece(piece):
    """
    Renvoie la position de la pièce
    """
    return piece[3]


def chercher_piece_par_id(pieces, id):
    """
    Cherche la pièce qui a le même identifiant dans pieces
    """
    for piece in pieces:
        if identifier(piece) == id:
            return piece


def creer_plateau_jeu(hauteur, largeur):
    """
    Créer un plateau de jeu
    """
    plateau = []
    for _ in range(hauteur):
        ligne = []
        for _ in range(largeur):
            ligne.append(-1)
        plateau.append(ligne)
    return plateau


def identifier(identifiable):
    """
    Renvoie l'identifiant d'une pièce
    """
    return identifiable[0]


def creer_etat_jeu(plateau, generateur_piece):
    """
    Renvoie un tableau contenant l'état du jeu
    `0` -> Temps de la dernière action
    `1` -> Plateau de jeu
    `2` -> Piece active
    `3` -> Prochaine piece
    `4` -> Pieces sur le plateau de jeu
    `5` -> Score
    `6` -> Difficulte
    `7` -> Niveau
    `8` -> Progression Niveau

    """
    piece_active = generateur_piece()

    forme = forme_piece(piece_active)
    largeur = len(plateau[0]) // 2 - len(forme[0]) // 2
    position_piece(piece_active)[0] = largeur

    return [0, plateau, piece_active, generateur_piece(), [piece_active], 0, 0, 0, 0]


def mise_a_jour_action(etat_jeu):
    """
    Met le temps de la dernière action à maintenant
    """
    etat_jeu[0] = time.time()


def peut_faire_action(etat_jeu):
    """
    Renvoie un booleen si l'action peut être réalisé
    """
    return time.time() - etat_jeu[0] > constantes.DELAIS_ACTIONS


def obtenir_plateau_jeu(etat_jeu):
    """
    Renvoie le plateau de jeu
    """
    return etat_jeu[1]


def obtenir_piece_active(etat_jeu):
    """
    Renvoie la pièce actuellement controllé par le joueur
    """
    return etat_jeu[2]


def piece_suivante(etat_jeu, generateur_piece):
    """
    Change la pièce actuellement controllé par le joueur
    """
    piece = etat_jeu[3]
    etat_jeu[2] = piece
    etat_jeu[3] = generateur_piece()
    etat_jeu[4].append(piece)

    return piece


def prochaine_piece(etat_jeu):
    """
    Renvoie la prochaine piece qui seras joué
    """
    return etat_jeu[3]


def pieces_sur_jeu(etat_jeu):
    """
    Renvoie les pièces présente sur le plateau de jeu
    """
    return etat_jeu[4]


def obtenir_score(etat_jeu):
    """
    Renvoie le score
    """
    return etat_jeu[5]


def ajout_score_a_partir_de_nb_ligne(etat_jeu, nb_lignes):
    """
    Ajoute le score en fonction du nombre de lignes remplies
    """
    if nb_lignes == 0:
        return
    etat_jeu[5] += int(
        calculer_score_ajout(nb_lignes) * (1 + obtenir_niveau(etat_jeu) / 10)
    )


def obtenir_difficulte(etat_jeu):
    """
    Renvoie la difficulté actuelle
    """
    return etat_jeu[6]


def ajouter_difficulte(etat_jeu, difficulte):
    """
    Ajout à la difficulté la valeur passé en paramètre
    """
    etat_jeu[6] += difficulte


def obtenir_niveau(etat_jeu):
    """
    Renvoie le niveau actuel
    """
    return etat_jeu[7]


def definir_niveau(etat_jeu, niveau):
    """
    Change le niveau actuel
    """
    etat_jeu[7] = niveau


def ajouter_niveau(etat_jeu):
    etat_jeu[7] += 1


def obtenir_progression_niveau(etat_jeu):
    """
    Renvoie la progression du niveau
    """
    return etat_jeu[8]


def avancer_progression_niveau(etat_jeu):
    """
    Ajoute 1 à la progression du niveau
    """
    etat_jeu[8] += 1


def reset_progression_niveau(etat_jeu):
    """
    Met à 0 la progression du niveau
    """
    etat_jeu[8] = 0


def cloner_etat(etat):
    """
    Clone l'état du jeu
    """

    return [
        etat[0],
        matrice.cloner_matrice(etat[1]),
        cloner_piece(etat[2]),
        cloner_piece(etat[3]),
        [cloner_piece(piece) for piece in etat[4]],
        etat[5],
        etat[6],
        etat[7],
        etat[8],
    ]


def creer_bouton(x, y, w, h, texte, couleur_bouton, couleur_texte):
    """
    Créer un bouton
    `0` -> (x, y)
    `1` -> (largeur, hauteur)
    `2` -> texte
    `3` -> couleur bouton
    `4` -> couleur texte
    """
    return ((x, y), (w, h), texte, couleur_bouton, couleur_texte)


def position_bouton(bouton):
    """
    Renvoie la position du bouton
    """
    return bouton[0]


def taille_bouton(bouton):
    """
    Renvoie les dimensions du boutons
    """
    return bouton[1]


def texte_bouton(bouton):
    """
    Renvoie le texte du bouton
    """
    return bouton[2]


def couleur_bouton(bouton):
    """
    Renvoie la couleur d'arrière plan du bouton
    """
    return bouton[3]


def couleur_texte_bouton(bouton):
    """
    Renvoie la couleur du bouton
    """
    return bouton[4]
