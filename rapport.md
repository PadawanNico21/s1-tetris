---
title: Rapport SAE 1.01
author: Nicolas BOUCHER, Charles SUSINI et Kiruchanth KIRUPAKARAN
date: 13/01/2025
lang: fr-FR
description: Rapport SAE
numbersections: true
toc: true
toc-own-page: true
header-includes: |
    \usepackage[T1]{fontenc}
    \usepackage{todonotes}
geometry:
    - a4paper
    - margin=3cm
top-level-division: section
titlepage: true
footnotes-pretty: true
---

\pagebreak

# Présentation de notre Tetris

## Variantes

Nous avons implementé les variantes:

-   Polynominos arbitraires
-   Mode 2 joueurs
-   Pause et Sauvegarde
-   Points liés au niveau

## Bonus

Nous avons implementé les bonus suivants:

-   Élimination par couleurs adjacentes
-   Sauvegarde des paramètres
-   Bonus Polynominos de taille $\leq n$

## Contrôles

Les contrôles du mode solo et du premier joueur du mode 2 joueurs sont:

-   `Z` Rotation droite
-   `S` Rotation gauche
-   `Q` Déplacement gauche
-   `D` Déplacement droit
-   `A` Accélerer descente de la pièce

Les contrôles du deuxième joueur pour le mode 2 joueurs sont:

-   `U` Rotation droite
-   `J` Rotation gauche
-   `H` Déplacement gauche
-   `K` Déplacement droit
-   `Y` Accélerer descente de la pièce

Les contrôles peuvent être consultés à tout moment dans le menu principal avec le bouton "Contrôles" dans le menu principal.

# Les choix techniques et le fonctionnement du programme

## Choix techniques

Nous avons choisi de représenter chaque pièce sous la forme d'un tuple. Ce tuple contient:

1. L'identifiant qui permet de référencer la pièce dans le plateau de jeu.
2. La forme de la pièce (une matrice carrée)
3. Le code héxadécimal de la couleur de la pièce
4. Un vecteur (une liste de 2 nombres) qui représente la position de la pièce

Ce choix rend plus complexe certaines opérations basiques du tétris (nettoyage de ligne remplie, déplacement de la pièce). Mais cela permet de rendre plus facile le bonus "Élimination par couleurs adjacentes"

Pour permettre un meilleur partage du code du mode solo et duo nous avons créé un état du jeu qui est stocké en une seule variable et qui permet de créer des fonctions se basant uniquement sur cette valeur.

## Fonctionnement du programme

Nous avons la fonction `main` dans le fichier `main.py` qui éxécute la fonction `menu_principal` qui se charge de lancer le bon mode de jeu avec les variantes voulues. Ensuite nous avons le mode de jeu solo et duo, la logique des 2 modes est très similaire donc nous allons expliquer uniquement le fonctionnement du mode duo.

### Fonctionnement de la boucle de jeu

-   Nous créons la fonction `choisir_piece` avec les formes qui sont passées en paramètres des fonctions jeu_solo et jeu_duo. On créé aussi les plateaux, ainsi que les états de jeu.
-   On boucle jusqu'à ce qu'un joueur est perdu
-   Dans cette boucle on calcule les délais de descente des pièces en fonction de la difficulté (nombre de pièces posées)
-   On vérifie si le joueur veut afficher la pause
-   On applique la gravité ainsi que le mode couleur adjacente sur les pièces si cela est nécessaire
-   On calcule les déplacements horizontaux
-   On calcule la rotation des pièces
-   On supprime les lignes complètes et _on les ajoute pour l'adversaire_ (mode 2 duo uniquement)
-   On dessine le plateau de jeu
-   On continue la boucle

# Analyse de la complexité

## Déplacement des pièces lorsqu'une ligne est complétée

### Lister lignes remplies

La complexité de la fonction `lister_lignes_remplies` dans le fichier `jeu.py` est en $O(mn)$ où $m$ et $n$ sont les dimensions du plateau de jeu.

### Détruire ligne

La complexité de la fonction `detruire_ligne` dans le fichier `piece.py` est en $O(n(m_pn_p) + m_jn_j)$ où $n$ est le nombre de pièces sur les plateau, $m_p$ et $n_p$ les dimensions de la pièce et $m_j$ et $n_j$ les dimensions du plateau de jeu

Compléxité totale: $O(n(m_pn_p))$

## Génération des polynomes de taille $\leq n$

La compléxité de la fonction `generer_polynominos` dans le fichier `polygen.py` est en $O(4^n)$
