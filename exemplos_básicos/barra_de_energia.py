# Exemplo que mostra a implementação de uma barra de energia
# que é alterada conforme o jogador pressiona a tecla A
import pygame

class BarraDeEnergia(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.energia = 100 # porcentagem de energia restante
    # A barra de energia é visualmente composta por dois retângulos. O retângulo 
    # azul representa a quantidade restante de energia, enquanto o
    # retânuglo vermelho representa a quantidade energia perdida
    self.largura_barra = 300 # largura em pixels da barra de energia, incluindo os dois retângulos
    self.altura = 50
    self.x_barra = 10  # coordenada do canto superior esquerdo da barra de energia
    self.y_barra = 10  # coordenada do canto superior esquerdo da barra de energia
    # a largura da barra azul e da barra vermelha é calculada na função update
    self.barra = pygame.Surface([self.largura_barra, self.altura]) # contém os retângulos azul e vermelho
    self.rect = self.barra.get_rect()
    self.rect.topleft = (self.x_barra, self.y_barra)
    self.image = self.barra
  
  def update(self):
    self.barra.fill((255, 0, 0)) # a barra vermelha é na verdade o fundo da barra
    largura_barra_azul = self.energia / 100 * self.largura_barra
    rect_barra_azul = pygame.Rect(0, 0, largura_barra_azul, self.altura)
    pygame.draw.rect(self.barra, (0, 0, 255), rect_barra_azul)

pygame.init()
janela = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

barra_de_energia = BarraDeEnergia()
sprites = pygame.sprite.Group([barra_de_energia])

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
      barra_de_energia.energia -= 10 # cada pressionamento da tecla A reduz a energia em 10%
 	 
  janela.fill((255, 255, 255)) # limpa o quadro atual
  
  sprites.update() # chama o método update de todos os sprites presentes no grupo
  sprites.draw(janela)

  pygame.display.flip()  # Desenha o quadro atual na tela do computador
  clock.tick(60)         # Controla a taxa de quadros por segundo (FPS)
