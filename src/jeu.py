"""
Fonctions pour la partie jeu
"""

import random
import constantes
import modeles
import piece


def calculer_score_ajout(nb_lignes):
    """
    Renvoie le score a ajouter
    """
    if nb_lignes == 1:
        return 40
    if nb_lignes == 2:
        return 100
    if nb_lignes == 3:
        return 300
    if nb_lignes >= 4:
        return 500
    return 0


def calcul_difficulte(nb_lignes):
    """
    Renvoie un delais en fonction du nombre de ligne supprimées
    """
    return 0.2 - 0.05 * (nb_lignes // 10)


def lister_lignes_remplies(jeu, piece_active):
    """
    Renvoie la position y de toutes les lignes remplies.
    """

    lignes_remplies = []
    for i in range(len(jeu)):
        remplie = True
        for j in range(len(jeu[0])):
            if jeu[i][j] == -1 or jeu[i][j] == piece_active:
                remplie = False
                break
        if remplie:
            lignes_remplies.append(i)

    return lignes_remplies


def est_fin_jeu(jeu, pieces):
    """
    Vérifie si il est possible d'ajouter une nouvelle pièce sur le
    plateau de jeu
    """
    for i in range(2):
        for j in range(len(jeu[0])):
            if jeu[i][j] != -1:
                p = modeles.chercher_piece_par_id(pieces, jeu[i][j])
                if piece.est_piece_au_sol(jeu, p):
                    return True
    return False


def choisir_piece(formes):
    """
    Choisi une forme et couleur au hasard
    et créer une pièce
    """
    forme = random.choice(formes)
    couleur = random.choice(constantes.COULEURS)

    return modeles.creer_piece(forme, couleur)


def injecter_choisir_piece(formes):
    """
    Renvoie une fonction ne prenant aucun paramètre
    et choisi une pièce au hasar (même comportement que choisir_piece)
    """

    def choisir_piece_sans_arg():
        return choisir_piece(formes)

    return choisir_piece_sans_arg


# Partie debug
# Ces fonctions ne sont pas utilisé dans le jeu mais sont utiles en cas de problèmes


def generateur_couleur(i):
    """
    Tente de générer une couleur unique pour chaque identifiant
    """
    return f"\x1B[48;2;{(i*10)%255};{((i+5)*10)%255};{(i+10)%255}m"


def affichage_constant(chaine, taille):
    """
    Renvoie une chaine de caractère prefixé d'un certain nombre
    d'espace pour que la taille de la chaine corresponde à la taille
    passée en paramètre
    """
    return " " * (taille - len(chaine)) + chaine


def jeu_debug(plateau, surbrillance=None):
    """
    Affiche le plateau de jeu dans la console
    """
    print("Plateau de jeu:")
    for i in range(len(plateau)):
        ligne = plateau[i]
        for id in ligne:
            if i == surbrillance:
                print("\x1B[7m", end="")
            if id == -1:
                print("░░", end="")
            else:
                print(
                    generateur_couleur(id)
                    + affichage_constant(str(id % 100), 2)
                    + "\x1B[0m",
                    end="",
                )
        print("\x1B[0m")
    print("")
