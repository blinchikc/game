from pygame import *
from random import*
window = display.set_mode ((700,500))
FPS = 60
display.set_caption("shooter")
mixer.init()
mixer.music.load('space.ogg')
kick=mixer.Sound('fire.ogg')
mixer.music.play()
clock=time.Clock()
font.init()
background=transform.scale(image.load("galaxy.jpg"),(700,500))
win_width = 700
win_height = 500
font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,36)
font3 = font.Font(None,50)
font4 = font.Font(None,50)
win = 0
lost = 0

class GameSprite(sprite.Sprite):
        def __init__(self,player_image,player_x,player_y,player_speed,size1,size2):
                super().__init__()
                self.image = transform.scale(image.load(player_image),(size1,size2))
                self.rect = self.image.get_rect()
                self.rect.x = player_x
                self.rect.y = player_y
                self.speed = player_speed
        def reset(self):
                window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
        def update(self):
                keys = key.get_pressed()
                if keys[K_LEFT] and self.rect.x > 5:
                        self.rect.x -= self.speed
                if keys[K_RIGHT] and self.rect.x < win_width - 80:
                        self.rect.x += self.speed
               
        def fire(self):
                bullet=Bullet('bullet.png.',self.rect.centerx, self.rect.top, 7,15,25)
                bullets.add(bullet)
                kick.play()
               
               
class Enemy(GameSprite):
        def update(self):
                self.rect.y += self.speed
                global lost
                if self.rect.y > 495:
                        self.rect.y = 0
                        self.rect.x = randint(30,670)
                        lost = lost+1
class Bullet(GameSprite):
        def update(self):
                self.rect.y -= self.speed
                if self.rect.y < 0:
                        self.kill()
class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 495:
            self.rect.x = randint(30,670)
            self.rect.y = 0              

hero = Player('rocket.png', 5, win_height - 80, 4,65,65)

bullets = sprite.Group()
monsters = sprite.Group()
aster = sprite.Group()
for i in range(1,6):
        cyborg = Enemy('ufo.png', win_width - randint(200,600),0, randint(1,3),85,65)
        monsters.add(cyborg)
for q in range(1, 4):
    asterr = Aster('asteroid.png', win_width - randint(200,600),0, randint(1,2),85,65)
    aster.add(asterr)
game= True
finish = False
while game:
        for e in event.get():
                if e.type == QUIT:
                        game = False
                elif e.type == KEYDOWN:
                        if e.key == K_SPACE:
                                hero.fire()
                               
        if finish != True:
                window.blit(background,(0, 0))
                
                hero.update()
                bullets.update()
                bullets.draw(window)
                monsters.update()
                monsters.draw(window)
                aster.draw(window)
                aster.update()
                hero.reset()
                winer = font3.render('Ты победил!', True, (127, 255, 0))
                lose = font4.render('Ты Проиграл!', True, (255, 0, 0))
                
                if sprite.groupcollide(monsters,bullets, True, True):
                        win+=1
                        cyborg = Enemy('ufo.png', win_width - randint(200,600),0, randint(1,3),85,65)
                        monsters.add(cyborg)
                        
                if sprite.spritecollide(hero, aster, False) or sprite.spritecollide(hero, monsters, False):
                        finish = True
                        window.blit(lose, (225, 200))
                
                if lost >= 3:
                        finish = True
                        window.blit(lose, (225, 200))
                if win >= 10:
                        finish = True
                        window.blit(winer, (225, 200))

                text_lose = font1.render("Пропущено: "+str(lost),1,(255,255,255))
                text_lose1 = font2.render("Cчет:"+str(win),1,(255,255,255))
                window.blit(text_lose,(0,20))
                window.blit(text_lose1,(0,0))
       
        display.update()
        clock.tick(FPS)