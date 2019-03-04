#!/usr/bin/python3
# -*- coding: Utf-8 -*-

#---------------------------------------------------------------------------------------------------------
#Battle of Heroes
#Développé par Thibault AYANIDES et Eloi BOUTILLON
#License GPL v3
#Les images les sons et les polices utilisés ne nous appartiennent pas
#2015-2016
#---------------------------------------------------------------------------------------------------------

#Pygame
import pygame
from pygame.locals import *


def rafraichissement(ecran, fond_ecran, personnage1, personnage2):
	"""Rafraichîssement de l'écran. Affichage des widgets sur l'écran (barres de vie, personnages, projectiles)."""
	ecran.blit(fond_ecran, (0, 0))
	ecran.blit(personnage1.personnage_courant, personnage1.position_personnage)
	ecran.blit(personnage2.personnage_courant, personnage2.position_personnage)

	ecran.blit(personnage1.icone, (0, 0, 2*personnage1.vie, 20)) #icône du personnage 1
	pygame.draw.rect(ecran, (255,0,0), (100, 10, 2*personnage1.vie, 20))#barre de vie du personnage 1
	pygame.draw.rect(ecran, (0,0,0), (100, 10, 200, 20), 5)

	ecran.blit(personnage2.icone, (700, 0, -2*personnage2.vie, 20)) #icône du personnage 2
	pygame.draw.rect(ecran, (255,0,0), (700, 10, -2*personnage2.vie, 20)) #barre de vie du personnage 2
	pygame.draw.rect(ecran, (0,0,0), (500, 10, 200, 20), 5)
	try:
		for projectiles in personnage1.liste_projectile:
			if projectiles.position_projectile[0] < 800 or projectiles.position_projectile[0] > 0:
				projectiles.move()
				ecran.blit(personnage1.image_projectile, projectiles.position_projectile)
	except AttributeError:
		pass
	try:
		for projectiles in personnage2.liste_projectile:
			if projectiles.position_projectile[0] < 800 or projectiles.position_projectile[0] > 0:
				projectiles.move()
				ecran.blit(personnage2.image_projectile, projectiles.position_projectile)
	except AttributeError:
         pass

def sortirecran(*personnages):
	"""Fonction testant si les personnages sont dans l'écran. S'ils ne le sont pas, on les remets dans l'écran."""
	for monpersonnage in personnages:
		if monpersonnage.position_personnage[0] <= 0:
			monpersonnage.position_personnage[0] = 0
			monpersonnage.vitessex = 0

		if monpersonnage.position_personnage[0] >= 720:
			monpersonnage.position_personnage[0] = 720
			monpersonnage.vitessex = 0

		if monpersonnage.position_personnage[1] <= 0:
			monpersonnage.position_personnage[1] = 0
			monpersonnage.vitessey =- 1



def collision(personnage_tireur="", personnage_cible=""):
	"""Teste si les collisions entre les projectiles du mage et l'autre personnage."""
	if personnage_cible.invulnerabilite == 0 : #Si le personnage n'est pas invulnérable
		estcollision = 0
		for i, projectiles in enumerate(personnage_tireur.liste_projectile):
			if projectiles.position_projectile[0] < 800 or projectiles.position_projectile[0] > 0:
				estcollision = personnage_cible.position_personnage.colliderect(projectiles.position_projectile)
			if estcollision == 1: #si collision
				del personnage_tireur.liste_projectile[i]
				personnage_cible.invulnerabilite += 60
				personnage_cible.affecter_personnage_courant("touche")
				personnage_cible.blesse(7)
				son = pygame.mixer.Sound("sons/touche.ogg")
				son.play()
