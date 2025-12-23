# Exemplo de jogo de plataforma
# Fonte: From: http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py

import pygame

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
 
# Dimensões da janela
JANELA_LARGURA = 800
JANELA_ALTURA = 600

class Personagem(pygame.sprite.Sprite):
    # Representa o personagem do jogo, o qual é controlado pelo usuário.
    # Visualmente, é um retângulo vermelho
    
    def __init__(self):
        super().__init__()
 
        # Imagem do personagem
        self.image = pygame.Surface([40, 60])
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
 
        # Velocidades do personagem
        self.velocidade_x = 0
        self.velocidade_y = 0
 
        # Lista de sprites que representam as plataformas
        self.plataformas = None
 
    def update(self):
        # Gravidade
        self.acionar_gravidade()
 
        # Mover para direita ou esquerda
        self.rect.x += self.velocidade_x
 
        # Verifica se alguma plataforma foi atingida durante a movimentação horizontal
        plataformas_atingidas = pygame.sprite.spritecollide(self, self.plataformas, False)
        for p in plataformas_atingidas:
            # Se está movendo para a direita, alinha a extremidade direita 
            # do personagem com a extremidade esquerda da plataforma
            if self.velocidade_x > 0:
                self.rect.right = p.rect.left
            elif self.velocidade_x < 0:
                # Se está movendo para a esquerda, alinha a extremidade esquerda 
                # do personagem com a extremidade direita da plataforma
                self.rect.left = p.rect.right
 
        # Move para cima ou para baixo
        self.rect.y += self.velocidade_y
 
        # Verifica se alguma plataforma foi atingida durante a movimentação vertical
        plataformas_atingidas = pygame.sprite.spritecollide(self, self.plataformas, False)
        for p in plataformas_atingidas:
            # Reset our position based on the top/bottom of the object.
            # Se está subindo, alinha a extremidade superior do personagem 
            # com a a extremidade inferior da plataforma
            if self.velocidade_y > 0:
                self.rect.bottom = p.rect.top
            # Se está descendo, alinha a extremidade inferior do personagem 
            # com a a extremidade superior da plataforma
            elif self.velocidade_y < 0:
                self.rect.top = p.rect.bottom
 
            # Encerra o movimento vertical
            self.velocidade_y = 0
 
    def acionar_gravidade(self):
        # Processa o efeito da gravidade
        if self.velocidade_y == 0:
            # não está subindo, então ajustar velocidade para puxar o personagem para baixo
            self.velocidade_y = 1
        else:
            # está subindo, então diminuir a velocidade de subida
            self.velocidade_y += 0.35
 
        # Verifica se o personagem está no chão
        if self.rect.y >= JANELA_ALTURA - self.rect.height and self.velocidade_y >= 0:
            self.velocidade_y = 0
            self.rect.y = JANELA_ALTURA - self.rect.height
 
    def pular(self):
        # Função executada quando o botão de pular é acionado.
        # Permite o pulo apenas caso o personagem esteja sobre o chão ou 
        # sobre uma plataforma.
        
        # Verificando se o personagem está sobre uma plataforma. Para isso, 
        # move o personagem para baixo em 2 pixels e verifica se houve colisão.
        # Não funciona corretamente caso a movimentação seja de apenas 1 pixel.
        self.rect.y += 2
        plataformas_atingidas = pygame.sprite.spritecollide(self, self.plataformas, False)
        # Feita a verificação de colisão, retorna o personagem para a altura inicial.
        self.rect.y -= 2
 
        # Verifica se é permitido que o personagem pule
        if (
            len(plataformas_atingidas) > 0 or  # está sobre uma plataforma ?
            self.rect.bottom >= JANELA_ALTURA  # está sobre o chão ?
        ):
            self.velocidade_y = -10
 
    def para_esquerda(self):
        # Função executada quando o usuário pressiona a tecla direcional da esquerda
        self.velocidade_x = -6
 
    def para_direita(self):
        # Função executada quando o usuário pressiona a tecla direcional da direita
        self.velocidade_x = 6
 
    def parar(self):
        # Função executada quando o usuário libera uma tecla
        self.velocidade_x = 0
 
 
class Plataforma(pygame.sprite.Sprite):
    # Representa uma plataforma. Visualmente é um retângulo verde.
 
    def __init__(self, largura, altura, x, y):
        super().__init__()
        self.image = pygame.Surface([largura, altura])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
def main():
    # Jogo 
    pygame.init()
    janela = pygame.display.set_mode([JANELA_LARGURA, JANELA_ALTURA])
    pygame.display.set_caption("Jogo de Plataforma")
    clock = pygame.time.Clock()

    # Cria as plataformas
    plataformas = pygame.sprite.Group()
    plataformas.add(Plataforma(210, 70, 500, 500))
    plataformas.add(Plataforma(210, 70, 200, 400))
    plataformas.add(Plataforma(210, 70, 600, 300))

    # Cria o personagem
    personagem = Personagem()
    personagem.rect.x = 340
    personagem.rect.y = JANELA_ALTURA - personagem.rect.height
    personagem.plataformas = plataformas
 
    sprites_ativos = pygame.sprite.Group()
    sprites_ativos.add(personagem)
 
    # Game loop
    continuar = True
    while continuar:
        # Eventos/entrada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # ativa o andar para a esquerda
                    personagem.para_esquerda()
                if event.key == pygame.K_RIGHT:
                    # ativa o andar para a direita
                    personagem.para_direita()
                if event.key == pygame.K_UP:
                    # ativa o pulo
                    personagem.pular()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and personagem.velocidade_x < 0:
                    # interrompe o andar para a esquerda
                    personagem.parar()
                if event.key == pygame.K_RIGHT and personagem.velocidade_x > 0:
                    # interrompe o andar para a direita
                    personagem.parar()
 
        # Atualiza o personagem
        sprites_ativos.update()
 
        # Recua o personagem caso ele ultrapasse os limites da janela
        if personagem.rect.right > JANELA_LARGURA:
            personagem.rect.right = JANELA_LARGURA
        if personagem.rect.left < 0:
            personagem.rect.left = 0
 
        # Atualização do quadro
        janela.fill(AZUL) 
        plataformas.draw(janela)    # desenha as plataformas
        sprites_ativos.draw(janela) # desenha o personagem
        
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
 
if __name__ == "__main__":
    main()