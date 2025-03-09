import sys, random
import pygame

def load_image(name):
  # name => nome do arquivo da imagem
  image = pygame.image.load('insetos/' + name) # lê arquivo de imagem
  image = image.convert()     # ajusta a imagem para a tela em uso
  return image

class InsetoSprite(pygame.sprite.Sprite):
  def __init__(self, x, y, dim_img):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([dim_img, dim_img])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)

def gerar_texto(janela, texto, y):
  text = fonte_padrao.render(
    texto, 
    True,         # antialising
    (10, 10, 10)  # cor do texto
  )
  # calcula posição do texto:
  text_pos = text.get_rect(centerx=janela.get_width() // 2, y=y)
  janela.blit(text, text_pos) # desenha o texto na tela

def gerar_titulo(janela, texto, y):
  text = fonte_grande.render(
    texto, 
    True,         # antialising
    (10, 10, 10)  # cor do texto
  )
  # calcula posição do texto:
  text_pos = text.get_rect(centerx=janela.get_width() // 2, y=y)
  janela.blit(text, text_pos) # desenha o texto na tela

def main():
  global dim_img
  dim_img = 100
  # calcula tamanho da tela
  espacamento = dim_img // 2
  largura_tela = espacamento + dim_img + espacamento + dim_img + espacamento + dim_img + espacamento
  altura_tela = largura_tela + 80

  pygame.init()                      # inicializa os módulos do PyGame
  janela = pygame.display.set_mode(  # cria a janela do jogo
    (largura_tela, altura_tela)  # largura e altura da janela
  )
  pygame.display.set_caption("Insetos")  # título da janela

  clock = pygame.time.Clock()

  global fonte_padrao
  fonte_padrao = pygame.font.Font(None, 24)
  global fonte_grande
  fonte_grande = pygame.font.Font(None, 60)

  # carrega imagens
  global imagens
  imagens = [
    load_image('barata.jpg'), 
    load_image('besouro.jpg'), 
    load_image('borboleta.jpg'), 
    load_image('formiga.jpg'), 
    load_image('lagarta.jpg'), 
    load_image('mosca.jpg')
  ]
  global img_barata
  img_barata = imagens[0] # imagem alvo

  abertura(clock)
  jogo(clock)

def abertura(clock):
  janela = pygame.display.get_surface() # obtém a janela do jogo
  separador_vertical = 20
  separador_horizontal = (janela.get_width() - dim_img * 3) // 4

  jogar = False
  while not jogar:
    # GERENCIAMENTO DE EVENTOS
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
        jogar = True

    # LIMPA O QUADRO
    janela.fill((255, 255,255))
    # ATUALIZAÇÃO DA TELA
    gerar_titulo(janela, "I N S E T O S", 20)
    janela.blit(imagens[0], (separador_horizontal, dim_img))
    janela.blit(imagens[1], (separador_horizontal + dim_img + separador_horizontal, dim_img))
    janela.blit(imagens[2], (separador_horizontal + dim_img + separador_horizontal + dim_img + separador_horizontal, dim_img))
    janela.blit(imagens[3], (separador_horizontal, dim_img + dim_img + separador_vertical))
    janela.blit(imagens[4], (separador_horizontal + dim_img + separador_horizontal, dim_img + dim_img + separador_vertical))
    janela.blit(imagens[5], (separador_horizontal + dim_img + separador_horizontal + dim_img + separador_horizontal, dim_img + dim_img + separador_vertical))
    gerar_texto(janela, "Pressione ENTER para jogar", dim_img + dim_img + separador_vertical + dim_img + separador_vertical)
    pygame.display.flip()
    clock.tick(60) # 60 FPS (quadros por segundo)

def jogo(clock):
  separador = 20
  janela = pygame.display.get_surface() # obtém a janela do jogo
  espacamento_horizontal = (janela.get_width() - dim_img * 3 - separador * 2) // 2
  espacamento_vertical = 50

  # inicializa sprites
  sprite_cima = InsetoSprite(
    espacamento_horizontal + dim_img + separador, # x
    espacamento_vertical, # y
    dim_img
  )
  sprite_esquerdo = InsetoSprite(
    espacamento_horizontal, # x
    espacamento_vertical + dim_img + separador, # y
    dim_img
  )
  sprite_direito = InsetoSprite(
    espacamento_horizontal + dim_img + separador + dim_img + separador, # x
    espacamento_vertical + dim_img + separador, # y
    dim_img
  ) 
  sprite_baixo = InsetoSprite(
    espacamento_horizontal + dim_img + separador, # x
    espacamento_vertical + dim_img + separador + dim_img + separador, # y
    dim_img
  )
  grupo_sprites = pygame.sprite.Group([sprite_cima, sprite_esquerdo, sprite_direito, sprite_baixo])
  
  tentativas = 3
  acertos = 0

  em_jogo = True
  inicio = pygame.time.get_ticks() # usado para medir o tempo
  while True:
    # GERENCIAMENTO DE EVENTOS
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN and em_jogo:
        if (
          (event.key == pygame.K_UP and sprite_cima.image == img_barata) or 
          (event.key == pygame.K_LEFT and sprite_esquerdo.image == img_barata) or 
          (event.key == pygame.K_RIGHT and sprite_direito.image == img_barata) or 
          (event.key == pygame.K_DOWN and sprite_baixo.image == img_barata)
        ):
          acertos += 1
        else:
          tentativas -= 1
        if tentativas == 0:
          em_jogo = False
      elif not em_jogo:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s: # jogar de novo
          em_jogo = True
          tentativas = 3
          acertos = 0
    
    # LIMPA O QUADRO
    janela.fill((255, 255,255))

    # LÓGICA E RENDERIZAÇÃO DO JOGO
    if em_jogo:
      tempo = pygame.time.get_ticks()
      cronometragem = tempo - inicio
      # troca imagens a cada 600 ms
      if cronometragem >= 600:
        inicio = tempo
        sorteio = random.sample(imagens, 4) # sorteia 4 itens da lista de imagens
        for sprite, img in zip(grupo_sprites.sprites(), sorteio): # itera sprites e imagens sorteadas
          sprite.image = img
      
    grupo_sprites.draw(janela) # desenha sprites no quadro
    y_texto = espacamento_horizontal + dim_img + separador + dim_img + separador + dim_img + separador
    if em_jogo:
      gerar_texto(janela, 'Use as teclas direcionais para selecionar a imagem', y_texto)
      gerar_texto(janela, 'Tente acertar a barata', y_texto + separador)
    else:
      gerar_texto(janela, 'Fim de Jogo!', y_texto)
      gerar_texto(janela, 'Jogar de novo (S/N)?', y_texto + separador)
    gerar_texto(janela, f'Tentativas restantes: {tentativas}', y_texto + separador * 2)
    gerar_texto(janela, f'Acertos: {acertos}', y_texto + separador * 3)

    # ATUALIZAÇÃO DA TELA
    pygame.display.flip()
    clock.tick(60) # 60 FPS (quadros por segundo)
    
if __name__ == "__main__":
  main()