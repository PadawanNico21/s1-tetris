---
title: Rapport SAE 1.01
author: Nicolas BOUCHER
date: 00/01/2025
lang: fr-FR
description: Rapport SAE
numbersections: true
toc: true
toc-own-page: true
header-includes: |
  \usepackage[T1]{fontenc}
  \usepackage{emo}
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

Nous avons implementé toutes les variantes:

- Polynominos arbitraires
- Mode pourissement
- Mode 2 joueurs
- Pause et Sauvegarde
- Points liés au niveau

## Bonus

Nous avons implementé les bonus suivants:

- Élimination par couleurs adjacentes
- Sauvegarde des paramètres
- Bonus Polyominos de taille $\leq$ n

## Contrôles

Les contrôles du mode solo et du premier joueur du mode 2 joueurs sont:

- `Z` Rotation droite
- `S` Rotation gauche
- `Q` Déplacement gauche
- `D` Déplacement droit
- `A` Accélerer déscente de la pièce

Les contrôles du deuxième joueur pour le mode 2 joueurs sont:

- `U` Rotation droite
- `J` Rotation gauche
- `H` Déplacement gauche
- `K` Déplacement droit
- `Y` Accélerer déscente de la pièce

Les contrôles peuvent être consultés a tout moment dans le menu principal avec le bouton "Contrôles".



# Les choix techniques et le fonctionnement du programme


# Analyse de la complexité

fournir une analyse de la complexitè des algorithmes principaux que vous utilisez.

## Deplacement des pièces lorsqu'une ligne est complétée

## Génération des polynomes de taille $\leq$ n

Complexité en : $O($inconnu$)$


