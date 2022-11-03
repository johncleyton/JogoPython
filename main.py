import pygame
import sys
import math
import random
pygame.init()


# sw = screen width (largura de tela), sh = screen height (altura da tela)
sw = 800
sh = 800

# define em quantos fps o jogo vai rodar, usando clock.tick() mais abaixo no codigo
clock = pygame.time.Clock()


#Carrega as imagens que serão usadas no jogo
fundo = pygame.image.load('Imagens/fundo.png')
jogador = pygame.image.load('Imagens/nave.png')
asteroide1 = pygame.image.load('Imagens/asteroide50.png')
asteroide2 = pygame.image.load('Imagens/asteroide100.png')
asteroide3 = pygame.image.load('Imagens/asteroide150.png')
asteroideLogo = pygame.image.load('Imagens/asteroidLogo.png')

# Carrega os áudios que serão usados
tiro = pygame.mixer.Sound('Audios/Tiro.mp3')
tiro.set_volume(.5)
explosao = pygame.mixer.Sound('Audios/Explosao.mp3')
explosao.set_volume(.25)
vidaExtra = pygame.mixer.Sound('Audios/1UP.mp3')
vidaExtra.set_volume(.25)
vitoria = pygame.mixer.Sound('Audios/Vitoria.mp3')
vitoria.set_volume(.5)
pygame.mixer.music.load('Audios/Musica.mp3')
pygame.mixer.music.set_volume(0.15)

pygame.display.set_caption("Asteroides")
# win é a janela do jogo, e sw controla a largura e sh controla a altura respectivamente
win = pygame.display.set_mode((sw, sh))

def menu():
    pygame.mixer.music.play(-1)
    while True:
        # Desenha o fundo
        win.blit(fundo, (0,0))

        # Pega a posicao do mouse
        mx, my = pygame.mouse.get_pos()

        # Define fontes e os textos que serão escritos no menu
        fontMenu = pygame.font.SysFont('Fontes/SendhaFreeTrial-ywXpm.otf', 80)
        fontBotoes = pygame.font.SysFont('Fontes/PROTECTOR (Italic) Font by 7NTypes.otf', 48)
        tituloJogo = fontMenu.render('Asteroides', 1, (255,255,255))
        botaoJogar = fontBotoes.render('Jogar', 1, (255,255,255))
        botaoComoJogar = fontBotoes.render('Como Jogar', 1, (255,255,255))
        botaoSobre = fontBotoes.render('Sobre', 1, (255,255,255))
        botaoVoltar = fontBotoes.render('Para sair, aperte "ESC"', 1, (255,255,255))
        
        # Define os botões que serão retângulos que o levarão para outras def's, sendo elas, o jogo(), comoJogar() e sobre() 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        # Verifica onde foi clicado com o mouse
        if button_1.collidepoint((mx, my)):
            if click:
                jogo()
        if button_2.collidepoint((mx, my)):
            if click:
                comoJogar()
        if button_3.collidepoint((mx, my)):
            if click:
                sobre()
        # Escreve os textos e desenha os retângulos
        pygame.draw.rect(win, (255, 0, 0), button_1)
        win.blit(botaoJogar, (100, 110))
        pygame.draw.rect(win, (255, 0, 0), button_2)
        win.blit(botaoComoJogar, (53, 210))
        pygame.draw.rect(win, (255, 0, 0), button_3)
        win.blit(botaoSobre, (100, 310))
        win.blit(botaoVoltar, (10, 760))
        win.blit(tituloJogo, (400, 60))
        win.blit(asteroideLogo, (300, 100))
        
        click = False
        # Eventos que ocorrerão ao apertar um botao
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(60)


# Def onde vai ocorrer o jogo
def jogo():

    # define em quantos fps o jogo vai rodar, usando clock.tick() mais abaixo no codigo
    clock = pygame.time.Clock()
    fimDeJogo = False
    ganhou = False
    temAudio = True
    vidas = 3
    pontuacao = 0

    # ---------------------------------- Inicio da classe Jogador ----------------------------------------------

    class Player(object):
        def __init__(self):
            self.img = jogador
            self.w = self.img.get_width()
            self.h = self.img.get_height()
            self.x = sw//2
            self.y = sh//2
            # Verifica o ângulo atual da nave, pois será necessário ver isso para definir onde a seta para cima vai mover a nave
            self.angulo = 0
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosseno = math.cos(math.radians(self.angulo + 90))
            self.seno = math.sin(math.radians(self.angulo + 90))
            self.frente = (self.x + self.cosseno * self.w//2, self.y - self.seno * self.h//2)

        def desenhar(self, win):
            win.blit(self.rotatedSurf, self.rotatedRect)

#-------------------------------------Comandos relacionados à movimentação da nave------------------------------------------
        def virarEsquerda(self):
            # Ajusta a rotação da nave, uma vez que a sua frente sempre vai estar sendo modificada
            self.angulo += 5
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)    
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosseno = math.cos(math.radians(self.angulo + 90))
            self.seno = math.sin(math.radians(self.angulo + 90))
            self.frente = (self.x + self.cosseno * self.w//2, self.y - self.seno * self.h//2)

        def virarDireita(self):
            # Ajusta a rotação da nave, uma vez que a sua frente sempre vai estar sendo modificada
            self.angulo -= 5
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)    
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosseno = math.cos(math.radians(self.angulo + 90))
            self.seno = math.sin(math.radians(self.angulo + 90))
            self.frente = (self.x + self.cosseno * self.w//2, self.y - self.seno * self.h//2)

        def irParaFrente(self):
            self.x += self.cosseno * 6
            self.y -= self.seno * 6
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)    
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosseno = math.cos(math.radians(self.angulo + 90))
            self.seno = math.sin(math.radians(self.angulo + 90))
            self.frente = (self.x + self.cosseno * self.w//2, self.y - self.seno * self.h//2)

        # Impede que o jogador simplesmente saia do mapa, teleportando-o caso ele tente
        def atualizaPosicao(self):
            if self.x > sw + 50:
                self.x = 0
            elif self.x < 0 - self.w:
                self.x = sw
            elif self.y < -50:
                self.y = sh
            elif self.y > sh + 50:
                self.y = 0
    #---------------------------------------Fim dos comandos de movimentação e da classe Jogador----------------------------------------

    # ---------------------------------------Inicio da classe bala------------------------------------------------------
    # A classe bala é responsável pela criação das balas da nave, que detruirão os asteroides
    class Bala(object):
        def __init__(self):
            #As balas sempre sairão na drente da nave
            self.point = player.frente
            self.x, self.y = self.point
            # Tamanho das balas, sendo w a largura e h a altura
            self.w = 4
            self.h = 6
            self.c = player.cosseno
            self.s = player.seno
            # xv e xy são responsáveis pela velocidade x e y das balas
            self.xv = self.c * 10
            self.yv = self.s * 10

        def move(self):
            self.x += self.xv
            self.y -= self.yv

        def desenhar(self, win):
            pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])


        # Verifica se a bala atirada pela nave está fora da tela, para depois apagá-la
        def foraDaTela(self):
            if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
                return True

# --------------------------------------Fim da classe bala--------------------------------------------------------

# ---------------------------------------Inicio da classe Asteroide------------------------------------------------

# A classe asteroides é responsável por instanciar os asteroides que terão que ser destruidos
    class Asteroides(object):
        def __init__(self, rank):
        # O rank dos asteroides indica o tamanho deles, quando um é destruído se transforma em 2 de um rank menor
            self.rank = rank
            if self.rank == 1:
                self.image = asteroide1
            elif self.rank == 2:
                self.image = asteroide2
            else:
                self.image = asteroide3
            self.w = 50 * rank
            self.h = 50 * rank
            # Instancia uma posição aleatória fora da tela para criar os asteroides, evitando que nasça em cima do jogador
            self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
            self.x, self.y = self.ranPoint
            # Seta a direção x para direita se o asteroide foi criado na esquerda da tela
            if self.x < sw//2:
                self.xdir = 1
            # Seta a direção x para esquerda se o asteroide foi criado na direita da tela
            else:
                self.xdir = -1
            # Seta a direção y para baixo se o asteroide foi criado em cima na tela
            if self.y < sh//2:
                self.ydir = 1
            # Seta a direção y para cima se o asteroide foi criado em baixo na tela
            else:
                self.ydir = -1
            # A velocidade dos asteroides é randomizada também, deixando o jogo mais imprevisível e divertido (se quiser alterar os valores),
            # ele sorteia um numero de 1 à 3 nos parênteses então é so trocar
            self.xv = self.xdir * random.randrange(1,3)
            self.yv = self.ydir * random.randrange(1,3)

        def desenhar(self, win):
            win.blit(self.image, (self.x, self.y))

# --------------------------------------Fim da classe Asteroide-------------------------------------------------------

    # Re-desenha tudo, background, nova posicao da nave, balas, etc.
    def atualizaTela():
        win.blit(fundo, (0,0))
        player.desenhar(win)
        # Fonte que as palavras irão usar
        fontJogo = pygame.font.SysFont('Fontes\PROTECTOR (Italic) Font by 7NTypes.otf',40)
        quantasVidas = fontJogo.render('Vidas: ' + str(vidas), 1, (255, 255, 255))
        jogarNovamente = fontJogo.render('Quer jogar novamente? Aperte "Espaço"', 1, (255, 255, 255))
        voltarMenu = fontJogo.render('Quer voltar ao menu? Aperte "ESC"', 1, (255, 255, 255))
        pontuacaoAtual = fontJogo.render('Pontuação: ' + str(pontuacao), 1, (255,255,255))
        parabens = fontJogo.render('Parabéns! Você ganhou!', 1, (255,255,255))


        for i in balasJogador:
            i.desenhar(win)
        for a in asteroides:
            a.desenhar(win)
        
        # Verifica se o usuário ganhou
        if fimDeJogo and ganhou:
            win.blit(parabens, (sw//2-parabens.get_width()//2, sh//2 - parabens.get_height()//2 - 40))
            win.blit(jogarNovamente, (sw//2-jogarNovamente.get_width()//2, sh//2 - jogarNovamente.get_height()//2))
            win.blit(voltarMenu, (sw//2-voltarMenu.get_width()//2, sh//2 - voltarMenu.get_height()//2 + 40))

        elif fimDeJogo:
            win.blit(jogarNovamente, (sw//2-jogarNovamente.get_width()//2, sh//2 - jogarNovamente.get_height()//2))
            win.blit(voltarMenu, (sw//2-voltarMenu.get_width()//2, sh//2 - voltarMenu.get_height()//2 - 40))
        win.blit(pontuacaoAtual, (20, 50))
        win.blit(quantasVidas, (20, 20))
        pygame.display.update()

    # count vai definir de quanto em quanto tempo asteroides vao aparecer
    count = 0
    jaOcorreu = False
    jaOcorreu1000 = False
    divisor = 60
    player = Player()
    # balasJogador[] é responsável por armazenar as balas que o jogador atirou
    balasJogador = []
    # asteroides[] é responsável por armazenar os asteroides que serão criados
    asteroides = []

    run = True
    while run:
        # Define os fps's que o jogo vai rodar
        clock.tick(60)
        if not fimDeJogo:
            player.atualizaPosicao()
            count += 1
            if pontuacao != 0:
                # A cada 500 pontos, irao nascer mais asteroide e o jogador ganhará mais uma vida, o mesmo ocorre com 1000 pontos
                if pontuacao >= 500 and not jaOcorreu:
                    if temAudio:
                        vidaExtra.play()
                    vidas += 1
                    jaOcorreu = True
                    divisor -=15
                elif pontuacao >= 1000 and not jaOcorreu1000:
                    if temAudio:
                        vidaExtra.play()
                    vidas += 1
                    jaOcorreu1000 = True
                    divisor -=15
            # count vai aumentando a cada tick que se passa no jogo, e divisor é de quanto em quanto tempo um asteroide vai aparecer
            # o jogo roda a 60 ticks por segundo resultado em 1 meteoro a cada 60 ticks nos primeiros pontos e a cada 30 ticks a partir dos 1000
            if count % divisor == 0:
                # Randomiza qual o tamanho do asteroide, com maior chance para ser o menor pois há mais "uns"
                ran = random.choice([1,1,1,2,2,3])
                asteroides.append(Asteroides(ran))

            for i in balasJogador:
                i.move()
                if i.foraDaTela():
                    balasJogador.pop(balasJogador.index(i))

            for a in asteroides:
                a.x += a.xv
                a.y += a.yv

                # Detecta colisão da nave com os asteroides
                if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                    if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                        if temAudio:
                            explosao.play()
                        vidas -= 1
                        asteroides.pop(asteroides.index(a))
                        break

                # Colisão das balas
                for i in balasJogador:
                    # Verifica a posição das balas do jogador em relação aos meteoros
                    if (i.x >= a.x and i.x <= a.x + a.w) or i.x + i.w >= a.x and i.x + i.w <= a.x + a.w:
                        # Ocorrendo uma colisao o asteroide explode em dois menores e a bala do jogador some
                        if (i.y >= a.y and i.y <= a.y + a.h) or i.y + i.h >= a.y and i.y + i.h <= a.y + a.h:
                            if temAudio:
                                explosao.play()
                            # Verfica se o asteroide destruido é de rank 2 ou superior, separando em 2 menores na posicao que o antigo foi destruido
                            if a.rank == 3:
                                pontuacao += 5
                                separar1 = Asteroides(2)
                                separar2 = Asteroides(2)
                                separar1.x = a.x
                                separar2.x = a.x
                                separar1.y = a.y
                                separar2.y = a.y
                                asteroides.append(separar1)
                                asteroides.append(separar2)
                            elif a.rank == 2:
                                pontuacao += 10
                                separar1 = Asteroides(1)
                                separar2 = Asteroides(1)
                                separar1.x = a.x
                                separar2.x = a.x
                                separar1.y = a.y
                                separar2.y = a.y
                                asteroides.append(separar1)
                                asteroides.append(separar2)
                            else:
                                pontuacao += 20
                            asteroides.pop(asteroides.index(a))
                            balasJogador.pop(balasJogador.index(i))

            # Acabando as vidas, acaba o jogo
            if vidas <= 0:
                fimDeJogo = True


            # Jogo acaba quando a pontuação chega a 1500 pontos
            if pontuacao >= 1500:
                if temAudio:
                    vitoria.play()
                fimDeJogo = True
                ganhou = True
            

            # As setinhas do teclado controlam a movimentação da nave
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.virarEsquerda() 
            if keys[pygame.K_RIGHT]:
                player.virarDireita() 
            if keys[pygame.K_UP]:
                player.irParaFrente() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Apertando espaço irá fazer atirar
                if event.key == pygame.K_SPACE:
                    if not fimDeJogo:
                        balasJogador.append(Bala())
                        if temAudio:
                            tiro.play()
                    # Ou caso o jogo tenha acabado, irá reiniciar o jogo e suas variáveis
                    else:
                        fimDeJogo = False
                        ganhou = False
                        vidas = 3
                        pontuacao = 0
                        jaOcorreu = False
                        jaOcorreu1000 = False
                        divisor = 60
                        asteroides.clear()
                if fimDeJogo == True:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                # Ao apertar M, ele tira o aúdio do jogo ou o coloca de novo
                if event.key == pygame.K_m:
                    temAudio = not temAudio
        atualizaTela()

# def da tela de como jogar
def comoJogar():
    run = True
    while run:
        # Define a fonte, tamanho e textos dessa aba
        fontTexto = pygame.font.SysFont('Arial', 30)
        
        textoTutorial1 = fontTexto.render('Destrua os meteoros com os tiros para aumentar sua pontuação.', 1, (255,255,255))

        textoTutorial2 = fontTexto.render( 'Evite bater neles. Ao bater, você perde uma vida.',1, (255,255,255))

        textoTutorial3 = fontTexto.render(' O jogo chega ao fim quando você tiver 0 vídas ou ao atingir 1500 pontos.' ,1, (255,255,255))
        
        textoControles1 = fontTexto.render(
        '← ↑ →   - Movimentação;',
            1, (255,255,255))
            
        textoControles2 = fontTexto.render(
        '[espaço] - Atirar;',
            1, (255,255,255))
            
        textoControles3 = fontTexto.render(
        '[M]     - Mutar os efeitos sonoros;',
            1, (255,255,255))

        textoControles4 = fontTexto.render(
        '[esc]   - Sair do jogo;',
            1, (255,255,255))

        win.blit(textoTutorial1, (sw//2-textoTutorial1.get_width()//2, sh//2 + textoTutorial1.get_height()//2 - textoControles1.get_height()- textoTutorial3.get_height()- textoTutorial2.get_height()))
        win.blit(textoTutorial2, (sw//2-textoTutorial2.get_width()//2, sh//2 + textoTutorial2.get_height()//2 - textoControles1.get_height() - textoTutorial3.get_height()))
        win.blit(textoTutorial3, (sw//2-textoTutorial3.get_width()//2, sh//2 + textoTutorial3.get_height()//2 - textoControles1.get_height()))
        
        win.blit(textoControles1, (sw//2-textoControles1.get_width()//2, sh//2 + textoControles1.get_height()//2 ))
        win.blit(textoControles2, (sw//2-textoControles2.get_width()//2, sh//2 + textoControles2.get_height()//2 + textoControles1.get_height()))
        win.blit(textoControles3, (sw//2-textoControles3.get_width()//2, sh//2 + textoControles3.get_height()//2 + textoControles1.get_height() + textoControles2.get_height()))
        win.blit(textoControles4, (sw//2-textoControles4.get_width()//2, sh//2 + textoControles4.get_height()//2 + textoControles1.get_height() + textoControles2.get_height() + textoControles3.get_height()))

        # Ao apertar esc ele vai sair dessa pagina
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()
        clock.tick(60)

# def da tela de sobre
def sobre():
    run = True
    while run:
        # Define a fonte, tamanho e textos dessa aba
        fontTexto = pygame.font.SysFont('Arial', 36)
        
        sobreJogo = fontTexto.render('Esse jogo é inspirado no jogo de atari "Asteroids".', 1, (255,255,255))
        instrucoes = fontTexto.render('Destrua os asteroides antes que eles batam em você!', 1, (255, 255, 255))
        integrante1 = fontTexto.render('Integrantes: Frederico Scheffel Oliveira - RA:20133', 1, (255,255,255))
        integrante2 = fontTexto.render('Lucas Coimbra da Silva - RA: 20144', 1, (255, 255, 255))

        win.blit(sobreJogo, (sw//2-sobreJogo.get_width()//2, sh//2 - sobreJogo.get_height()//2 + -80))
        win.blit(instrucoes, (sw//2-sobreJogo.get_width()//2, sh//2 - sobreJogo.get_height()//2 - 40))
        win.blit(integrante1, (sw//2-sobreJogo.get_width()//2, sh//2 - sobreJogo.get_height()//2))
        win.blit(integrante2, (sw//2-sobreJogo.get_width()//2, sh//2 - sobreJogo.get_height()//2 + 40))
        # Ao apertar esc ele vai sair dessa pagina
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        pygame.display.update()
        clock.tick(60)

menu()
