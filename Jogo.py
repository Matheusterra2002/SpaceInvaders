import pygame, random
from pygame.locals import *
import _thread

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
COR =  (0,255,0)
MENU = True
START = False
SOBRE = False
HELP = False


## Métodos referentes aos seletores de opção
x_seletor = 240
x_seletor2 = 340
y_seletor = 275

def desce_seletor():
    global y_seletor
    if y_seletor < 325:
        y_seletor += 25

def sobe_seletor():
    global y_seletor
    if y_seletor > 275:
        y_seletor -= 25


## Inicializa a o pygame
pygame.init()

## Criação da tela (Medidas já foram estabelecidas no início)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

## Parte referente ao titulo
font = pygame.font.SysFont("comicsansms", 70)
text_titulo = font.render('Space', True, (255, 255, 0))
text_titulo2 = font.render('Invaders', True, (255, 255, 0))

## Parte referente aos textos de start, sobre e help apresentados no menu
font_menu = pygame.font.SysFont("comicsansms", 30)
text_start = font_menu.render('Start', True, (255, 255, 255))
text_sobre = font_menu.render('Sobre', True, (255, 255, 255))
text_help = font_menu.render('Help', True, (255, 255, 255))

## Parte referente aos seletores
text_seletor1 = font_menu.render('>>', True, (255, 255, 255))
text_seletor2 = font_menu.render('<<', True, (255, 255, 255))

## Parte referente ao texto de instrução
font = pygame.font.SysFont("comicsansms", 20)
text = font.render('Pressione espaço para selecionar', True, (255, 255, 255))
clock = pygame.time.Clock()

## Primeiro while é para o programa rodar infinitamente
while True:

    ## O while MENU só irá funcionar quando o usuário estiver na tela de menu, ou seja, quando MENU for igual a True
    while MENU:
        
        ## criação do envento caso o usuário feche o jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        ## Pressed é responsável por ver qual tecla foi pressionada
        pressed = pygame.key.get_pressed()
        ## Caso a tecla seta para cima for pressionada é chamada a função para que os seletores mudem de posição
        if pressed[pygame.K_UP]: 
            sobe_seletor()
            pygame.time.delay(100)
        
        ## Caso a tecla seta para baixo for pressionada é chamada a função para que os seletores mudem de posição
        if pressed[pygame.K_DOWN]: 
            desce_seletor()
            pygame.time.delay(100)
        
        ## Caso a tecla Espaço for pressionada, haverá uma verificação para identificar 
        ## qual posição o Y dos seletores pararam, para que assim seja selecionada a opção
        if pressed[pygame.K_SPACE]:
            MENU = False
            if y_seletor == 275:
                START = True
            if y_seletor == 300:
                SOBRE = True
            if y_seletor == 325:
                HELP = True
        
        ## screen.fill define a cor da tela 
        screen.fill((0, 0, 0))

        ## Escrevendo os textos na tela 
        ## As contas servem para alinhar o texto no meio da tela
        screen.blit(text_titulo,(300 - text_titulo.get_width() // 2, 100 - text_titulo.get_height() // 2))
        screen.blit(text_titulo2,(310 - text_titulo2.get_width() // 2, 150 - text_titulo2.get_height() // 2))
        
        screen.blit(text_start,(300 - text_start.get_width() // 2, 285 - text_start.get_height() // 2))
        screen.blit(text_sobre,(300 - text_sobre.get_width() // 2, 310 - text_sobre.get_height() // 2))
        screen.blit(text_help,(300 - text_help.get_width() // 2, 335 - text_help.get_height() // 2))

        screen.blit(text_seletor1,(x_seletor, y_seletor))
        screen.blit(text_seletor2,(x_seletor2, y_seletor))

        screen.blit(text,(200,400))

        pygame.display.flip()
        clock.tick(60)

    ## O while START só irá funcionar quando o usuário estiver na tela de start, ou seja, quando START for igual a True
    while START:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            
            pressed = pygame.key.get_pressed()
            ## Caso a tecla ESC seja pressionada o jogo retorna para a tela de Menu
            if pressed[pygame.K_ESCAPE]:
                START = False
                MENU = True

        screen.fill((0, 0, 0))
        
        
        pygame.display.flip()
        clock.tick(60)
    
    ## criando texto da tela Sobre
    font_info = pygame.font.SysFont("comicsansms", 40)
    text_TelaSobre = font_info.render('Sobre o jogo', True, (255, 255, 0))

    ## O while SOBRE só irá funcionar quando o usuário estiver na tela de sobre, ou seja, quando SOBRE for igual a True
    while SOBRE:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            
            pressed = pygame.key.get_pressed()
            ## Caso a tecla ESC seja pressionada o jogo retorna para a tela de Menu
            if pressed[pygame.K_ESCAPE]:
                SOBRE = False
                MENU = True

        screen.fill((0, 0, 0))

        ## Exibindo texto da tela Sobre
        screen.blit(text_TelaSobre,(300 - text_TelaSobre.get_width() // 2, 40 - text_TelaSobre.get_height() // 2))
        
        ## Criando imagem referente ao texto encontrado na tela Sobre
        image = pygame.image.load('./assets/images/tela_sobre.png').convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH,SCREEN_HEIGHT))
        if image == None:
            print("Erro ao carregar")
            quit()
        
        ## Exibindo a imagem
        screen.blit(image,(10,100))

        pygame.display.flip()
        clock.tick(60)

    ## criando texto da tela Help
    text_TelaHelp = font_info.render('Help', True, (255, 255, 0))
    while HELP:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                HELP = False
                MENU = True

        screen.fill((0, 0, 0))

        ## Exibindo texto da tela Help
        screen.blit(text_TelaHelp,(300 - text_TelaHelp.get_width() // 2, 40 - text_TelaHelp.get_height() // 2))
        
        ## Criando imagem referente ao texto encontrado na tela Sobre   
        image = pygame.image.load('./assets/images/tela_help.png').convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH,SCREEN_HEIGHT))
        if image == None:
            print("Erro ao carregar")
            quit()
        
        ## Exibindo a imagem
        screen.blit(image,(10,60))
        
        pygame.display.flip()
        clock.tick(60)
    