# Exemplo de como construir um labirinto cujas paredes impedem
# a movimentação do personagem
import pygame

class Bloco(pygame.sprite.Sprite):
  # Um bloco é um pedaço de parede. Visualmente, é um quadrado amarelo.
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
    # O desenho do personagem será um círculo, então vamos 
    # guardar o centro e o raio desse círculo
    self.centro = (dimensao // 2, dimensao // 2)
    self.raio = dimensao // 2
  
  def update(self):
    pygame.draw.circle(self.surface, "green", self.centro, self.raio)

  # Como a colisão entre o personagem e a parede ocorre apenas após a movimentação 
  # do personagem, a detecção de colisão é realizada nas funções de movimentação
  # definidas a seguir.

  def para_cima(self, blocos):
    # Move o personagem para cima. Caso seja detectada uma colisão após a movimentação,
    # recua o personagem de forma que ele não fique em cima da parede.
    self.rect.y -= self.velocidade
    hit_list = pygame.sprite.spritecollide(self, blocos, False)
    for bloco in hit_list:
      if bloco.rect.bottom > personagem.rect.top: # bloco está acima do personagem
        self.rect.top = bloco.rect.bottom

  def para_baixo(self, blocos):
    # Move o personagem para baixo. Caso seja detectada uma colisão após a movimentação,
    # recua o personagem de forma que ele não fique em cima da parede.
    self.rect.y += self.velocidade
    hit_list = pygame.sprite.spritecollide(self, blocos, False)
    for bloco in hit_list:
      if self.rect.bottom > bloco.rect.top: # bloco está abaixo do personagem
        self.rect.bottom = bloco.rect.top
  
  def para_direita(self, blocos):
    # Move o personagem para a direita. Caso seja detectada uma colisão após a movimentação,
    # recua o personagem de forma que ele não fique em cima da parede.
    self.rect.x += self.velocidade
    hit_list = pygame.sprite.spritecollide(self, blocos, False)
    for bloco in hit_list:
      if bloco.rect.x > self.rect.x: # bloco está à direita do personagem
        self.rect.right = bloco.rect.left
  
  def para_esquerda(self, blocos):
    # Move o personagem para a esquerda. Caso seja detectada uma colisão após a movimentação,
    # recua o personagem de forma que ele não fique em cima da parede.
    self.rect.x -= self.velocidade
    hit_list = pygame.sprite.spritecollide(self, blocos, False)
    for bloco in hit_list:
      if bloco.rect.x < self.rect.x: # bloco está à esquerda do personagem
        self.rect.left = bloco.rect.right

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
DIM_TILE = 60 # dimensões de um tile, o qual representa uma célula do mapa
# Calcula largura e altura da janela do jogo com base na quantidade de tiles do mapa
DIM_JANELA = (
  len(mapa[0]) * DIM_TILE, # len(mapa[0]) obtém a quantidade de colunas do mapa
  len(mapa) * DIM_TILE     # len(mapa) obtém a quantidade de linha do mapa
)
DIM_PERSONAGEM = DIM_TILE

pygame.init()
janela = pygame.display.set_mode(DIM_JANELA)
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
blocos = pygame.sprite.Group()
# cria e posiciona os sprites de bloco/parede de acordo com o mapa
for i, linha in enumerate(mapa):
  for j, v in enumerate(linha):
    x = j * DIM_TILE
    y = i * DIM_TILE
    if v == 1:
      s = Bloco(x, y, DIM_TILE)
      sprites.add(s)
      blocos.add(s)
    elif v == 2:
      personagem = Personagem(x + 5, y, DIM_PERSONAGEM)
      sprites.add(personagem)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  teclas = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if teclas[pygame.K_LEFT]:
    personagem.para_esquerda(blocos)
  if teclas[pygame.K_RIGHT]:
    personagem.para_direita(blocos)
  if teclas[pygame.K_UP]:
    personagem.para_cima(blocos)
  if teclas[pygame.K_DOWN]:
    personagem.para_baixo(blocos)

  sprites.update()
  janela.fill((0, 0, 0))
  sprites.draw(janela)
  pygame.display.flip()
  clock.tick(60)
