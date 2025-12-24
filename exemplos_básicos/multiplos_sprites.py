# Exemplo de jogo com múltiplos sprites
import pygame

JANELA_LARGURA = 500
JANELA_ALTURA = 500

class InimigoA(pygame.sprite.Sprite):
  # Visualmente, é um quadrado verde que pulsa
  def __init__(self, x, y, dimensao, direcao_inicial, velocidade):
    pygame.sprite.Sprite.__init__(self)
    self.surface_original = pygame.Surface([dimensao, dimensao])
    self.surface_original.fill("green")
    self.image = self.surface_original
    self.rect = self.surface_original.get_rect()
    self.rect.topleft = (x, y)
    # variáveis para controle de movimento
    self.velocidade = velocidade
    # variáveis para controle de pulso
    self.dimensao_max = dimensao
    self.dimensao_min = dimensao * 0.6
    self.crescimento = -1
  
  def update(self):
    # movimentação
    self.rect.y += self.velocidade
    if self.rect.y < 0:
        self.rect.y = 0
        self.velocidade *= -1
    if self.rect.bottom > JANELA_ALTURA:
        self.rect.bottom = JANELA_ALTURA
        self.velocidade *= -1
    # pulso: dimensões aumentam ou diminuiem em 1 pixel
    d = self.rect.width + self.crescimento
    self.image = pygame.transform.scale(self.surface_original, (d, d))
    self.rect = self.image.get_rect(center=self.rect.center)
    if d >= self.dimensao_max or d <= self.dimensao_min:
      self.crescimento = self.crescimento * -1

class InimigoB(pygame.sprite.Sprite):
  # Visualmente, é um quadrado vermelho cuja dimensão 
  # vertical varia
  def __init__(self, x, y, velocidade):
    pygame.sprite.Sprite.__init__(self)
    self.surface_original = pygame.Surface([30, 30])
    self.surface_original.fill("red")
    self.image = self.surface_original
    self.rect = self.surface_original.get_rect()
    self.rect.topleft = (x, y)
    # variáveis para controle da alteração de tamanho
    self.velocidade = velocidade
    self.dimensao_max = JANELA_ALTURA * 0.85
    self.dimensao_min = 30
  
  def update(self):
    # crescimento/diminuição
    d = self.rect.height + self.velocidade
    self.image = pygame.transform.scale(
      self.surface_original, 
      (self.rect.width, d)
    )
    self.rect = self.image.get_rect(center=self.rect.center)
    if d >= self.dimensao_max or d <= self.dimensao_min:
      self.velocidade *= -1

class InimigoC(pygame.sprite.Sprite):
  # Visualmente, é uma barra preta que gira
  def __init__(self, x, y, tamanho, velocidade):
    pygame.sprite.Sprite.__init__(self)
    self.surface_original = pygame.Surface(
      (3, tamanho), 
      pygame.SRCALPHA  # define que os pixels são transparentes
    )
    rect_barra = pygame.Rect(0, 0, 3, tamanho)
    pygame.draw.rect(self.surface_original, "black", rect_barra)
    self.image = self.surface_original
    self.rect = self.surface_original.get_rect()
    self.rect.topleft = (x, y)
    self.mask = pygame.mask.from_surface(self.image) # para ignorar pixels transparentes na detecção de colisão
    # variáveis para controle do girto
    self.velocidade = velocidade
    self.angulo = 0
  
  def update(self):
    # giro
    self.angulo += self.velocidade
    self.image = pygame.transform.rotate(
      self.surface_original, 
      self.angulo
    )
    self.rect = self.image.get_rect(center=self.rect.center)
    self.mask = pygame.mask.from_surface(self.image)

class Personagem(pygame.sprite.Sprite):
  # Visualmente, é um quadrado azul
  def __init__(self, x, y, dimensao):
    pygame.sprite.Sprite.__init__(self)
    self.surface = pygame.Surface([dimensao, dimensao])
    self.surface.fill((0, 0, 255))
    self.rect = self.surface.get_rect()
    self.rect.topleft = (x, y)
    self.image = self.surface
    self.velocidade = 5

  def para_cima(self):
    # Move o personagem para cima.
    self.rect.y -= self.velocidade
    if self.rect.y < 0: # Recua o personagem de forma que ele não ultrapasse os limites da janela
      self.rect.y = 0

  def para_baixo(self):
    # Move o personagem para baixo.
    self.rect.y += self.velocidade
    if self.rect.bottom > JANELA_ALTURA: # Recua o personagem de forma que ele não ultrapasse os limites da janela
      self.rect.bottom = JANELA_ALTURA
  
  def para_direita(self):
    # Move o personagem para a direita.
    self.rect.x += self.velocidade
    if self.rect.right > JANELA_LARGURA: # Recua o personagem de forma que ele não ultrapasse os limites da janela
      self.rect.right = JANELA_LARGURA
  
  def para_esquerda(self):
    # Move o personagem para a esquerda.
    self.rect.x -= self.velocidade
    if self.rect.x < 0: # Recua o personagem de forma que ele não ultrapasse os limites da janela
      self.rect.x = 0

# PROGRAMA PRINCIPAL
pygame.init()
janela = pygame.display.set_mode([JANELA_LARGURA, JANELA_ALTURA])
clock = pygame.time.Clock()

todos_sprites = pygame.sprite.Group()
# personagem
x_personagem_inicial = 5
personagem = Personagem(x_personagem_inicial, JANELA_ALTURA / 2, 30)
todos_sprites.add(personagem)
# inimigos
inimigos = pygame.sprite.Group()       # para inimigos sem pixels transparentes
inimigos_mask = pygame.sprite.Group()  # para inimigos com pixels transparentes
inimigo = InimigoA(70, 5, 50, 1, 5) # inimigo 1
todos_sprites.add(inimigo)
inimigos.add(inimigo)
inimigo = InimigoB(180, JANELA_ALTURA / 2 - 15, 8) # inimigo 2
todos_sprites.add(inimigo)
inimigos.add(inimigo)
inimigo = InimigoC(300, 20, 100, 1) # inimigo 3
todos_sprites.add(inimigo)
inimigos_mask.add(inimigo)
inimigo = InimigoC(350, 180, 280, -2) # inimigo 4
todos_sprites.add(inimigo)
inimigos_mask.add(inimigo)

continuar = True
while continuar:
  # eventos/entrada
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      continuar = False

  teclas = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if teclas[pygame.K_LEFT]:
    personagem.para_esquerda()
  if teclas[pygame.K_RIGHT]:
    personagem.para_direita()
  if teclas[pygame.K_UP]:
    personagem.para_cima()
  if teclas[pygame.K_DOWN]:
    personagem.para_baixo()

  # atualização do estado do jogo
  todos_sprites.update() # atualiza o estado de todos os sprites
  colididos = pygame.sprite.spritecollide(personagem, inimigos, False)
  colididos.extend(
    pygame.sprite.spritecollide(personagem, inimigos_mask, False, pygame.sprite.collide_mask)
  )
  for i in colididos:
    personagem.rect.x = x_personagem_inicial # move personagem para posição inicial

  # atualização do quadro
  janela.fill((255, 255, 255))
  todos_sprites.draw(janela)
  pygame.display.flip()
  clock.tick(60)
pygame.quit()