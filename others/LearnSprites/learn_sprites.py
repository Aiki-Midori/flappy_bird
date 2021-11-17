import pygame as pg, sys, random

class Crosshair(pg.sprite.Sprite):
   def __init__(self):
      super().__init__()
      # image & rect are mandatory for sprite classes!
      self.image = pg.image.load('crosshair_white_large.png').convert_alpha()
      self.rect = self.image.get_rect()

   def shoot(self):
      pg.sprite.spritecollide(crosshair, target_group, True)

   def update(self):
      pg.mouse.set_visible(False)
      self.rect.center = pg.mouse.get_pos()


class Target(pg.sprite.Sprite):
   def __init__(self, pos):
      super().__init__()
      self.image = pg.image.load('target_red2.png').convert_alpha()
      # self.pos = pos ;; whats the diff when u add a "self." with the param?
      self.rect = self.image.get_rect(center=pos)


pg.init()

w, h = 800, 800
screen = pg.display.set_mode((w,h))
clock = pg.time.Clock()

crosshair = Crosshair()
crosshair_group = pg.sprite.Group() # Group is a simple container for sprites
crosshair_group.add(crosshair)

target_group = pg.sprite.Group()
for target in range(20):
   new_target = Target((random.randrange(50, w), random.randrange(50, w)))
   target_group.add(new_target)

while True:
   screen.fill("#333333")
   for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()    
      if event.type == pg.MOUSEBUTTONDOWN:
         crosshair.shoot()

   # "draw" is like blit
   target_group.draw(screen)
   crosshair_group.draw(screen)
   crosshair_group.update()

   pg.display.update()
   clock.tick(50)



# --------------TODO------------- #
   #


# --------------NOTE------------- #
   #