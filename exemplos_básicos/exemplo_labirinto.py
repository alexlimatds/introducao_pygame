# Exemplo TODO
import pygame

class Bloco(pygame.sprite.Sprite):
  # Um bloco é um pedaço de parede
  def __init__(self, x, y, dimensao):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    self.surface = pygame.Surface([dimensao, dimensao])
    self.surface.fill('yellow')
    self.rect = self.surface.get_rect()
    self.rect.topleft = (x, y)
    self.image = self.surface

class Personagem(pygame.sprite.Sprite):
  def __init__(self, x, y, dimensao):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    self.surface = pygame.Surface([dimensao, dimensao])
    pygame.draw.circle(self.surface, "blue", (x + dimensao) // 2, (y + dimensao) // 2, dimensao // 2)
    self.rect = self.surface.get_rect()
    self.rect.topleft = (x, y)
    self.image = self.surface

# Mapa do labirinto como uma matriz. O valor 0 representa uma área vazia, 
# 1 representa um bloco, 2 representa o ponto de chegada, 3 representa 
# o ponto de partida do personagem.
# Este mapa é usado para criar os sprites que representam as paredes,  
# o ponto de chegada e o personagem.
mapa = [
  [0, 0, 0, 0, 0, 0, 0, 0], 
  [0, 0, 0, 0, 0, 0, 0, 0], 
  [0, 1, 1, 1, 1, 1, 1, 1], 
  [0, 1, 0, 0, 0, 0, 0, 2], 
  [0, 1, 0, 0, 1, 1, 1, 1], 
  [0, 1, 0, 0, 1, 0, 0, 0], 
  [0, 1, 3, 0, 1, 0, 0, 0]
]
DIM_TILE = 30 # dimensões de um tile, o qual representa uma célula do mapa
DIM_JANELA = (len(mapa[0]) * DIM_TILE, len(mapa) * DIM_TILE) # largura e altura da janela do jogo

pygame.init()
janela = pygame.display.set_mode(DIM_JANELA)
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
# cria e posiciona os sprites de bloco/parede de acordo com o mapa
for i, linha in enumerate(mapa):
  for j, v in enumerate(linha):
    if v == 1:
      x = j * DIM_TILE
      y = i * DIM_TILE
      s = Bloco(x, y, DIM_TILE)
      sprites.add(s)
    elif v == 3:
      s = Personagem(x, y, DIM_TILE * 0.7 // 1)
      sprites.add(s)

while True:
  for event in pygame.event.get():       # detecta a ocorrência de um evento
    if event.type == pygame.QUIT:        # para tratar o evento de fechamento da janela
      pygame.quit()                      # encerra o programa

  teclas = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if teclas[pygame.K_LEFT]:   # tecla direcional esquerda está sendo pressionada?
    x = x - velocidade
  if teclas[pygame.K_RIGHT]:  # tecla direcional direita está sendo pressionada?
    x = x + velocidade
 	
  sprites.update()

  janela.fill((0, 0, 0))
  sprites.draw(janela)
  pygame.display.flip()
  clock.tick(60)
