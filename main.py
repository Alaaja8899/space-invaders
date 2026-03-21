"""
#####################################
Outhor: Abdirizak abdullahi hussein #
Date:7/4/2022                       ###########################
Note: i have only the copyright of the code but images Source:#
	*flaticon												  #
	*walpapers eff											  #
###############################################################
"""



import pygame as pyg,random as rand , sys , time
from pygame.locals import*

#importing the classes from classes file
from classes import Player,Bullet,Enemy,EnemyBullet
from pygame import mixer
#screen width screen height 
sw,sh = 800,600
#preparing the screen 
pyg.init()
screen = pyg.display.set_mode([sw,sh])
pyg.display.set_caption('space-fire')
#setting icon for our window game
icon = pyg.image.load('images/ufo.png')
pyg.display.set_icon(icon)
#init for pygame fonts
pyg.font.init()
#game sounds
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)
explosions = pyg.mixer.Sound('sounds/explosion.wav')
#images 
bg = pyg.image.load('images/background.png')
player_img = pyg.image.load('images/Player.png')
bullet_img = pyg.image.load('images/bullet.png')
enemy_img =  pyg.image.load('images/enemy.png')
#game variables
fps = pyg.time.Clock()#frame per second
#score counter
score_count = 0

player =  Player([sw//3,sh-100],player_img,800,bullet_img)
enemy = Enemy(sw//3-50,100,enemy_img)

#new enemies creating and adding into the list
enemy_list = []
enemy_list.append(enemy)
def enemies(x,y,image):
	for e in range(7):
		enemy = Enemy(x,y,image)
		x += 200
		enemy_list.append(enemy)
enemies(0,180,enemy_img)
#ui function
def draw_ui(score_count, health):
	nmfont = pyg.font.SysFont('carbel',36)
	txt = 'Score: '+ str(score_count)	
	scrFont = nmfont.render(txt,True,'white')
	screen.blit(scrFont,[20,20])
	
	health_txt = 'Health: '+ str(health)
	health_surf = nmfont.render(health_txt,True,'red')
	screen.blit(health_surf,[sw - 150, 20])

#game over surface
def gameover():
	global bg
	screen.blit(bg,[0,0])
	nmfont = pyg.font.SysFont('carbel',70)
	txt = 'END GAME'	
	scrFont = nmfont.render(txt,True,'green')
	screen.blit(scrFont,[250,300])

	pyg.display.update()
	time.sleep(5)
	sys.exit()
Gameover = False
enemy_bullets = []
while not Gameover:
	screen.fill('black')
	fps.tick(60)
	#background
	screen.blit(bg,[0,0])
	#event handling
	for event in pyg.event.get():
		if event.type == QUIT:
			Gameover= True

	#keystrokes listening and returning what key is pressed
	key_pressed = pyg.key.get_pressed()
	
	#if keypressed is K_ESCAPE that means the game will exit 
	if key_pressed[K_ESCAPE]:
		Gameover = True

	#drawing,moving,shooting for the player
	player.draw(screen)
	player.move(key_pressed)
	player.shoot(screen,key_pressed) 
	#iterating enemy list and ; drawing moving ,checking collision
	for en in enemy_list[:]:
		en.draw(screen)
		en.move(sw,sh)

		if rand.randint(1, 150) == 1:
			enemy_bullets.append(EnemyBullet((en.rect.centerx, en.rect.bottom)))

		if en.rect.y >= player.rect.y:
			gameover()
		for buli in player.Bullets:
			if buli.rect.colliderect(en.rect):
				#when ever the bullet colliderect enemy score+=1
				score_count+=1
				explosions.play()
				#and enemy will vanish from the screen 
				if en in enemy_list:
					enemy_list.remove(en)
				# and removing the bullet
				buli.remove()

	# handle enemy bullets
	for e_bul in enemy_bullets[:]:
		e_bul.draw(screen)
		e_bul.move()
		if e_bul.rect.colliderect(player.rect):
			player.health -= 20
			explosions.play()
			enemy_bullets.remove(e_bul)
			if player.health <= 0:
				gameover()
		elif e_bul.rect.y > sh:
			enemy_bullets.remove(e_bul)

	#ui count function
	draw_ui(score_count, player.health)
	pyg.display.update() 
