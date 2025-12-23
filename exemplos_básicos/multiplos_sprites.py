# Exemplo de jogo com múltiplos sprites
import pygame

JANELA_LARGURA = 500
JANELA_ALTURA = 500

class Inimigo(pygame.sprite.Sprite):
  # Visualmente, é um quadrado verde que pulsa
  def __init__(self, x, y, dimensao, direcao_inicial, velocidade):
    pygame.sprite.Sprite.__init__(self)
    self.surface_original = pygame.Surface([dimensao, dimensao])
    self.image = self.surface_original
    self.rect = self.surface_original.get_rect()
    self.rect.topleft = (x, y)
    # variáveis para controle de movimento
    self.direcao_inicial = direcao_inicial
    self.velocidade = velocidade
    # variáveis para controle de pulso
    self.dimensao_max = dimensao
    self.dimensao_min = dimensao * 0.6
    self.crescimento = -1
  
  def update(self):
    self.image.fill("green")
    # movimentação
    if self.direcao_inicial >= 0: # subindo
      self.rect.y -= self.velocidade
      if self.rect.y < 0:
        self.rect.y = 0
        self.direcao_inicial = -1
    else: # descendo
      self.rect.bottom += self.velocidade
      if self.rect.bottom > JANELA_ALTURA:
        self.rect.bottom = JANELA_ALTURA
        self.direcao_inicial = 1
    # pulso
    d = self.rect.width + self.crescimento
    self.image = pygame.transform.scale(self.surface_original, (d, d))
    self.rect = self.image.get_rect(center=self.rect.center)
    if d >= self.dimensao_max:
      self.crescimento = self.crescimento * -1
    elif d <= self.dimensao_min:
      self.crescimento = self.crescimento * -1

class Personagem(pygame.sprite.Sprite):
  # Visualmente, é um quadrado azul
  def __init__(self, x, y, dimensao):
    pygame.sprite.Sprite.__init__(self)
    self.surface = pygame.Surface([dimensao, dimensao])
    self.rect = self.surface.get_rect()
    self.rect.topleft = (x, y)
    self.image = self.surface
    self.velocidade = 5
  
  def update(self):
    self.surface.fill((0, 0, 255))

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
inimigos = pygame.sprite.Group()
inimigo = Inimigo(70, 5, 50, 1, 5) # inimigo 1
todos_sprites.add(inimigo)
inimigos.add(inimigo)
inimigo = Inimigo(180, JANELA_ALTURA - 30, 30, -1, 20) # inimigo 2
todos_sprites.add(inimigo)
inimigos.add(inimigo)
inimigo = Inimigo(270, 5, 100, 1, 2) # inimigo 3
todos_sprites.add(inimigo)
inimigos.add(inimigo)

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
  for i in colididos:
    personagem.rect.x = x_personagem_inicial # move personagem para posição inicial

  # atualização do quadro
  janela.fill((255, 255, 255))
  todos_sprites.draw(janela)
  pygame.display.flip()
  clock.tick(60)
pygame.quit()