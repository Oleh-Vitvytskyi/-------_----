import random

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WEIGHT = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WEIGHT, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WEIGHT, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

player_size = (15, 15)
player = pygame.image.load('player.png').convert_alpha() #pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = player.get_rect()
player_rect.center = main_display.get_rect().center
# player_speed = [1, 1]
player_move_down = [0, 7]
player_move_right = [7, 0]
player_move_up = [0, -7]
player_move_left = [-7, 0]

def creare_bonus():
    bonus_size = (20, 20)
    bonus = pygame.image.load('bonus.png').convert_alpha() #pygame.Surface(bonus_size)
    # bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(100, WEIGHT-100), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 2000)

bonuses = []


def create_enemy():
    enemy_size = (15, 15)
    enemy = pygame.image.load('enemy.png').convert_alpha() #pygame.Surface(enemy_size)
    # enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WEIGHT, random.randint(50, HEIGHT-50), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

score = 0

playing = True

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(creare_bonus())

    # main_display.fill(COLOR_BLACK)
            
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
            
    main_display.blit(bg, (bg_X1,0))
    main_display.blit(bg, (bg_X2,0))


    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
       player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WEIGHT:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top :
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left :
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WEIGHT-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))