from re import X
import pygame
from pygame.locals import *
from sys import exit
from random import randint

import cv2
import mediapipe as mp

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

maos = mp_maos.Hands()

camera = cv2.VideoCapture(0)

resolucao_x = 468
resolucao_y = 351
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucao_y)

def EncotrarCoordMaos(img, lado_invertido = False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = maos.process(img_rgb)

    todas_maos = []

    if resultado.multi_hand_landmarks:
        for lado_mao, marcacoes_maos in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_mao = {}
            coordenadas = []

            for marcacao in marcacoes_maos.landmark:
                coord_x, coord_y, coord_z = int(marcacao.x * resolucao_x), int(marcacao.y * resolucao_y), int(marcacao.z * resolucao_x)
                coordenadas.append((coord_x, coord_y, coord_z))

            info_mao['coordenadas'] = coordenadas

            if lado_invertido:
                if lado_mao.classification[0].label == 'Left':
                    info_mao['Lado'] = 'Right'
                else:
                    info_mao['Lado'] = 'Left'
            else:
                info_mao['Lado'] = lado_mao.classification[0].label

            todas_maos.append(info_mao)

            mp_desenho.draw_landmarks(img, marcacoes_maos, mp_maos.HAND_CONNECTIONS)

    return img, todas_maos

def DedosLevantados(mao):
    dedos = []

    for ponta_dedos in [8, 12, 16, 20]:
        if mao['coordenadas'][ponta_dedos][1] < mao['coordenadas'][ponta_dedos - 2][1]:
            dedos.append(True)
        else:
            dedos.append(False)

    return dedos

clock = pygame.time.Clock()

x = 1000
y = 650

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
player_venceu = False

pos_x_player = 175
pos_y_player = y/2

movimento_y_player = 5

pontuacao = 0

level = 1

#Inimigo
inimigo_img = pygame.image.load('img/inimigo.png').convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (65,65))
inimigo_img = pygame.transform.rotate(inimigo_img, 90)
inimigo_rect = inimigo_img.get_rect()

pos_x_inimigo = 1100
pos_y_inimigo = randint(67, 583)

velocidade_inimigo = 6

#Fonte
pygame.font.init()
fonte_pontuacao_jogo = pygame.font.SysFont('fonte/TTSquares-Bold.ttf', 40, True, False)
fonte_pontuacao_derrota = pygame.font.SysFont('fonte/TTSquares-Bold.ttf', 100, True, False)

#Surfaces
tiro_surface = pygame.Surface(tiro_rect.size, pygame.SRCALPHA)
tiro_surface.blit(tiro_img, (0, 0))

player_surface = pygame.Surface(player_rect.size, pygame.SRCALPHA)
player_surface.blit(player_img, (0, 0))

inimigo_surface = pygame.Surface(inimigo_rect.size, pygame.SRCALPHA)
inimigo_surface.blit(inimigo_img, (0, 0))

pygame.init()
while True:
    clock.tick(10000)

    sucesso, img = camera.read()
    if not sucesso:
        print('Não encontrou imagem.')
        break

    img = cv2.flip(img, 1)

    img, todas_maos = EncotrarCoordMaos(img)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if iniciar:
        if not player_derrotado:
            screen.blit(bg, (0, 0))

            #Movimentação da tela
            rel_x = x % bg.get_rect().width
            screen.blit(bg, (rel_x - bg.get_rect().width, 0))
            if rel_x < 1000:
                screen.blit(bg, (rel_x, 0))
            x -= 2

            #Player
            if len(todas_maos) == 1:
                info_dedos_mao1 = DedosLevantados(todas_maos[0])
                if todas_maos[0]['Lado'] == 'Right':
                    if info_dedos_mao1 == [True, False, False, False]:                
                        pos_y_player -= movimento_y_player
                        pos_y_tiro -= movimento_y_tiro

                        if pos_y_player > 10:
                            if level == 1:
                                movimento_y_player = 7
                            elif level == 2:
                                movimento_y_player = 7
                            else: 
                                movimento_y_player = 10

                            if not atirou:
                                if level == 1:
                                    movimento_y_tiro = 7
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

            if len(todas_maos) == 1:
                info_dedos_mao1 = DedosLevantados(todas_maos[0])
                if todas_maos[0]['Lado'] == 'Right':
                    if info_dedos_mao1 == [True, True, False, False]:              
                        pos_y_player += movimento_y_player
                        pos_y_tiro += movimento_y_tiro           

                        if pos_y_player <= 575:
                            if level == 1:
                                movimento_y_player = 7
                            elif level == 2:
                                movimento_y_player = 7
                            else: 
                                movimento_y_player = 10

                            if not atirou:
                                if level == 1:
                                    movimento_y_tiro = 7
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

            #Evitar bugs
            if pos_y_player <= 10:
                pos_y_player = 11
                if not atirou:
                    pos_y_tiro = 36

            if pos_y_player > 576:
                pos_y_player = 575
                if not atirou:
                    pos_y_tiro = 600

            screen.blit(tiro_surface, (pos_x_tiro, pos_y_tiro))
            tiro_rect.y = pos_y_tiro
            tiro_rect.x = pos_x_tiro

            screen.blit(player_surface, (pos_x_player, pos_y_player))
            player_rect.y = pos_y_player
            player_rect.x = pos_x_player
            
            #Tiro
            if len(todas_maos) == 1:
                info_dedos_mao1 = DedosLevantados(todas_maos[0])
                if todas_maos[0]['Lado'] == 'Right':
                    if info_dedos_mao1 == [True, True, True, False]:
                        atirou = True
                        if level == 1:
                            velocidade_x_tiro = 15
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
                        pontuacao += 25
                    elif level == 2:
                        pontuacao += 50
                    elif level == 3:
                        pontuacao += 100
                    
                    pos_x_tiro = pos_x_player + 26
                    pos_y_tiro = pos_y_player + 26
                    pos_x_inimigo = 1100
                    pos_y_inimigo = randint(10, 575)
                    velocidade_x_inimigo = 6
                    #if level == 1:
                    #    velocidade_x_inimigo = randint(3, 4)
                    #elif level == 2:
                    #    velocidade_x_inimigo = randint(5, 6)
                    #elif level == 3:
                    #    velocidade_x_inimigo = randint(7, 8)

                if pos_x_tiro >= 1001:
                    atirou = False
                    velocidade_x_tiro = 0
                    pos_x_tiro = pos_x_player + 26
                    pos_y_tiro = pos_y_player + 26

            #Inimigo
            screen.blit(inimigo_surface, (pos_x_inimigo, pos_y_inimigo))
            inimigo_rect.y = pos_y_inimigo
            inimigo_rect.x = pos_x_inimigo

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
                velocidade_x_inimigo = 6
                #if level == 1:
                    #velocidade_x_inimigo = randint(3, 4)
                #elif level == 2:
                    #velocidade_x_inimigo = randint(5, 6)
                #elif level == 3:
                    #velocidade_x_inimigo = randint(7, 8)

            

            #Pontuação
            if pontuacao <= -1:
                player_derrotado = True
                pontuacao = 0
            mensagem = fonte_pontuacao_jogo.render(f'Pontuação: {pontuacao}', False, (255, 255, 255))
            screen.blit(mensagem, (410, 50))

            if pontuacao == 150:
                level = 2
            
            if pontuacao >= 1000:
                level = 3

            #Colisão para derrota do player
            if inimigo_rect.colliderect(player_rect):
                player_derrotado = True
        
            if pontuacao >= 5000:
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

        cv2.imshow('Imagem', img)
    else:
        #Tela iniciar
        screen.blit(bg_comecar, (0, 0))
        #if pygame.key.get_pressed()[K_KP_ENTER] or pygame.key.get_pressed()[K_RETURN]:
        if len(todas_maos) == 1:
                info_dedos_mao1 = DedosLevantados(todas_maos[0])
                if todas_maos[0]['Lado'] == 'Right':
                    if info_dedos_mao1 == [True, False, False, False]:
                        iniciar = True

    pygame.display.update()
    
camera.release()
cv2.destroyAllWindows()