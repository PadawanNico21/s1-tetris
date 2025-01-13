"""
Fonctions pour la partie jeu
"""

import random
import constantes
import modeles
import piece
import matrice


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


def id_piece_meme_couleur(piece, id_piece, pieces):
    """
    Renvoie True si la piece piece a la même couleur que la piece ayant pour identifiant id_piece
    """
    autre_piece = modeles.chercher_piece_par_id(pieces, id_piece)
    return autre_piece != None and modeles.couleur_piece(
        piece
    ) == modeles.couleur_piece(autre_piece)


def detection_couleur_adjacente(jeu, piece, pieces):
    """
    Renvoie un dictionnaire des pièces de même couleur qui touchent la piece 'piece' avec le nombre de côtés touchés
    """
    x, y = modeles.position_piece(piece)
    forme = modeles.forme_piece(piece)
    resultat = {}
    for i in range(len(forme)):
        for j in range(len(forme[0])):
            if not forme[i][j]:
                continue
            if (i <= 0 or not forme[i - 1][j]) and i + y > 0:
                id_piece_touche = jeu[y + i - 1][x + j]
                if id_piece_touche != -1 and id_piece_meme_couleur(
                    piece, id_piece_touche, pieces
                ):
                    if id_piece_touche not in resultat:
                        resultat[id_piece_touche] = 0
                    resultat[id_piece_touche] += 1
            if (i >= len(forme) - 1 or not forme[i + 1][j]) and i + y < len(jeu) - 1:
                id_piece_touche = jeu[y + i + 1][x + j]
                if id_piece_touche != -1 and id_piece_meme_couleur(
                    piece, id_piece_touche, pieces
                ):
                    if id_piece_touche not in resultat:
                        resultat[id_piece_touche] = 0
                    resultat[id_piece_touche] += 1
            if (j <= 0 or not forme[i][j - 1]) and j + x > 0:
                id_piece_touche = jeu[y + i][x + j - 1]
                if id_piece_touche != -1 and id_piece_meme_couleur(
                    piece, id_piece_touche, pieces
                ):
                    if id_piece_touche not in resultat:
                        resultat[id_piece_touche] = 0
                    resultat[id_piece_touche] += 1
            if (j >= len(forme[0]) - 1 or not forme[i][j + 1]) and j + x < len(
                jeu[0]
            ) - 1:
                id_piece_touche = jeu[y + i][x + j + 1]
                if id_piece_touche != -1 and id_piece_meme_couleur(
                    piece, id_piece_touche, pieces
                ):
                    if id_piece_touche not in resultat:
                        resultat[id_piece_touche] = 0
                    resultat[id_piece_touche] += 1
    return resultat


def fusion_pieces_par_couleur(jeu, pieces, piece_active):
    """
    Fusionne et supprime les pieces en fonction de leurs couleurs
    Logique du mode couleur adjacente
    """
    suppressions = set()

    for p in pieces:
        if p == piece_active:
            continue
        a_fusionner = detection_couleur_adjacente(jeu, p, pieces)

        # On trie par ordre de priorité: plus 2 pièces se touchent plus on va les process en premier
        ordre = sorted(a_fusionner.items(), key=lambda p: p[1])
        for id_fusion, cote_touche in ordre:
            if id_fusion == modeles.identifier(piece_active):
                continue
            if cote_touche >= 2:
                suppressions.add(pieces.index(p))
                suppressions.add(
                    pieces.index(modeles.chercher_piece_par_id(pieces, id_fusion))
                )
                continue
            piece_a = p
            piece_b = modeles.chercher_piece_par_id(pieces, id_fusion)
            nouvelle_piece = fusionner_piece(piece_a, piece_b)
            pieces.pop(pieces.index(piece_a))
            pieces.pop(pieces.index(piece_b))
            pieces.append(nouvelle_piece)
    # On réalise les suppressions a la fin car il y'a des cas ou une pièce peut toucher sur 2 côtés deux pièces de même couleur en même temps
    nouvelle_pieces = []
    blocks_supprimes = 0
    for i in range(len(pieces)):
        if i in suppressions:
            forme = modeles.forme_piece(pieces[i])
            blocks_supprimes += sum([sum(ligne) for ligne in forme])
            continue
        nouvelle_pieces.append(pieces[i])
    pieces[:] = nouvelle_pieces

    plateau = modeles.creer_plateau_jeu(len(jeu), len(jeu[0]))
    for p in pieces:
        piece.deplacer_piece(plateau, p, modeles.creer_vecteur(0, 0))
    jeu[:] = plateau
    return blocks_supprimes


def fusionner_piece(piece_a, piece_b):
    """
    Créer une nouvelle pièce avec la même couleur et une nouvelle forme fusionnée.
    """
    forme_a = modeles.forme_piece(piece_a)
    x_a, y_a = modeles.position_piece(piece_a)
    forme_b = modeles.forme_piece(piece_b)
    x_b, y_b = modeles.position_piece(piece_b)
    nouvelle_position = (min(x_a, x_b), min(y_a, y_b))

    pos_fin_x_a = len(forme_a[0]) + x_a
    pos_fin_y_a = len(forme_a) + y_a

    pos_fin_x_b = len(forme_b[0]) + x_b
    pos_fin_y_b = len(forme_b) + y_b

    pos_fin_x = max(pos_fin_x_a, pos_fin_x_b)
    pos_fin_y = max(pos_fin_y_a, pos_fin_y_b)

    largeur_matrice = pos_fin_x - nouvelle_position[0]
    hauteur_matrice = pos_fin_y - nouvelle_position[1]

    nouvelle_forme = matrice.creer_matrice(hauteur_matrice, largeur_matrice, 0)

    for i in range(len(forme_a)):
        for j in range(len(forme_a[0])):
            nouvelle_forme[i + y_a - nouvelle_position[1]][
                j + x_a - nouvelle_position[0]
            ] |= forme_a[i][j]
    for i in range(len(forme_b)):
        for j in range(len(forme_b[0])):
            nouvelle_forme[i + y_b - nouvelle_position[1]][
                j + x_b - nouvelle_position[0]
            ] |= forme_b[i][j]

    nouvelle_piece = modeles.creer_piece(nouvelle_forme, modeles.couleur_piece(piece_a))
    position = modeles.position_piece(nouvelle_piece)
    modeles.modifier_vecteur(position, nouvelle_position[0], nouvelle_position[1])
    return nouvelle_piece


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
