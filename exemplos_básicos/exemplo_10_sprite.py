import pygame

class CerejaSprite(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    cereja_img  = pygame.image.load('exemplos_básicos/cereja.png').convert_alpha()
    cereja_img = pygame.transform.scale(cereja_img, (100, 100))
    self.image = cereja_img
    self.rect = cereja_img.get_rect()
    self.rect.topleft = (x, y)

class PacmanSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    img = pygame.image.load('exemplos_básicos/pacman.png').convert_alpha()
    self.img_1 = pygame.transform.scale(img, (100, 100))
    img = pygame.image.load('exemplos_básicos/pacman2.png').convert_alpha()
    self.img_2 = pygame.transform.scale(img, (100, 100))
    self.image = self.img_1
    self.rect = self.image.get_rect()
    self.rect.topleft = (250, 250)
    # variáveis para controlar a movimentação do pacman
    self.velocidade = 10
    self.sentido = 1 # 1 = para a direita, -1 = para a esquerda
    # variável para controlar a velocidade de animação do pacman
    self.tique = 1

  # O método/função update é usado para atualizar a animação do pacman. 
  # Este método é chamado a cada iteração do game loop
  def update(self):
    if self.tique == 15: # Altera a imagem do pacman a cada 15 tiques. Um tique corresponde a uma iteração do game loop
      self.tique = 0
      if self.image == self.img_1:
        self.image = self.img_2
      else:
        self.image = self.img_1
    self.tique += 1

  def para_a_esquerda(self):
    if self.sentido == 1:
      self.sentido = -1
      self.img_1 = pygame.transform.flip(self.img_1, True, False)
      self.img_2 = pygame.transform.flip(self.img_2, True, False)
      self.image = pygame.transform.flip(self.image, True, False)
    self.rect.x -= self.velocidade

  def para_a_direita(self):
    if self.sentido == -1:
      self.sentido = 1
      self.img_1 = pygame.transform.flip(self.img_1, True, False)
      self.img_2 = pygame.transform.flip(self.img_2, True, False)
      self.image = pygame.transform.flip(self.image, True, False)
    self.rect.x += self.velocidade

  def para_cima(self):
    self.rect.y -= self.velocidade

  def para_baixo(self):
    self.rect.y += self.velocidade

### GAME LOOP ###
pygame.init()
janela = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# Cria sprites e grupos
pacman = PacmanSprite()
sprites_cerejas = pygame.sprite.Group([CerejaSprite(10, 10), CerejaSprite(500, 10), CerejaSprite(250, 500)])
todos_sprites = pygame.sprite.Group()
todos_sprites.add(pacman)
todos_sprites.add(sprites_cerejas.sprites())

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

  # Usa a função pygame.sprite.spritecollide para detectar colisão entre 
  # o pacman e os sprites no grupo sprites_cerejas. Requer que as sprites
  # possuam uma variável/atributo self.rect
  # O parâmetro True indica que os sprites/cerejas que colidiram com o pacman 
  # devem ser removidos de todos os grupos em que se encontram. 
  # O retorno é uma lista das cerejas que colidiram com o pacman.
  hit_list = pygame.sprite.spritecollide(pacman, sprites_cerejas, True)

  todos_sprites.update() # chama o método update de todos os sprites presentes no grupo

  janela.fill((255, 255, 255)) # limpa o quadro

  # Desenha no quadro todo os sprites presentes no grupo. Requer que 
  # cada sprite possua uma variável/atributo self.image
  todos_sprites.draw(janela)

  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)
