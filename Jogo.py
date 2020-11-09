import pygame, random
from pygame.locals import *
import _thread
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
COR =  (0,255,0)
MENU = True
START = False
SOBRE = False
HELP = False
SPEED_NAVE = 20
SPEED_TIRO = 15
X_NAVE = 0
X_ALIEN = 0 
Y_TIRO = 460
X_TIRO = 0

continua = False


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('./assets/images/nave.png').convert_alpha]

        self.image = pygame.image.load('./assets/images/nave.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))     
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[1] = 450

    def move_direita(self):
        global X_NAVE
        X_NAVE += SPEED_NAVE
        self.rect[0] = X_NAVE

    def move_esquerda(self):
        global X_NAVE
        X_NAVE -= SPEED_NAVE
        self.rect[0] = X_NAVE
    
class Tiro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.image.load('./assets/images/tiro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (10,20)) 
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 460

    def update(self):
        self.rect[0] = X_TIRO
        self.rect[1] = Y_TIRO

def atira():
        global continua
        global Y_TIRO
        global X_NAVE
        global X_TIRO

        X_TIRO = X_NAVE

        while continua:
            if Y_TIRO > 10:
                Y_TIRO -= SPEED_TIRO
                
            time.sleep(0.08)
    

class Alien(pygame.sprite.Sprite):
    def __init__(self,proximo,x_proximo):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED_NAVE
        
        self.current_image = 0

        self.image = pygame.image.load('./assets/images/alien.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))     
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 100

        if proximo:
            self.rect[0] = x_proximo
    
    def update(self):
        self.rect[0] = X_ALIEN

def get_aliens(x_proximo):
    x_proximo = X_ALIEN + x_proximo
    inimigo = Alien(True, x_proximo)
    return (inimigo)
    
sentido = 0
def movimenta(width, height):
        global X_ALIEN
        global sentido
        
        while True:
            if sentido == 0:
                X_ALIEN += 5
            if sentido ==1:
                X_ALIEN -= 5
            
            if X_ALIEN == width - 50:
                sentido = 1
            
            if X_ALIEN == 20:
                sentido = 0
            
            time.sleep(0.1)


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

BACKGROUND = pygame.image.load('./assets/images/fundo.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


## Criação da tela (Medidas já foram estabelecidas no início)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

## Parte referente ao titulo
font = pygame.font.SysFont("comicsansms", 70)
text_titulo = font.render('Space', True, (255, 255, 0))
text_titulo2 = font.render('Invaders', True, (255, 255, 0))

## Parte referente aos textos de start, sobre e help apresentados no menu
font_menu = pygame.font.SysFont("comicsansms", 30)
text_start = font_menu.render('Start', True, (255, 255, 255))
text_sobre = font_menu.render('About', True, (255, 255, 255))
text_help = font_menu.render('Help', True, (255, 255, 255))

## Parte referente aos seletores
text_seletor1 = font_menu.render('>>', True, (255, 255, 255))
text_seletor2 = font_menu.render('<<', True, (255, 255, 255))

## Parte referente ao texto de instrução
font = pygame.font.SysFont("comicsansms", 20)
text = font.render('Pressione espaço para selecionar', True, (255, 255, 255))


nave_group = pygame.sprite.Group()
nave = Nave()
nave_group.add(nave)

tiro_group = pygame.sprite.Group()
projetil = Tiro()
tiro_group.add(projetil)


alien_group = pygame.sprite.Group()
alien = Alien(False, 0)
for i in range(2):
    inimigo = get_aliens(10)
    alien_group.add(alien)



_thread.start_new_thread(movimenta, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
            pygame.time.delay(100)
        
        ## screen.fill define a cor da tela 
        screen.fill((0, 0, 0))

        ## define o fundo
        screen.blit(BACKGROUND, (0, 0))

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

    pressionado = False
    ## O while START só irá funcionar quando o usuário estiver na tela de start, ou seja, quando START for igual a True
    while START:
        pressionado = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            
            pressed = pygame.key.get_pressed()
            ## Caso a tecla ESC seja pressionada o jogo retorna para a tela de Menu
            if pressed[pygame.K_ESCAPE]:
                START = False
                MENU = True
            
            if pressed[pygame.K_RIGHT] and X_NAVE < 560:
                nave.move_direita()
            

            if pressed[pygame.K_LEFT] and X_NAVE > 0:
                nave.move_esquerda()
                
            
            if Y_TIRO == 10 or Y_TIRO == 460:
                if pressed[pygame.K_SPACE]: 
                    if Y_TIRO == 460:
                        continua = True
                        _thread.start_new_thread(atira,())
                        
                        
                    if Y_TIRO == 10:
                        continua = False
                        Y_TIRO = 460
                    
                pygame.time.delay(50)
            

        screen.fill((0, 0, 0))
        
        if pressionado != True:
            X_TIRO = X_NAVE + 15

        ## define o fundo
        screen.blit(BACKGROUND, (0, 0))

        tiro_group.update()
        alien_group.update()

        nave_group.draw(screen)
        tiro_group.draw(screen)
        alien_group.draw(screen)
        
        clock.tick(100)
        pygame.display.update()
        
    
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
        screen.blit(BACKGROUND, (0, 0))

        ## Exibindo texto da tela Sobre
        screen.blit(text_TelaSobre,(300 - text_TelaSobre.get_width() // 2, 40 - text_TelaSobre.get_height() // 2))
        
        ## Criando imagem referente ao texto encontrado na tela Sobre
        image = pygame.image.load('./assets/images/tela_sobre.png').convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH,SCREEN_HEIGHT))
        if image == None:
            print("Erro ao carregar")
            quit()
        
        ## Exibindo a imagem
        screen.blit(image,(0,100))

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

        screen.blit(BACKGROUND, (0, 0))

        ## Exibindo texto da tela Help
        screen.blit(text_TelaHelp,(300 - text_TelaHelp.get_width() // 2, 40 - text_TelaHelp.get_height() // 2))
        
        ## Criando imagem referente ao texto encontrado na tela Sobre   
        image = pygame.image.load('./assets/images/tela_help.png').convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH,SCREEN_HEIGHT))
        if image == None:
            print("Erro ao carregar")
            quit()
        
        ## Exibindo a imagem
        screen.blit(image,(0,60))
        
        pygame.display.flip()
        clock.tick(60)
    