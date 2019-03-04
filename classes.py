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
#os
import os

class Projectile:
	"""Classe des projectiles du mage"""
	def __init__(self):
		"""Initialisation de la taille du projectile et de sa direction initiale"""
		self.TAILLE = (60,40)
		self.direction = "R"

	def creer_projectile(self, image, position0x, position0y, direction):
		"""Création du projectile en fonction de la position du personnage et de sa direction"""
		if direction == "R":
			self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(image), self.TAILLE).convert_alpha(), 1, 0)
		elif direction =="L":
			self.image = pygame.transform.scale(pygame.image.load(image), self.TAILLE).convert_alpha()

		self.position_projectile = self.image.get_rect() #position du projectile
		self.position_init = (position0x, position0y) #position initiale
		self.position_projectile = self.position_projectile.move(position0x, position0y)
		self.vitesse = 6
		self.direction = "" #direction

	def move(self):
		"""Déplace le projectile vers la droite ou vers la gauche selon sa direction"""
		if self.direction == "R":
			self.position_projectile = self.position_projectile.move(self.vitesse, 0)
		elif self.direction =="L":
			self.position_projectile = self.position_projectile.move(-self.vitesse, 0)

class Personnage:
	"""Classes des personnages utilisés par les deux joueurs"""
	def __init__(self):
		"""Constructeur de la classe : déclaration des variables de l'objet"""
		self.icone = ""
		self.indice_position_courant = 0 #position de personnage pendant déplacement

		self.cooldown_attaque = 0 #définit le temps durant lequel le personnage ne peut pas attaquer
		self.cooldown_saut = 0 #définit le temps durant lequel le personnage ne peut pas sauter
		self.invulnerabilite = 0 #définit le temps durant lequel le personnage ne peut pas prendre de coup


		self.vitessex = 0 #définit la vitesse sur l'axe des x (i.e la distance parcourue en pixels à chaque itération de la boucle.)
		self.vitessey = 0 #définit la vitesse sur l'axe des y (i.e la distance parcourue en pixels à chaque itération de la boucle.)
		self.vie = 100

	def deplacement(self, x):
		"""Fonction permettant de gérer le déplacement des personnages en fonction de leur direction. Gère également l'animation de marche"""
		if x > 0:
			self.direction = "R"
			self.personnage_courant = self.liste_personnage_R[int(self.indice_position_courant)]

		if x < 0:
			self.direction = "L"
			self.personnage_courant = self.liste_personnage_L[int(self.indice_position_courant)]

		self.position_personnage = self.position_personnage.move(x, 0)

		self.indice_position_courant += 0.1 #on incrémente le compteur pour que le prochaine appel de la fonction déplacement charge l'image suivante
		self.indice_position_courant %= 2

	def saut(self, distancex, distancey):
		"""Si les paramètres donnés sont différents de 0, on change l'image et on applique le déplacement dans la direction voulue"""
		if distancex != 0 or distancey != 0:
			if self.direction == "R":
				self.position_personnage = self.position_personnage.move(distancex, -distancey)

			elif self.direction == "L":
				self.position_personnage = self.position_personnage.move(-distancex, -distancey)

			self.affecter_personnage_courant("saut")

	def blesse(self, degats):
		"""Gère les dégats subits lors d'une collision"""
		if self.vie > 0 :
			self.vie -= degats #on applique les dégats
		if self.vie <= 0:
			self.vie = 0 #si la vie devient inférieur 0 on la remet à 0
			self.affecter_personnage_courant("mort")
			if self.direction == "R": #on définit l'image de mort comme nouvelle image de base
				self.passifR  = self.mortR
			if self.direction == "L":
				self.passifL  = self.mortL

	def affecter_personnage_courant(self, nouvelle_image):
		"""Fonction affectant une nouvelle image à la variable personnage_courant (i.e image courante)"""
		if self.direction == "R":
			self.personnage_courant = eval("self." + nouvelle_image + "R")
		elif self.direction == "L":
			self.personnage_courant = eval("self." + nouvelle_image + "L")

class Mage(Personnage):
	"""Classe héritant de Personnage et simulant la classe mage"""
	def __init__(self, direction):
		Personnage.__init__(self)
		os.chdir("mage/")

		self.CLASSE_PERSONNAGE = "mage"
		self.VITESSEX = 3
		self.VITESSESAUT = 9
		self.COOLDOWN_ATTAQUE = 50
		self.COOLDOWN_SAUT = 100

		self.direction = direction #initialisation de la direction de départ
		self.liste_projectile = []
		self.image_projectile = ""
		self.texte_menace = "Que la partie commence !"
		self.son_menace = pygame.mixer.Sound("menace.ogg")
		self.icone = pygame.transform.scale(pygame.image.load("icone.png"), (100, 150)).convert_alpha()
		self.liste_personnage_R, self.liste_personnage_L = list(), list()

		for i in range(2):
			self.liste_personnage_R.append(pygame.transform.scale(pygame.image.load("personnage" + str(i) + ".png"), (92, 144)).convert_alpha())
			self.liste_personnage_L.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage" + str(i) + ".png"), (92, 144)), 1, 0).convert_alpha())

		self.attaqueR = pygame.transform.scale(pygame.image.load("personnage_attaque.png"), (100, 144)).convert_alpha()
		self.attaqueL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_attaque.png"), (100, 144)), 1, 0).convert_alpha()
		self.volR = pygame.transform.scale(pygame.image.load("personnage_vol.png"), (64, 124)).convert_alpha()
		self.volL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_vol.png"), (64, 124)), 1, 0).convert_alpha()
		self.sautR = pygame.transform.scale(pygame.image.load("personnage_saut.png"), (106, 114)).convert_alpha()
		self.sautL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_saut.png"), (106, 114)), 1, 0).convert_alpha()
		self.toucheR = pygame.transform.scale(pygame.image.load("personnage_touche.png"), (110, 100)).convert_alpha()
		self.toucheL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_touche.png"), (110, 100)), 1, 0).convert_alpha()
		self.mortR = pygame.transform.scale(pygame.image.load("personnage_mort.png"), (140, 100)).convert_alpha()
		self.mortL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_mort.png"), (140, 100)), 1, 0).convert_alpha()

		self.passifR = pygame.transform.scale(pygame.image.load("personnage.png"), (92, 144)).convert_alpha()
		self.passifL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage.png"), (92, 144)), 1, 0).convert_alpha()

		self.personnage_courant = eval("self.passif" + direction) #on commence sur la direction donnée lors de la construction de l'objet
		self.position_personnage = self.personnage_courant.get_rect()

		os.chdir("../")

	def attaque(self, personnage):
		"""Gère l'attaque de boule de feu du mage en créant les objets Projectiles"""
		if self.cooldown_attaque == 0:
			son = pygame.mixer.Sound("sons/tir.ogg")
			son.play()
			os.chdir(self.CLASSE_PERSONNAGE + "/")
			self.cooldown_attaque = 50

			if self.direction == "R":
				projectile = Projectile()
				projectile.creer_projectile("projectile.png", self.position_personnage[0] + 30, self.position_personnage[1] + 30,"R")
				self.liste_projectile.append(projectile)
				self.image_projectile = projectile.image
				projectile.direction = "R"

			elif self.direction == "L":
				projectile = Projectile() #on créé un objet Projectile
				projectile.creer_projectile("projectile.png", self.position_personnage[0], self.position_personnage[1] + 30,"L")
				self.liste_projectile.append(projectile) #on l'ajoute à la liste des projectiles du personnage
				self.image_projectile = projectile.image
				projectile.direction = "L"

			self.affecter_personnage_courant("attaque")
			os.chdir("../")

	def initsaut(self):
		if self.cooldown_saut == 0:
			self.vitessey = self.VITESSESAUT
			self.cooldown_saut = self.COOLDOWN_SAUT

class Guerrier(Personnage):
	"""Classe héritant de Personnage et simulant la classe guerrier"""
	def __init__(self, direction):
		Personnage.__init__(self)
		os.chdir("guerrier/")

		self.CLASSE_PERSONNAGE = "guerrier"
		self.VITESSEX = 3
		self.VITESSESAUT = 9
		self.COOLDOWN_ATTAQUE = 50
		self.COOLDOWN_SAUT = 100

		self.direction = direction #initialisation de la direction de départ
		self.texte_menace = "Que justice soit faite !"
		self.son_menace = pygame.mixer.Sound("menace.ogg")
		self.icone = pygame.transform.scale(pygame.image.load("icone.png"), (100, 150)).convert_alpha()
		self.liste_personnage_R, self.liste_personnage_L = list(), list()

		for i in range(2):
			self.liste_personnage_R.append(pygame.transform.scale(pygame.image.load("personnage" + str(i) + ".png"), (92, 144)).convert_alpha())
			self.liste_personnage_L.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage" + str(i) + ".png"), (92, 144)), 1, 0).convert_alpha())

		self.attaqueR = pygame.transform.scale(pygame.image.load("personnage_attaque.png"), (140, 144)).convert_alpha()
		self.attaqueL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_attaque.png"), (140, 144)), 1, 0).convert_alpha()
		self.volR = pygame.transform.scale(pygame.image.load("personnage_vol.png"), (64, 124)).convert_alpha()
		self.volL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_vol.png"), (64, 124)), 1, 0).convert_alpha()
		self.sautR = pygame.transform.scale(pygame.image.load("personnage_saut.png"), (92, 125)).convert_alpha()
		self.sautL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_saut.png"), (92, 125)), 1, 0).convert_alpha()
		self.toucheR = pygame.transform.scale(pygame.image.load("personnage_touche.png"), (92, 144)).convert_alpha()
		self.toucheL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_touche.png"), (92, 144)), 1, 0).convert_alpha()
		self.mortR = pygame.transform.scale(pygame.image.load("personnage_mort.png"), (140, 100)).convert_alpha()
		self.mortL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage_mort.png"), (140, 100)), 1, 0).convert_alpha()

		self.passifR = pygame.transform.scale(pygame.image.load("personnage.png"), (92, 144)).convert_alpha()
		self.passifL = pygame.transform.flip(pygame.transform.scale(pygame.image.load("personnage.png"), (92, 144)), 1, 0).convert_alpha()

		self.personnage_courant = eval("self.passif" + direction) #on commence sur la direction donnée lors de la construction de l'objet
		self.position_personnage = self.personnage_courant.get_rect()

		os.chdir("../")

	def attaque(self, personnage):
		"""Gère l'attaque du guerrier ainsi que la collision de l'attaque avec un potentiel personnage"""
		if self.cooldown_attaque == 0:
			os.chdir(self.CLASSE_PERSONNAGE + "/")
			self.cooldown_attaque = 50

			if self.direction == "R":
				iscollision = self.position_personnage.move(25, 0).colliderect(personnage.position_personnage) #le .move est la pour équilibrer les collisions
			if self.direction == "L":
				iscollision = self.position_personnage.colliderect(personnage.position_personnage)
			if iscollision == 1: #si collision

				son = pygame.mixer.Sound("../sons/coup.ogg")
				son.play() #on joue le son

				personnage.affecter_personnage_courant("touche")
				personnage.blesse(5)
				personnage.cooldown_attaque += 25
				personnage.invulnerabilite += 40 #définit le temps avant de pouvoir reprendre un coup
				if personnage.direction == self.direction: #on donne une vitesse au personnage touche afin de simuler le recul
					personnage.vitessey = 2
					personnage.vitessex = 7
				else:
					personnage.vitessey = 2
					personnage.vitessex = -7

			self.affecter_personnage_courant("attaque")
			os.chdir("../")

	def initsaut(self):
		if self.cooldown_saut == 0:
			self.vitessey = self.VITESSESAUT
			self.cooldown_saut = self.COOLDOWN_SAUT

