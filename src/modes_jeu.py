"""
Module contenant la logique du jeu solo et duo
"""

import piece
import modeles
import graphisme
import fltk
import time
import jeu
import random
import constantes
import menus


def gravite_joueur(etat, generateur_piece):
    """
    Applique la gravite sur l'etat et créer une nouvelle pièce si nécessaire
    """
    plateau_jeu = modeles.obtenir_plateau_jeu(etat)
    piece_active = modeles.obtenir_piece_active(etat)

    if piece.est_piece_au_sol(plateau_jeu, piece_active):
        nouvelle_piece = modeles.piece_suivante(etat, generateur_piece)
        forme = modeles.forme_piece(nouvelle_piece)
        largeur = len(plateau_jeu[0]) // 2 - len(forme[0]) // 2
        modeles.avancer_progression_niveau(etat)

        if (
            modeles.obtenir_progression_niveau(etat)
            >= constantes.AJOUT_NIVEAU_TOUTES_NB_PIECES
        ):
            modeles.reset_progression_niveau(etat)
            modeles.ajouter_niveau(etat)

        piece.deplacer_piece(
            plateau_jeu, nouvelle_piece, modeles.creer_vecteur(largeur, 0)
        )
        return

    piece.deplacement_piece_si_valide(
        plateau_jeu, piece_active, modeles.creer_vecteur(0, 1)
    )


def deplacements_horizontaux_joueur(etat, touche_r, touche_l):
    """
    Gère les deplacements horizontaux
    """
    plateau_jeu = modeles.obtenir_plateau_jeu(etat)
    piece_active = modeles.obtenir_piece_active(etat)

    if fltk.touche_pressee(touche_r):
        return piece.deplacement_piece_si_valide(
            plateau_jeu, piece_active, modeles.creer_vecteur(1, 0)
        )
    if fltk.touche_pressee(touche_l):
        return piece.deplacement_piece_si_valide(
            plateau_jeu, piece_active, modeles.creer_vecteur(-1, 0)
        )


def rotations_joueur(etat, ev, touche_r, touche_l):
    """
    Gère la rotation
    """
    plateau_jeu = modeles.obtenir_plateau_jeu(etat)
    piece_active = modeles.obtenir_piece_active(etat)

    if fltk.type_ev(ev) == "Touche":
        code = fltk.touche(ev)
        if code == touche_r:
            piece.rotation_piece_si_valide(plateau_jeu, piece_active, "droite")
        if code == touche_l:
            piece.rotation_piece_si_valide(plateau_jeu, piece_active, "gauche")


def gestion_lignes_remplies(etat, adverse):
    """
    Detecte et supprime les lignes complète et ajoute au score
    """
    plateau_jeu = modeles.obtenir_plateau_jeu(etat)
    piece_active = modeles.obtenir_piece_active(etat)
    pieces = modeles.pieces_sur_jeu(etat)

    lignes_remplies = jeu.lister_lignes_remplies(
        plateau_jeu, modeles.identifier(piece_active)
    )
    nb_lignes = len(lignes_remplies)

    modeles.ajout_score_a_partir_de_nb_ligne(etat, nb_lignes)
    modeles.ajouter_difficulte(etat, nb_lignes)

    while len(lignes_remplies) > 0:
        derniere_ligne = lignes_remplies[len(lignes_remplies) - 1]

        piece.detruire_ligne(plateau_jeu, pieces, derniere_ligne)

        lignes_remplies = jeu.lister_lignes_remplies(
            plateau_jeu, modeles.identifier(piece_active)
        )
    if nb_lignes > 0 and adverse is not None:
        ajouter_ligne_joueur(adverse, nb_lignes)


def ajouter_ligne_joueur(etat, nb_lignes):
    """
    (mode duo uniquement)
    Ajoute nb_lignes à l'adversaire
    """
    pieces = modeles.pieces_sur_jeu(etat)
    plateau_jeu = modeles.obtenir_plateau_jeu(etat)
    position_trou = random.randrange(0, len(plateau_jeu[0]))
    forme_piece_chiante = []
    for _ in range(nb_lignes):
        ligne = []
        for i in range(len(plateau_jeu[0])):

            ligne.append(i != position_trou)
        forme_piece_chiante.append(ligne)

    for p in pieces:
        piece.deplacer_piece(plateau_jeu, p, modeles.creer_vecteur(0, -nb_lignes))
    piece_chiante = modeles.creer_piece(forme_piece_chiante, "#888888")
    pieces.append(piece_chiante)
    piece.deplacer_piece(
        plateau_jeu,
        piece_chiante,
        modeles.creer_vecteur(0, len(plateau_jeu) - nb_lignes),
    )

    nouv_plat = modeles.creer_plateau_jeu(len(plateau_jeu), len(plateau_jeu[0]))
    for p in pieces:
        piece.deplacer_piece(nouv_plat, p, modeles.creer_vecteur(0, 0))

    for i in range(len(nouv_plat)):
        plateau_jeu[i][:] = nouv_plat[i]


def dessiner_plateau(etat, decalage):
    """
    Dessine une instance du jeu
    """
    plateau_jeu = modeles.obtenir_plateau_jeu(etat)
    pieces = modeles.pieces_sur_jeu(etat)
    score = modeles.obtenir_score(etat)
    prochaine_piece = modeles.prochaine_piece(etat)
    niveau = modeles.obtenir_niveau(etat)

    graphisme.dessiner_plateau(plateau_jeu, pieces, decalage)
    graphisme.afficher_score(score, decalage)
    graphisme.afficher_niveau(niveau, decalage)
    graphisme.dessiner_prochaine_piece(prochaine_piece, decalage)


def est_perdant(etat):
    """
    Renvoie True si le joueur (etat) est perdant
    """
    return jeu.est_fin_jeu(
        modeles.obtenir_plateau_jeu(etat), modeles.pieces_sur_jeu(etat)
    )


def jouable(etats):
    """
    Renvoie false si l'un des états est perdant
    """
    for etat in etats:
        if est_perdant(etat):
            return False
    return True


def arriere_plan():
    """
    Dessine l'arrière plan du jeu
    """
    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    fltk.rectangle(0, 0, largeur, hauteur, "black", "black")


def mode_couleur_adjacente(etat):
    """
    Logique du mode couleur adjacente lorsqu'il est actif dans l'etat
    """
    if modeles.mode_couleur_adjacente_actif(etat):
        suppressions = jeu.fusion_pieces_par_couleur(
            modeles.obtenir_plateau_jeu(etat),
            modeles.pieces_sur_jeu(etat),
            modeles.obtenir_piece_active(etat),
        )
        modeles.ajouter_score_a_partir_de_suppressions_blocks(etat, suppressions)


def jeu_solo(formes, etats, activer_couleur_adj):
    """
    La logique du jeu pour 1 joueur
    """
    choisir_piece = jeu.injecter_choisir_piece(formes)
    plateau = modeles.creer_plateau_jeu(20, 10)
    etat = modeles.creer_etat_jeu(plateau, choisir_piece)
    if etats is not None:
        etat = etats[0]
    temps = 0

    if activer_couleur_adj:
        modeles.activer_mode_couleur_adjacente(etat)

    while not est_perdant(etat):
        delais = jeu.calcul_difficulte(modeles.obtenir_difficulte(etat))

        if fltk.touche_pressee("Escape"):
            if menus.menu_pause("solo", [etat]):
                return
            temps = time.time()

        if fltk.touche_pressee(constantes.CONTROLES_J1_ACCEL):
            delais /= 3

        if time.time() - temps > delais:
            temps = time.time()
            gravite_joueur(etat, choisir_piece)
            mode_couleur_adjacente(etat)

        if modeles.peut_faire_action(etat):
            deplacements_horizontaux_joueur(
                etat,
                constantes.CONTROLES_J1_DEPLACEMENT_DROIT,
                constantes.CONTROLES_J1_DEPLACEMENT_GAUCHE,
            ) and modeles.mise_a_jour_action(etat)

        ev = fltk.donne_ev()
        rotations_joueur(
            etat,
            ev,
            constantes.CONTROLES_J1_ROTATION_DROITE,
            constantes.CONTROLES_J1_ROTATION_GAUCHE,
        )

        gestion_lignes_remplies(etat, None)

        fltk.efface_tout()
        arriere_plan()

        dessiner_plateau(etat, 0)
        fltk.mise_a_jour()

    fltk.texte(5, 5, "Vous avez perdu.", "red")

    fltk.attend_clic_gauche()


def jeu_duo(formes, etats, activer_couleur_adj):
    """
    La logique du jeu pour 2 joueurs
    """
    choisir_piece = jeu.injecter_choisir_piece(formes)

    plateau_j1 = modeles.creer_plateau_jeu(20, 10)
    plateau_j2 = modeles.creer_plateau_jeu(20, 10)

    etat_j1 = modeles.creer_etat_jeu(plateau_j1, choisir_piece)
    etat_j2 = modeles.creer_etat_jeu(plateau_j2, choisir_piece)
    if etats is not None:
        etat_j1 = etats[0]
        etat_j2 = etats[1]

    if activer_couleur_adj:
        modeles.activer_mode_couleur_adjacente(etat_j1)
        modeles.activer_mode_couleur_adjacente(etat_j2)

    temps_j1 = 0
    temps_j2 = 0

    while jouable([etat_j1, etat_j2]):
        delais_j1 = jeu.calcul_difficulte(modeles.obtenir_difficulte(etat_j1))

        delais_j2 = jeu.calcul_difficulte(modeles.obtenir_difficulte(etat_j2))

        if fltk.touche_pressee("Escape"):
            if menus.menu_pause("duo", [etat_j1, etat_j2]):
                return
            temps_j1 = time.time()
            temps_j2 = time.time()

        if fltk.touche_pressee(constantes.CONTROLES_J1_ACCEL):
            delais_j1 /= 3

        if fltk.touche_pressee(constantes.CONTROLES_J2_ACCEL):
            delais_j2 /= 3

        if time.time() - temps_j1 > delais_j1:
            temps_j1 = time.time()
            gravite_joueur(etat_j1, choisir_piece)
            mode_couleur_adjacente(etat_j1)

        if time.time() - temps_j2 > delais_j2:
            temps_j2 = time.time()
            gravite_joueur(etat_j2, choisir_piece)
            mode_couleur_adjacente(etat_j2)

        if modeles.peut_faire_action(etat_j1):
            deplacements_horizontaux_joueur(
                etat_j1,
                constantes.CONTROLES_J1_DEPLACEMENT_DROIT,
                constantes.CONTROLES_J1_DEPLACEMENT_GAUCHE,
            ) and modeles.mise_a_jour_action(etat_j1)

        if modeles.peut_faire_action(etat_j2):
            deplacements_horizontaux_joueur(
                etat_j2,
                constantes.CONTROLES_J2_DEPLACEMENT_DROIT,
                constantes.CONTROLES_J2_DEPLACEMENT_GAUCHE,
            ) and modeles.mise_a_jour_action(etat_j2)

        ev = fltk.donne_ev()

        rotations_joueur(
            etat_j1,
            ev,
            constantes.CONTROLES_J1_ROTATION_DROITE,
            constantes.CONTROLES_J1_ROTATION_GAUCHE,
        )
        rotations_joueur(
            etat_j2,
            ev,
            constantes.CONTROLES_J2_ROTATION_DROITE,
            constantes.CONTROLES_J2_ROTATION_GAUCHE,
        )

        gestion_lignes_remplies(etat_j1, etat_j2)
        gestion_lignes_remplies(etat_j2, etat_j1)

        fltk.efface_tout()
        arriere_plan()

        dessiner_plateau(etat_j1, -50)
        dessiner_plateau(etat_j2, 400)
        fltk.mise_a_jour()

    if est_perdant(etat_j1):
        fltk.texte(5, 5, "Le joueur 1 a perdu.", "red")
    else:
        fltk.texte(5, 5, "Le joueur 2 a perdu.", "red")
    fltk.attend_clic_gauche()
