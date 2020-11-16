import pygame, random
from pygame.locals import *
import _thread
import time
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
COR =  (0,255,0)
MENU = True
START = False
SOBRE = False
HELP = False
TELA_ACABOU = False
GERA = False
ACABOU = False

SPEED_NAVE = 20
SPEED_TIRO = 15
SPEED_INIMIGO = 1

X_NAVE = 0
VIDAS = 3
VIDAS_PROTECAO = 3

X_ALIEN = 0 
Y_ALIEN = 100

Y_TIRO = 460
X_TIRO = 0
x_tiro = 0

X_PROTECAO = 30

X_BONUS = 30

X_TIRO_INIMIGO = 0
Y_TIRO_INIMIGO = 0

COLIDIU = False
ACERTOU = False

continua = False
continua2 = False

pontos = 0

sentido = 0
sentido2 = 1

pressionado = False

linha1 = 0
linha2 = 0

xpos = 0

numAleatorio = 0

acertou = False

contador_tiros = 0

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
    def __init__(self, colidiu):
        pygame.sprite.Sprite.__init__(self)
        global Y_TIRO

        self.image = pygame.image.load('./assets/images/tiro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (5,20)) 
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 460

        if colidiu:
            Y_TIRO = 460
            self.rect[1] = Y_TIRO
        else:
            self.rect[1] = Y_TIRO

    def update(self, x):
        X_TIRO = x
        if pressionado != True:
            self.rect[0] = X_TIRO + 3
            self.rect[1] = Y_TIRO
        else:
            self.rect[1] = Y_TIRO
        

def atira(xpos):
        global continua
        global pressionado
        global Y_TIRO
        global X_NAVE
        global X_TIRO
        global COLIDIU

        X_TIRO = xpos
        if Y_TIRO == 460 or Y_TIRO == 10 and COLIDIU == False:    
            SOM_TIRO.play()
            while continua:
                if Y_TIRO > 10:
                    Y_TIRO -= SPEED_TIRO
    
                if Y_TIRO == 10:
                    continua = False
                    pressionado = False
                    Y_TIRO = 460
                time.sleep(0.03)


class Alien(pygame.sprite.Sprite):
    def __init__(self, x_novo, y_novo):
        pygame.sprite.Sprite.__init__(self)
        global X_TIRO_INIMIGO

        self.speed = SPEED_NAVE

        self.image = pygame.image.load('./assets/images/alien.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))     
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        X_ALIEN = x_novo
        Y_ALIEN = y_novo
        self.rect[0] = X_ALIEN
        self.rect[1] = Y_ALIEN      
        
    def update(self):
        global sentido
        global SPEED_INIMIGO
        global Y_ALIEN

        if sentido == 0:
            self.rect[0] += SPEED_INIMIGO

        if sentido == 1:
            self.rect[0] -= SPEED_INIMIGO

        if self.rect[0] == 0:
            sentido = 0
        
        if self.rect[0] == 560:
            sentido = 1
    
    def altera_y(self, y_novo):
        if self.rect[1] == 100:
            self.rect[1] = 150
        
        if self.rect[1] == 150:
            self.rect[1] = 200

        if self.rect[1] == 200:
            self.rect[1] = 250

class Protecao(pygame.sprite.Sprite):
    def __init__(self, x_novo):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./assets/images/protecao.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))     
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        X_PROTECAO = x_novo
        self.rect[0] = X_PROTECAO
        self.rect[1] = 350 

class alien_Bonus(pygame.sprite.Sprite):
    def __init__(self, x_novo):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED_NAVE

        self.image = pygame.image.load('./assets/images/nave_bonus.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,20))     
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        X_ALIEN = x_novo
        self.rect[0] = X_ALIEN
        self.rect[1] = 40 
    
    def update(self):
        global sentido2
        global SPEED_INIMIGO

        if sentido2 == 0:
            self.rect[0] += SPEED_INIMIGO + 1

        if sentido2 == 1:
            self.rect[0] -= SPEED_INIMIGO + 1
        
        if self.rect[0] == 0:
            sentido2 = 0
        
        if self.rect[0] == 560:
            sentido2 = 1

class Tiro_Inimigo(pygame.sprite.Sprite):
    def __init__(self,Xpos,Ypos):
        pygame.sprite.Sprite.__init__(self)
        
        global X_TIRO_INIMIGO
        global Y_TIRO_INIMIGO

        self.image = pygame.image.load('./assets/images/tiro_inimigo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (5,20))     
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        X_TIRO_INIMIGO = Xpos
        Y_TIRO_INIMIGO = Ypos

        self.rect[0] = X_TIRO_INIMIGO
        self.rect[1] = Y_TIRO_INIMIGO
    
    def update(self):
        global continua2
        global Y_TIRO_INIMIGO

        if Y_TIRO_INIMIGO == 130 or Y_TIRO_INIMIGO == 180 or Y_TIRO_INIMIGO == 230:
            if self.rect[1] <= 460:
                self.rect[1] += SPEED_INIMIGO
            
            if self.rect[1] == 460:
                self.rect[1] = Y_TIRO_INIMIGO
                numAleatorio = random.randint(0,9)
                self.rect[0] = numAleatorio * 50
            

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

## Definindo o fundo do jogo
BACKGROUND = pygame.image.load('./assets/images/fundo.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

## Inicializando o mixer e definindo os sons
pygame.mixer.init()
SOM_TEMA = pygame.mixer.Sound('./assets/sounds/som_Tema.wav')
SOM_TIRO = pygame.mixer.Sound('./assets/sounds/som_Tiro.wav')
SOM_BONUS = pygame.mixer.Sound('./assets/sounds/som_nave_bonus.wav')
SOM_EXPLOSAO = pygame.mixer.Sound('./assets/sounds/som_Explosao.wav')

## Criação da tela (Medidas já foram estabelecidas no início)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

logo = pygame.image.load('./assets/images/logo.png').convert_alpha()
logo = pygame.transform.scale(logo, (400,400))     
mask = pygame.mask.from_surface(logo)

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

## Parte referente ao texto dos pontos
font_pontos = pygame.font.SysFont("comicsansms", 25)
text_score = font_pontos.render('Score', True, (255, 255, 0))

clock = pygame.time.Clock()

## Primeiro while é para o programa rodar infinitamente
while True:    
    ## O while MENU só irá funcionar quando o usuário estiver na tela de menu, ou seja, quando MENU for igual a True
    while MENU:
        ## iniciando o som
        SOM_TEMA.play()

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
                GERA = True
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

        screen.blit(logo,(310 - logo.get_width() // 2, 250 - logo.get_height() // 2))
        
        screen.blit(text_start,(300 - text_start.get_width() // 2, 285 - text_start.get_height() // 2))
        screen.blit(text_sobre,(300 - text_sobre.get_width() // 2, 310 - text_sobre.get_height() // 2))
        screen.blit(text_help,(300 - text_help.get_width() // 2, 335 - text_help.get_height() // 2))

        screen.blit(text_seletor1,(x_seletor, y_seletor))
        screen.blit(text_seletor2,(x_seletor2, y_seletor))

        screen.blit(text,(200,400))

        pygame.display.flip()
        clock.tick(60)

    ## O while START só irá funcionar quando o usuário estiver na tela de start, ou seja, quando START for igual a True
    while START and ACABOU == False:
        clock.tick(100)
        SOM_TEMA.stop()

        if GERA:
            ## Criando a nave
            nave_group = pygame.sprite.Group()
            nave = Nave()
            nave_group.add(nave)

            ## Criando os tiros
            tiro_group = pygame.sprite.Group()
            projetil = Tiro(False)
            tiro_group.add(projetil)

            ## gerando nave dos aliens, juntamente com o seu tiro
            alien_group = pygame.sprite.Group()
            tiro_alien_group = pygame.sprite.Group()
            for i in range(30):
                numAleatorio = random.randint(0,30)
                if i <= 9:
                        inimigo = Alien(50 * i, Y_ALIEN)
                        alien_group.add(inimigo)
                        
                        if numAleatorio <= 9:
                            tiro_inimigo = Tiro_Inimigo((50 * i), 130)
                            tiro_alien_group.add(tiro_inimigo)
                        

                if i >= 10 and i <= 19:
                        inimigo = Alien(50 * linha1, Y_ALIEN + 50)
                        alien_group.add(inimigo)
                        
                        if numAleatorio >= 10 and numAleatorio <= 19:
                            tiro_inimigo = Tiro_Inimigo( (linha1 * 50), 180)
                            tiro_alien_group.add(tiro_inimigo)
                        
                        linha1 = linha1 + 1
                
                if i >= 20:
                        inimigo = Alien(50 * linha2, Y_ALIEN + 100)
                        alien_group.add(inimigo)
                        
                        if numAleatorio >= 20:
                            tiro_inimigo = Tiro_Inimigo( (linha2 * 50) , 230)
                            tiro_alien_group.add(tiro_inimigo)

                        linha2 = linha2 + 1

                ## Gerando as proteções
                protecao_group = pygame.sprite.Group()
                for i in range(4):
                    protecao = Protecao(180 * i)
                    protecao_group.add(protecao)

                ## Gerando a nave bonus
                bonus_group = pygame.sprite.Group()
                bonus_nave = alien_Bonus(40)

                GERA = False


        ## Mostra os pontos do jogador
        text_pontos = font_pontos.render(str(pontos), True, (255, 255, 0))

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
                
            if pressionado != True:
                xpos = X_NAVE

            if pressed[pygame.K_SPACE]: 
                continua = True
                continua2 = True
                _thread.start_new_thread(atira,(xpos,))
                pressionado = True
                pygame.time.delay(50)
            
        x_tiro = X_NAVE + 15
        screen.fill((0, 0, 0))

        ## define o fundo
        screen.blit(BACKGROUND, (0, 0))

        ## colocando os pontos na tela
        screen.blit(text_score,(10,10))
        screen.blit(text_pontos,(70,10))

        tiro_group.update(x_tiro)
        alien_group.update()
        bonus_group.update()
        tiro_alien_group.update()

        nave_group.draw(screen)
        tiro_group.draw(screen)
        alien_group.draw(screen)
        protecao_group.draw(screen)
        bonus_group.draw(screen)
        tiro_alien_group.draw(screen)
        
        ## Verifica se houve colisão entre o tiro da nave e o inimigo
        if pygame.sprite.groupcollide(tiro_group, alien_group, True, True):
            
            SOM_EXPLOSAO.play()
            
            continua = False
            pontos += 10
            pressionado = False

            tiro_alien_group.remove(tiro_group)

            ## Criando um novo tiro
            tiro_group = pygame.sprite.Group()
            projetil = Tiro(True)
            tiro_group.add(projetil)
            tiro_group.draw(screen)


        ## Verifica se houve colisão entre o tiro do jogador e a proteção
        if pygame.sprite.groupcollide(tiro_group, protecao_group, True, False):
            continua = False
            pressionado = False

            tiro_group = pygame.sprite.Group()
            projetil = Tiro(True)
            tiro_group.add(projetil)
            tiro_group.update(x_tiro)
            tiro_group.draw(screen)

        ## Verifica se já acabou todos os aliens da tela, porém acertando a nave bonus
        if acertou == True:
            if pontos == 350 or pontos == 650:
                
                linha1 = 0
                linha2 = 0

                alien_group = pygame.sprite.Group()
                tiro_alien_group = pygame.sprite.Group()
                for i in range(30):
                    numAleatorio = random.randint(0,30)
                    if i <= 9:
                            inimigo = Alien(50 * i, Y_ALIEN)
                            alien_group.add(inimigo)
                            
                            if numAleatorio <= 9:
                                tiro_inimigo = Tiro_Inimigo((50 * i), 130)
                                tiro_alien_group.add(tiro_inimigo)
                            

                    if i >= 10 and i <= 19:
                            inimigo = Alien(50 * linha1, Y_ALIEN + 50)
                            alien_group.add(inimigo)
                            
                            if numAleatorio >= 10 and numAleatorio <= 19:
                                tiro_inimigo = Tiro_Inimigo( (linha1 * 50), 180)
                                tiro_alien_group.add(tiro_inimigo)
                            
                            linha1 = linha1 + 1
                    
                    if i >= 20:
                            inimigo = Alien(50 * linha2, Y_ALIEN + 100)
                            alien_group.add(inimigo)
                            
                            if numAleatorio >= 20:
                                tiro_inimigo = Tiro_Inimigo( (linha2 * 50) , 230)
                                tiro_alien_group.add(tiro_inimigo)

                            linha2 = linha2 + 1

        ## Cria a nave bonus
        if pontos >= 150 and pontos < 200 or pontos >= 450 and pontos < 500 :
            bonus_group.add(bonus_nave)
            SOM_BONUS.play()
        if pontos >= 200 or pontos >= 500:
            bonus_group.remove(bonus_nave)
            SOM_BONUS.stop()

        
        ## Verifica se acabou os aliens na tela, porém sem ter acertado a nave bonus
        if acertou == False: 
            if pontos == 300 or pontos == 600:
                
                linha1 = 0
                linha2 = 0

                alien_group = pygame.sprite.Group()
                tiro_alien_group = pygame.sprite.Group()
                for i in range(30):
                    numAleatorio = random.randint(0,30)
                    if i <= 9:
                            inimigo = Alien(50 * i, Y_ALIEN)
                            alien_group.add(inimigo)
                            
                            if numAleatorio <= 9:
                                tiro_inimigo = Tiro_Inimigo((50 * i), 130)
                                tiro_alien_group.add(tiro_inimigo)
                            

                    if i >= 10 and i <= 19:
                            inimigo = Alien(50 * linha1, Y_ALIEN + 50)
                            alien_group.add(inimigo)
                            
                            if numAleatorio >= 10 and numAleatorio <= 19:
                                tiro_inimigo = Tiro_Inimigo( (linha1 * 50), 180)
                                tiro_alien_group.add(tiro_inimigo)
                            
                            linha1 = linha1 + 1
                    
                    if i >= 20:
                            inimigo = Alien(50 * linha2, Y_ALIEN + 100)
                            alien_group.add(inimigo)
                            
                            if numAleatorio >= 20:
                                tiro_inimigo = Tiro_Inimigo( (linha2 * 50) , 230)
                                tiro_alien_group.add(tiro_inimigo)

                            linha2 = linha2 + 1

        ## Verifica se houve a colisão com a nave bonus
        if pygame.sprite.groupcollide(tiro_group, bonus_group, True, True):
            SOM_EXPLOSAO.play()
            
            continua = False
            pontos += 50
            pressionado = False
            acertou = True

            ## Criando um novo tiro
            tiro_group = pygame.sprite.Group()
            projetil = Tiro(True)
            tiro_group.add(projetil)
            tiro_group.update(x_tiro)
            tiro_group.draw(screen)



        img_vida = pygame.image.load('./assets/images/nave.png').convert_alpha()
        img_vida = pygame.transform.scale(img_vida, (30,30))     
        mask = pygame.mask.from_surface(img_vida)
        
        font_vidas = pygame.font.SysFont("comicsansms", 25)
        text_vidas = font_pontos.render('Lives:', True, (255, 255, 0))
        screen.blit(text_vidas, (430, 20))

        if VIDAS == 3:
            screen.blit(img_vida, (490, 10))
            screen.blit(img_vida, (530, 10))
            screen.blit(img_vida, (570, 10))
        if VIDAS == 2:
            screen.blit(img_vida, (530, 10))
            screen.blit(img_vida, (570, 10))
        if VIDAS == 1:
            screen.blit(img_vida, (570, 10))
    
        
        
        ## Verifica se houve colisão do tiro inimigo com o jogador
        if pygame.sprite.groupcollide(tiro_alien_group, nave_group, True, True):
            VIDAS -= 1
            if VIDAS >= 0:
                #Criando a nave novamente
                nave = Nave()
                nave_group.add(nave)
                
                projetil = Tiro(True)
                tiro_group.add(projetil)


            else:
                ACABOU = True
                START = False
                TELA_ACABOU = True

        ## Verifica se houve colisão do tiro inimigo com a protecão
        if pygame.sprite.groupcollide(protecao_group, tiro_alien_group, ACERTOU, True):
            VIDAS_PROTECAO -= 1
            if VIDAS_PROTECAO == 0:
                ACERTOU = True

        

        pygame.display.flip()
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
        
        ## Criando imagem referente ao texto encontrado na tela Help   
        image = pygame.image.load('./assets/images/tela_help.png').convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH,SCREEN_HEIGHT))
        if image == None:
            print("Erro ao carregar")
            quit()
        
        ## Exibindo a imagem
        screen.blit(image,(0,60))
        
        pygame.display.flip()
        clock.tick(60)

    ## criando texto da tela para quando acabar o jogo
    font_acabou = pygame.font.SysFont("comicsansms", 50)
    text_acabou = font_acabou.render('Derrotado', True, (255, 0, 0))
    text_acabou2 = font_acabou.render('A invasão alienígena irá acontecer', True, (255, 0, 0))
    text_acabou3 = font.render('Pressione ESC para voltar ao menu', True, (255, 255, 0))

    while TELA_ACABOU:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                TELA_ACABOU = False
                MENU = True
                pygame.sprite.Sprite.kill(nave)
                pygame.sprite.Sprite.kill(projetil)
                pygame.sprite.Sprite.kill(inimigo)
                pygame.sprite.Sprite.kill(tiro_inimigo)
                pygame.sprite.Sprite.kill(protecao)
                pygame.sprite.Sprite.kill(bonus_nave)

        screen.fill((0, 0, 0))

        screen.blit(BACKGROUND, (0, 0))

        ## Exibindo texto da tela acabou
        screen.blit(text_acabou,(300 - text_acabou.get_width() // 2, 200 - text_acabou.get_height() // 2))
        screen.blit(text_acabou2,(300 - text_acabou2.get_width() // 2, 300 - text_acabou2.get_height() // 2))
        screen.blit(text_acabou3,(200, 400))
        
        pygame.display.flip()
        clock.tick(60)
    