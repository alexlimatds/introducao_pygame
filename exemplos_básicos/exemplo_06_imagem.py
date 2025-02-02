# Exemplo que carrega e exibe duas imagens. 
# Uma das imagens não possui fundo transparente (canal alpha) e então a cor do seu
# pixel no ponto (0, 0) é usada como cor de transparência.
# A outra imagem possui fundo transparente.
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Carregando imagem sem canal alpha
imagem = pygame.image.load('exemplos_básicos/logo_ifrn.png') # lê arquivo de imagem
imagem = imagem.convert()        # otimiza a imagem para a tela em uso
color = imagem.get_at((0, 0))    # obtém a cor do pixel na posição (0, 0)
imagem.set_colorkey(color)       # define a cor de transparência da imagem

# Carregando imagem com canal alpha
imagem_alpha = pygame.image.load('exemplos_básicos/logo_ifrn_alpha.png')
imagem_alpha = imagem_alpha.convert_alpha() # otimiza a imagem e deixa o canal alpha transparente

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
  
  screen.fill((200, 200, 200)) # limpa o quadro atual

  # desenha imagens no quadro atual
  screen.blit(imagem, (15, 15))
  screen.blit(imagem_alpha, (300, 15))

  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)
