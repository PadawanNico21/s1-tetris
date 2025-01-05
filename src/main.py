import polynomino_parser
import menus
import modes_jeu


def main():
    formes = polynomino_parser.forme_init()

    menus.menu_principal(formes, modes_jeu.jeu_solo, modes_jeu.jeu_duo)


if __name__ == "__main__":
    main()
