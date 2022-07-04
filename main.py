import pygame as pyg,random as rand , sys , time
from pygame.locals import*
from classes import Player,Bullet,Enemy
from pygame import mixer

sw,sh = 800,600
pyg.init()
screen = pyg.display.set_mode([sw,sh])
pyg.display.set_caption('space-fire')
icon = pyg.image.load('images/ufo.png')
pyg.display.set_icon(icon)
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
fps = pyg.time.Clock()
score_count = 0

player =  Player([sw//3,sh-100],player_img,800,bullet_img)
enemy = Enemy(sw//3-50,100,enemy_img)


enemy_list = []
enemy_list.append(enemy)
def enemies(x,y,image):
	for e in range(7):
		enemy = Enemy(x,y,image)
		x += 200
		enemy_list.append(enemy)
enemies(0,180,enemy_img)

def score(score_count):
	nmfont = pyg.font.SysFont('carbel',36)
	txt = 'Dhibcaha: '+ str(score_count)	
	scrFont = nmfont.render(txt,True,'white')
	screen.blit(scrFont,[20,20])
def gameover():
	global bg
	screen.blit(bg,[0,0])
	nmfont = pyg.font.SysFont('carbel',70)
	txt = 'DHAMMAAD'	
	scrFont = nmfont.render(txt,True,'green')
	screen.blit(scrFont,[250,300])

	pyg.display.update()
	time.sleep(5)
	sys.exit()
Gameover = False
while not Gameover:
	screen.fill('black')
	fps.tick(60)
	screen.blit(bg,[0,0])
	#event handling
	for event in pyg.event.get():
		if event.type == QUIT:
			Gameover= True
	key_pressed = pyg.key.get_pressed()
	if key_pressed[K_ESCAPE]:
		Gameover = True
	player.draw(screen)
	player.move(key_pressed)
	player.shoot(screen,key_pressed) 
	for en in enemy_list:
		en.draw(screen)
		en.move(sw,sh)
		if en.rect.y >= player.rect.y:
			gameover()
		for buli in player.Bullets:
			if buli.rect.colliderect(en.rect):
				score_count+=1
				explosions.play()
				en.restart()
				buli.remove()
	score(score_count)
	pyg.display.update() 