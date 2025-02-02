# Exemplo de criação e exibição de texto
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Criando o objeto Font. O primeiro argumento é uma string que indica a fonte a ser utilizada.
# O valor None faz com que o pygame use sua fonte padrão. O segundo argumento indica o tamanho da fonte.
font = pygame.font.Font(None, 24)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  # Define o texto e cria sua superfície. O segundo argumento indica o uso ou não de anti-aliasing.
  # O terceiro argumento indica a cor do texto.
  surface_texto = font.render(f"Olá Mundo!", True, 'black')
  # Calcula posição do texto de forma que ele fique centralizado na janela
  x = (640 // 2) - surface_texto.get_width() // 2
  y = (480 // 2) - surface_texto.get_height() // 2

  screen.fill((255, 255, 255)) # apaga o quadro atual
  
  # Desenha o texto na posição x, y
  screen.blit(surface_texto, (x, y))
  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)
