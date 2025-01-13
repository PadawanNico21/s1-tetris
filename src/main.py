import menus
import modes_jeu


def main():
    """
    Fonction a lancer
    """
    menus.menu_principal(modes_jeu.jeu_solo, modes_jeu.jeu_duo)


if __name__ == "__main__":
    main()
