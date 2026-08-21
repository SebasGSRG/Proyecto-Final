"""Sistema de almacenamiento y visualización de marcadores."""

import json
import os

import pygame

from config import WIDTH, HEIGHT, BLACK, WHITE, GRAY


# Ruta principal del proyecto
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Carpeta donde se guardarán los resultados
DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# Archivo de resultados
SCORES_FILE = os.path.join(
    DATA_DIR,
    "resultados.json"
)


def load_scores():
    """Carga las partidas guardadas."""

    if not os.path.exists(SCORES_FILE):
        return []

    try:
        with open(
            SCORES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_match(player1_score, player2_score):
    """Guarda el resultado de una partida."""

    # Crear la carpeta data si no existe.
    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    scores = load_scores()

    # Determinar ganador.
    if player1_score > player2_score:
        winner = "JUGADOR 1"

    elif player2_score > player1_score:
        winner = "JUGADOR 2"

    else:
        winner = "EMPATE"

    # Crear registro de la partida.
    match = {
        "jugador1": player1_score,
        "jugador2": player2_score,
        "ganador": winner
    }

    scores.append(match)

    # Guardar solamente las últimas 10 partidas.
    scores = scores[-10:]

    try:
        with open(
            SCORES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                scores,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:
        print("No se pudo guardar el resultado.")


def show_scores(screen):
    """Muestra el historial de partidas."""

    clock = pygame.time.Clock()

    title_font = pygame.font.Font(
        None,
        70
    )

    row_font = pygame.font.Font(
        None,
        32
    )

    help_font = pygame.font.Font(
        None,
        28
    )

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "SALIR"

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):
                    return "MENU"

        screen.fill(BLACK)

        # Título
        title = title_font.render(
            "MARCADORES",
            True,
            WHITE
        )

        title_rectangle = title.get_rect(
            center=(WIDTH // 2, 70)
        )

        screen.blit(
            title,
            title_rectangle
        )

        scores = load_scores()

        # Si todavía no existen partidas.
        if not scores:

            empty_text = row_font.render(
                "Todavía no hay partidas registradas.",
                True,
                GRAY
            )

            empty_rectangle = empty_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            screen.blit(
                empty_text,
                empty_rectangle
            )

        else:

            # Mostrar primero la partida más reciente.
            recent_scores = list(
                reversed(scores)
            )

            for index, match in enumerate(
                recent_scores
            ):

                y = 140 + index * 42

                result_text = (
                    f"{index + 1}. "
                    f"J1 {match['jugador1']} - "
                    f"{match['jugador2']} J2"
                )

                result_surface = row_font.render(
                    result_text,
                    True,
                    WHITE
                )

                result_rectangle = (
                    result_surface.get_rect(
                        center=(WIDTH // 2, y)
                    )
                )

                screen.blit(
                    result_surface,
                    result_rectangle
                )

                winner_text = (
                    f"Ganador: {match['ganador']}"
                )

                winner_surface = row_font.render(
                    winner_text,
                    True,
                    GRAY
                )

                winner_rectangle = (
                    winner_surface.get_rect(
                        center=(WIDTH // 2, y + 22)
                    )
                )

                screen.blit(
                    winner_surface,
                    winner_rectangle
                )

        # Instrucción inferior
        help_text = help_font.render(
            "ENTER / ESC: volver al menú",
            True,
            GRAY
        )

        help_rectangle = help_text.get_rect(
            center=(WIDTH // 2, HEIGHT - 35)
        )

        screen.blit(
            help_text,
            help_rectangle
        )

        pygame.display.flip()

        clock.tick(60)

