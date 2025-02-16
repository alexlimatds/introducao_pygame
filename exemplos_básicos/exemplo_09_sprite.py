import pygame

class CerejaSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    cereja_img  = pygame.image.load('exemplos_básicos/cereja.png').convert_alpha()
    cereja_img = pygame.transform.scale(cereja_img, (100, 100))
    self.image = cereja_img            # self.image é usado por Group para renderizar o sprite
    self.rect = cereja_img.get_rect()  # self.rect é usado por Group para renderizar o sprite na posição indicada
    self.rect.topleft = (10, 10)       # posiciona o sprite nas coordenadas indicadas
  
  def mover(self):
    if self.rect.x == 10:
      self.rect.topleft = (500, 500)
    else:
      self.rect.topleft = (10, 10)

class PacmanSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    pacman_img = pygame.image.load('exemplos_básicos/pacman.png').convert_alpha()
    pacman_img = pygame.transform.scale(pacman_img, (100, 100))
    self.image = pacman_img            # self.image é usado por Group para renderizar o sprite
    self.rect = pacman_img.get_rect()  # self.rect é usado por Group para renderizar o sprite na posição indicada
    self.rect.topleft = (250, 250)     # posiciona o sprite nas coordenadas indicadas
    # variáveis para controlar a movimentação do pacman
    self.velocidade = 10
    self.sentido = 1 # 1 = para a direita, -1 = para a esquerda

  def para_a_esquerda(self): # move o sprite para a esquerda
    if self.sentido == 1:
      self.sentido = -1
      self.image = pygame.transform.flip(self.image, True, False) # inverte a imagem
    self.rect.x -= self.velocidade

  def para_a_direita(self): # move o sprite para a direita
    if self.sentido == -1:
      self.sentido = 1
      self.image = pygame.transform.flip(self.image, True, False) # inverte a imagem
    self.rect.x += self.velocidade

  def para_cima(self): # move o sprite para cima
    self.rect.y -= self.velocidade

  def para_baixo(self): # move o sprite para baixo
    self.rect.y += self.velocidade

### GAME LOOP ###
pygame.init()
janela = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# cria sprites
cereja = CerejaSprite()
pacman = PacmanSprite()
todos_sprites = pygame.sprite.Group([cereja, pacman])

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  keys = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if keys[pygame.K_LEFT]:
    pacman.para_a_esquerda()
  if keys[pygame.K_RIGHT]:
    pacman.para_a_direita()
  if keys[pygame.K_UP]:
    pacman.para_cima()
  if keys[pygame.K_DOWN]:
    pacman.para_baixo()

  # Verifica colisão e move a cereja em caso positivo
  if pacman.rect.colliderect(cereja.rect):
    cereja.mover()

  janela.fill((255, 255, 255)) # Limpa o quadro

  # Desenha no quadro todo os sprites presentes no grupo. Requer que 
  # cada sprite possua uma variável/atributo self.image
  todos_sprites.draw(janela)

  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)
