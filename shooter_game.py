from pygame import *
from random import randint

#hafta5
from time import time as timer
#hafta5
#Selamlar burayı github ile değiştirdim

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

#Sound.set_volume(0.5) #Oyun ses seviyesi

#Font ve yazılar - hafta2
font.init()
font2 =font.Font(None, 36)
img_enemy = "ufo.png" #Düşman resmi

score = 0 #vurulan gemiler
lost = 0 #kaçan gemiler

img_back = "galaxy.jpg"
img_hero = "rocket.png"

img_ast = "asteroid.png"
life = 3


#hafta3
img_bullet = "bullet.png"
max_lost = 5
win = font2.render("You Win", True, (0,255,0))
lose = font2.render("You Lose", True, (180,0,0))
#hafta3

#hafta4
goal = 15



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        # Her sprite image - resim özelliğini depolamalıdır
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # Her sprite, içine yazıldığı dikdörtgenin  rect özelliğini saklamalıdır
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self): #karakteri ekrana çizecek
        window.blit(self.image, (self.rect.x , self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -=self.speed

        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#düşman sınıfı oluştur. Hafta-2
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost #değişkeni her alanda kullanabilmek için kapsamı geniş hale getir

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
#3.hafta
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed     
        if self.rect.y < 0:
            self.kill()
#3.hafta

#Arayüzz
win_width = 700
win_height = 500
display.set_caption("Shooter Game")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width,win_height))

#2.hafta
ship = Player(img_hero,5,win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80,50, randint(2,7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range (1,3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80,50, randint(1,7))
    asteroids.add(asteroid)

bullets = sprite.Group()

#Oyun döngüsü ve ekranı başlatma

finish = False #Oyunun bitip bitmediğini kontrol eden değişken.
run = True

rel_time = False #şarjdan sorumlü değişken
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        #3hafta
        elif e.type == KEYDOWN:#klavyeden kullanıcı bir tuşa tıklarsa elif çalışacaktır.
            if e.key == K_SPACE:

                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
    
    if not finish:
        window.blit(background, (0,0))


        #ekrana metin yazıyoruz
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: "+ str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()#2.hafta


        ship.reset()
        monsters.draw(window)#2.hafta

        #3.hafta
        bullets.update()
        bullets.draw(window)
        #3.hafta

        #5.hafta
        asteroids.update()
        asteroids.draw(window)

        #şarj
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3: 
                reload = font2.render("Wait, reload..", 1, (150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False

        #5.hafta


        #4.hafta
        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80,50, randint(4,9))
            monsters.add(monster)

        #hafta5
        collides2 = sprite.groupcollide(asteroids, bullets,True, True)
        for a in collides2:
            #Bu döngü, canavarlar vurulduğu kadar tekrarlanır
            score = score + 1
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

           #hafta5
         #eğer sprite düşmana dokunursa, canı azalır
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True#kaybettik, arka planı koyduk ve artık spriteları yönetmiyoruz.
            window.blit(lose, (200, 200))

        if score >= goal:
            #finish = True
            self.speed + 5
            window.blit(win,(200,200))

        #hafta5
        text_life = font2.render(str(life), 1, (0,255,0))
        window.blit(text_life, (650, 10))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        #hafta5
        num_fire = 0
        life = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()   
            #hafta5
        for a in asteroids:
            a.kill()     

        time.delay(2000)

        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80,50, randint(2,7))
            monsters.add(monster)
    
    time.delay(50) #0.05 saniye
