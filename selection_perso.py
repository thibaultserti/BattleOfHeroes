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
import sys

def selection_perso():
	if sys.platform == "win32":
		k_haut = K_w
		k_bas = K_s
		k_droite = K_d
		k_gauche = K_a
		k_attaque = K_q
	elif sys.platform == "linux":
		k_haut = K_z
		k_bas = K_s
		k_droite = K_d
		k_gauche = K_q
		k_attaque = K_a

	pygame.init()
	police_taille80 = pygame.font.Font("polices/magic.ttf", 80) #polices d'écriture
	ecran = pygame.display.set_mode((800, 600),pygame.FULLSCREEN)
	pygame.display.set_caption("Battle of Heroes")
	pygame.mouse.set_visible(False) #on rend la souris invisible
	fond_ecran = pygame.transform.scale(pygame.image.load("ressources/fond_ecran_selection.jpg"), (800, 600)).convert()
	liste_personnage = list()
	cadre_vignette = pygame.image.load("ressources/cadre_vignette.png").convert_alpha()

	ecran.blit(fond_ecran, (0, 0))

	#positionnement des icônes et des cadres
	for i in range(1, 13):
		try: #pour ajouter des nouveaux personnages, il suffit de remplir la liste classes avec le nom des nouvelles classes et mettre la vignette dans vignettes
			liste_personnage.append(pygame.transform.scale(pygame.image.load("vignettes/personnage" + str(i) + ".png"), (100, 100)).convert())
		except pygame.error:
			break



	#positionnement des cadres de sélection
	cadre1 = pygame.image.load("ressources/cadre_selection.png").convert_alpha() #joueur 1
	cadre1_position = cadre1.get_rect()
	cadre1_position = cadre1_position.move (50, 100)

	cadre2 = pygame.image.load("ressources/cadre_selection.png").convert_alpha() #joueur 2
	cadre2_position = cadre2.get_rect()
	cadre2_position = cadre2_position.move (450, 100)

	label_joueur1 = police_taille80.render("Joueur 1", 1, (0,0,0))
	label_joueur2 = police_taille80.render("Joueur 2", 1, (0,0,0))

	#musique
	pygame.mixer.music.load("sons/musique_selection.ogg")
	pygame.mixer.music.play()

	continuer = 1
	personnage_selectionne1, personnage_selectionne2 = 1, 1
	personnage_choisi1, personnage_choisi2 = None, None
	classes = ["mage", "guerrier"]
	while continuer:
		ecran.blit(fond_ecran, (0, 0))

		ecran.blit(label_joueur1, (100, 10))
		ecran.blit(label_joueur2, (500, 10))

		for i in range(2):
			ecran.blit(liste_personnage[i],((50 + 100 * i) % 400, 100 * ((i) // 3 + 1)))
			ecran.blit(cadre_vignette, ((50 + 100 * i) % 400, 100 * ((i) // 3 + 1)))
			ecran.blit(liste_personnage[i],((50 + 100 * i) % 400 + 400, 100 * ((i) // 3 + 1)))
			ecran.blit(cadre_vignette, ((50 + 100 * i) % 400 + 400, 100 * ((i) // 3 + 1)))

		ecran.blit(cadre1, (cadre1_position[0], cadre1_position[1]))
		ecran.blit(cadre2, (cadre2_position[0], cadre2_position[1]))

		pygame.display.flip()

		if personnage_choisi1 is not None and personnage_choisi2 is not None: #si les deux joueur ont choisi, on lance le jeu
			return classes[personnage_choisi1 - 1], classes[personnage_choisi2 - 1]
			break

		#événement de type QUIT
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer = 0

				#choix du personnage du joueur 1
				if personnage_choisi1 is None:
					if event.key == k_gauche and personnage_selectionne1 %3 != 1:
						personnage_selectionne1 -= 1
						cadre1_position = cadre1_position.move (- 100, 0)
					if event.key == k_droite and personnage_selectionne1 %3 != 0 and personnage_selectionne1 + 1 <= len(liste_personnage):
						personnage_selectionne1 += 1
						cadre1_position = cadre1_position.move (100, 0)
					if event.key == k_haut and personnage_selectionne1 > 3:
						personnage_selectionne1 -= 3
						cadre1_position = cadre1_position.move (0, - 100)
					if event.key == k_bas and personnage_selectionne1 + 3 <= len(liste_personnage):
						personnage_selectionne1 += 3
						cadre1_position = cadre1_position.move (0, 100)

					#quand le personnage est choisit
					if event.key == k_attaque:
						personnage_choisi1 = personnage_selectionne1

				#choix du personnage du joueur 2
				if personnage_choisi2 is None:
					if event.key == K_LEFT and personnage_selectionne2 % 3 != 1 :
						personnage_selectionne2 -= 1
						cadre2_position = cadre2_position.move (-100, 0)
					if event.key == K_RIGHT and personnage_selectionne2 % 3 != 0 and personnage_selectionne2 + 1 <= len(liste_personnage):
						personnage_selectionne2 += 1
						cadre2_position = cadre2_position.move (100, 0)
					if event.key == K_UP and personnage_selectionne2 > 3:
						personnage_selectionne2 -= 3
						cadre2_position = cadre2_position.move (0, - 100)
					if event.key == K_DOWN and personnage_selectionne2 + 3 <= len(liste_personnage):
						personnage_selectionne2 += 3
						cadre2_position = cadre2_position.move (0, 100)

					#quand le personnage est choisit
					if event.key == K_RETURN:
						personnage_choisi2 = personnage_selectionne2

	pygame.quit()
	sys.exit(0)
