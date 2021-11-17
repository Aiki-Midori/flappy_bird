# proud 🙂
import pygame as pg, sys, random


pg.init()

w, h = 280, 500
screen = pg.display.set_mode((w,h))
screen.fill("#333333")
clock = pg.time.Clock()
img_path = 'assets/images/'
sound_path = 'assets/sound/'

score, hiscore = 0, 0

font = pg.font.Font('assets/04B_19.TTF', 20)

bg_img = pg.image.load(f'{img_path}background-night.png').convert_alpha()
ground_img = pg.image.load(f'{img_path}base.png').convert_alpha()
play_img = pg.image.load(f'{img_path}message.png').convert_alpha()

play = False

class Player(pg.sprite.Sprite):
   def __init__(self, x, y):
      super().__init__()
      global play
      self.x, self.y = x, y
      self.gravity, self.vely = 0.2, 10
      self.time = pg.time.get_ticks()
      self.imgs = []
      for i in range(3): self.imgs.append(pg.image.load(f"{img_path}bluebird/{i}.png").convert_alpha())
      self.frame_index = 0
      self.image = self.imgs[self.frame_index]
      self.rect = self.image.get_rect(center=(self.x, self.y))
      
   def jump(self): 
      self.vely -= 8
      pg.mixer.Sound(f'{sound_path}sfx_wing.wav').play()
      self.image = pg.transform.rotate(self.image, 45)

   def animate(self):
      global start_time
      frame_duration = 100
      if pg.time.get_ticks() - self.time >= frame_duration:
         if self.frame_index >= 2: self.frame_index = 0
         else:
            self.frame_index += 1
            self.image = self.imgs[self.frame_index]
            self.time = pg.time.get_ticks() 

      # if self.frame_index >= 2: self.frame_index = 0
      # else: 
      #    self.frame_index += 0.1
      #    self.image = self.imgs[int(self.frame_index)]

   def reset(self): 
      self.x, self.y = w/8, h/2
      self.gravity, self.vely = 0.2, 10
      tube_group.empty()

   def update(self):
      if play: 
         self.vely += self.gravity
         self.rect.centery += self.vely
      else: self.reset()
      if self.rect.centery >= h-45: self.rect.centery = h-45
      if self.rect.top <= 0: 
         self.rect.top = 0
         self.vely += 2
      self.animate()


class Tubes(pg.sprite.Sprite):
   def __init__(self, x, y):
      super().__init__()
      self.x, self.y = x, y
      self.speed = 2

      self.down_tube_img = pg.image.load(f'{img_path}pipe-red.png').convert_alpha()
      self.up_tube_img = pg.transform.flip(self.down_tube_img, False, True)
      self.down_tube_rect = self.down_tube_img.get_rect(bottom=h+340)
      self.up_tube_rect = self.up_tube_img.get_rect(topleft=(0, -20))

      self.image = pg.Surface((50, h+500)).convert_alpha()
      self.image.blit(self.down_tube_img, self.down_tube_rect)
      self.image.blit(self.up_tube_img, self.up_tube_rect)
      self.rect = self.image.get_rect(center=(self.x, self.y))

      self.hole = pg.Surface((60, 200)).convert_alpha()
      # self.hole.fill('white')


   def play_sound(self, hole_hit, tube_hit):
      global score
      if (self.hole_rect.left <= player.rect.right) and hole_hit: 
         pg.mixer.Sound(f'{sound_path}sfx_point.wav').play()
         score += 1
      if (self.rect.left <= player.rect.right) and tube_hit: pg.mixer.Sound(f'{sound_path}sfx_hit.wav').play()

   def update(self):
      global hole_hit, tube_hit, score, play
      self.rect.x -= self.speed
      self.hole_rect = self.hole.get_rect(topleft=(self.rect.centerx-25, self.rect.centery-180))
      screen.blit(self.hole, self.hole_rect)

      if self.rect.right < 0: self.kill()
      if self.hole_rect.colliderect(player.rect) and self.rect.colliderect(player.rect): 
         hole_hit = True
         tube_hit = False
         self.play_sound(hole_hit, tube_hit)
      elif self.rect.colliderect(player.rect) and hole_hit == False: 
         hole_hit = False
         tube_hit = True
         self.play_sound(hole_hit,tube_hit)
         play = False
      else: 
         hole_hit = False
         tube_hit = False
      

      # WHY IS THIS NOT WORKING??!
         # self.up_tube_rect.x + 304  
         # if self.up_tube_rect.colliderect(player.rect) or self.down_tube_rect.colliderect(player.rect): print(pg.time.get_ticks())
         # print(self.rect.center, self.down_tube_rect.center, self.up_tube_rect.center)
      # CZ U DIDNT PUT THE COORDS IN THE RECT INIT ITSELF, URE SEPARATING THE MOVEMENT OF THE RECT ON THE UPDATE WHICH MAKES AN OFFSET


player_group = pg.sprite.GroupSingle()
player = Player(w/8, h/2)
player_group.add(player)

tube_group = pg.sprite.Group()

tube_event = pg.event.custom_type()
pg.time.set_timer(tube_event, 2000)

hole_hit = False
tube_hit = False

def get_hiscore():
   with open('hiscore.txt') as f:
      return f.readline()


while True:
   screen.blit(bg_img, (0, 0))
   screen.blit(ground_img, ground_img.get_rect(center=(w/2, h+20)))

   for event in pg.event.get():
      if event.type == pg.QUIT:
         pg.quit()
         sys.exit()

      if event.type == pg.KEYDOWN:
         if event.key == pg.K_SPACE:
            player.jump()
            play = True
 
      if event.type == tube_event:
         tube = Tubes(w+50, (h/2)+random.randint(-70, 250))
         tube_group.add(tube)

   if play:
      tube_group.draw(screen)
      tube_group.update()

      score_text = font.render(f'{score//50}', False, 'white').convert_alpha()
      screen.blit(score_text, (w/2, 40))

   player_group.draw(screen)
   player_group.update()

   if play == False: 
      screen.blit(play_img, play_img.get_rect(center=(w/2, h/2)))

      if score//50 > hiscore: 
         hiscore = score//50
         with  open('hiscore.txt', 'w') as file: file.write(f'{hiscore}')

      hiscore_text = font.render(f'hiscore:{get_hiscore()}', False, 'white').convert_alpha()
      screen.blit(hiscore_text, hiscore_text.get_rect(center=(w/2, 60)))

      score = 0

   pg.display.update()
   clock.tick(60)



# --------------TODO------------- # 
   # set up bg & floor
   # create player & apply gravity into it (dont animate yet)
   # make player jump, add boundaries
   # spawn tubes, make it approach left side with random heights
   # if tubes goes too far off left kill it
   # detect collisions on ground & tubes with player
   # add score when goes thru hole
   # add player animation with tilt
   # add game over screen
   # add sounds
   # CHALLENGE: add highscore mechanism

# --------------NOTE------------- #
 # CAN WE STILL DETECT COLLISIONS EVEN IF THE SPRITE IS ON ANOTHER? YES!