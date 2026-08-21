"""Menú principal de Atari Pong."""

import pygame

from config import (
    WIDTH,
    HEIGHT,
    WHITE,
    GRAY,
    DARK_GRAY,
    BLACK
)


class Menu:
    """Controla la pantalla principal del juego."""

    def __init__(self, screen):

        self.screen = screen

        self.font_title = pygame.font.Font(
            None,
            100
        )

        self.font_option = pygame.font.Font(
            None,
            55
        )

        self.font_help = pygame.font.Font(
            None,
            28
        )

        # Opciones del menú.
        self.options = [
            "JUGAR",
            "MARCADORES",
            "SALIR"
        ]

        self.selected = 0

    def draw_text_center(
        self,
        text,
        font,
        y,
        color
    ):
        """Dibuja texto centrado."""

        surface = font.render(
            text,
            True,
            color
        )

        rectangle = surface.get_rect(
            center=(WIDTH // 2, y)
        )

        self.screen.blit(
            surface,
            rectangle
        )

    def draw(self):
        """Dibuja el menú."""

        self.screen.fill(BLACK)

        # Título
        self.draw_text_center(
            "ATARI PONG",
            self.font_title,
            120,
            WHITE
        )

        # Opciones
        for index, option in enumerate(
            self.options
        ):

            y = 260 + index * 100

            if index == self.selected:

                color = WHITE

                rectangle = pygame.Rect(
                    WIDTH // 2 - 180,
                    y - 35,
                    360,
                    70
                )

                pygame.draw.rect(
                    self.screen,
                    DARK_GRAY,
                    rectangle,
                    border_radius=10
                )

            else:

                color = GRAY

            self.draw_text_center(
                option,
                self.font_option,
                y,
                color
            )

        # Instrucciones
        self.draw_text_center(
            "Flechas / W-S: mover    ENTER: seleccionar",
            self.font_help,
            HEIGHT - 40,
            GRAY
        )

        pygame.display.flip()

    def handle_event(self, event):
        """Procesa las teclas del menú."""

        if event.type == pygame.QUIT:
            return "SALIR"

        if event.type == pygame.KEYDOWN:

            # Subir.
            if event.key in (
                pygame.K_UP,
                pygame.K_w
            ):

                self.selected -= 1

                if self.selected < 0:
                    self.selected = len(
                        self.options
                    ) - 1

            # Bajar.
            elif event.key in (
                pygame.K_DOWN,
                pygame.K_s
            ):

                self.selected += 1

                if self.selected >= len(
                    self.options
                ):
                    self.selected = 0

            # Seleccionar.
            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                return self.options[
                    self.selected
                ]

        return None

    def run(self):
        """Ejecuta el menú."""

        clock = pygame.time.Clock()

        while True:

            for event in pygame.event.get():

                result = self.handle_event(event)

                if result is not None:
                    return result

            self.draw()

            clock.tick(60)


def show_menu(screen):
    """Muestra el menú principal."""

    menu = Menu(screen)

    return menu.run()