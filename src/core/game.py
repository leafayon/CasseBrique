from typing import TYPE_CHECKING

from pygame.locals import MOUSEBUTTONDOWN

from ..objects.ball import Ball
from ..objects.brick import Brick
from ..objects.paddle import Paddle

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.event import Event


class Game:
    def __init__(self) -> None:
        self.paddle = Paddle()
        self.ball = Ball()

        self.bricks: list[Brick] = []

        for i in range(1, 15):
            for j in range(1, 19):
                self.bricks.append(Brick((40*j, 30*i)))

    def event(self, event: Event) -> None:
        if event.type == MOUSEBUTTONDOWN:  # On vient de cliquer
            if event.button == 1:  # Bouton gauche
                if self.ball.sur_raquette:
                    self.ball.sur_raquette = False
                    self.ball.vitesse_par_angle(60)

        self.paddle.event(event)

    def update(self) -> None:
        self.ball.move(self.paddle)

        for brick in self.bricks:
            brick.collision_ball(self.ball)

    def render(self, screen: Surface) -> None:
        self.paddle.render(screen)
        self.ball.render(screen)

        for brick in self.bricks:
            if brick.is_alive():
                brick.render(screen)
