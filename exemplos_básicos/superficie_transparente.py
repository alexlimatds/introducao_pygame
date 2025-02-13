# Exemplo que cria uma superfície com nível de transparência
import pygame

pygame.init()
janela = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()

fundo = pygame.Surface([200, 200])
desenho_fundo = pygame.Rect(0, 90, 200, 20)
superficie_transparente = pygame.Surface([50, 50])
font = pygame.font.Font(None, 24)
texto = font.render(f"Olá Mundo!", True, 'black')

valor_alpha = 100 # nível de transparência da superfície transparente
while True:
  # Processamento de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  # Atualiza os objetos do jogo
  fundo.fill((0, 0, 0))
  pygame.draw.rect(fundo, (255, 255,255), desenho_fundo) # desenha retângulo branco no fundo
  superficie_transparente.fill((255, 0, 0))
  superficie_transparente.set_alpha(valor_alpha) # define nível de transparência da superfície

  # Desenha novo quadro
  janela.fill((255, 255, 255))  # limpa o quadro atual
  janela.blit(fundo, (0, 0))
  janela.blit(superficie_transparente, (75, 75))
  janela.blit(texto, (80, 90))

  pygame.display.flip()
  clock.tick(10)
