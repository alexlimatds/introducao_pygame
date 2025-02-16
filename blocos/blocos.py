import sys, random
import pygame as pg

class BlocoSprite(pg.sprite.Sprite):
  def __init__(self, x, y, dim):
    # x, y => coordenadas do canto superior esquerdo do bloco
    # dim => dimensão do bloco
    pg.sprite.Sprite.__init__(self)      # prepara o comportamento do Sprite
    self.image = pg.Surface([dim, dim])  # imagem que representa o bloco
    self.image.fill((0, 255, 255))       # pinta o bloco de azul
    self.rect = self.image.get_rect()    # usado para posicionar o sprite
    self.rect.topleft = (x, y)           # posiciona o sprite

  def acender(self):
    self.image.fill((255, 0, 0)) # pinta o bloco de vermelho

  def apagar(self):
    self.image.fill((0, 255, 255)) # pinta o bloco de azul

def gerar_texto(screen, contagem):
  font = pg.font.Font(None, 24)
  text = font.render(
    f'Acertos: {contagem}', 
    True,         # antialising
    (10, 10, 10)  # cor do texto
  )
  # calcula posição do texto:
  text_pos = text.get_rect(centerx=screen.get_width() / 2, y=screen.get_height() - 60)
  screen.blit(text, text_pos) # desenha o texto na tela

def main():
  # define dimensões, espaçamentos e quantidade de blocos
  dim_bloco = 70
  dim_separador = 15
  blocos_por_linha = 8
  espacamento = 20
  # calcula tamnaho da tela
  largura_tela = blocos_por_linha * dim_bloco + (blocos_por_linha - 1) * dim_separador + espacamento * 2
  altura_tela = largura_tela + espacamento + 80

  pg.init()                      # inicializa os módulos do PyGame
  screen = pg.display.set_mode(  # cria a janela do jogo
    (largura_tela, altura_tela) 
  )
  pg.display.set_caption("Blocos")  # título da janela

  # inicializa sprites
  lista_sprites = []
  for i in range(blocos_por_linha):
    for j in range(blocos_por_linha):
      lista_sprites.append(
        BlocoSprite(
          i * (dim_bloco + dim_separador) + espacamento, # coordenada x
          j * (dim_bloco + dim_separador) + espacamento, # coordenada y
          dim_bloco                                      # dimensão do bloco
        )
      )
  groupo_sprites = pg.sprite.Group(lista_sprites)

  clock = pg.time.Clock()  # usado para controlar a taxa de FPS
  
  contagem = 0  # contagem de cliques bem-sucedidos do jogador
  inicio = pg.time.get_ticks() # usado para medir o tempo
  alvo = None   # bloco aceso

  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
      elif event.type == pg.MOUSEBUTTONUP: # trata liberação do botão do mouse
        posicao_clique = event.pos  # coordenadas do ponteiro do mouse
        # verifica se jogador clicou no bloco aceso
        if alvo is not None and alvo.rect.collidepoint(posicao_clique):
          alvo.apagar()
          alvo = None
          contagem += 1
    
    screen.fill((255, 255,255)) # preenche tela com cor branca (limpa o quadro atual)

    # Mede o tempo decorrido desde o último acendimento de bloco 
    # ou do último apagamento de bloco
    tempo = pg.time.get_ticks()
    cronometragem = tempo - inicio
    if alvo is not None and cronometragem >= 800: # o alvo fica disponível por 800 ms
      inicio = tempo
      alvo.apagar()
      alvo = None
    elif alvo is None and cronometragem >= 1500: # acende um bloco a cada 1500 ms
      inicio = tempo
      # sorteia o bloco a ser aceso
      i = random.randint(0, len(groupo_sprites) - 1) # gera número aleatório entre zero e número de blocos - 1
      alvo = groupo_sprites.sprites()[i]
      alvo.acender()

    groupo_sprites.draw(screen)    # desenha sprites no quadro
    gerar_texto(screen, contagem)  # escreve texto no quadro
    
    pg.display.flip()
    clock.tick(60) # 60 FPS (quadros por segundo)

if __name__ == "__main__":
  main()