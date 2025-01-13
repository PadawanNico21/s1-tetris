"""
Module contenant les menus
"""

import fltk
import modeles
import sauvegarde
import constantes


def dessiner_bouton(bouton):
    """
    Dessine a bouton à l'écran
    """
    xs = fltk.abscisse_souris()
    ys = fltk.ordonnee_souris()

    x, y = modeles.position_bouton(bouton)
    w, h = modeles.taille_bouton(bouton)
    texte = modeles.texte_bouton(bouton)
    couleur_btn = modeles.couleur_bouton(bouton)
    couleur_texte = modeles.couleur_texte_bouton(bouton)

    if souris_collision(xs, ys, bouton):
        couleur_btn = "#888888"

    dw = w / 2
    dh = h / 2

    objets = []

    objets.append(
        fltk.rectangle(x - dw, y - dh, x + dw, y + dh, couleur_btn, couleur_btn)
    )
    objets.append(fltk.texte(x, y, texte, couleur_texte, "center"))
    return objets


def souris_collision(x, y, bouton):
    """
    Renvoie true si x et y sont contenu dans le bouton
    """
    xb, yb = modeles.position_bouton(bouton)
    w, h = modeles.taille_bouton(bouton)
    dw = w / 2
    dh = h / 2

    return xb - dw <= x <= (xb + dw) and yb - dh <= y <= (yb + dh)


def menu_principal(formes, jeu_solo, jeu_duo):
    """
    Affiche le menu principal
    """
    fltk.cree_fenetre(1000, 720, redimension=True)

    while True:
        largeur = fltk.largeur_fenetre()
        hauteur = fltk.hauteur_fenetre()

        fltk.efface_tout()
        fltk.rectangle(0, 0, largeur, hauteur, "black", "black")

        largeur_mid = largeur / 2
        hauteur_mid = hauteur / 2

        fltk.texte(largeur_mid, 30, "MENU PRINCIPAL", "white", "center")

        btn_jeu_solo = modeles.creer_bouton(
            largeur_mid - 25, hauteur_mid - 150, 250, 50, "Jeu SOLO", "#27ae60", "#fff"
        )

        btn_jeu_solo_save = modeles.creer_bouton(
            largeur_mid + 130, hauteur_mid - 150, 40, 50, "💿", "#000000", "#fff"
        )

        btn_jeu_duo = modeles.creer_bouton(
            largeur_mid - 25, hauteur_mid - 50, 250, 50, "Jeu DUO", "#27ae60", "#fff"
        )

        btn_jeu_duo_save = modeles.creer_bouton(
            largeur_mid + 130, hauteur_mid - 50, 40, 50, "💿", "#000000", "#fff"
        )

        btn_controles = modeles.creer_bouton(
            largeur_mid, hauteur_mid + 50, 300, 50, "Controles", "#2980b9", "#fff"
        )
        btn_parametres = modeles.creer_bouton(
            largeur_mid, hauteur_mid + 150, 300, 50, "Paramètres", "#2980b9", "#fff"
        )
        btn_quitter = modeles.creer_bouton(
            largeur_mid, hauteur_mid + 250, 300, 50, "Quitter", "#c0392b", "#fff"
        )

        ev = fltk.donne_ev()
        if fltk.type_ev(ev) == "ClicGauche":
            xs = fltk.abscisse(ev)
            ys = fltk.ordonnee(ev)

            if souris_collision(xs, ys, btn_jeu_solo):
                jeu_solo(formes, None)
            if souris_collision(xs, ys, btn_jeu_duo):
                jeu_duo(formes, None)
            if souris_collision(xs, ys, btn_jeu_solo_save):
                jeu_solo(formes, sauvegarde.charger("solo"))
            if souris_collision(xs, ys, btn_jeu_duo_save):
                jeu_duo(formes, sauvegarde.charger("duo"))
            if souris_collision(xs, ys, btn_controles):
                controles()
            if souris_collision(xs, ys, btn_parametres):
                parametres({})
            if souris_collision(xs, ys, btn_quitter):
                return

        dessiner_bouton(btn_jeu_solo)
        dessiner_bouton(btn_jeu_solo_save)
        dessiner_bouton(btn_jeu_duo)
        dessiner_bouton(btn_jeu_duo_save)
        dessiner_bouton(btn_controles)
        dessiner_bouton(btn_parametres)
        dessiner_bouton(btn_quitter)

        fltk.mise_a_jour()


def parametres(config):
    while True:
        largeur = fltk.largeur_fenetre()
        hauteur = fltk.hauteur_fenetre()

        fltk.efface_tout()
        fltk.rectangle(0, 0, largeur, hauteur, "black", "black")

        fltk.mise_a_jour()


def menu_pause(emplacement, etats):
    """
    Affiche le menu de pause
    """
    objets = []

    while True:
        largeur = fltk.largeur_fenetre()
        hauteur = fltk.hauteur_fenetre()

        for obj in objets:
            # Permet d'éviter des artéfacts lorsque la fenêtre est redimensionnée.
            fltk.efface(obj)

        objets.append(
            fltk.texte(
                largeur / 2,
                30,
                "Pause",
                "white",
                "center",
            )
        )

        btn_continuer = modeles.creer_bouton(
            largeur / 2, hauteur / 2 - 100, 300, 50, "Continuer", "#27ae60", "#fff"
        )

        btn_save = modeles.creer_bouton(
            largeur / 2, hauteur / 2, 300, 50, "Sauvegarder", "#2980b9", "#fff"
        )

        btn_menu = modeles.creer_bouton(
            largeur / 2, hauteur / 2 + 100, 300, 50, "Menu Principal", "#c0392b", "#fff"
        )

        ev = fltk.donne_ev()
        if fltk.type_ev(ev) == "ClicGauche":
            xs = fltk.abscisse(ev)
            ys = fltk.ordonnee(ev)

            if souris_collision(xs, ys, btn_continuer):
                return False
            if souris_collision(xs, ys, btn_save):
                sauvegarde.sauvegarder(emplacement, etats)
                continue
            if souris_collision(xs, ys, btn_menu):
                return True

        objets.extend(dessiner_bouton(btn_continuer))
        objets.extend(dessiner_bouton(btn_save))
        objets.extend(dessiner_bouton(btn_menu))

        fltk.mise_a_jour()


def boite_texte(texte, x, y):
    """
    Affiche du texte blanc avec un arrière plan bleu à la position x y
    """
    texte_maj = texte.upper()

    w, h = fltk.taille_texte(texte_maj, taille=18)

    decalage = max(w, h)

    w_demi = decalage / 2 + 5
    h_demi = decalage / 2 + 5

    fltk.rectangle(x - w_demi, y - h_demi, x + w_demi, y + h_demi, "#2980b9", "#2980b9")
    fltk.texte(x, y, texte_maj, "white", "center", taille=18)


def controles():
    """
    Affiche le menu des contrôles
    """
    while True:
        largeur = fltk.largeur_fenetre()
        hauteur = fltk.hauteur_fenetre()

        fltk.efface_tout()
        fltk.rectangle(0, 0, largeur, hauteur, "black", "black")

        largeur_mid = largeur / 2

        centre_j1 = largeur_mid / 2
        centre_j2 = largeur_mid * 3 / 2

        fltk.texte(largeur_mid, 30, "CONTRÔLES", "white", "center")
        fltk.texte(centre_j1, 100, "Joueur 1", "white", "center")
        fltk.texte(centre_j2, 100, "Joueur 2", "white", "center")

        position_j1_controle = centre_j1 + 50
        position_j2_controle = centre_j2 - 50

        boite_texte(
            constantes.CONTROLES_J1_DEPLACEMENT_GAUCHE, position_j1_controle, 150
        )
        boite_texte(
            constantes.CONTROLES_J1_DEPLACEMENT_DROIT, position_j1_controle, 200
        )
        boite_texte(constantes.CONTROLES_J1_ROTATION_GAUCHE, position_j1_controle, 250)
        boite_texte(constantes.CONTROLES_J1_ROTATION_DROITE, position_j1_controle, 300)
        boite_texte(constantes.CONTROLES_J1_ACCEL, position_j1_controle, 350)

        boite_texte(
            constantes.CONTROLES_J2_DEPLACEMENT_GAUCHE, position_j2_controle, 150
        )
        boite_texte(
            constantes.CONTROLES_J2_DEPLACEMENT_DROIT, position_j2_controle, 200
        )
        boite_texte(constantes.CONTROLES_J2_ROTATION_GAUCHE, position_j2_controle, 250)
        boite_texte(constantes.CONTROLES_J2_ROTATION_DROITE, position_j2_controle, 300)
        boite_texte(constantes.CONTROLES_J2_ACCEL, position_j2_controle, 350)

        for zone, ancre in [(centre_j1, "e"), (centre_j2, "w")]:
            fltk.texte(
                zone,
                150,
                "Deplacement Gauche",
                "white",
                ancre,
                taille=18,
            )
            fltk.texte(
                zone,
                200,
                "Deplacement Droite",
                "white",
                ancre,
                taille=18,
            )

            fltk.texte(
                zone,
                250,
                "Rotation Gauche",
                "white",
                ancre,
                taille=18,
            )
            fltk.texte(
                zone,
                300,
                "Rotation Droite",
                "white",
                ancre,
                taille=18,
            )

            fltk.texte(
                zone,
                350,
                "Accélérer Descente",
                "white",
                ancre,
                taille=18,
            )

        btn_ok = modeles.creer_bouton(
            largeur_mid, hauteur - 100, 250, 50, "OK", "#27ae60", "#fff"
        )
        fltk.texte(
            largeur_mid,
            60,
            "Les contrôles ne sont pas encore modifiables",
            "#aaaaaa",
            "center",
            taille=14,
        )

        dessiner_bouton(btn_ok)

        ev = fltk.donne_ev()
        if fltk.type_ev(ev) == "ClicGauche":
            xs = fltk.abscisse(ev)
            ys = fltk.ordonnee(ev)

            if souris_collision(xs, ys, btn_ok):
                break

        fltk.mise_a_jour()
