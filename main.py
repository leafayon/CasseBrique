import math
import random
import sys

import pygame
import pygame.freetype

pygame.init()  # Initialisation du jeu

# Pour le texte
pygame.freetype.init()
taille_texte = 20
myfont = pygame.freetype.SysFont(None, taille_texte)  # texte de taille taille_texte

# Taille de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping")

# Pour limiter le nombre d'image par seconde (FPS)
clock = pygame.time.Clock()

blanc = (255, 255, 255)
noir = (0, 0, 0)

score = 0
rayon_balle = 10
x_min, y_min = 0, 0
x_max, y_max = width, height


class Balle:
    def __init__(self):
        self.x, self.y = (400, 400)
        self.vitesse = 8  # vitesse initiale
        self.vitesse_par_angle(60)  # vecteur vitesse
        self.sur_raquette = True

    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def afficher(self):
        pygame.draw.circle(
            screen,
            blanc,
            (int(self.x - rayon_balle), int(self.y - rayon_balle)),
            rayon_balle,
            0
        )

    def rebond_raquette(self, raquette):
        diff = raquette.x - self.x
        longueur_totale = raquette.longueur / 2 + rayon_balle
        angle = 90 + 80 * diff / longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette):
        if self.sur_raquette:
            self.y = raquette.y - 2 * rayon_balle
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
            if raquette.collision_balle(self) and self.vy > 0:
                self.rebond_raquette(raquette)
            if (self.x + rayon_balle > x_max) or (self.x - rayon_balle < x_min):
                self.vx = -self.vx
            if self.y + rayon_balle > y_max:
                self.sur_raquette = True
            if self.y - rayon_balle < y_min:
                self.vy = -self.vy


class Raquette:
    def __init__(self):
        self.x = (x_min + x_max) / 2
        self.y = y_max - rayon_balle
        self.longueur = 10 * rayon_balle

    def afficher(self):
        pygame.draw.rect(
            screen,
            blanc,
            (int(self.x - self.longueur / 2), int(self.y - rayon_balle),  self.longueur, 2 * rayon_balle),
            0
        )

    def deplacer(self, x):
        if x - self.longueur / 2 < x_min:
            self.x = x_min + self.longueur / 2
        elif x + self.longueur / 2 > x_max:
            self.x = x_max - self.longueur / 2
        else:
            self.x = x

    def collision_balle(self, balle):
        vertical = abs(self.y - balle.y) < 2 * rayon_balle
        horizontal = abs(self.x - balle.x) < self.longueur / 2 + rayon_balle
        return vertical and horizontal


class Brique:
    def __init__(self, x, y, longueur=5 * rayon_balle, largeur=5 * rayon_balle):
        self.x, self.y = x, y
        self.vie = 1
        self.longueur = longueur
        self.largeur = largeur
        self.score = score

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        #pygame.draw.rect(screen, blanc, (int(self.x - self.longueur/2), int(self.y - self.largeur/2),
        #                                 self.longueur ,self.largeur),0)
        pygame.draw.rect(screen, blanc, (int(self.x), int(self.y),
                                         self.longueur, self.largeur), 0)

    def collision_balle(self, balle):

        # On suppose que largeur < longueur
        marge = self.largeur / 2 + rayon_balle
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x:  #on regarde à droite
            dx = balle.x - (self.x + self.longueur / 2 - self.largeur / 2)
            if abs(dy) <= marge and dx <= marge:  # on touche
                touche = True
                if dx <= abs(dy):
                    balle.vy = - balle.vy
                else:  # a droite
                    balle.vx = -balle.vx
        else:  # on regarde à gauche
            dx = balle.x - (self.x - self.longueur / 2 + self.largeur / 2)
            if abs(dy) <= marge and -dx <= marge:  # on touche
                touche = True
                if -dx <= abs(dy):
                    balle.vy = - balle.vy
                else:  # a gauche
                    balle.vx = -balle.vx
        if touche:
            global score
            self.vie = -1
            score = score + 1

        return touche


class Jeu:
    def __init__(self):
        self.balle = Balle()
        self.raquette = Raquette()
        self.briques: list[Brique] = []

        x = 20
        y = 20

        for _ in range(100):
            brique = Brique(x + 20, y + 20, 20, 20)

            if x >= width - 100:
                x = 20
                y = y + 20
            elif y >= height - 50:
                break
            else:
                x = x + 20

            self.briques.append(brique)

    def gestion_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Pour quitter
            elif event.type == pygame.MOUSEBUTTONDOWN:  # On vient de cliquer
                if event.button == 1:  # Bouton gauche
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        for brique in self.briques:
            if brique.en_vie():
                brique.collision_balle(self.balle)
        self.raquette.deplacer(x)

    def affichage(self):
        screen.fill(noir)  # On efface l'écran
        self.balle.afficher()
        self.raquette.afficher()
        print(score)
        e = myfont.render(str(score), "red")
        screen.blit(e[0], (width - 50, 10))
        for brique in self.briques:
            if brique.en_vie():
                brique.afficher()


jeu = Jeu()

while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()

    pygame.display.flip()  # Envoi de l'image à la carte graphique
    clock.tick(60)  # On attend pour ne pas dépasser 60 FPS
