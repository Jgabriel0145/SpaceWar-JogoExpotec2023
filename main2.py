from re import X
import pygame
from pygame.locals import *
from sys import exit
from random import choice, randint

clock = pygame.time.Clock()

x = 1000
y = 650

perdeujogo = False

#Tela
screen = pygame.display.set_mode((x, y), pygame.SRCALPHA)
pygame.display.set_caption('Space War')

imagem_icon = pygame.image.load('img/player.ico')
pygame.display.set_icon(imagem_icon)

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

#Background Vitória
bg_vitoria = pygame.image.load('img/vitoria.png').convert_alpha()
bg_vitoria = pygame.transform.scale(bg_vitoria, (x, y))

#Tiro
tiro_img = pygame.image.load('img/tiro.png').convert_alpha()
tiro_img = pygame.transform.scale(tiro_img, (15, 15))
tiro_rect = tiro_img.get_rect()
tiro_rect_2 = tiro_img.get_rect()

pos_x_tiro = 200
pos_y_tiro = (y/2) + 26

pos_x_tiro_2 = 200
pos_y_tiro_2 = (y/2) + 26

movimento_y_tiro = 0
movimento_x_tiro = 0

movimento_y_tiro_2 = 0
movimento_x_tiro_2 = 0

velocidade_x_tiro = 0
velocidade_x_tiro_2 = 0

atirou = False
atirou2 = False

#Player
player_img = pygame.image.load('img/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (67, 67))
player_img = pygame.transform.rotate(player_img, -90)
player_rect = player_img.get_rect()

player_img_2 = pygame.image.load('img/player2.png').convert_alpha()
player_img_2 = pygame.transform.scale(player_img_2, (67, 67))
player_img_2 = pygame.transform.rotate(player_img_2, -90)
player_rect_2 = player_img_2.get_rect()

player_derrotado = False
player_derrotado_2 = False

player_venceu = False

pos_x_player = 175
pos_y_player = y/2

pos_x_player_2 = 175
pos_y_player_2 = y/2

movimento_y_player = 5
movimento_y_player_2 = 5

pontuacao = 0

level = 1

#Inimigo
inimigo_img = pygame.image.load('img/inimigo.png').convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (65,65))
inimigo_img = pygame.transform.rotate(inimigo_img, 90)
inimigo_rect = inimigo_img.get_rect()

inimigo_rect_2 = inimigo_img.get_rect()

pos_x_inimigo = 1100
pos_y_inimigo = randint(67, 583)

pos_x_inimigo_2 = 1100
pos_y_inimigo_2 = randint(67, 583)

velocidade_inimigo = 3
velocidade_inimigo_2 = 5

#Fonte
pygame.font.init()
fonte_pontuacao_jogo = pygame.font.SysFont('fonte/TTSquares-Bold.ttf', 40, True, False)
fonte_pontuacao_derrota = pygame.font.SysFont('fonte/TTSquares-Bold.ttf', 100, True, False)

#Surfaces
tiro_surface = pygame.Surface(tiro_rect.size, pygame.SRCALPHA)
tiro_surface.blit(tiro_img, (0, 0))

tiro_surface_2 = pygame.Surface(tiro_rect_2.size, pygame.SRCALPHA)
tiro_surface_2.blit(tiro_img, (0, 0))

player_surface = pygame.Surface(player_rect.size, pygame.SRCALPHA)
player_surface.blit(player_img, (0, 0))

player_surface_2 = pygame.Surface(player_rect_2.size, pygame.SRCALPHA)
player_surface_2.blit(player_img_2, (0, 0))

inimigo_surface = pygame.Surface(inimigo_rect.size, pygame.SRCALPHA)
inimigo_surface.blit(inimigo_img, (0, 0))

inimigo_surface_2 = pygame.Surface(inimigo_rect_2.size, pygame.SRCALPHA)
inimigo_surface_2.blit(inimigo_img, (0, 0))

pygame.init()
while True:
    clock.tick(125)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if iniciar == True:
        if perdeujogo == False:
            screen.blit(bg, (0, 0))

            #Movimentação da tela
            rel_x = x % bg.get_rect().width
            screen.blit(bg, (rel_x - bg.get_rect().width, 0))
            if rel_x < 1000:
                screen.blit(bg, (rel_x, 0))
            x -= 2

            if player_derrotado == False:
                #Player
                if pygame.key.get_pressed()[K_w]:
                    pos_y_player -= movimento_y_player
                    pos_y_tiro -= movimento_y_tiro

                    if pos_y_player > 10:
                        if level == 1:
                            movimento_y_player = 5
                        elif level == 2:
                            movimento_y_player = 7
                        else: 
                            movimento_y_player = 10

                        if not atirou:
                            if level == 1:
                                movimento_y_tiro = 5
                            elif level == 2:
                                movimento_y_tiro = 7
                            else: 
                                movimento_y_tiro = 10
                        else:
                            movimento_y_tiro = 0


                    else:
                        movimento_y_player = 0
                        if not atirou:
                            movimento_y_tiro = 0

                if not atirou:
                    tiro_rect.y = pos_y_tiro
                    tiro_rect.x = pos_x_tiro

                if pygame.key.get_pressed()[K_s]:                
                    pos_y_player += movimento_y_player
                    pos_y_tiro += movimento_y_tiro          

                    if pos_y_player <= 575:
                        if level == 1:
                            movimento_y_player = 5
                        elif level == 2:
                            movimento_y_player = 7
                        else: 
                            movimento_y_player = 10

                        if not atirou:
                            if level == 1:
                                movimento_y_tiro = 5
                            elif level == 2:
                                movimento_y_tiro = 7
                            else: 
                                movimento_y_tiro = 10
                        else:
                            movimento_y_tiro = 0
                                
                    else:
                        movimento_y_player = 0
                        if not atirou:
                            movimento_y_tiro = 0
                
                if not atirou:
                    tiro_rect.y = pos_y_tiro
                    tiro_rect.x = pos_x_tiro

            if player_derrotado_2 == False:
                #Player2
                if pygame.key.get_pressed()[K_UP]:
                    pos_y_player_2 -= movimento_y_player_2
                    pos_y_tiro_2 -= movimento_y_tiro_2

                    if pos_y_player_2 > 10:
                        if level == 1:
                            movimento_y_player_2 = 5
                        elif level == 2:
                            movimento_y_player_2 = 7
                        else: 
                            movimento_y_player_2 = 10

                        if not atirou2:
                            if level == 1:
                                movimento_y_tiro_2 = 5
                            elif level == 2:
                                movimento_y_tiro_2 = 7
                            else: 
                                movimento_y_tiro_2 = 10
                        else:
                            movimento_y_tiro_2 = 0


                    else:
                        movimento_y_player_2 = 0
                        if not atirou2:
                            movimento_y_tiro_2 = 0

                if pygame.key.get_pressed()[K_DOWN]:                
                    pos_y_player_2 += movimento_y_player_2
                    pos_y_tiro_2 += movimento_y_tiro_2          

                    if pos_y_player_2 <= 575:
                        if level == 1:
                            movimento_y_player_2 = 5
                        elif level == 2:
                            movimento_y_player_2 = 7
                        else: 
                            movimento_y_player_2 = 10

                        if not atirou2:
                            if level == 1:
                                movimento_y_tiro_2 = 5
                            elif level == 2:
                                movimento_y_tiro_2 = 7
                            else: 
                                movimento_y_tiro_2 = 10
                        else:
                            movimento_y_tiro_2 = 0


                    else:
                        movimento_y_player_2 = 0
                        if not atirou2:
                            movimento_y_tiro_2 = 0

            #Evitar bugs
            if player_derrotado == False:
                if pos_y_player <= 10:
                    pos_y_player = 11
                    if not atirou:
                        pos_y_tiro = 36

            if player_derrotado_2 == False:
                if pos_y_player_2 <= 10:
                    pos_y_player_2 = 11
                    if not atirou2:
                        pos_y_tiro_2 = 36

            if player_derrotado == False:
                if pos_y_player > 576:
                    pos_y_player = 575
                    if not atirou:
                        pos_y_tiro = 600

            if player_derrotado_2 == False:
                if pos_y_player_2 > 576:
                    pos_y_player_2 = 575
                    if not atirou2:
                        pos_y_tiro_2 = 600

            if player_derrotado == False:
                screen.blit(tiro_surface, (pos_x_tiro, pos_y_tiro))
                tiro_rect.y = pos_y_tiro
                tiro_rect.x = pos_x_tiro

                screen.blit(player_surface, (pos_x_player, pos_y_player))
                player_rect.y = pos_y_player
                player_rect.x = pos_x_player

            if player_derrotado_2 == False:
                screen.blit(tiro_surface_2, (pos_x_tiro_2, pos_y_tiro_2))
                tiro_rect_2.y = pos_y_tiro_2
                tiro_rect_2.x = pos_x_tiro_2

                screen.blit(player_surface_2, (pos_x_player_2, pos_y_player_2))
                player_rect_2.y = pos_y_player_2
                player_rect_2.x = pos_x_player_2
            
            if player_derrotado == False:
                #Tiro
                if pygame.key.get_pressed()[K_SPACE]:
                    atirou = True
                    if level == 1:
                        velocidade_x_tiro = 10
                    elif level == 2:
                        velocidade_x_tiro = 15
                    else:
                        velocidade_x_tiro = 20   

                if atirou:
                    pos_x_tiro += velocidade_x_tiro

                    if inimigo_rect.colliderect(tiro_rect):
                        atirou = False
                        velocidade_x_tiro = 0
                        
                        if level == 1:
                            pontuacao += 10
                        elif level == 2:
                            pontuacao += 50
                        elif level == 3:
                            pontuacao += 100
                        
                        pos_x_tiro = pos_x_player + 26
                        pos_y_tiro = pos_y_player + 26
                        pos_x_inimigo = 1100
                        pos_y_inimigo = randint(10, 575)
                        if level == 1:
                            velocidade_x_inimigo = randint(3, 4)
                        elif level == 2:
                            velocidade_x_inimigo = randint(5, 6)
                        elif level == 3:
                            velocidade_x_inimigo = randint(7, 8)
                    
                    if inimigo_rect_2.colliderect(tiro_rect):
                        atirou = False
                        velocidade_x_tiro = 0
                        
                        if level == 1:
                            pontuacao += 10
                        elif level == 2:
                            pontuacao += 50
                        elif level == 3:
                            pontuacao += 100

                        pos_x_tiro = pos_x_player + 26
                        pos_y_tiro = pos_y_player + 26
                        pos_x_inimigo_2 = 1100
                        pos_y_inimigo_2 = randint(10, 575)
                        if level == 2:
                            velocidade_x_inimigo = randint(5, 6)
                        elif level == 3:
                            velocidade_x_inimigo = randint(7, 8)

                    if pos_x_tiro >= 1001:
                        atirou = False
                        velocidade_x_tiro = 0
                        pos_x_tiro = pos_x_player + 26
                        pos_y_tiro = pos_y_player + 26

            if player_derrotado_2 == False:
                #Tiro2
                if pygame.key.get_pressed()[K_0]:
                    atirou2 = True
                    if level == 1:
                        velocidade_x_tiro_2 = 10
                    elif level == 2:
                        velocidade_x_tiro_2 = 15
                    else:
                        velocidade_x_tiro_2 = 20   

                if atirou2:
                    pos_x_tiro_2 += velocidade_x_tiro_2

                    if inimigo_rect.colliderect(tiro_rect_2):
                        atirou2 = False
                        velocidade_x_tiro_2 = 0
                        
                        if level == 1:
                            pontuacao += 10
                        elif level == 2:
                            pontuacao += 50
                        elif level == 3:
                            pontuacao += 100
                        
                        pos_x_tiro_2 = pos_x_player_2 + 26
                        pos_y_tiro_2 = pos_y_player_2 + 26
                        pos_x_inimigo = 1100
                        pos_y_inimigo = randint(10, 575)
                        if level == 1:
                            velocidade_x_inimigo = randint(3, 4)
                        elif level == 2:
                            velocidade_x_inimigo = randint(5, 6)
                        elif level == 3:
                            velocidade_x_inimigo = randint(7, 8)
                    
                    if inimigo_rect_2.colliderect(tiro_rect_2):
                        atirou2 = False
                        velocidade_x_tiro_2 = 0
                        
                        if level == 1:
                            pontuacao += 10
                        elif level == 2:
                            pontuacao += 50
                        elif level == 3:
                            pontuacao += 100

                        pos_x_tiro_2 = pos_x_player_2 + 26
                        pos_y_tiro_2 = pos_y_player_2 + 26
                        pos_x_inimigo_2 = 1100
                        pos_y_inimigo_2 = randint(10, 575)
                        if level == 2:
                            velocidade_x_inimigo = randint(5, 6)
                        elif level == 3:
                            velocidade_x_inimigo = randint(7, 8)

                    if pos_x_tiro_2 >= 1001:
                        atirou2 = False
                        velocidade_x_tiro_2 = 0
                        pos_x_tiro_2 = pos_x_player_2 + 26
                        pos_y_tiro_2 = pos_y_player_2 + 26


            #Inimigo
            screen.blit(inimigo_surface, (pos_x_inimigo, pos_y_inimigo))
            inimigo_rect.y = pos_y_inimigo
            inimigo_rect.x = pos_x_inimigo

            if level == 2 or level == 3:
                screen.blit(inimigo_surface_2, (pos_x_inimigo_2, pos_y_inimigo_2))
                inimigo_rect_2.y = pos_y_inimigo_2
                inimigo_rect_2.x = pos_x_inimigo_2

            pos_x_inimigo -= velocidade_inimigo
            if pos_x_inimigo <= -65:
                if level == 1:
                    pontuacao -= 10
                elif level == 2:
                    pontuacao -= 50
                elif level == 3:
                    pontuacao -= 100
                pos_x_inimigo = 1100
                pos_y_inimigo = randint(10, 575)
                if level == 1:
                    velocidade_x_inimigo = randint(3, 4)
                elif level == 2:
                    velocidade_x_inimigo = randint(5, 6)
                elif level == 3:
                    velocidade_x_inimigo = randint(7, 8)

            if level == 2 or level == 3:
                pos_x_inimigo_2 -= velocidade_inimigo_2
                if pos_x_inimigo_2 <= -65:
                    if level == 2:
                        pontuacao -= 50
                    if level == 3:
                        pontuacao -= 100
                    pos_x_inimigo_2 = 1100
                    pos_y_inimigo_2 = randint(10, 575)
                    if level == 2:
                        velocidade_x_inimigo = randint(5, 6)
                    elif level == 3:
                        velocidade_x_inimigo = randint(7, 8)

            #Pontuação
            if pontuacao <= -1:
                perdeujogo = True
                pontuacao = 0
            mensagem = fonte_pontuacao_jogo.render(f'Pontuação: {pontuacao}', False, (255, 255, 255))
            screen.blit(mensagem, (410, 50))

            if pontuacao == 150:
                level = 2
            
            if pontuacao >= 1000:
                level = 3

            #Colisão para derrota do player
            if inimigo_rect.colliderect(player_rect) or inimigo_rect_2.colliderect(player_rect):
                player_derrotado = True

            if inimigo_rect.colliderect(player_rect_2) or inimigo_rect_2.colliderect(player_rect_2):
                player_derrotado_2 = True

            if player_derrotado and player_derrotado_2:
                perdeujogo = True
        
            if pontuacao >= 7000:
                player_venceu = True

            if player_venceu:
                screen.blit(bg_vitoria, (0, 0))
                if pygame.key.get_pressed()[K_KP_ENTER] or pygame.key.get_pressed()[K_RETURN]:
                    pontuacao = 0
                    pygame.quit()
                    exit()
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
    
