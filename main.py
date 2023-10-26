from re import X
import pygame
from pygame.locals import *
from sys import exit
from random import choice, randint

clock = pygame.time.Clock()

x = 1000
y = 650

#Tela
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Guerra de Aviões')

#Background
bg = pygame.image.load('img/fundo_teste.png').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

#Player
player = pygame.image.load('img/aviao.png').convert_alpha()
player = pygame.transform.scale(player, (67, 67))
player = pygame.transform.rotate(player, -90)

pos_x_player = 175
pos_y_player = y/2

movimento_y_player = 5

#Inimigo
inimigo = pygame.image.load('img/inimigo.png').convert_alpha()
inimigo = pygame.transform.scale(inimigo, (67,67))
inimigo = pygame.transform.rotate(inimigo, -90)

pos_x_inimigo = 1100
pos_y_inimigo = randint(67, 583)
velocidade_inimigo = 3

#Fonte
pygame.font.init()
fonte_letra = pygame.font.SysFont('arial', 14, False, False)


pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.blit(bg, (0, 0))

    #Movimentação da tela
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 1000:
        screen.blit(bg, (rel_x, 0))
    x -= 2

    #Player
    screen.blit(player, (pos_x_player, pos_y_player))
    if pygame.key.get_pressed()[K_UP]:
        pos_y_player -= movimento_y_player
        if pos_y_player > 10:
            movimento_y_player = 5
        else:
            movimento_y_player = 0

    if pygame.key.get_pressed()[K_DOWN]:
        pos_y_player += movimento_y_player
        if pos_y_player <= 575:
            movimento_y_player = 5
        else:
            movimento_y_player = 0 

        
        

    #Inimigo
    screen.blit(inimigo, (pos_x_inimigo, pos_y_inimigo))
    pos_x_inimigo -= velocidade_inimigo
    if pos_x_inimigo <= -65:
        pos_x_inimigo = 1100
        pos_y_inimigo = randint(10, 575)
        velocidade_inimigo = randint(3, 10)

    pygame.display.update()
    
