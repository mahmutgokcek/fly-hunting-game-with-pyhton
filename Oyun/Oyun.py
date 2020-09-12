#Gerekli kütüphaneleri ekliyoruz.
import math
import random

import pygame 
from pygame import mixer

# Oyunu başlatma
pygame.init()

# Pencere büyüklüğünü oluşturma
screen = pygame.display.set_mode((800, 600))

# Arkaplan ekleme
arkaplan = pygame.image.load('arkaplan.png')


# Oyundaki karakterimiz ve ikonlar
pygame.display.set_caption("Sinek Avi")
icon = pygame.image.load('orumcek.png')
pygame.display.set_icon(icon)

# Oyuncu bilgileri
karakterImg = pygame.image.load('orumcek.png')
karakterX = 370
karakterY = 480
karakterX_change = 0

# Düşman bilgileri
dusmanImg = []
dusmanX = []
dusmanY = []
dusmanX_change = []
dusmanY_change = []
num_of_enemies = 6

#Düşmanın görselini ekliyoruz ve x-y konumunu random ile rastgele ayarlıyoruz.

for i in range(num_of_enemies):
    dusmanImg.append(pygame.image.load('sinek.png'))
    dusmanX.append(random.randint(0, 736))
    dusmanY.append(random.randint(50, 150))
    dusmanX_change.append(4)
    dusmanY_change.append(40)

# Örümcekten çıkan ağı oluşturuyoruz.

agImg = pygame.image.load('ag.png')
agX = 0
agY = 480
agX_change = 0
agY_change = 10
ag_state = "hazır"

# Skor

skor_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Oyun Bitti
over_font = pygame.font.Font('freesansbold.ttf', 64)


#Skor görüntüleme.
def show_skor(x, y):
    skor = font.render("Skor : " + str(skor_value), True, (255, 255, 255))
    screen.blit(skor, (x, y))


#Oyun bitti yazısı
def game_over_text():
    over_text = over_font.render("Oyun Bitti.", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#Karakterinizi x-y konumunda hareket ettirme
def karakter(x, y):
    screen.blit(karakterImg, (x, y))

#Düşmanı x-y de hareket ettirme
def dusman(x, y, i):
    screen.blit(dusmanImg[i], (x, y))

#Karakterin atacağı ağın konumu
def atis_ag(x, y):
    global ag_state
    ag_state = "atis"
    screen.blit(agImg, (x + 16, y + 10))

#Ağın düşmana değmesini sağlar.
def isCollision(dusmanX, dusmanY, agX, agY):
    distance = math.sqrt(math.pow(dusmanX - agX, 2) + (math.pow(dusmanY - agY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Oyunun döngüsünu başlatıyoruz.
running = True
while running:

    # RGB = Kırmızı, yeşil, mavi
    screen.fill((0, 0, 0))
    # Arkaplan resmi
    screen.blit(arkaplan, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # tuşa basıldığında sağ ya da sol olup olmadığını kontrol eder ve space tuşu ile ağ atımı sağlanır
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                karakterX_change = -5
            if event.key == pygame.K_RIGHT:
                karakterX_change = 5
            if event.key == pygame.K_SPACE:
                if ag_state is "hazır":
                  
                    # Ağ atmanın mevcut x-y koordinatını alır
                    agX = karakterX
                    atis_ag(agX, agY)
            #Karakterin sağ sol hareketlerini sağlar.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                karakterX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    karakterX += karakterX_change
    if karakterX <= 0:
        karakterX = 0
    elif karakterX >= 736:
        karakterX = 736

    # Düşman Hareket
    for i in range(num_of_enemies):

        # Oyun bitiyor
        if dusmanY[i] > 440:
            for j in range(num_of_enemies):
                dusmanY[j] = 2000
            game_over_text()
            break
        #Düşmanın hareketini belirler
        dusmanX[i] += dusmanX_change[i]
        if dusmanX[i] <= 0:
            dusmanX_change[i] = 4
            dusmanY[i] += dusmanY_change[i]
        elif dusmanX[i] >= 736:
            dusmanX_change[i] = -4
            dusmanY[i] += dusmanY_change[i]

        # Ağ ile düşmanın birbirine değme anı.
        atis = isCollision(dusmanX[i], dusmanY[i], agX, agY)
        if atis:
         
            agY = 480
            ag_state = "hazır"
            skor_value += 1
            dusmanX[i] = random.randint(0, 736)
            dusmanY[i] = random.randint(50, 150)

        dusman(dusmanX[i], dusmanY[i], i)

    # Ağın hareketi
    if agY <= 0:
        agY = 480
        ag_state = "hazır"

    if ag_state is "atis":
        atis_ag(agX, agY)
        agY -= agY_change

    karakter(karakterX, karakterY)
    show_skor(textX, testY)
    pygame.display.update()