"""
Module contenant les menus
"""

import fltk
import modeles
import sauvegarde
import constantes
import polynomino_parser
import polygen


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


def charger_formes(configuration):
    """
    Renvoie les formes en fonction de la configuration
    """
    fournisseur = configuration["fournisseur_polynominos"]
    if fournisseur == "integre":
        return constantes.FORMES_BASE
    if fournisseur == "fichier":
        return polynomino_parser.forme_init()
    if fournisseur == "generateur":
        return polygen.generer_polynominos(int(configuration["generateur_taille_max"]))


def menu_principal(jeu_solo, jeu_duo):
    """
    Affiche le menu principal
    """
    configuration = sauvegarde.charger_fichier_parametres()
    fltk.cree_fenetre(
        int(configuration["largeur_fenetre"]),
        int(configuration["hauteur_fenetre"]),
        redimension=True,
    )
    formes = charger_formes(configuration)

    while True:
        largeur = fltk.largeur_fenetre()
        hauteur = fltk.hauteur_fenetre()

        configuration["largeur_fenetre"] = str(largeur)
        configuration["hauteur_fenetre"] = str(hauteur)

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

            activer_couleur_adj = configuration["mode_couleur_adj"] == "1"

            if souris_collision(xs, ys, btn_jeu_solo):
                jeu_solo(formes, None, activer_couleur_adj)
            if souris_collision(xs, ys, btn_jeu_duo):
                jeu_duo(formes, None, activer_couleur_adj)
            if souris_collision(xs, ys, btn_jeu_solo_save):
                jeu_solo(formes, sauvegarde.charger("solo"), activer_couleur_adj)
            if souris_collision(xs, ys, btn_jeu_duo_save):
                jeu_duo(formes, sauvegarde.charger("duo"), activer_couleur_adj)
            if souris_collision(xs, ys, btn_controles):
                controles()
            if souris_collision(xs, ys, btn_parametres):
                parametres(configuration)
                sauvegarde.ecrire_fichier_parametres(configuration)
                formes = charger_formes(configuration)
                print("Formes disponibles avec cette configuration:", len(formes))
            if souris_collision(xs, ys, btn_quitter):
                sauvegarde.ecrire_fichier_parametres(configuration)
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
    """
    Affiche le menu des paramètres
    """
    while True:
        largeur = fltk.largeur_fenetre()
        hauteur = fltk.hauteur_fenetre()

        fltk.efface_tout()
        fltk.rectangle(0, 0, largeur, hauteur, "black", "black")

        largeur_mid = largeur / 2
        hauteur_mid = hauteur / 2

        fltk.texte(largeur_mid, 30, "PARAMETRES", "white", "center")

        btn_fermer = modeles.creer_bouton(
            largeur_mid, hauteur_mid + 250, 300, 50, "Fermer", "#c0392b", "#fff"
        )

        fltk.texte(
            50,
            100,
            "Fournisseur de polynominos: " + config["fournisseur_polynominos"],
            "white",
            taille=16,
        )

        btn_fournisseur_integre = modeles.creer_bouton(
            125, 150, 150, 50, "Intégré", "#2980b9", "#fff"
        )

        btn_fournisseur_fichier = modeles.creer_bouton(
            275, 150, 150, 50, "Fichier", "#2980b9", "#fff"
        )

        btn_fournisseur_generateur = modeles.creer_bouton(
            450, 150, 200, 50, "Générateur", "#2980b9", "#fff"
        )

        fltk.texte(
            50,
            200,
            "Taille max générateur: " + (config["generateur_taille_max"]),
            "white",
            taille=16,
        )

        generateur_btns = []
        for i in range(1, 11):
            generateur_btns.append(
                modeles.creer_bouton(
                    i * 50 + 25, 250, 50, 50, str(i), "#2980b9", "#fff"
                )
            )

        texte = "Activer mode couleur adjacente"
        couleur_btn = "#27ae60"
        if config["mode_couleur_adj"] != "0":
            texte = "Desactiver mode couleur adjacente"
            couleur_btn = "#c0392b"

        btn_toggle_couleur_adj = modeles.creer_bouton(
            300, 325, 500, 50, texte, couleur_btn, "#fff"
        )

        ev = fltk.donne_ev()
        if fltk.type_ev(ev) == "ClicGauche":
            xs = fltk.abscisse(ev)
            ys = fltk.ordonnee(ev)

            if souris_collision(xs, ys, btn_fermer):
                fltk.texte(largeur_mid, hauteur_mid, "Chargement...", "white", "center")
                fltk.mise_a_jour()
                return
            if souris_collision(xs, ys, btn_fournisseur_integre):
                config["fournisseur_polynominos"] = "integre"
            if souris_collision(xs, ys, btn_fournisseur_fichier):
                config["fournisseur_polynominos"] = "fichier"
            if souris_collision(xs, ys, btn_fournisseur_generateur):
                config["fournisseur_polynominos"] = "generateur"
            for btn in generateur_btns:
                if souris_collision(xs, ys, btn):
                    config["generateur_taille_max"] = modeles.texte_bouton(btn)
            if souris_collision(xs, ys, btn_toggle_couleur_adj):
                val = not int(config["mode_couleur_adj"])
                config["mode_couleur_adj"] = "0"
                if val:
                    config["mode_couleur_adj"] = "1"

        dessiner_bouton(btn_fermer)
        dessiner_bouton(btn_fournisseur_integre)
        dessiner_bouton(btn_fournisseur_fichier)
        dessiner_bouton(btn_fournisseur_generateur)
        for btn in generateur_btns:
            dessiner_bouton(btn)
        dessiner_bouton(btn_toggle_couleur_adj)

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

        dessiner_bouton(btn_ok)

        ev = fltk.donne_ev()
        if fltk.type_ev(ev) == "ClicGauche":
            xs = fltk.abscisse(ev)
            ys = fltk.ordonnee(ev)

            if souris_collision(xs, ys, btn_ok):
                break

        fltk.mise_a_jour()
