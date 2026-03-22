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

class EnemyBullet:
	def __init__(self, pos, speed=5):
		self.x = pos[0]
		self.y = pos[1]
		self.speed = speed
		self.rect = pyg.Rect(self.x, self.y, 5, 15)
	def draw(self, surface):
		pyg.draw.rect(surface, "#D13100", self.rect)
	def move(self):
		self.rect.y += self.speed
	def remove(self):
		self.rect.y = 1000

class PowerUp:
	def __init__(self, pos, power_type):
		self.x = pos[0]
		self.y = pos[1]
		self.power_type = power_type
		self.speed = 2
		self.rect = pyg.Rect(self.x, self.y, 30, 30)
		self.colors = {
			'health': '#00FF00',
			'rapid_fire': '#FFFF00',
			'shield': '#00FFFF'
		}
	def draw(self, surface):
		pyg.draw.circle(surface, self.colors[self.power_type], self.rect.center, 15)
		pyg.draw.circle(surface, 'white', self.rect.center, 15, 2)
	def move(self):
		self.rect.y += self.speed

class Player:
	def __init__(self,pos,image,scr_width,bullet_img):
		self.x = pos[0]
		self.y = pos[1]
		self.image = image
		self.width = image.get_width()
		self.height = image.get_height()
		self.Player_speed = 5
		self.health = 100
		self.max_health = 100
		self.rect = image.get_rect()
		self.rect.center = (self.x,self.y)
		self.scr_width = scr_width
		self.Bullets = []
		self.bullet_img = bullet_img
		self.cool_down_count = 0
		self.rapid_fire = False
		self.rapid_fire_timer = 0
		self.shield = False
		self.shield_timer = 0#cooldown_count is allowing the bullet not be as chain like this -----
	def draw(self,surface):
	 	surface.blit(self.image,[self.rect.x,self.rect.y])
	 	if self.shield:
	 		pyg.draw.circle(surface, '#00FFFF', self.rect.center, 40, 3)
	def move(self,key_pressed):
		if key_pressed[K_RIGHT] and self.rect.x <= self.scr_width-self.width:
			self.rect.x += self.Player_speed
		if key_pressed[K_LEFT] and self.rect.x >= 0:
			self.rect.x -= self.Player_speed
		if key_pressed[K_UP] and self.rect.y >= 0:
			self.rect.y -= self.Player_speed
		if key_pressed[K_DOWN] and self.rect.y <= self.scr_width-self.height:
			self.rect.y += self.Player_speed

	def cool_down_func(self):
		cooldown_limit = 10 if self.rapid_fire else 25
		if self.cool_down_count >= cooldown_limit:
			self.cool_down_count = 0
		if self.cool_down_count > 0:
			self.cool_down_count += 1
			if self.cool_down_count >= cooldown_limit:
				self.cool_down_count = 0
		
		if self.rapid_fire_timer > 0:
			self.rapid_fire_timer -= 1
			if self.rapid_fire_timer == 0:
				self.rapid_fire = False
		
		if self.shield_timer > 0:
			self.shield_timer -= 1
			if self.shield_timer == 0:
				self.shield = False
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
	def __init__(self,x,y,image,enemy_type='normal'):
		self.width = image.get_width()
		self.hight = image.get_height()
		self.x =x 
		self.y = y
		self.image = image
		self.rect = image.get_rect()
		self.rect.center = (self.x,self.y)
		self.enemy_type = enemy_type
		if enemy_type == 'fast':
			self.Enemy_speed = 5
			self.bolock = 30
			self.health = 1
		elif enemy_type == 'tank':
			self.Enemy_speed = 2
			self.bolock = 50
			self.health = 3
		else:
			self.Enemy_speed = 3
			self.bolock = 40
			self.health = 1
		self.rigth = True 
		self.left = False #this block when ever enemy hits the wall will falling by this block


	def draw(self,surface):
		self.enemy = surface.blit(self.image,[self.rect.x,self.rect.y])
		if self.enemy_type == 'tank' and self.health > 1:
			pyg.draw.rect(surface, 'yellow', (self.rect.x, self.rect.y - 5, self.width * (self.health / 3), 3))
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
	def take_damage(self):
		self.health -= 1
		return self.health <= 0

class BossEnemy:
	def __init__(self, x, y, image):
		self.width = image.get_width() * 2
		self.height = image.get_height() * 2
		self.image = pyg.transform.scale(image, (int(self.width), int(self.height)))
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.speed = 2
		self.health = 20
		self.max_health = 20
		self.right = True
		self.shoot_pattern = 0
		
	def draw(self, surface):
		surface.blit(self.image, [self.rect.x, self.rect.y])
		health_bar_width = 100
		health_percentage = self.health / self.max_health
		pyg.draw.rect(surface, 'red', (self.rect.centerx - 50, self.rect.y - 15, health_bar_width, 8))
		pyg.draw.rect(surface, 'green', (self.rect.centerx - 50, self.rect.y - 15, health_bar_width * health_percentage, 8))
		
	def move(self, screen_width, screen_height):
		if self.right:
			if self.rect.x <= screen_width - self.width:
				self.rect.x += self.speed
			else:
				self.right = False
		else:
			if self.rect.x >= 0:
				self.rect.x -= self.speed
			else:
				self.right = True
				
	def take_damage(self):
		self.health -= 1
		return self.health <= 0
		
	def get_bullet_positions(self):
		self.shoot_pattern = (self.shoot_pattern + 1) % 3
		if self.shoot_pattern == 0:
			return [(self.rect.centerx, self.rect.bottom)]
		elif self.shoot_pattern == 1:
			return [(self.rect.left + 20, self.rect.bottom), (self.rect.right - 20, self.rect.bottom)]
		else:
			return [(self.rect.left + 20, self.rect.bottom), (self.rect.centerx, self.rect.bottom), (self.rect.right - 20, self.rect.bottom)]
