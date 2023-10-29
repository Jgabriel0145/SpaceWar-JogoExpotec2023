from re import X
import pygame
from pygame.locals import *
from sys import exit
from random import choice, randint

clock = pygame.time.Clock()

x = 1000
y = 650

#Tela
screen = pygame.display.set_mode((x, y), pygame.SRCALPHA)
pygame.display.set_caption('Space War')

#Background Jogo
bg = pygame.image.load('img/fundo_jogo.png').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

#Background Começar
bg_comecar = pygame.image.load('img/comecar.png').convert_alpha()
bg_comecar = pygame.transform.scale(bg_comecar, (x, y))
iniciar = False

#Background Derrota
bg_derrota = pygame.image.load('img/derrota.png').convert_alpha()
bg_derrota = pygame.transform.scale(bg_derrota, (x, y))


#Tiro
tiro_img = pygame.image.load('img/tiro.png').convert_alpha()
tiro_img = pygame.transform.scale(tiro_img, (15, 15))
tiro_rect = tiro_img.get_rect()

pos_x_tiro = 200
pos_y_tiro = (y/2) + 26

movimento_y_tiro = 0
movimento_x_tiro = 0

velocidade_x_tiro = 0

atirou = False

#Player
player_img = pygame.image.load('img/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (67, 67))
player_img = pygame.transform.rotate(player_img, -90)
player_rect = player_img.get_rect()
player_derrotado = False

pos_x_player = 175
pos_y_player = y/2

movimento_y_player = 5

pontuacao = 0

#Inimigo
inimigo_img = pygame.image.load('img/inimigo.png').convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (65,65))
inimigo_img = pygame.transform.rotate(inimigo_img, 90)
inimigo_rect = inimigo_img.get_rect()

pos_x_inimigo = 1100
pos_y_inimigo = randint(67, 583)
velocidade_inimigo = 3

#Fonte
pygame.font.init()
fonte_pontuacao_jogo = pygame.font.SysFont('fonte/TTSquares-Bold.ttf', 40, True, False)
fonte_pontuacao_derrota = pygame.font.SysFont('fonte/TTSquares-Bold.ttf', 100, True, False)

#Surfaces
tiro_surface = pygame.Surface(player_rect.size, pygame.SRCALPHA)
tiro_surface.blit(tiro_img, (0, 0))

player_surface = pygame.Surface(player_rect.size, pygame.SRCALPHA)
player_surface.blit(player_img, (0, 0))

inimigo_surface = pygame.Surface(inimigo_rect.size, pygame.SRCALPHA)
inimigo_surface.blit(inimigo_img, (0, 0))

pygame.init()
while True:
    clock.tick(400)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if iniciar == True:
        if player_derrotado == False:
            screen.blit(bg, (0, 0))

            #Movimentação da tela
            rel_x = x % bg.get_rect().width
            screen.blit(bg, (rel_x - bg.get_rect().width, 0))
            if rel_x < 1000:
                screen.blit(bg, (rel_x, 0))
            x -= 2

            #Pontuação
            if pontuacao <= -1:
                player_derrotado = True
                pontuacao = 0
            mensagem = fonte_pontuacao_jogo.render(f'Pontuação: {pontuacao}', False, (255, 255, 255))
            screen.blit(mensagem, (410, 50))

            #Tiro
            #A movimentação y está no player.
            screen.blit(tiro_surface, (pos_x_tiro, pos_y_tiro))
            tiro_rect.y = pos_y_tiro
            tiro_rect.x = pos_x_tiro

            if pygame.key.get_pressed()[K_SPACE]:
                atirou = True
                velocidade_x_tiro = 10

            if atirou:
                pos_x_tiro += velocidade_x_tiro

                if inimigo_rect.colliderect(tiro_rect):
                    atirou = False
                    velocidade_x_tiro = 0
                    pontuacao += 10
                    pos_x_tiro = pos_x_player + 26
                    pos_y_tiro = pos_y_player + 26
                    pos_x_inimigo = 1100
                    pos_y_inimigo = randint(10, 575)
                    velocidade_x_inimigo = randint(3, 10)

                if pos_x_tiro >= 1001:
                    atirou = False
                    velocidade_x_tiro = 0
                    pos_x_tiro = pos_x_player + 26
                    pos_y_tiro = pos_y_player + 26


            #Player
            screen.blit(player_surface, (pos_x_player, pos_y_player))
            player_rect.y = pos_y_player
            player_rect.x = pos_x_player

            if pygame.key.get_pressed()[K_UP]:
                pos_y_tiro -= movimento_y_tiro
                pos_y_player -= movimento_y_player

                if pos_y_player > 10:
                    movimento_y_player = 5
                    if not atirou:
                        movimento_y_tiro = 5
                    else:
                        movimento_y_tiro = 0
                else:
                    movimento_y_player = 0
                    movimento_y_tiro = 0

            if pygame.key.get_pressed()[K_DOWN]:
                pos_y_tiro += movimento_y_tiro
                pos_y_player += movimento_y_player

                if pos_y_player <= 575:
                    movimento_y_player = 5
                    if not atirou:
                        movimento_y_tiro = 5
                    else:
                        movimento_y_tiro = 0
                else:
                    movimento_y_player = 0 
                    movimento_y_tiro = 0

            #Evitar bugs
            if pos_y_player <= 10:
                pos_y_player = 11
                if not atirou:
                    pos_y_tiro = 36

            if pos_y_player > 576:
                pos_y_player = 575
                if not atirou:
                    pos_y_tiro = 600

            #Inimigo
            screen.blit(inimigo_surface, (pos_x_inimigo, pos_y_inimigo))
            inimigo_rect.y = pos_y_inimigo
            inimigo_rect.x = pos_x_inimigo

            pos_x_inimigo -= velocidade_inimigo
            if pos_x_inimigo <= -65:
                pontuacao -= 10
                pos_x_inimigo = 1100
                pos_y_inimigo = randint(10, 575)
                velocidade_inimigo = randint(3, 10)

            
            #Colisão para derrota do player
            if inimigo_rect.colliderect(player_rect):
                player_derrotado = True
        
        else:
            #Tela de derrota
            screen.blit(bg_derrota, (0, 0))
            mensagem = fonte_pontuacao_derrota.render(f'{pontuacao}', False, (255, 255, 255))
            screen.blit(mensagem, (675, 320))

            if pygame.key.get_pressed()[K_KP_ENTER] or pygame.key.get_pressed()[K_RETURN]:
                pontuacao = 0
                pygame.quit()
                exit()

    else:
        #Tela iniciar
        screen.blit(bg_comecar, (0, 0))
        if pygame.key.get_pressed()[K_KP_ENTER] or pygame.key.get_pressed()[K_RETURN]:
            iniciar = True

    pygame.display.update()
    
