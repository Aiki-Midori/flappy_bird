import pygame as pg, sys

pg.init()

w, h = 600, 600
screen = pg.display.set_mode(w,h)
screen.fill("#333333")
clock = pg.time.Clock()


while True:
   for event in pg.event.get():
      if event.type == pg.QUIT:
         pg.quit()
         sys.exit()


   pg.display.update()
   clock.tick(50)



# --------------TODO------------- #
   #


# --------------NOTE------------- #
   #