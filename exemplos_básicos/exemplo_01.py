# Exemplo que cria uma janela com fundo branco e que contém um quadrado preto
import pygame

pygame.init() # inicializa os recursos do PyGame
janela = pygame.display.set_mode((640, 480)) # cria a janela do jogo
clock = pygame.time.Clock() # objeto que controla a taxa de FPS
continuar = True

quadrado = pygame.Surface([30, 30]) # cria quadrado com 30 pixels de lado

while continuar:
  # Processamento de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      continuar = False

  # Lógica de jogo: atualiza os objetos do jogo
  quadrado.fill((0, 0, 0))         # preenche o quadrado com cor preta

  # Desenha novo quadro
  janela.fill((255, 255, 255))     # limpa o quadro atual
  janela.blit(quadrado, (50, 200)) # desenha o quadrado no quadro atual e nas coordenadas indicadas

  pygame.display.flip() # Desenha o quadro atual na tela do computador
  clock.tick(60)        # Controla a taxa de quadros por segundo (FPS)

pygame.quit()
