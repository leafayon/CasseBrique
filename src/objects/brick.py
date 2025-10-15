from typing import TYPE_CHECKING

from pygame import Surface
from pygame.draw import rect

from ..constants import COLORS, WINDOW_SIZE

if TYPE_CHECKING:
    from pygame.event import Event


class Brick:
    def __init__(self, position: tuple[int | float, int | float] = (0, 0)) -> None:
        self.length = (40, 30)  # (Largeur, Hauteur)

        self._surface = Surface(self.length)
        self.rect = rect(
            self._surface,
            COLORS["WHITE"],
            (-1, -1, self.length[0], self.length[1])
        )
        self.rect.x, self.rect.y = position[0], position[1]

        self.life = 1

    def is_alive(self) -> int:
        return self.life > 0

    def collision_ball(self, ball):
        if self.rect.colliderect(ball.rect):
            self.life -= 1

            return True

        return False

    def event(self, event: Event) -> None:
        pass

    def render(self, screen: Surface) -> None:
        screen.blit(self._surface, self.rect)
