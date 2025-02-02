# Exemplo que cria uma janela com fundo branco e que contém um quadrado preto
import pygame, math

class Barra(pygame.sprite.Sprite): # barra da grade do jogo
  def __init__(self, largura, altura, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((largura, altura))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.image.fill((0, 0, 0))

class Celula(pygame.sprite.Sprite): # célula da grade do jogo
  def __init__(self, dimensao, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((dimensao, dimensao))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.jogador = 0 # jogador que marcou a célula

  def update(self):
    self.image.fill((255, 255, 255))
    if self.jogador == 1: # desenha X
      pad = DIMENSAO_CELULA * 0.2
      peso = math.ceil(LARGURA_BARRA * 0.9)
      pygame.draw.line(self.image, pygame.Color("red"), (pad, pad), (DIMENSAO_CELULA - pad, DIMENSAO_CELULA - pad), peso)
      pygame.draw.line(self.image, pygame.Color("red"), (pad, DIMENSAO_CELULA - pad), (DIMENSAO_CELULA - pad, pad), peso)
    elif self.jogador == 2: # desenha 0
      p = DIMENSAO_CELULA // 2
      pygame.draw.circle(self.image, pygame.Color("blue"), (p, p), p * 0.8)
      pygame.draw.circle(self.image, pygame.Color("white"), (p, p), p * 0.6)

def marcar_posicao(x, y, jogador, matriz):
  # x: linha da matriz a ser marcada
  # y: coluna da matriz a ser marcada
  # jogador: inteiro do jogador que tenta a jogada
  # matriz: uma matriz de sprites do tipo Celula
  if not(x >= 0 and x < 3 and y >= 0 and y < 3 and matriz[x][y].jogador == 0):
    return False # jogada inválida
  matriz[x][y].jogador = jogador
  return True

def indices_da_celula_clicada(x, y, celulas):
  # Obtém a linha e coluna da célula clicada, caso o jogador tenha realmente clicado em uma célula
  # x, y: coordenadas do clique de mouse
  # celulas: uma matriz de sprites do tipo Celula
  for l in range(3):
    for c in range(3):
      if celulas[l][c].rect.collidepoint(x, y):
        return l, c
  return None

def checar_vencedor(matriz):
  # matriz: uma matriz de sprites do tipo Celula
  for i in range(0, 3):
    # verifica linha
    if matriz[i][0].jogador != 0 and matriz[i][0].jogador == matriz[i][1].jogador and matriz[i][1].jogador == matriz[i][2].jogador:
      return matriz[i][0].jogador
    # verifica coluna
    if matriz[0][i].jogador != 0 and matriz[0][i].jogador == matriz[1][i].jogador and matriz[1][i].jogador == matriz[2][i].jogador:
      return matriz[0][i].jogador
  # verifica diagonal
  if matriz[0][0].jogador != 0 and matriz[0][0].jogador == matriz[1][1].jogador and matriz[1][1].jogador == matriz[2][2].jogador:
    return matriz[0][0].jogador
  # verifica a outra diagonal
  if matriz[0][2].jogador != 0 and matriz[0][2].jogador == matriz[1][1].jogador and matriz[1][1].jogador == matriz[2][0].jogador:
    return matriz[0][2].jogador
  # verifica empate
  contador = 0
  for i in range(0, 3):
    for j in range(0, 3):
      if matriz[i][j].jogador != 0:
        contador += 1
  if contador == 9:
    return -1 # empate
  return 0 # partida não acabou

PADDING = 10 # espaçamento entre a barra e a borda da janela
global LARGURA_BARRA
LARGURA_BARRA = 10
global DIMENSAO_CELULA
DIMENSAO_CELULA = 100
COMPRIMENTO_BARRA = DIMENSAO_CELULA * 3 + LARGURA_BARRA * 2
LARGURA_JANELA = PADDING * 2 + COMPRIMENTO_BARRA
ALTURA_JANELA = LARGURA_JANELA + 100

pygame.init()
janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# sprites
barra_horizontal_1 = Barra(COMPRIMENTO_BARRA, LARGURA_BARRA, PADDING, PADDING + DIMENSAO_CELULA)
barra_horizontal_2 = Barra(COMPRIMENTO_BARRA, LARGURA_BARRA, PADDING, PADDING + DIMENSAO_CELULA * 2 + LARGURA_BARRA)
barra_vertical_1 = Barra(LARGURA_BARRA, COMPRIMENTO_BARRA, PADDING + DIMENSAO_CELULA, PADDING)
barra_vertical_2 = Barra(LARGURA_BARRA, COMPRIMENTO_BARRA, PADDING + DIMENSAO_CELULA * 2 + LARGURA_BARRA, PADDING)
sprites = pygame.sprite.Group([barra_horizontal_1, barra_horizontal_2, barra_vertical_1, barra_vertical_2])
celulas = [[None, None, None], [None, None, None], [None, None, None]]
y = PADDING
for l in range(3):
  x = PADDING
  for c in range(3):
    cel = Celula(DIMENSAO_CELULA, x, y)
    sprites.add(cel)
    celulas[l][c] = cel
    x += DIMENSAO_CELULA + LARGURA_BARRA
  y += DIMENSAO_CELULA + LARGURA_BARRA

jogador_da_vez = 1
vencedor = 0
while True:
  # Processamento de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.MOUSEBUTTONDOWN and vencedor == 0:
      x, y = event.pos
      indices = indices_da_celula_clicada(x, y, celulas)
      if indices:
        jogada_ok = marcar_posicao(indices[0], indices[1], jogador_da_vez, celulas)
        if jogada_ok and jogador_da_vez == 1:
          jogador_da_vez = 2
        elif jogada_ok and jogador_da_vez == 2:
          jogador_da_vez = 1
  
  vencedor = checar_vencedor(celulas)
  str = None
  if vencedor == -1:
    str = "EMPATE"
  elif vencedor == 1:
    str = "X é o vencedor"
  elif vencedor == 2:
    str = "0 é o vencedor"
  else:
    if jogador_da_vez == 1:
      str = "É a vez do X"
    else:
      str = "É a vez do 0"
  texto = font.render(str, True, 'black')

  sprites.update()
  # Desenha novo quadro
  janela.fill((255, 255, 255)) # limpa o quadro atual
  sprites.draw(janela)
  # Calcula posição do texto de forma que ele fique centralizado na janela
  x = (LARGURA_JANELA // 2) - texto.get_width() // 2
  y = ALTURA_JANELA - 70
  janela.blit(texto, (x, y))

  pygame.display.flip() # Desenha o quadro atual na tela do computador
  clock.tick(60)        # Controla a taxa de quadros por segundo (FPS)
