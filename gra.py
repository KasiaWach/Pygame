import pygame
import random
import os

# inicjalizacja
pygame.init()

# tworzenie okna gry
screen = pygame.display.set_mode((800, 600))

# obrazek w tle
background = pygame.image.load('Grafika\ezgif.com-optimize.gif')

# tytuł okna i ikonka
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load(os.path.join('Grafika', 'ufo.png'))
pygame.display.set_icon(icon)

# Ikonka gracza
playerImg = pygame.image.load(os.path.join('Grafika', 'space-invaders.png'))
playerX = 370  # 370 px od lewej
playerY = 480  # 480 px od góry
playerX_change = 0

# Ikonka kosmity
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(os.path.join('Grafika', 'alien.png')))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.choice([-0.3, 0.3]))
    enemyY_change.append(40)

# Ikonka pocisku
bulletImg = pygame.image.load(os.path.join('Grafika', 'bullets.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = 'ready'  # ready - nie widać pocisku; fire - widać jak pocisk leci

# punkty
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    final_text = over_font.render('FINAL SCORE: '+str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(final_text, (150, 350))

def player(x, y):
    # screen.blit = rysuj na ekranie
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


# funkcja kolizji ufoludka z pociskiem
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** (1 / 2)
    if distance < 45:
        return True
    else:
        return False


# pętla aby okno gry pozostawało otwarte dopóki go sami nie zamkniemy
running = True
while running:
    # RGB na ekranie
    screen.fill((26, 11, 56))
    # obrazek na ekranie
    screen.blit(background, (0, 0))

    # ruch statku (zmiana współrzędnej x)
    # playerX += 0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # sprawdza czy wciśnięty przycisk to strzałka w lewo
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:  # sprawdza czy wciśnięty przycisk to strzałka w prawo
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change  # przesunięcie statku
    # granice poruszania się statku
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enemies):

        # koniec gry
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # poruszanie się kosmity
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # droga pocisku
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
