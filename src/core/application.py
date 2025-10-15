import pygame

from ..constants import COLORS, WINDOW_SIZE
from .game import Game


class Application:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Casse Brique")

        self.clock = pygame.time.Clock()

        self.game = Game()

        self.is_running = True

    def _events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            self.game.event(event)

    def _updates(self) -> None:
        self.game.update()

    def _renders(self):
        self.screen.fill(COLORS["BLACK"])

        self.game.render(self.screen)

    def start(self) -> None:
        while self.is_running:
            self._events()
            self._updates()
            self._renders()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
