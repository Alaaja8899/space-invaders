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
from classes import Player,Bullet,Enemy,EnemyBullet,PowerUp,BossEnemy
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
wave_number = 1
max_wave = 10
enemies_per_wave = 7
power_ups = []
boss_active = False
boss = None
wave_complete_timer = 0

player =  Player([sw//3,sh-100],player_img,800,bullet_img)
enemy = Enemy(sw//3-50,100,enemy_img)

#new enemies creating and adding into the list
enemy_list = []
enemy_list.append(enemy)

def spawn_wave(wave_num):
	global enemy_list, boss_active, boss
	enemy_list.clear()
	
	if wave_num % 3 == 0:
		boss_active = True
		boss = BossEnemy(sw//2, 100, enemy_img)
		return
	
	x = 0
	y = 100 + (wave_num % 3) * 50
	num_enemies = min(enemies_per_wave + wave_num, 12)
	
	for e in range(num_enemies):
		if wave_num >= 5 and e % 3 == 0:
			enemy_type = 'tank'
		elif wave_num >= 3 and e % 2 == 0:
			enemy_type = 'fast'
		else:
			enemy_type = 'normal'
		
		enemy = Enemy(x, y, enemy_img, enemy_type)
		x += 150 if num_enemies > 8 else 200
		if x > sw - 100:
			x = 0
			y += 80
		enemy_list.append(enemy)

spawn_wave(wave_number)
#ui function
def draw_ui(score_count, health, wave_num):
	nmfont = pyg.font.SysFont('carbel',36)
	txt = 'Score: '+ str(score_count)	
	scrFont = nmfont.render(txt,True,'white')
	screen.blit(scrFont,[20,20])
	
	health_txt = 'Health: '+ str(health)
	health_surf = nmfont.render(health_txt,True,'red')
	screen.blit(health_surf,[sw - 200, 20])
	
	wave_txt = 'Wave: '+ str(wave_num)
	wave_surf = nmfont.render(wave_txt,True,'cyan')
	screen.blit(wave_surf,[sw//2 - 60, 20])
	
	if player.rapid_fire:
		rf_txt = 'RAPID FIRE!'
		rf_surf = nmfont.render(rf_txt, True, 'yellow')
		screen.blit(rf_surf, [20, 60])
	
	if player.shield:
		shield_txt = 'SHIELD ACTIVE'
		shield_surf = nmfont.render(shield_txt, True, 'cyan')
		screen.blit(shield_surf, [20, 100])

#game over surface
def gameover(win=False):
	global bg
	screen.blit(bg,[0,0])
	nmfont = pyg.font.SysFont('carbel',70)
	if win:
		txt = 'YOU WIN!'
		color = 'green'
	else:
		txt = 'END GAME'
		color = 'red'
	scrFont = nmfont.render(txt,True,color)
	screen.blit(scrFont,[250,300])

	pyg.display.update()
	time.sleep(5)
	sys.exit()
Gameover = False
enemy_bullets = []
frame_count = 0
while not Gameover:
	screen.fill('black')
	fps.tick(60)
	frame_count += 1
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
	
	# Handle boss enemy
	if boss_active and boss:
		boss.draw(screen)
		boss.move(sw, sh)
		
		if frame_count % 60 == 0:
			for pos in boss.get_bullet_positions():
				enemy_bullets.append(EnemyBullet(pos, speed=6))
		
		for buli in player.Bullets:
			if buli.rect.colliderect(boss.rect):
				if boss.take_damage():
					score_count += 50
					explosions.play()
					boss_active = False
					boss = None
					wave_complete_timer = 120
					if rand.randint(1, 2) == 1:
						power_type = rand.choice(['health', 'rapid_fire', 'shield'])
						power_ups.append(PowerUp((sw//2, 100), power_type))
				else:
					score_count += 5
				buli.remove()
	
	#iterating enemy list and ; drawing moving ,checking collision
	for en in enemy_list[:]:
		en.draw(screen)
		en.move(sw,sh)

		shoot_chance = max(50, 150 - wave_number * 10)
		if rand.randint(1, shoot_chance) == 1:
			bullet_speed = 5 + wave_number // 2
			enemy_bullets.append(EnemyBullet((en.rect.centerx, en.rect.bottom), speed=bullet_speed))

		if en.rect.y >= player.rect.y:
			gameover(win=False)
		for buli in player.Bullets:
			if buli.rect.colliderect(en.rect):
				if en.take_damage():
					score_count += 1
					explosions.play()
					if en in enemy_list:
						enemy_list.remove(en)
					
					if rand.randint(1, 15) == 1:
						power_type = rand.choice(['health', 'rapid_fire', 'shield'])
						power_ups.append(PowerUp((en.rect.centerx, en.rect.centery), power_type))
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
				gameover(win=False)
		elif e_bul.rect.y > sh:
			enemy_bullets.remove(e_bul)

	if not enemy_list:
		gameover(win=True)

	#ui count function
	draw_ui(score_count, player.health, wave_number)
	pyg.display.update() 
