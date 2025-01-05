# SAE 1.01 -- Tetris

## Execution

Pour lancer le tetris il faut executer le fichier main.py

## Contrôles

Déplacement horizontaux: touche ← et touche →
Rotation de la pièce: touche ↑ et touche ↓
Accélérer la descente: Barre espace

## Choix techniques

Nous avons décidé d'utiliser une matrice d'identifiant pour représenter le plateau de jeu.
Ces identifiants pointent vers des pièces qui sont composées d'une position, d'une forme et d'une couleur.
Nous pensons que cette structuration permettra de faciliter l'ajout des variantes et bonus pour les prochains rendus.

## Organisation du programme

Le programme est organisé en modules:
constantes.py: ce module contient la configuration du jeu
graphisme.py: ce module contient toute la partie graphique du jeu
jeu.py: ce module contient des fonctions diverses en rapport avec la logique du jeu
main.py: programme principal
matrice.py: ce module contient des fonctions permettant de manipuler des matrices
pieces.py: ce module permet de manipuler les pièces sur le plateau de jeu
polyomino_parser.py: ce module gère la variante "polyominos arbitraires" et se charge d'interpréter le fichier "pieces.txt"

## Difficultés rencontrées

La principale difficulté rencontrée lors de la conception de cette première version est le nettoyage des lignes complètes.
En effet, à cause des choix techniques que nous avons faits, l'altération de lignes sur le plateau de jeu est plus complexe car il faut propager ces changements aux pièces affectées.

## Variante implémentée

Polyominos arbitraires: vous pouvez modifier le fichier pieces.txt pour changer les polyominos
