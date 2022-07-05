"""
#####################################
Outhor: Abdirizak abdullahi hussein #
Date:7/4/2022                       ###########################
Note: i have only the copyright of the code but images Source:#
	*flaticon												  #
	*walpapers eff											  #
###############################################################
"""


import pygame as pyg,random
from pygame.locals import*
from pygame import mixer


mixer.init()
global bullet_sound
#bullet sound when player shoot
bullet_sound = mixer.Sound('sounds/laser.wav')

#bullet class
class Bullet:
	def __init__(self,pos,image):
		self.x = pos[0]
		self.y = pos[1]
		self.image = image
		self.hight = image.get_height()
		self.width = image.get_width()
		self.rect = image.get_rect()
		self.rect.center = (self.x,self.y)
		self.bullet_speed = 8
	def draw(self,surface):
		self.bullet = surface.blit(self.image,[self.rect.x , self.rect.y])
	def move(self):
		self.rect.y -= self.bullet_speed
	def remove(self):
		self.rect.y = -1000
class Player:
	def __init__(self,pos,image,scr_width,bullet_img):
		self.x = pos[0]
		self.y = pos[1]
		self.image = image
		self.width = image.get_width()
		self.Player_speed = 5
		self.rect = image.get_rect()
		self.rect.center = (self.x,self.y)
		self.scr_width = scr_width
		self.Bullets = []
		self.bullet_img = bullet_img
		self.cool_down_count = 0#cooldown_count is allowing the bullet not be as chain like this -----
	def draw(self,surface):
	 	surface.blit(self.image,[self.rect.x,self.rect.y])
	def move(self,key_pressed):
		if key_pressed[K_RIGHT] and self.rect.x <= self.scr_width-self.width:
			self.rect.x += self.Player_speed
		if key_pressed[K_LEFT] and self.rect.x >= 0:
			self.rect.x -= self.Player_speed
	def cool_down_func(self):
		#if u wanna to increase the amount of bullet u shooting decrease the 25 below by 5
		if self.cool_down_count >=25:
			self.cool_down_count = 0
		if self.cool_down_count > 0:
			self.cool_down_count +=1
			if self.cool_down_count >=25:
				self.cool_down_count = 0
	def shoot(self,surface,key_pressed):
		self.cool_down_func()
		#when pressed space bar creating a bullet and adding into bullets list
		if key_pressed[K_SPACE] and self.cool_down_count == 0:
				self.Bullets.append(Bullet([self.rect.x+25+3,self.rect.y-8],self.bullet_img))
				self.cool_down_count = 1
				bullet_sound.play()
		for bullet in self.Bullets:
			bullet.draw(surface)
			bullet.move()

class Enemy:
	def __init__(self,x,y,image):
		self.width = image.get_width()
		self.hight = image.get_height()
		self.x =x 
		self.y = y
		self.image = image
		self.rect = image.get_rect()
		self.rect.center = (self.x,self.y)
		self.Enemy_speed = 3
		self.rigth = True 
		self.left = False
		self.bolock = 40 #this block when ever enemy hits the wall will falling by this block


	def draw(self,surface):
		self.enemy = surface.blit(self.image,[self.rect.x,self.rect.y])
	def move(self,screen_width,screen_hight):
		if self.rigth:
			if self.rect.x <=screen_width-self.width:
				self.rect.x += self.Enemy_speed
			else:
				if self.rect.y <480: #480 is the > player postion that means not moving any way
					self.rect.y += self.bolock
				self.rigth = False
				self.left = True
		if self.left:
			if self.rect.x >=0:
				self.rect.x -= self.Enemy_speed
			else:
				if self.rect.y <480:
					self.rect.y += self.bolock
				self.left = False
				self.rigth = True
	def restart(self):
		save = 0
		self.rect.y = 100
		self.rect.x = random.randint(0,800-64)
		self.Enemy_speed = 7
		save +=1
		if save >0:
			self.Enemy_speed = 8
		if save >3:
			self.Enemy_speed = 10
