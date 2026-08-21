"""Punto de entrada principal de Atari Pong."""

import pygame

from config import WIDTH, HEIGHT, TITLE
from menu import show_menu
from game import Game
from scores import show_scores


def main():
    """Inicializa Pygame y controla el programa."""

    # Inicializar Pygame.
    pygame.init()

    # Crear ventana.
    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        TITLE
    )

    running = True

    while running:

        # Mostrar menú.
        action = show_menu(screen)

        # Jugar.
        if action == "JUGAR":

            game = Game(screen)

            result = game.run()

            if result == "SALIR":
                running = False

        # Marcadores.
        elif action == "MARCADORES":

            result = show_scores(screen)

            if result == "SALIR":
                running = False

        # Salir.
        elif action == "SALIR":

            running = False

    # Cerrar Pygame.
    pygame.quit()


if __name__ == "__main__":
    main()