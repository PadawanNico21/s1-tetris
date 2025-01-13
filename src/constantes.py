"""
Constantes du jeu
"""

# Toutes les formes doivent être stockées dans des matrices carrées pour permettre la rotation.

BARRE = [
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]

L_DROITE = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
]

L_GAUCHE = [
    [0, 1, 0],
    [0, 1, 0],
    [1, 1, 0],
]

ZIGZAG_DROITE = [
    [0, 1, 0],
    [1, 1, 0],
    [1, 0, 0],
]

ZIGZAG_GAUCHE = [
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
]

CARREE = [[1, 1], [1, 1]]

LE_T = [
    [1, 0, 0],
    [1, 1, 0],
    [1, 0, 0],
]

FORMES_BASE = [BARRE, L_DROITE, L_GAUCHE, ZIGZAG_DROITE, ZIGZAG_GAUCHE, CARREE, LE_T]

COULEURS = [
    "#1abc9c",  # Cyan
    "#f1c40f",  # Jaune
    "#9b59b6",  # Violet
    "#e67e22",  # Orange
    "#3498db",  # Bleu
    "#e74c3c",  # Rouge
    "#2ecc71",  # Vert
]

# La même chose que la variable couleur mais au format "terminal" (escape codes)

COULEURS_TERMINAL = [
    "\x1B[48;2;26;188;156m",
    "\x1B[48;2;241;196;15m",
    "\x1B[48;2;155;89;182m",
    "\x1B[48;2;230;126;34m",
    "\x1B[48;2;52;152;219m",
    "\x1B[48;2;231;76;60m",
    "\x1B[48;2;46;204;113m",
]

COTE_PIXEL_PIECE = 24

DELAIS_ACTIONS = 0.15

CONTROLES_J1_ROTATION_DROITE = "z"
CONTROLES_J1_ROTATION_GAUCHE = "s"
CONTROLES_J1_DEPLACEMENT_DROIT = "d"
CONTROLES_J1_DEPLACEMENT_GAUCHE = "q"
CONTROLES_J1_ACCEL = "a"

CONTROLES_J2_ROTATION_DROITE = "u"
CONTROLES_J2_ROTATION_GAUCHE = "j"
CONTROLES_J2_DEPLACEMENT_DROIT = "k"
CONTROLES_J2_DEPLACEMENT_GAUCHE = "h"
CONTROLES_J2_ACCEL = "y"


AJOUT_NIVEAU_TOUTES_NB_PIECES = 20

CONFIGURATION_PAR_DEFAUT = {
    "fournisseur_polynominos": "integre",
    "generateur_taille_max": "4",
    "mode_couleur_adj": "0",
    "largeur_fenetre": "1000",
    "hauteur_fenetre": "720",
}

# Emplacement des fichiers

RACINE = "."
EMPLACEMENT_FICHIER_SAUVEGARDE = RACINE + "/sauvegardes.json"
FICHIER_PIECE = RACINE + "/pieces.txt"
FICHIER_PARAMETRES = RACINE + "/parametres.txt"
