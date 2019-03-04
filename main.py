#!/usr/bin/python
# -*- coding: Utf-8 -*-

# ---------------------------------------------------------------------------------------------------------
# Battle of Heroes
# Développé par Thibault AYANIDES et Eloi BOUTILLON
# License GPL v3
# Les images les sons et les polices utilisés ne nous appartiennent pas
# 2015-2016
# ---------------------------------------------------------------------------------------------------------

# Pygame
import pygame
from pygame.locals import *
import sys
from classes import *
from fonctions import *
from selection_perso import *


def main():
    personnage1, personnage2 = selection_perso()
    pygame.init()
    if sys.platform == "win32":
        k_haut = K_w
        k_droite = K_d
        k_gauche = K_a
        k_attaque = K_q
    elif sys.platform == "linux":
        k_haut = K_z
        k_droite = K_d
        k_gauche = K_q
        k_attaque = K_a

    police_taille80 = pygame.font.Font("polices/magic.ttf", 80)  # polices d'écriture
    police_taille14 = pygame.font.Font("polices/magic.ttf", 14)
    SOL = 430
    # initialisation de la fenêtre d'affichage

    ecran = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battle of Heroes")
    pygame.mouse.set_visible(False)  # on rend la souris invisible
    fond_ecran = pygame.transform.scale(pygame.image.load("fond_ecran/fond_ecran.gif"), (800, 600)).convert()

    # création personnage1
    personnage1 = eval(personnage1.capitalize())("R")
    personnage1.position_personnage = personnage1.position_personnage.move(30, SOL)  # position initiale du personnage 1

    # création personnage2
    personnage2 = eval(personnage2.capitalize())("L")
    personnage2.position_personnage = personnage2.position_personnage.move(700,
                                                                           SOL)  # position initiale du personnage 2

    # musique
    pygame.mixer.music.load("sons/musique.mp3")
    pygame.mixer.music.play(10)

    continuer = 1  # variable booléene des boucles événementielles

    temps_init = pygame.time.get_ticks()
    booleen = False  # booleen utilisé pour les phrases d'introduction

    taille = [2, 1]  # variable contenant la taille de l'image fight
    image_bulleR = pygame.transform.scale(pygame.image.load("ressources/bulle.png"), (150, 111)).convert_alpha()
    image_bulleL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("ressources/bulle.png"), (150, 111)),
                                         1, 0).convert_alpha()
    # première boucle d'événement : cinématique de début
    while continuer:
        pygame.display.flip()
        rafraichissement(ecran, fond_ecran, personnage1, personnage2)
        temps = pygame.time.get_ticks() - temps_init

        if temps <= 5000:  # compte à rebours 5,4,3,2,1
            compte_a_rebours = police_taille80.render(str((6000 - (pygame.time.get_ticks() - temps_init)) // 1000), 1,
                                                      (0, 0, 0))
            ecran.blit(compte_a_rebours, (400, 250))

        if temps <= 2000:  # bulle et son personnage 1
            ecran.blit(image_bulleR, (100, SOL - 80))
            ecran.blit(police_taille14.render(personnage1.texte_menace, 1, (0, 0, 0)), (103, SOL - 40))
            if booleen == False:
                personnage1.son_menace.play()
                booleen = True

        if temps > 2000:  # bulle et son personnage 2
            ecran.blit(image_bulleL, (580, SOL - 80))
            ecran.blit(police_taille14.render(personnage2.texte_menace, 1, (0, 0, 0)), (592, SOL - 40))
            if booleen == True:
                personnage2.son_menace.play()
                booleen = False

        if temps > 5000 and taille[0] < 200:  # grossit l'image "fight"
            image_fight = pygame.transform.scale(pygame.image.load("ressources/fight.png"), taille).convert_alpha()
            ecran.blit(image_fight, (340, 250))
            taille[0] += 4
            taille[1] += 2

        if taille[0] >= 200:  # on arrête de faire grossir l'image "fight"
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0

    personnages = [personnage1, personnage2]
    # boucle d'évènements
    while continuer:
        for personnage in personnages:
            personnage.saut(personnage.vitessex,
                            personnage.vitessey)  # on lance la méthode saut qui ne fait rien si les deux vitesses valent 0 et qui sinon déplacent le personnage
            if personnage.position_personnage[1] < SOL:  # si le personnage est en l'air, on simule la gravité
                personnage.vitessey -= 0.15
            else:  # sinon on l'arrete
                personnage.vitessey = 0
                personnage.vitessex = 0

        for personnage in personnages:
            # on diminue le compteur d'action saut
            if personnage.cooldown_saut > 0:
                personnage.cooldown_saut -= 1

        for personnage in personnages:
            # si les invulérabilités sont supérieures 0 alors on affiche l'image du personnage touché
            if personnage.invulnerabilite > 0:
                personnage.affecter_personnage_courant("touche")
                personnage.invulnerabilite -= 1
        for personnage in personnages:
            # on diminue le cooldown des attaques tant que celui-ci est supérieur 0
            if personnage.cooldown_attaque > 0:
                personnage.cooldown_attaque -= 1

        for personnage in personnages:
            # on laisse l'image de l'attaque affichée tant que le cooldown supérieur 25
            if personnage.cooldown_attaque > 25:
                personnage.affecter_personnage_courant("attaque")

        sortirecran(personnage1, personnage2)  # on vérifie si les personnages sont toujours dans l'écran
        try:
            collision(personnage_tireur=personnage1,
                      personnage_cible=personnage2)  # on teste la collision avec les projectiles du personnage 1
        except AttributeError:
            pass
        try:
            collision(personnage_tireur=personnage2,
                      personnage_cible=personnage1)  # on teste la collision avec les projectiles du personnage 2
        except AttributeError:
            pass

        rafraichissement(ecran, fond_ecran, personnage1, personnage2)  # on rafraichit en replaçant tous les objets
        pygame.display.flip()  # on actualise

        # ---------------------------------------------------------------------------------------------------------
        # personnage 1
        if personnage1.vie > 0 and personnage2.vie > 0:  # si les deux personnages ont de la vie, le jeu continue
            # on capture les événements claviers
            if pygame.key.get_pressed()[k_gauche]:
                personnage1.deplacement(-personnage1.VITESSEX)

            if pygame.key.get_pressed()[k_droite]:
                personnage1.deplacement(personnage1.VITESSEX)

            if pygame.key.get_pressed()[k_haut]:
                personnage1.initsaut()

            if pygame.key.get_pressed()[k_attaque]:
                personnage1.attaque(personnage2)

        # si aucune touche n'a été pressée et que les personnages ne bougent pas on remet les images passives
        if not pygame.key.get_pressed()[k_gauche] and not pygame.key.get_pressed()[k_droite] and not \
        pygame.key.get_pressed()[k_haut] and not pygame.key.get_pressed()[k_attaque]:
            if personnage1.vitessex == 0 and personnage1.vitessey == 0:
                personnage1.affecter_personnage_courant("passif")

        # ---------------------------------------------------------------------------------------------------------
        # personnage 2
        if personnage2.vie > 0 and personnage1.vie > 0:  # si les deux personnages ont de la vie, le jeu continue
            # on capture les événements claviers
            if pygame.key.get_pressed()[K_LEFT]:
                personnage2.deplacement(-personnage2.VITESSEX)

            if pygame.key.get_pressed()[K_RIGHT]:
                personnage2.deplacement(personnage2.VITESSEX)

            if pygame.key.get_pressed()[K_UP]:
                personnage2.initsaut()

            if pygame.key.get_pressed()[K_RETURN]:
                personnage2.attaque(personnage1)

        # si aucune touche n'a été pressée et que les personnages ne bougent pas on remet les images passives
        if not pygame.key.get_pressed()[K_LEFT] and not pygame.key.get_pressed()[K_RIGHT] and not \
        pygame.key.get_pressed()[K_UP] and not pygame.key.get_pressed()[K_RETURN]:
            if personnage2.vitessex == 0 and personnage2.vitessey == 0:
                personnage2.affecter_personnage_courant("passif")

        # ---------------------------------------------------------------------------------------------------------
        # si un personnage est mort, on le ramène au sol
        if personnage1.vie <= 0:
            if personnage1.position_personnage[1] < SOL + 50:  # le 50 en plus simule la chute
                personnage1.position_personnage = personnage1.position_personnage.move(0, 10)
        if personnage2.vie <= 0:
            if personnage2.position_personnage[1] < SOL + 50:
                personnage2.position_personnage = personnage2.position_personnage.move(0, 10)

        # événement de type QUIT
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0

    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
