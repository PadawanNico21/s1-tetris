"""
Module de gestion des sauvegardes
"""

import modeles
import constantes
import json
import pathlib


def sauvegarder(emplacement, etats):
    """
    Sauvegarde les etats dans l'emplacement
    """
    sauvegardes = contenu_fichier_sauvegarde()
    sauvegarde = [modeles.cloner_etat(etat) for etat in etats]

    sauvegardes[emplacement] = sauvegarde
    ecrire_fichier_sauvegarde(sauvegardes)


def charger(emplacement):
    """
    Tente de charger le fichier de sauvegarde sinon cela créer une sauvegarde vide
    """
    sauvegardes = contenu_fichier_sauvegarde()
    if emplacement not in sauvegardes:
        return None
    sauvegarde = sauvegardes[emplacement]

    max_id = 0

    for etat in sauvegarde:
        active = modeles.obtenir_piece_active(etat)
        pieces = modeles.pieces_sur_jeu(etat)
        id_active = modeles.identifier(active)
        if id_active > max_id:
            max_id = id_active

        for i in range(len(pieces)):
            if id_active == modeles.identifier(pieces[i]):
                pieces[i] = active
                break
    modeles.definir_dernier_identifiant(max_id)
    return sauvegarde


def contenu_fichier_sauvegarde():
    """
    Lis le contenu du fichier de sauvegarde ou créer un nouveau fichier
    """
    if not pathlib.Path(constantes.EMPLACEMENT_FICHIER_SAUVEGARDE).exists():
        ecrire_fichier_sauvegarde(dict())
        return dict()

    with open(constantes.EMPLACEMENT_FICHIER_SAUVEGARDE, "r") as fichier:
        return json.load(fichier)


def ecrire_fichier_sauvegarde(sauvegardes):
    """
    Ecris dans le fichier de sauvegarde
    """
    with open(constantes.EMPLACEMENT_FICHIER_SAUVEGARDE, "w") as fichier:
        json.dump(sauvegardes, fichier)
