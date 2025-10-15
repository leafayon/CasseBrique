import math
from typing import TYPE_CHECKING

from pygame import Surface
from pygame.draw import circle

from ..constants import COLORS

if TYPE_CHECKING:
    from .paddle import Paddle
x_min, y_min = 0, 0
x_max, y_max = 800, 600

class Ball:
    def __init__(self) -> None:
        self.position = [
            400,
            400
        ]  # (X, Y)

        self.radius = 10

        self.speed = 8

        self._surface = Surface((self.radius*2, self.radius*2))
        self.rect = circle(
            self._surface,
            COLORS["WHITE"],
            (self.radius, self.radius),
            self.radius
        )

        self.vitesse_par_angle(60)  # vecteur vitesse
        self.sur_raquette = True

    def vitesse_par_angle(self, angle):
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = -self.speed * math.sin(math.radians(angle))
    def rebond_raquette(self, paddle):
        diff = paddle.position[0] - self.position[0]
        longueur_totale = paddle.length[0] / 2 + self.radius
        angle = 90 + 80 * diff / longueur_totale
        self.vitesse_par_angle(angle)
    def move(self, paddle: Paddle) -> None:
        if self.sur_raquette:
            self.position[1] = paddle.position[1] - 2 * self.radius
            self.position[0] = paddle.position[0]
        else:
            self.position[0] += self.vx
            self.position[1] += self.vy
            if paddle.collision_balle(self) and self.vy > 0:
                self.rebond_raquette(paddle)
            if (self.position[0] + self.radius > x_max) or (self.position[0] - self.radius < x_min):
                self.vx = -self.vx

            if self.position[1] + self.radius > y_max:
                self.sur_raquette = True
            if self.position[1] - self.radius < y_min:
                self.vy = -self.vy

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def render(self, screen: Surface) -> None:
        screen.blit(self._surface, (self.position[0]-self.radius, self.position[1]-self.radius))
