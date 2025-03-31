import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 457

# Carrega os efeitos sonoros e música
gem_sound = sounds.gem  # Som ao coletar ossos
bit_sound = sounds.bit  # Som do menu
mystery_music = sounds.mystery  # Música do jogo

# Variável para controlar se os sons estão ativados
sounds_enabled = True

background = Actor("background")
background.pos = (WIDTH // 2, HEIGHT // 2)

ground_y_position = HEIGHT - 30

grounds = [
    Actor("floor1", (33, ground_y_position)),
    Actor("floor2", (400, 470)),
    Actor("floor3", (730, 375)),
]

base = Actor("base", (280, 150))

# Posições dos ossos (4 no total)
bone_positions = [
    (220, 70), (420, 330), (220, 320), (750, 150)
]
bones = [Actor("bone", pos) for pos in bone_positions]

boxes = [
    Actor('box', (489, 400)),
    Actor('box', (489, 332)),
    Actor('box', (420, 400)),
]

player = Actor("p1", anchor=('center', 'bottom'), pos=(80, ground_y_position - 1))

# Animação do personagem
player.idle_images = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15']
player.idleL_images = [f'{img}l' for img in player.idle_images]
player.walking_images = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10', 'w11', 'w12', 'w13', 'w14', 'w15']
player.walkingL_images = [f'{img}l' for img in player.walking_images]

# Inimigos caveira
caveira_data = [
    {"pos": (315, 110), "min_x": 180, "max_x": 385, "direction": 1},
    {"pos": (560, 200), "min_x": 560, "max_x": 770, "direction": 1},
    {"pos": (467, 420), "min_x": 300, "max_x": 500, "direction": 1},
]

caveiras = []
for data in caveira_data:
    caveira = Actor("1l", pos=data["pos"])
    caveira.caveira_images = ['1l', '2l', '3l', '2l']
    caveira.caveira_imagesL = ['1', '2', '3', '2']
    caveira.image = caveira.caveira_images[0]
    caveira.direction = data["direction"]
    caveira.min_x = data["min_x"]
    caveira.max_x = data["max_x"]
    caveira.facing_right = True
    caveira.last_hit_time = 0
    caveiras.append(caveira)

player.image = player.idle_images[0]
player.facing_right = True

# Configurações de física
move_speed = 5
jump_strength = -10
gravity = 0.5
player.y_velocity = 0
player.on_ground = False

# Estados do jogo
game_state = "menu"
lives = 3
invincible = False
invincible_time = 0
respawn_time = 0
win = False

# Botões do menu
button_width = 200
button_height = 50
button_x = (WIDTH - button_width) // 2
start_y = (HEIGHT - button_height * 3 - 40) // 2  # Ajustado para 3 botões

play_button = Rect(button_x, start_y, button_width, button_height)
sound_button = Rect(button_x, start_y + button_height + 20, button_width, button_height)
exit_button = Rect(button_x, start_y + button_height * 2 + 40, button_width, button_height)

# Contadores
frame_count = 0
score = 0

def toggle_sounds():
    global sounds_enabled
    sounds_enabled = not sounds_enabled
    if sounds_enabled:
        if game_state == "menu":
            bit_sound.play(-1)
        elif game_state == "game":
            mystery_music.play(-1)
    else:
        bit_sound.stop()
        mystery_music.stop()
        gem_sound.stop()

def draw():
    screen.blit("background", (0, 0))
    if game_state == "menu":
        screen.draw.filled_rect(play_button, (27, 48, 52))
        screen.draw.text("Play", center=play_button.center, color=(224, 240, 255), fontsize=40)
        
        screen.draw.filled_rect(sound_button, (27, 48, 52))
        sound_text = "Sound: ON" if sounds_enabled else "Sound: OFF"
        screen.draw.text(sound_text, center=sound_button.center, color=(224, 240, 255), fontsize=40)
        
        screen.draw.filled_rect(exit_button, (27, 48, 52))
        screen.draw.text("Exit", center=exit_button.center, color=(224, 240, 255), fontsize=40)
    elif game_state == "game":
        for ground in grounds:
            ground.draw()
        for box in boxes:
            box.draw()
        base.draw()
        for bone in bones:
            bone.draw()
        
        if not invincible or (invincible and frame_count % 10 < 5):
            player.draw()
            
        for caveira in caveiras:
            caveira.draw()
        
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")
        
        vida_spacing = 50
        start_x = WIDTH - 60
        for i in range(lives):
            screen.blit("vida", (start_x - (i * vida_spacing), 10))
        
        if lives <= 0:
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//6), fontsize=60, color="red")
            screen.draw.filled_rect(play_button, (27, 48, 52))
            screen.draw.text("Menu", center=play_button.center, color=(224, 240, 255), fontsize=40)
        elif win:
            screen.draw.text("YOU WIN", center=(WIDTH//2, HEIGHT//3), fontsize=60, color=(246,213,133))
            screen.draw.filled_rect(play_button, (27, 48, 52))
            screen.draw.text("Menu", center=play_button.center, color=(224, 240, 255), fontsize=40)

def reset_game():
    global lives, score, bones, invincible, invincible_time, respawn_time, win
    player.pos = (80, ground_y_position - 1)
    player.y_velocity = 0
    player.on_ground = True
    lives = 3
    score = 0
    bones = [Actor("bone", pos) for pos in bone_positions]
    invincible = False
    invincible_time = 0
    respawn_time = 0
    win = False
    for caveira in caveiras:
        caveira.last_hit_time = 0

def play_menu_sound():
    if sounds_enabled:
        mystery_music.stop()
        bit_sound.play(-1)

def play_game_music():
    if sounds_enabled:
        bit_sound.stop()
        mystery_music.play(-1)

def update():
    global frame_count, score, bones, lives, invincible, invincible_time, game_state, respawn_time, win
    
    if game_state == "game":
        if win or lives <= 0:
            return
            
        frame_count += 1
        
        if respawn_time > 0:
            respawn_time -= 1
            if respawn_time <= 0:
                player.pos = (80, ground_y_position - 1)
                player.y_velocity = 0
                player.on_ground = True
                invincible = True
                invincible_time = 0
            return
            
        if invincible:
            invincible_time += 1
            if invincible_time > 60:
                invincible = False
                invincible_time = 0
        
        moving = False
        dx = 0
        
        if (keyboard.left or keyboard.a) and player.left > 0:
            dx -= move_speed
            player.facing_right = False
            moving = True
        elif (keyboard.right or keyboard.d) and player.right < WIDTH:
            dx += move_speed
            player.facing_right = True
            moving = True
            
        player.x += dx
        
        # Colisão horizontal
        for obj in grounds + boxes + [base]:
            if player.colliderect(obj):
                if dx > 0:
                    player.right = obj.left
                elif dx < 0:
                    player.left = obj.right
                break
        
        # Gravidade
        player.y_velocity += gravity
        player.y += player.y_velocity
        
        # Limites da tela
        if player.top > HEIGHT:
            lives -= 1
            respawn_time = 30
            return
            
        player.on_ground = False
        
        # Colisão vertical
        for obj in grounds + boxes + [base]:
            if player.colliderect(obj):
                if player.y_velocity > 0:
                    player.bottom = obj.top
                    player.on_ground = True
                    player.y_velocity = 0
                elif player.y_velocity < 0:
                    player.top = obj.bottom
                    player.y_velocity = 0
                break
        
        # Pulo
        if (keyboard.space or keyboard.up) and player.on_ground:
            player.y_velocity = jump_strength
            player.on_ground = False
            
        # Animação do personagem
        if moving:
            animation = player.walking_images if player.facing_right else player.walkingL_images
            frame_rate = 6
        else:
            animation = player.idle_images if player.facing_right else player.idleL_images
            frame_rate = 8
        player.image = animation[(frame_count // frame_rate) % len(animation)]
        
        # Movimento e animação das caveiras
        for caveira in caveiras:
            if caveira.facing_right:
                caveira.image = caveira.caveira_images[(frame_count // 10) % len(caveira.caveira_images)]
            else:
                caveira.image = caveira.caveira_imagesL[(frame_count // 10) % len(caveira.caveira_imagesL)]
            
            caveira.x += caveira.direction * 2
            
            if caveira.x >= caveira.max_x:
                caveira.direction *= -1
                caveira.facing_right = False
            elif caveira.x <= caveira.min_x:
                caveira.direction *= -1
                caveira.facing_right = True

        # Coleta de ossos com som
        bones_to_remove = []
        for bone in bones:
            if player.colliderect(bone):
                score += 1
                bones_to_remove.append(bone)
                if sounds_enabled:
                    gem_sound.play()
        
        for bone in bones_to_remove:
            if bone in bones:
                bones.remove(bone)
        
        # Verifica vitória
        if len(bones) == 0:
            win = True
                
        # Dano das caveiras
        if not invincible:
            for caveira in caveiras:
                if frame_count - caveira.last_hit_time > 30:
                    caveira_hitbox = Rect(
                        caveira.x - 12,
                        caveira.y - 8,
                        24,
                        20
                    )
                    
                    player_hitbox = Rect(
                        player.x - 10,
                        player.y - 20,
                        20,
                        40
                    )
                    
                    if player_hitbox.colliderect(caveira_hitbox):
                        lives -= 1
                        invincible = True
                        caveira.last_hit_time = frame_count
                        if player.x < caveira.x:
                            player.x -= 30
                        else:
                            player.x += 30
                        break

def on_mouse_down(pos):
    global game_state
    if game_state == "menu":
        if play_button.collidepoint(pos):
            game_state = "game"
            reset_game()
            play_game_music()
        elif sound_button.collidepoint(pos):
            toggle_sounds()
        elif exit_button.collidepoint(pos):
            exit()
    elif game_state == "game" and (lives <= 0 or win):
        if play_button.collidepoint(pos):
            game_state = "menu"
            play_menu_sound()

# Inicia o som do menu em loop quando o jogo começa
play_menu_sound()

pgzrun.go()