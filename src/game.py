"""Lógica principal de Atari Pong."""

import random

import pygame

from config import (
    WIDTH,
    HEIGHT,
    FPS,
    BLACK,
    WHITE,
    GRAY,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    BALL_SIZE,
    BALL_SPEED_X,
    BALL_SPEED_Y,
    WINNING_SCORE
)

from scores import save_match


class Paddle:
    """Representa una paleta."""

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )

    def move(self, direction):
        """Mueve la paleta."""

        self.rect.y += (
            direction * PADDLE_SPEED
        )

        # Limitar la paleta por arriba.
        if self.rect.top < 0:
            self.rect.top = 0

        # Limitar la paleta por abajo.
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        """Dibuja la paleta."""

        pygame.draw.rect(
            screen,
            WHITE,
            self.rect
        )


class Ball:
    """Representa la pelota."""

    def __init__(self):

        self.rect = pygame.Rect(
            0,
            0,
            BALL_SIZE,
            BALL_SIZE
        )

        self.speed_x = 0
        self.speed_y = 0

        self.reset()

    def reset(self):
        """Reinicia la pelota."""

        self.rect.center = (
            WIDTH // 2,
            HEIGHT // 2
        )

        self.speed_x = random.choice(
            [-BALL_SPEED_X, BALL_SPEED_X]
        )

        self.speed_y = random.choice(
            [-BALL_SPEED_Y, BALL_SPEED_Y]
        )

    def update(self):
        """Actualiza la posición."""

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebote superior.
        if self.rect.top <= 0:

            self.rect.top = 0

            self.speed_y = abs(
                self.speed_y
            )

        # Rebote inferior.
        if self.rect.bottom >= HEIGHT:

            self.rect.bottom = HEIGHT

            self.speed_y = -abs(
                self.speed_y
            )

    def draw(self, screen):
        """Dibuja la pelota."""

        pygame.draw.rect(
            screen,
            WHITE,
            self.rect
        )


class Game:
    """Controla una partida."""

    def __init__(self, screen):

        self.screen = screen

        self.clock = pygame.time.Clock()

        self.score_font = pygame.font.Font(
            None,
            80
        )

        self.message_font = pygame.font.Font(
            None,
            64
        )

        self.help_font = pygame.font.Font(
            None,
            24
        )

        # Jugador 1.
        self.left_paddle = Paddle(
            40,
            HEIGHT // 2 - PADDLE_HEIGHT // 2
        )

        # Jugador 2.
        self.right_paddle = Paddle(
            WIDTH - 55,
            HEIGHT // 2 - PADDLE_HEIGHT // 2
        )

        # Pelota.
        self.ball = Ball()

        # Marcador.
        self.left_score = 0
        self.right_score = 0

    def reset_round(self):
        """Reinicia la ronda."""

        self.left_paddle.rect.centery = (
            HEIGHT // 2
        )

        self.right_paddle.rect.centery = (
            HEIGHT // 2
        )

        self.ball.reset()

    def handle_input(self):
        """Procesa los controles."""

        keys = pygame.key.get_pressed()

        # Jugador 1: W / S
        left_direction = 0

        if keys[pygame.K_w]:

            left_direction = -1

        elif keys[pygame.K_s]:

            left_direction = 1

        self.left_paddle.move(
            left_direction
        )

        # Jugador 2: flechas
        right_direction = 0

        if keys[pygame.K_UP]:

            right_direction = -1

        elif keys[pygame.K_DOWN]:

            right_direction = 1

        self.right_paddle.move(
            right_direction
        )

    def check_paddle_collision(self):
        """Comprueba colisiones con las paletas."""

        # Paleta izquierda.
        if self.ball.rect.colliderect(
            self.left_paddle.rect
        ):

            if self.ball.speed_x < 0:

                self.ball.rect.left = (
                    self.left_paddle.rect.right
                )

                self.ball.speed_x *= -1

        # Paleta derecha.
        if self.ball.rect.colliderect(
            self.right_paddle.rect
        ):

            if self.ball.speed_x > 0:

                self.ball.rect.right = (
                    self.right_paddle.rect.left
                )

                self.ball.speed_x *= -1

    def update(self):
        """Actualiza la partida."""

        self.ball.update()

        self.check_paddle_collision()

        # La pelota salió por la izquierda.
        if self.ball.rect.right < 0:

            self.right_score += 1

            self.reset_round()

        # La pelota salió por la derecha.
        elif self.ball.rect.left > WIDTH:

            self.left_score += 1

            self.reset_round()

    def draw_center_line(self):
        """Dibuja la línea central."""

        for y in range(
            0,
            HEIGHT,
            30
        ):

            pygame.draw.rect(
                self.screen,
                GRAY,
                (
                    WIDTH // 2 - 2,
                    y,
                    4,
                    15
                )
            )

    def draw_score(self):
        """Dibuja el marcador."""

        left_text = self.score_font.render(
            str(self.left_score),
            True,
            WHITE
        )

        right_text = self.score_font.render(
            str(self.right_score),
            True,
            WHITE
        )

        left_rectangle = left_text.get_rect(
            center=(
                WIDTH // 2 - 100,
                60
            )
        )

        right_rectangle = right_text.get_rect(
            center=(
                WIDTH // 2 + 100,
                60
            )
        )

        self.screen.blit(
            left_text,
            left_rectangle
        )

        self.screen.blit(
            right_text,
            right_rectangle
        )

    def draw_help(self):
        """Dibuja los controles."""

        text = self.help_font.render(
            "J1: W/S    J2: Flechas    ESC: Menu",
            True,
            GRAY
        )

        rectangle = text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT - 20
            )
        )

        self.screen.blit(
            text,
            rectangle
        )

    def draw(self):
        """Dibuja el juego."""

        self.screen.fill(BLACK)

        self.draw_center_line()

        self.draw_score()

        self.left_paddle.draw(
            self.screen
        )

        self.right_paddle.draw(
            self.screen
        )

        self.ball.draw(
            self.screen
        )

        self.draw_help()

        pygame.display.flip()

    def show_winner(self, winner):
        """Muestra la pantalla de ganador."""

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return "SALIR"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return "MENU"

                    if event.key in (
                        pygame.K_RETURN,
                        pygame.K_SPACE
                    ):
                        return "REINICIAR"

            self.screen.fill(BLACK)

            winner_text = self.message_font.render(
                f"{winner} GANA",
                True,
                WHITE
            )

            winner_rectangle = winner_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 50
                )
            )

            self.screen.blit(
                winner_text,
                winner_rectangle
            )

            help_text = self.help_font.render(
                "ENTER: jugar de nuevo    ESC: menú",
                True,
                GRAY
            )

            help_rectangle = help_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 + 40
                )
            )

            self.screen.blit(
                help_text,
                help_rectangle
            )

            pygame.display.flip()

            self.clock.tick(FPS)

    def run(self):
        """Ejecuta el ciclo principal."""

        while True:

            # Eventos.
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return "SALIR"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return "MENU"

            # Actualizar.
            self.handle_input()

            self.update()

            # Dibujar.
            self.draw()

            # Victoria del jugador 1.
            if self.left_score >= WINNING_SCORE:

                save_match(
                    self.left_score,
                    self.right_score
                )

                result = self.show_winner(
                    "JUGADOR 1"
                )

                if result == "REINICIAR":

                    self.left_score = 0
                    self.right_score = 0

                    self.reset_round()

                    continue

                return result

            # Victoria del jugador 2.
            if self.right_score >= WINNING_SCORE:

                save_match(
                    self.left_score,
                    self.right_score
                )

                result = self.show_winner(
                    "JUGADOR 2"
                )

                if result == "REINICIAR":

                    self.left_score = 0
                    self.right_score = 0

                    self.reset_round()

                    continue

                return result

            self.clock.tick(FPS)