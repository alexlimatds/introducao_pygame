# Exemplo que mostra como tratar eventos do teclado
import pygame

pygame.init()
janela = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
continuar = True

quadrado = pygame.Surface([30, 30])
quadrado.fill((0, 0, 0))
x = 50 # coordenada x do quadrado

while continuar:
  for event in pygame.event.get():       # detecta a ocorrência de um evento
    if event.type == pygame.QUIT:        # para tratar o evento de fechamento da janela
      continuar = False                  # para encerrar o game loop
    elif event.type == pygame.KEYDOWN:   # para tratar eventos de pressionamento de tecla
      if event.key == pygame.K_ESCAPE:   # tecla ESC
        continuar = False                # para encerrar o game loop
      elif event.key == pygame.K_RIGHT:  # tecla direcional para a direita
        x = x + 20                       # move quadrado em 20 pixels para a direita
 	 
  janela.fill((255, 255, 255))     # limpa o quadro atual
  janela.blit(quadrado, (x, 200))  # desenha quadrado na janela

  pygame.display.flip()  # Desenha o quadro atual na tela do computador
  clock.tick(60)         # Controla a taxa de quadros por segundo (FPS)

pygame.quit()  # finaliza os recursos do PyGame
