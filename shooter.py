from random import randint
from time import time as timer
from pygame import *
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))


class GameSprite(sprite.Sprite):
   def __init__(self, image_name, x, y , speed, size_x, size_y):
      super().__init__()
      self.image = transform.scale(image.load(image_name), (size_x, size_y))
      self.speed = speed
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
   def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))
    
bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x > 5: 
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630: 
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 5, 20, 20)
        bullets.add(bullet)

font.init()
font1 = font.SysFont('Arial', 36)
lost = 0
text_lose = font1.render('Пропущено ' + str(lost), 1, (255, 255, 255))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global text_lose
        if self.rect.y > 500:
            self.rect.y = - 65
            self.rect.x = randint(0, 635) 
            lost = lost + 1            
            text_lose = font1.render('Пропущено ' + str(lost), 1, (255, 255, 255))

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png',randint(0, 635)  , 0 , randint(1, 4), 65, 55 )
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(0, 635)  , 0 , randint(1, 2), 65, 55 )
    asteroids.add(asteroid)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -20:
            self.kill()


clock = time.Clock()
player = Player('rocket.png',350 , 430 , 5, 65, 65)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()

music = mixer.Sound('fire.ogg')

font2 = font.SysFont('Arial', 70)
win = font2.render(
   'YOU WIN!', True, (255, 215, 0)
)
lose = font2.render(
   'YOU DEAD!', True, (255, 215, 0)
)

scor = 0 
text_scor = font1.render('Сбито ' + str(scor), 1, (255, 255, 255))

life = 3 

time = False
shot = 0

game = True
finish = False
while game:
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        asteroids.update()
        asteroids.draw(window)
        window.blit(text_lose,(5, 5))
        window.blit(text_scor,(5, 45))
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        for i in sprites_list:
            scor = scor + 1
            text_scor = font1.render('Сбито ' + str(scor), 1, (255, 255, 255))
            monster = Enemy('ufo.png',randint(0, 635)  , 0 , randint(1, 4), 65, 55 )
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            life = life - 1
        if life == 0 or lost >= 3:
            finish = True
            window.blit(lose, (250 , 250))
        if scor >= 10:
            finish = True
            window.blit(win, (250, 250))
        text_life = font1.render('количество жизней ' + str(life), 1, (255, 255, 255))
        window.blit(text_life, (450, 10))
        if time == True:
            cold_time = timer()
            if cold_time - chek_time < 3:
                text_reload = font1.render('Перезорядка', 1, (255, 255, 255))
                window.blit(text_reload, (350, 250))
            else:
                shot = 0 
                time = False

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if shot < 5 and time == False:
                    shot = shot + 1
                    player.fire() 
                    music.play()
                if shot >= 5 and time == False:
                    time = True
                    chek_time = timer()


    clock.tick(60)
    display.update()
