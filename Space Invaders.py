import pygame as pg
import os 
import time 
import random

#initialize the game 
pg.init()
pg.font.init()

#Window in tuple
WIDTH, HEIGHT = 750, 750
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('SPACE INVADERS')


#load all the images 
BACK_BLACK = pg.transform.scale(pg.image.load(os.path.join('assets', 'background-black.png')), (WIDTH,HEIGHT))
#lasers
LASER_BLUE = pg.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
LASER_GREEN = pg.image.load(os.path.join('assets', 'pixel_laser_green.png'))
LASER_YELLOW = pg.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
LASER_RED = pg.image.load(os.path.join('assets', 'pixel_laser_red.png'))
#blit's in our game
SHIP_BLUE_SMALL = pg.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
SHIP_GREEN_SMALL = pg.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
SHIP_RED_SMALL = pg.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
SHIP_YELLOW = pg.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))
pg.display.set_icon(SHIP_YELLOW)

class Laser:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pg.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self, vel):
		self.y += vel

	#if the laser is off screen
	def off_screen(self, height):
		return not (self.y <= height and self.y >= 0)
	
	def collision(self, obj):
		return collide(self, obj)

class Ship:

	COOLDOWN = 30

	def __init__(self, x, y, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_png = None 
		self.laser_png = None
		self.lasers = []
		self.cool_down_counter = 0
        
	def draw(self, window):
	    window.blit(self.ship_png, (self.x, self.y))
	    for laser in self.lasers:
	    	laser.draw(window)

	def move_lasers(self, vel, obj):
		self.cooldown
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				obj.health -= 10
				self.lasers.remove(laser)

	def cooldown(self):
		if self.cool_down_counter >= self.COOLDOWN:
			self.cool_down_counter = 0

		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_png)
			self.lasers.append(laser)
			self.cool_down_counter = 1
        
class Player(Ship):
    def __init__(self, x, y, health=100):
        #to use the player initialization on this
        super().__init__(x, y, health)
        self.ship_png = SHIP_YELLOW
        self.laser_png = LASER_YELLOW
        self.max_health = health
        #for pixel and collision mechanics 
        self.mask = pg.mask.from_surface(self.ship_png)

    def move_lasers(self, vel, objs):
    	self.cooldown()
    	for laser in self.lasers:
    		laser.move(vel)
    		if laser.off_screen(HEIGHT):
    			self.lasers.remove(laser)
    		else:
    			for obj in objs:
    				if laser.collision(obj):
    					objs.remove(obj)
    					self.lasers.remove(laser)

class Enemy(Ship):
    #Create a dictionary full for laser_ship and their colours
    LASER_MAP = {
                    "green" : (SHIP_GREEN_SMALL, LASER_GREEN),
                    "red" : (SHIP_RED_SMALL, LASER_RED),
                    "blue" : (SHIP_BLUE_SMALL, LASER_BLUE) 
                }
                    
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_png, self.laser_png = self.LASER_MAP[color]
        self.mask = pg.mask.from_surface(self.ship_png)
        
    def move(self, velocity):
        self.y += velocity

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))

def main():
    #setting FPS = 60, to run game at the same speed regardless of computer speed
    run = True
    FPS = 60
    level = 0
    lives = 5
    player_speed = 5
    laser_speed = 4
    clock = pg.time.Clock()
    main_font = pg.font.SysFont('comicsans', 50)

    player = Player(300, 620)
    
    all_enemies = []
    wave_length = 5 #decides the number of enemy ships as level increases
    enemy_speed = 1
    
    lost = False
    lost_count = -0
    
        
    def redraw():
        WIN.blit(BACK_BLACK, (0,0))
        #convert fonts to images by rendering
        lives_caption = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_caption = main_font.render(f"Level: {level}", 1, (255,255,255))
        WIN.blit(lives_caption, (10,10))
        WIN.blit(level_caption, (WIDTH-level_caption.get_width()-10, 10))
        
        for enemy in all_enemies:
            enemy.draw(WIN)
        
        if lost:
            lost_caption = main_font.render(f"You Lost", 1, (255,255,255))
            WIN.blit(lost_caption, (WIDTH/2 - lost_caption.get_width()/2, HEIGHT/2))
        player.draw(WIN)
        
        #draw a rectangle:
        pg.draw.rect(WIN, (0,255,0), (player.x , player.y + player.ship_png.get_height()+5, player.ship_png.get_width(), 18))
            
        pg.display.update()
        
    while run:
        clock.tick(FPS)
        redraw()
        
        if lives<=0 or player.health<=0:
            lost = True
            lost_count+=1
        
        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue
            
        if len(all_enemies) == 0:
            level+=1
            wave_length+=5 
            for enemy in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(['green', 'blue', 'red']))
                all_enemies.append(enemy)
        
        
        '''input keys from user, keys (is  dictionary giving on, off for each key)
            (and it's outside for loop, because for every frame *FPS* we will check if 
             Key is pressed) '''
        keys = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                run = False
                
        if keys[pg.K_RIGHT] and player.x < WIDTH - player.ship_png.get_width(): # right
            player.x += player_speed
        if keys[pg.K_LEFT] and player.x > 0: #left
            player.x -= player_speed
        if keys[pg.K_DOWN] and player.y < HEIGHT - player.ship_png.get_height() - 20: #down
            player.y += player_speed
        if keys[pg.K_UP] and player.y > 0: # up
            player.y -= player_speed
       	if keys[pg.K_SPACE]:
       		player.shoot()
        
        for enemy in all_enemies[:]:
            enemy.move(enemy_speed)
            enemy.move_lasers(laser_speed, player)

            if random.randrange(0, 8*60) == 1:
            	enemy.shoot()    

            if enemy.y + enemy.ship_png.get_height() > HEIGHT:
                lives -=1
                all_enemies.remove(enemy)

        player.move_lasers(-laser_speed, all_enemies)
        

main()

