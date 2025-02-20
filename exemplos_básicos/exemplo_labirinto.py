# Exemplo de como construir um labirinto cujas paredes impedem
# a movimentação do personagem
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
    self.rect = self.surface.get_rect()
    self.rect.topleft = (x, y)
    self.image = self.surface
    self.velocidade = 5
    self.ultimo_x = x  # caso o movimente precise ser anulado
    self.ultimo_y = y  # caso o movimente precise ser anulado
    # O desenho do personagem será um círculo, então vamos 
    # guardar o centro e o raio desse círculo
    self.centro = (dimensao // 2, dimensao // 2)
    self.raio = dimensao // 2
  
  def para_cima(self):
    self.ultimo_y = self.rect.y
    self.rect.y -= self.velocidade
  def para_baixo(self):
    self.ultimo_y = self.rect.y
    self.rect.y += self.velocidade
  def para_direita(self):
    self.ultimo_x = self.rect.x
    self.rect.x += self.velocidade
  def para_esquerda(self):
    self.ultimo_x = self.rect.x
    self.rect.x -= self.velocidade
  
  def anular_movimento(self):
    self.rect.x = self.ultimo_x
    self.rect.y = self.ultimo_y

  def update(self):
    pygame.draw.circle(self.surface, "green", self.centro, self.raio)

# Mapa do labirinto como uma matriz. O valor 0 representa uma área vazia, 
# 1 representa um bloco, 2 representa o ponto de partida do personagem.
# Este mapa é usado para criar os sprites que representam as paredes  
# e o personagem.
mapa = [
  [0, 0, 0, 0, 0, 1, 1, 1], 
  [0, 0, 0, 0, 0, 1, 0, 1], 
  [0, 1, 1, 1, 1, 1, 0, 1], 
  [0, 1, 0, 0, 0, 0, 0, 1], 
  [0, 1, 0, 0, 1, 1, 1, 1], 
  [0, 1, 2, 0, 1, 0, 0, 0], 
  [0, 1, 1, 1, 1, 0, 0, 0]
]
DIM_TILE = 30 # dimensões de um tile, o qual representa uma célula do mapa
DIM_JANELA = (len(mapa[0]) * DIM_TILE, len(mapa) * DIM_TILE) # largura e altura da janela do jogo

pygame.init()
janela = pygame.display.set_mode(DIM_JANELA)
clock = pygame.time.Clock()

velocidade = 5 # velocidade do personagem
sprites = pygame.sprite.Group()
paredes = pygame.sprite.Group()
# cria e posiciona os sprites de bloco/parede de acordo com o mapa
for i, linha in enumerate(mapa):
  for j, v in enumerate(linha):
    x = j * DIM_TILE
    y = i * DIM_TILE
    if v == 1:
      s = Bloco(x, y, DIM_TILE)
      sprites.add(s)
      paredes.add(s)
    elif v == 2:
      personagem = Personagem(x + 5, y, DIM_TILE * 0.7 // 1)
      sprites.add(personagem)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  teclas = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if teclas[pygame.K_LEFT]:
    personagem.para_esquerda()
  if teclas[pygame.K_RIGHT]:
    personagem.para_direita()
  if teclas[pygame.K_UP]:
    personagem.para_cima()
  if teclas[pygame.K_DOWN]:
    personagem.para_baixo()

  hit_list = pygame.sprite.spritecollide(personagem, paredes, False)
  if hit_list: # anula o último movimento caso tenha havido uma colisão
    personagem.anular_movimento()

  sprites.update()
  janela.fill((0, 0, 0))
  sprites.draw(janela)
  pygame.display.flip()
  clock.tick(60)
