import pygame as pg, sys, random

from pygame import display

pg.init()

class Player(pg.sprite.Sprite):
   def __init__(self, x, y): 
      super().__init__()
      self.gravity = 1.5
      self.vel_y = 1
      self.x, self.y = x, y
      self.image = pg.Surface((20, 20))
      self.rect = self.image.get_rect(center=(self.x, self.y))
      self.image.fill('red')
      self.jump_sound = pg.mixer.Sound('sound/sfx_wing.wav')

   def jump(self):
      self.rect.centery += self.vel_y
      self.vel_y += self.gravity
      if self.rect.top <= 0: 
         self.rect.top = 0
         self.vel_y = 1
      if self.rect.bottom >= h:
         self.rect.bottom = h
         self.vel_y = 1

   def reset(self): 
      self.gravity = 1.5
      self.vel_y = 1


class Tube(pg.sprite.Sprite):
   def __init__(self, x, y):
      super().__init__()     
      self.x, self.y = x, y
      self.speed = 5
      self.image = pg.Surface((50, h))
      self.rect = self.image.get_rect(center=(self.x, self.y))
      self.image.fill('green')
      self.tube_hit_sound = pg.mixer.Sound('sound/sfx_hit.wav')
      # NandeKoreKiiteneeNoKa?
         # self.hole = pg.draw.rect(screen, 'black', ((self.rect.centerx, random.randint(0, h-250)) , (60, 250)))

   def update(self):
      global hole_hit, game_active
      self.rect.centerx -= self.speed
      if self.rect.centerx < 0: self.kill()
      if self.rect.colliderect(player.rect) and hole_hit: hole_hit = True
      elif self.rect.colliderect(player.rect) and hole_hit == False:  game_active = False
      else: hole_hit = False
      # NandeKoreKiiteneeNoKa?
         # if self.hole.colliderect(player.rect): print(pg.time.get_ticks())


class Hole(pg.sprite.Sprite):
   def __init__(self, x, y, tube):
      super().__init__()
      self.x, self.y = x, y
      self.tube = tube
      self.image = pg.Surface((60, 250))
      self.rect = self.image.get_rect(center=(self.x, self.y))
      self.image.fill('#333333')
      self.update_score_sound = pg.mixer.Sound('sound/sfx_point.wav')

   def update(self):
      global hole_hit
      self.rect.centerx -= self.tube.speed
      if self.rect.centerx < 0: self.kill()
      if self.rect.colliderect(player.rect): 
         hole_hit = True


w, h = 600, 600
screen = pg.display.set_mode((w,h))
clock = pg.time.Clock()

player = Player(w/6, h/2)
player_group = pg.sprite.GroupSingle()
player_group.add(player)

tube_event = pg.event.custom_type() + 1
tube_timer = pg.time.set_timer(tube_event, 1500)
tube_group = pg.sprite.Group()

hole_group = pg.sprite.Group()
hole_hit = False

game_active = True


while True:
   screen.fill("#333333")
   for event in pg.event.get():
      if event.type == pg.QUIT:
         pg.quit()
         sys.exit()

      if game_active:
         if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
               player.vel_y -= 15
               player.gravity = 0.5
               player.jump_sound.play()

         if event.type == tube_event:
            tube = Tube(w, h/2)
            hole = Hole(tube.x, random.randint(0, h-200), tube)
            tube_group.add(tube)
            hole_group.add(hole)


   if game_active:
      tube_group.draw(screen)
      tube_group.update()

      hole_group.draw(screen)
      hole_group.update()

      player_group.draw(screen)
      player.jump()
   elif game_active == False: 
      screen.fill('#f0aaff')

   pg.display.update()
   clock.tick(50)



# --------------TODO------------- #
   # create player using sprite
   # make player jump with gravity
   # create tubes with random heights using sprite
   # make tubes move towards player, if its too far left delete it
   # add boundary at the top
   # detect collisions with [tubes, ground] and player 
   # if player goes pass tube increase score
   # add sounds



# --------------NOTE------------- #
   # Timers tell pygame to run piece of code on certain time intervals, we do this by creating a new user event thats triggered by pygame. 
      # 1;create a custom event, 2; tell pg to trigger that event continously, 3; add doe in the event loop
   # Sprite Class contains a surface & a rectagle, it can be drawn & updated very easily. think of sprites as an object in the game with all of the attributes & functions in its own class. Groups makes u target multiple sprites 