import random 
import numpy as np 

# Import the pygame module
import pygame

import time

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
	RLEACCEL,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_SPACE,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.image.load("p1_walk10.png").convert_alpha()
		# self.surf = pygame.transform.scale(self.surf, (50,50))
		# self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		# self.surf = pygame.Surface((75, 25))
		# self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect()

		self.gravity = np.array([0, 2])
		self.velocity = np.array([0, 0]) # x, y

		self.collision_with = None

	def is_colliding(self, obj):
		self.collision_with = obj

	def where_collision(self, colliding_object):
		Ro = colliding_object.rect
		Rp = self.rect

		

	def move(self, pos):

		if self.collision_with == None:
			self.move_ip(*pos)
		else:
			c = self.collision_with.rect
			ccent = ((c.left + c.right)/2, (c.top + c.bottom)/2)
			s = self.rect
			scent = ((s.left + s.right)/2, (s.top + s.bottom)/2)

			if (s.top > c.bottom) and (s.cent ):
				s.top = c.bottom



	# Move the sprite based on user keypresses
	def update(self, pressed_keys):

		is_not_coll = (self.collision_with == None)

		# Update based on velocity
		if self.rect.bottom <= 600:
			if is_not_coll:
				print('no collision')
				self.velocity = self.velocity + self.gravity
				self.rect.move_ip(self.velocity[0], self.velocity[1])
			else:
				print('collision')
		else:
			if is_not_coll:
				self.rect.bottom = SCREEN_HEIGHT
				self.velocity[1] = 1
		# self.gravity -= 1
		
		# Keep player on the screen
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT

		if not(is_not_coll):
			self.rect.bottom = self.collision_with.rect.top+1
			self.collision_with = None

		if pressed_keys[K_SPACE] or pressed_keys[K_UP]:
			self.velocity[1] = -20
			self.rect.move_ip(0, -1)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 20)
			# move_down_sound.play()
			# self.gravity += 0.01
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-15, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(15, 0)

from threading import Lock
class Stats:

	def __init__(self):

		self.score = 0
		self.lock = Lock()

	def add_score(self):

		self.lock.acquire()
		self.score += 1
		self.lock.release()

stats = Stats()


class World(pygame.sprite.Sprite):

	def __init__(self, w_type='grass', stretch=5):
		super(World, self).__init__()

		if w_type == None:
			raise NotImplementedError('Please supply a world type')

		elif w_type == 'grass':
			self.surfs = [pygame.image.load('grass_block_me.png').convert_alpha() for _ in range(stretch)]
			h, w = self.surfs[0].get_height(), self.surfs[0].get_width()
			self.surf = pygame.Surface((w * stretch, h))
			self.rect = self.surf.get_rect()

			for i in range(len(self.surfs)):
				self.surf.blit(self.surfs[i], (w*i, 0))

			self.rect.move_ip(0, 500)



# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
	def __init__(self):

		global stats
		self.stats = stats

		super(Enemy, self).__init__()
		# self.surf = pygame.Surface((20, 10))
		# self.surf.fill((255, 255, 255))
		self.surf = pygame.image.load('rocket.jpg')
		self.surf = pygame.transform.scale(self.surf, (40, 40))
		# self.surf.set_colorkey((255, 0, 0), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
				random.randint(0, SCREEN_HEIGHT),
			)
		)
		self.speed = random.randint(3, 6)

	# Move the sprite based on speed
	# Remove the sprite when it passes the left edge of the screen
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.stats.add_score()
			print(self.stats.score)
			self.kill()


# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        i = np.random.randint(3)
        self.surf = pygame.image.load("cloud" + str(i+1) + '.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        x0, y0, x1, y1 = self.rect
        h = abs(y1 - y0)
        w = abs(x1 - x0)
        # print(h,w)
        # self.surf = pygame.transform.scale(self.surf, (int(w/2), int(h/2)))	

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-2, 0)
        if self.rect.right < 0:
            self.kill()

# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 3000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

world = World()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
worlds = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

all_sprites.add(world)
worlds.add(world)


# Sound Settings

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("electric.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("smb_mariodie.wav")



# Variable to keep the main loop running
running = True

# Main loop
while running:
	# for loop through the event queue
	for event in pygame.event.get():
		# Check for KEYDOWN event
		if event.type == KEYDOWN:
			# If the Esc key is pressed, then exit the main loop
			if event.key == K_ESCAPE:
				running = False
		# Check for QUIT event. If QUIT, then set running to false.
		elif event.type == QUIT:
			running = False

		# Add a new enemy?
		elif event.type == ADDENEMY:
			# Create the new enemy and add it to sprite groups
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)

		elif event.type == ADDCLOUD:
			new_cloud = Cloud()
			clouds.add(new_cloud)
			all_sprites.add(new_cloud)

	pressed_keys = pygame.key.get_pressed()


	# Update enemy position
	enemies.update()
	clouds.update()

	# Fill the screen with black
	screen.fill((135, 206, 250))

	# Draw all sprites
	for entity in clouds:
		screen.blit(entity.surf, entity.rect)

	for entity in enemies:
		screen.blit(entity.surf, entity.rect)

	for entity in worlds:
		screen.blit(entity.surf, entity.rect)

	screen.blit(player.surf, player.rect)

	# Update the display
	pygame.display.flip()

	# Check if any enemies have collided with the player
	if pygame.sprite.spritecollideany(player, enemies):
		# If so, then remove the player and stop the loop
		player.kill()

		pygame.mixer.music.stop()
		move_up_sound.stop()
		move_down_sound.stop()
		collision_sound.play()

		# time.sleep(collision_sound.get_length())

		# running = False

	who_world = pygame.sprite.spritecollide(player, worlds, dokill=False)
	if who_world:
		# print(who_world)
		for world_obj in who_world:
			# print(world_obj)
			player.is_colliding( world_obj )

	player.update(pressed_keys)

	# Ensure program maintains a rate of 30 frames per second
	clock.tick(60)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()
