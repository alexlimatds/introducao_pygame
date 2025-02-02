# Exemplo que mostra como tratar eventos do mouse
import pygame

pygame.init()
janela = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 24)
mouse_x, mouse_y = 0, 0                # coordenadas do ponteiro do mouse
texto_1, texto_2 = None, "Sem clique"  # textos a serem exibidos

while True:
  for event in pygame.event.get():             # detecta a ocorrência de um evento
    if event.type == pygame.QUIT:              # para tratar o evento de fechamento da janela
      pygame.quit()                            # para encerrar o programa
    elif event.type == pygame.MOUSEMOTION:     # evento de movimentação do mouse
      mouse_x = event.pos[0]                   # obtém coordenada x ponteiro do mouse
      mouse_y = event.pos[1]                   # obtém coordenada y ponteiro do mouse
    elif event.type == pygame.MOUSEBUTTONDOWN: # evento de pressionamento de botão do mouse
      texto_2 = f"Último clique: botão {event.button} em ({event.pos[0]}, {event.pos[1]}) " # gera texto
  
  janela.fill((255, 255, 255)) # limpa quadro atual

  surface_texto_1 = fonte.render(f"Posição: {mouse_x}, {mouse_y}", True, 'black') # gera texto a ser desenhado na janela
  janela.blit(surface_texto_1, (15, 15)) # desenha texto na janela
  surface_texto_2 = fonte.render(texto_2, True, 'black') # gera texto a ser desenhado na janela
  janela.blit(surface_texto_2, (15, 40)) # desenha texto na janela
  
  pygame.display.flip()
  clock.tick(60)
