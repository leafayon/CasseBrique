from typing import TYPE_CHECKING

from pygame import Surface
from pygame.draw import rect
from pygame.locals import MOUSEMOTION

from ..constants import COLORS, WINDOW_SIZE

if TYPE_CHECKING:
    from pygame.event import Event


class Paddle:
    def __init__(self) -> None:
        self.position = [
            WINDOW_SIZE[0]//2,
            int(WINDOW_SIZE[1]*0.95),
        ]  # (X, Y)

        self.length = (100, 20)  # (Largeur, Hauteur)

        self._surface = Surface(self.length)
        self.rect = rect(
            self._surface,
            COLORS["WHITE"],
            (0, 0, *self.length)
        )

    def collision_balle(self, balle):
        vertical = abs(self.position[1] - balle.position[1]) < 2 * 10
        horizontal = abs(self.position[0] - balle.position[0]) < self.length[0] / 2 + 10
        return vertical and horizontal

    def move(self, x: int) -> None:
        if x - self.length[0]//2 < 0:
            self.position[0] = self.length[0]//2
        elif x + self.length[0]//2 > WINDOW_SIZE[0]:
            self.position[0] = WINDOW_SIZE[0] - self.length[0]//2
        else:
            self.position[0] = x

    def event(self, event: Event) -> None:
        if event.type == MOUSEMOTION:
            self.move(event.pos[0])

    def render(self, screen: Surface) -> None:
        screen.blit(self._surface, (self.position[0]-self.length[0]//2, self.position[1]))
