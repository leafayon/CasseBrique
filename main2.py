import math

import pygame

WIDTH, HEIGHT = (800, 600)
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255)
}

BALL_RADIUS = 10

X_MIN, Y_MIN = 0, 0
X_MAX, Y_MAX = WIDTH, HEIGHT


class Racket:
    def __init__(self) -> None:
        self.x = (X_MIN + X_MAX) / 2
        self.y = Y_MAX - BALL_RADIUS

        self.length = 10 * BALL_RADIUS

    def move(self, x: int):
        if x - self.length / 2 < X_MIN:
            self.x = X_MIN + self.length / 2
        elif x + self.length / 2 > X_MAX:
            self.x = X_MAX - self.length / 2
        else:
            self.x = x

    def ball_collision(self, ball: Ball) -> int:
        vertical = abs(self.y - ball.y) < 2 * BALL_RADIUS
        horizontal = abs(self.x - ball.x) < self.length / 2 + BALL_RADIUS

        return vertical and horizontal


class Brique:
    def __init__(self) -> None:
        self.life = 0

    def alive(self) -> bool:
        return self.life > 0


class Ball:
    def __init__(self) -> None:
        self.x, self.y = (400, 400)

        self.speed = 8
        self.speed_x, self.speed_y = (0, 0)

        self.on_racket = True

        self.vitesse_par_angle(60)  # vecteur vitesse

    def vitesse_par_angle(self, angle: int) -> None:
        self.speed_x = self.speed * math.cos(math.radians(angle))
        self.speed_y = -self.speed * math.sin(math.radians(angle))

    def move(self, racket: Racket) -> None:
        if self.on_racket:
            self.y = racket.y - 2 * BALL_RADIUS
            self.x = racket.x
        else:
            self.x += self.speed_x
            self.y += self.speed_y

            if racket.ball_collision(self) and self.speed_y > 0:
                self.rebond_raquette(racket)

            if (self.x + BALL_RADIUS > X_MAX) or (self.x - BALL_RADIUS < X_MIN):
                self.speed_x = -self.speed_x

            if self.y + BALL_RADIUS > Y_MAX:
                self.on_racket = True

            if self.y - BALL_RADIUS < Y_MIN:
                self.speed_y = -self.speed_y

    def render(self, screen) -> None:
        pygame.draw.circle(
            screen,
            COLORS["WHITE"],
            (int(self.x - BALL_RADIUS), int(self.y - BALL_RADIUS)),
            BALL_RADIUS,
            0
        )


class Jeu:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Casse Brique")

        self.clock = pygame.time.Clock()

        self.ball = Ball()
        self.racket = Racket()

        self.is_running = True

    def event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche
                    if self.ball.on_racket:
                        self.ball.on_racket = False
                        self.ball.vitesse_par_angle(60)

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.screen.fill(COLORS["BLACK"])

        self.ball.render(self.screen)

    def start(self) -> None:
        while self.is_running:
            self.event()
            self.update()
            self.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


Jeu().start()
