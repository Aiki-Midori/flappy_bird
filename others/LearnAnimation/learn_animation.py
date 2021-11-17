import pygame as pg, sys

pg.init()

w, h = 290, 500
screen = pg.display.set_mode((w,h))
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
   def __init__(self, x, y):
      super().__init__()
      self.x, self.y = x, y
      self.image_list = []
      self.frame_index = 0
      self.flap_time = 50
      self.gravity = 0.5
      self.vely = 10
      self.is_jump = False
      for i in range(3): self.image_list.append(pg.image.load(f'assets/images/bluebird/{i}.png'))
      self.image = self.image_list[self.frame_index]
      self.rect = self.image.get_rect(center=(self.x, self.y))

   def animate(self):
      if self.frame_index >= len(self.image_list): self.frame_index = 0
      else: 
         self.image = self.image_list[self.frame_index]
         self.frame_index += 1
      
      


bg_image = pg.image.load("assets/images/background-night.png").convert()
base_image = pg.image.load("assets/images/base.png").convert()
pipe_image = pg.image.load("assets/images/pipe-red.png").convert_alpha()

player_group = pg.sprite.GroupSingle()
player = Player(w/8, h/2)
player_group.add(player)

animation_event = pg.event.custom_type() + 1
pg.time.set_timer(animation_event, player.flap_time)



while True:
   for event in pg.event.get():
      if event.type == pg.QUIT: pg.quit(), sys.exit()
      if event.type == animation_event: player.animate()

      if event.type == pg.KEYDOWN: 
         if event.key == pg.K_SPACE: 
            player.vely -= 20
            

   print(player.rect.centery)

   screen.blit(bg_image, (0, 0))
   screen.blit(base_image, (0, 450))

   player_group.draw(screen)

   if player.rect.centery > h-50: player.rect.centery = h-50
   elif player.rect.centery < 50: player.rect.centery = 50
   player.vely += player.gravity
   player.rect.centery += player.vely

   pg.display.update()
   clock.tick(50)



# --------------NOTE------------- #

   # u just need "group of images" & a "timer" of how often u wanna update the image to the next image