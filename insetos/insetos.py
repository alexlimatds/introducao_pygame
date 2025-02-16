import sys, random
import pygame as pg

def load_image(name):
  # name => nome do arquivo da imagem
  image = pg.image.load('insetos/' + name) # lê arquivo de imagem
  image = image.convert()     # ajusta a imagem para a tela em uso
  return image

class InsetoSprite(pg.sprite.Sprite):
  def __init__(self, x, y, dim_img):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface([dim_img, dim_img])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)

def gerar_texto(screen, texto, y):
  font = pg.font.Font(None, 24)
  text = font.render(
    texto, 
    True,         # antialising
    (10, 10, 10)  # cor do texto
  )
  # calcula posição do texto:
  text_pos = text.get_rect(centerx=screen.get_width() / 2, y=y)
  screen.blit(text, text_pos) # desenha o texto na tela

def main():
  dim_img = 100
  separador = 20
  espacamento = 40
  # calcula tamanho da tela
  largura_tela = espacamento + dim_img + separador + dim_img + separador + dim_img + espacamento
  altura_tela = largura_tela + 80

  pg.init()                      # inicializa os módulos do PyGame
  janela = pg.display.set_mode(  # cria a janela do jogo
    (largura_tela, altura_tela)  # largura e altura da janela
  )
  pg.display.set_caption("Insetos")  # título da janela

  # inicializa sprites
  sprite_cima = InsetoSprite(
    espacamento + dim_img + separador, # x
    espacamento, # y
    dim_img
  )
  sprite_esquerdo = InsetoSprite(
    espacamento, # x
    espacamento + dim_img + separador, # y
    dim_img
  )
  sprite_direito = InsetoSprite(
    espacamento + dim_img + separador + dim_img + separador, # x
    espacamento + dim_img + separador, # y
    dim_img
  ) 
  sprite_baixo = InsetoSprite(
    espacamento + dim_img + separador, # x
    espacamento + dim_img + separador + dim_img + separador, # y
    dim_img
  )
  grupo_sprites = pg.sprite.Group([sprite_cima, sprite_esquerdo, sprite_direito, sprite_baixo])

  # carrega imagens
  imagens = [
    load_image('barata.jpg'), 
    load_image('besouro.jpg'), 
    load_image('borboleta.jpg'), 
    load_image('formiga.jpg'), 
    load_image('lagarta.jpg'), 
    load_image('mosca.jpg')
  ]
  img_barata = imagens[0] # imagem alvo

  clock = pg.time.Clock()
  
  tentativas = 3
  acertos = 0

  em_jogo = True
  inicio = pg.time.get_ticks() # usado para medir o tempo
  while True:
    # GERENCIAMENTO DE EVENTOS
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
      elif event.type == pg.KEYDOWN and em_jogo:
        if (
          (event.key == pg.K_UP and sprite_cima.image == img_barata) or 
          (event.key == pg.K_LEFT and sprite_esquerdo.image == img_barata) or 
          (event.key == pg.K_RIGHT and sprite_direito.image == img_barata) or 
          (event.key == pg.K_DOWN and sprite_baixo.image == img_barata)
        ):
          acertos += 1
        else:
          tentativas -= 1
        if tentativas == 0:
          em_jogo = False
    
    # LIMPA O QUADRO
    janela.fill((255, 255,255))

    # LÓGICA E RENDERIZAÇÃO DO JOGO
    if em_jogo:
      tempo = pg.time.get_ticks()
      cronometragem = tempo - inicio
      # troca imagens a cada 600 ms
      if cronometragem >= 600:
        inicio = tempo
        sorteio = random.sample(imagens, 4) # sorteia 4 itens da lista de imagens
        for sprite, img in zip(grupo_sprites.sprites(), sorteio): # itera sprites e imagens sorteadas
          sprite.image = img
      
    grupo_sprites.draw(janela) # desenha sprites no quadro
    y_texto = espacamento + dim_img + separador + dim_img + separador + dim_img + separador
    gerar_texto(janela, 'Use as teclas direcionais para selecionar a imagem', y_texto)
    gerar_texto(janela, 'Tente acertar a barata', y_texto + separador)
    gerar_texto(janela, f'Tentativas restantes: {tentativas}', y_texto + separador * 2)
    gerar_texto(janela, f'Acertos: {acertos}', y_texto + separador * 3)

    # ATUALIZAÇÃO DA TELA
    pg.display.flip()
    clock.tick(60) # 60 FPS (quadros por segundo)
    

if __name__ == "__main__":
  main()