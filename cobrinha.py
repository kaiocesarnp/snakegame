#Importamos os módulos necessários: pygame, time e random
import pygame
import time
import random

#Inicializamos o Pygame com pygame.init()
pygame.init()

#Definimos as configurações iniciais da tela, incluindo largura, altura e tamanho do bloco.
largura, altura, tamanho_bloco = 800, 600, 20
preto, verde = (0, 0, 0), (0, 255, 0) #Definimos as cores preto e verde em formato RGB.

#Criamos a janela do jogo com pygame.display.set_mode()
#e definimos seu título com pygame.display.set_caption()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Game")

#Definimos a função jogo() para conter o código do jogo. Função principal
def jogo():
    #Iniciando várias variáveis, incluindo:
    #'jogo_ativo' para controlar o loop principal do jogo
    #'pontuacao' para rastrear a pontuação do jogador
    #'posicao_cobra' para a posição inicial da cobra
    #'corpo_cobra' para rastrear os blocos do corpo da cobra
    #'posicao_comida' para a posição inicial da comida
    #'velocidade_cobra' para controlar o movimento da cobra.
    jogo_ativo, pontuacao, posicao_cobra, corpo_cobra, posicao_comida, velocidade_cobra = True, 0, [largura//2, altura//2], [[largura//2, altura//2]], [random.randrange(1, (largura//tamanho_bloco)) * tamanho_bloco, random.randrange(1, (altura//tamanho_bloco)) * tamanho_bloco], [20, 0]
    
    #Inicializamos tempo_inicial para registrar o tempo desde o início do jogo.
    tempo_inicial = time.time()

    #Iniciamos um loop principal do jogo, onde o jogo continuará enquanto jogo_ativo for True.
    while jogo_ativo:
        for evento in pygame.event.get(): #Utilizamos um loop for para verificar os eventos Pygame, incluindo a capacidade de fechar a janela clicando no botão "X" da janela.
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            if evento.type == pygame.KEYDOWN: #Capturamos eventos de tecla pressionada para controlar o movimento da cobra com as teclas de seta.
                if evento.key == pygame.K_LEFT: velocidade_cobra = [-tamanho_bloco, 0]
                elif evento.key == pygame.K_RIGHT: velocidade_cobra = [tamanho_bloco, 0]
                elif evento.key == pygame.K_UP: velocidade_cobra = [0, -tamanho_bloco]
                elif evento.key == pygame.K_DOWN: velocidade_cobra = [0, tamanho_bloco]

        #Atualizamos a posição da cabeça da cobra com base na velocidade.
        posicao_cobra = [posicao_cobra[0] + velocidade_cobra[0], posicao_cobra[1] + velocidade_cobra[1]]

        #Inserimos a nova posição da cabeça da cobra na lista corpo_cobra para rastrear a cobra.
        corpo_cobra.insert(0, list(posicao_cobra))

        #Verificamos se a cobra comeu a comida, o que aumenta a pontuação e move a comida para uma nova posição aleatória.
        #Caso contrário, removemos o último bloco da cobra para manter o seu tamanho.
        if posicao_cobra == posicao_comida:
            pontuacao += 1
            posicao_comida = [random.randrange(1, (largura//tamanho_bloco)) * tamanho_bloco, random.randrange(1, (altura//tamanho_bloco)) * tamanho_bloco]
        else:
            corpo_cobra.pop()

        #Preenchemos a tela com a cor preta para limpar a tela a cada iteração.
        tela.fill(preto)

        # Desenha a cabeça da cobra como um círculo
        pygame.draw.circle(tela, verde, (posicao_cobra[0] + tamanho_bloco // 2, posicao_cobra[1] + tamanho_bloco // 2), tamanho_bloco // 2)

        #Usamos uma list comprehension para desenhar todos os blocos do corpo da cobra.
        [pygame.draw.rect(tela, verde, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco]) for bloco in corpo_cobra]

        #Desenhamos a comida da cobra como um quadrado verde.
        pygame.draw.rect(tela, verde, [posicao_comida[0], posicao_comida[1], tamanho_bloco, tamanho_bloco])

        #Contador de tempo
        tempo_decorrido = int(time.time() - tempo_inicial)
        fonte = pygame.font.Font(None, 36)
        texto_tempo = fonte.render("Tempo: " + str(tempo_decorrido) + "s", True, verde)
        tela.blit(texto_tempo, (10, 10))

        # Tamanho da cobra
        tamanho_cobra = len(corpo_cobra)
        texto_tamanho = fonte.render("Tamanho: " + str(tamanho_cobra), True, verde)
        tela.blit(texto_tamanho, (10, 50))

        pygame.display.update()

        if (posicao_cobra[0] >= largura or posicao_cobra[0] < 0 or
            posicao_cobra[1] >= altura or posicao_cobra[1] < 0 or
            corpo_cobra[0] in corpo_cobra[1:]): jogo_ativo = False

        time.sleep(0.1)

#Registra a pontuação do jogador no arquivo pontuacoes.txt após o jogo terminar
#Abrimos o arquivo pontuacoes.txt no modo de escrita ('a' significa "append",
        #ou seja, acrescentar ao final do arquivo existente, se houver).
    with open('pontuacoes.txt', 'a') as arquivo:
        
        #Verificamos se a pontuação do jogador é maior que zero.
        #Isso evita que uma linha seja escrita no arquivo se o jogador não marcar pontos no jogo.
        if pontuacao > 0:
            
            #Escrevemos no arquivo a pontuação do jogador, que inclui o tempo decorrido
            #(tempo_decorrido) e o tamanho da cobra (tamanho_cobra) no formato de
            #uma linha de texto. O \n é usado para adicionar uma quebra de linha no final.
            arquivo.write(f"Tempo: {tempo_decorrido}s - Tamanho: {tamanho_cobra}\n")

    pygame.quit()

jogo()
