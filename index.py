import pgzrun

# Tamanho da tela
WIDTH = 800
HEIGHT = 457
TITLE = "Bruno"

# Estados do jogo
estado = "menu"  # Começa no menu

# Definindo o botão "Play"
botao_play = Rect(300, 250, 200, 50)  # Posição e tamanho do botão

# Carregar a imagem de fundo
fundo = Actor("background")  # A imagem "background.png" deve estar na pasta "images"


def ajustar_fundo():
    """Ajusta as dimensões da imagem de fundo para caber na tela."""
    proporcao_fundo = fundo.width / fundo.height
    nova_largura = WIDTH
    nova_altura = int(nova_largura / proporcao_fundo)

    if nova_altura > HEIGHT:
        nova_altura = HEIGHT
        nova_largura = int(nova_altura * proporcao_fundo)

    fundo.width = nova_largura
    fundo.height = nova_altura


def draw():
    """Desenha a tela com base no estado atual."""
    screen.clear()  # Limpa a tela

    if estado == "menu":
        ajustar_fundo()  # Ajusta o fundo para o menu
        fundo.draw()  # Desenha o fundo no menu

        # Desenha o botão "Play"
        screen.draw.filled_rect(botao_play, "white")
        screen.draw.text("Play", center=botao_play.center, color="black", fontsize=40)
    
    elif estado == "jogo":
        fundo.draw()  # Desenha a imagem de fundo na tela do jogo


def on_mouse_down(pos):
    """Detecta o clique no botão 'Play' para iniciar o jogo."""
    global estado
    if estado == "menu" and botao_play.collidepoint(pos):
        estado = "jogo"  # Muda para a tela do jogo


pgzrun.go()  # Inicia o jogo
