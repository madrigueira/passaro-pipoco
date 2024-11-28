import pygame
import random
import sys

pygame.init()

## Configurações da janela
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pássaro Pipoco")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
clock = pygame.time.Clock()

## Cores
white = (255, 255, 255)
black = (0, 0, 0)

## Menu principal
def tela_menu():
    ## Carrega sprites para o bg animado
    menu_bg_sprites = [
        pygame.image.load(f"assets/bg-menu/{i}.png").convert_alpha()
        for i in range(1, 9)
    ]
    menu_bg_frame_index = 0
    menu_bg_speed = 0.07

    while True:
        menu_bg_frame_index += menu_bg_speed
        if menu_bg_frame_index >= 8:
            menu_bg_frame_index = 0

        screen.blit(pygame.transform.scale(menu_bg_sprites[int(menu_bg_frame_index)], (width * 2.5, height)), (0, 0))

        ## Logo
        logo = pygame.image.load("assets/logo.png")
        screen.blit(pygame.transform.scale(logo, (300, 150)), (width // 2 - logo.get_width() // 2, 50))

        ## Carrega as imagens dos botões
        start_button_image = pygame.transform.scale(pygame.image.load("assets/btn-menu/play-1.png").convert_alpha(),(175, 90))
        quit_button_image = pygame.transform.scale(pygame.image.load("assets/btn-menu/quit-1.png").convert_alpha(),(175, 90))
        hover_start_button_image = pygame.transform.scale(pygame.image.load("assets/btn-menu/play-2.png").convert_alpha(), (175, 90))
        hover_quit_button_image = pygame.transform.scale(pygame.image.load("assets/btn-menu/quit-2.png").convert_alpha(), (175, 90))

        ## Obtem retângulos dos botões para detectar hover
        start_button_rect = start_button_image.get_rect(center=(width // 2, 350))
        quit_button_rect = quit_button_image.get_rect(center=(width // 2, 475))

        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            screen.blit(hover_start_button_image, start_button_rect.topleft)
        else:
            screen.blit(start_button_image, start_button_rect.topleft)

        if quit_button_rect.collidepoint(mouse_pos):
            screen.blit(hover_quit_button_image, quit_button_rect.topleft)
        else:
            screen.blit(quit_button_image, quit_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    reload()
                    return
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

## Predefinições
def reload():
    global pipoco_x, pipoco_y, pipoco_height, pipoco_width, pipoco_current_frame, pipoco_frame_speed, pipoco_frame_counter, pipoco_speed, gravity, logs, log_width, log_gap, frame_count, score, game_over, freeze, bg_x, bg_speed
    pipoco_x, pipoco_y = 50, height // 2
    pipoco_height = 80
    pipoco_width = 67
    pipoco_current_frame = 0
    pipoco_frame_speed = 5
    pipoco_frame_counter = 0
    pipoco_speed = 0
    gravity = 0.5
    logs = []
    log_width = 80
    log_gap = 210
    frame_count = 0
    score = 0
    game_over = False
    freeze = False
    bg_x = 0
    bg_speed = 1

## Desenha o pipoco
def draw_pipoco():
    global pipoco_current_frame, pipoco_frame_counter

    ## Carrega as imagens dos quadros do pipoco
    pipoco_frames = [
        pygame.image.load('assets/sprites-pipoco/1.png'),
        pygame.image.load('assets/sprites-pipoco/2.png'),
        pygame.image.load('assets/sprites-pipoco/3.png'),
        pygame.image.load('assets/sprites-pipoco/4.png'),
        pygame.image.load('assets/sprites-pipoco/5.png')
    ]

    ## Alterna os sprites do pipoco
    if pipoco_frame_counter % pipoco_frame_speed == 0:
        pipoco_current_frame = (pipoco_current_frame + 1) % len(pipoco_frames)

    ## Rotação do pipoco no pulo
    max_angle = 15  ## Inclinação máxima para cima
    min_angle = -90  ## Inclinação máxima para baixo
    angle = max(min(-pipoco_speed * 3, max_angle), min_angle)  ## Ajusta o ângulo dentro do intervalo permitido
    rotated_pipoco = pygame.transform.rotate(pipoco_frames[pipoco_current_frame], angle)
    pipoco_rect = rotated_pipoco.get_rect(center=(pipoco_x + pipoco_width // 2, pipoco_y + pipoco_height // 2))
    screen.blit(rotated_pipoco, pipoco_rect.topleft)

    pipoco_frame_counter += 1

## Desenha os logs
def draw_log():
    global log_image, log_top

    log_image = pygame.transform.scale(pygame.image.load('assets/log.png'), (log_width, height))

    for log in logs:
        ## Log de cima
        log_top = pygame.transform.flip(log_image, False, True)
        screen.blit(log_top, (log[0], log[1] - height))

        ## Log de baixo
        screen.blit(log_image, (log[0], height - log[2]))

## Desenha o background
def draw_background():
    global bg_image, bg_x

    bg_image = pygame.transform.scale(pygame.image.load('assets/background.png'), (width * 1.3, height))
    bg_width = bg_image.get_width()

    ## Desenha o background duas vezes para criar o efeito de scrolling infinito
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + bg_width, 0))

    ## Reposiciona o fundo se ele saiu da tela
    bg_x -= bg_speed
    if bg_x <= -bg_width:
        bg_x = 0

## Faz o pipoco cair
def pipoco_fall_and_shake():
    global pipoco_y, pipoco_speed, bg_x, logs

    ## Parametros
    fall_gravity = 2
    max_velocity = 20
    shake_intensity = 3
    shake_duration = 2
    shake_counter = 5

    ## Loop que faz o pipoco cair
    while pipoco_y < height:
        pipoco_speed = min(pipoco_speed + fall_gravity, max_velocity)
        pipoco_y += pipoco_speed

        if shake_counter < shake_duration:
            shake_offset_x = random.randint(-shake_intensity, shake_intensity)
            shake_offset_y = random.randint(-shake_intensity, shake_intensity)
        else:
            shake_offset_x = 0
            shake_offset_y = 0

        draw_background()
        screen.blit(bg_image, (bg_x + shake_offset_x, shake_offset_y))
        draw_pipoco()

        ## Redesenha os logs com tremor
        for log in logs:
            screen.blit(log_top,(log[0] + random.randint(-shake_intensity, shake_intensity), log[1] - height + random.randint(-shake_intensity, shake_intensity)))
            screen.blit(log_image,(log[0] + random.randint(-shake_intensity, shake_intensity), height - log[2] + random.randint(-shake_intensity, shake_intensity)))

        pygame.display.flip()
        shake_counter += 1

        ## Controla a velocidade da queda
        pygame.time.delay(15)

# Função principal do jogo
def game_loop():
    global pipoco_y, pipoco_speed, game_over, freeze, score, logs, frame_count, bg_x

    reload()

    while not game_over:
        draw_background()

        ## Seta os botões de pulo do pipoco
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over)
                    or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over)):
                if freeze:
                    tela_menu()
                    freeze = False
                pipoco_speed = -10

        if freeze:
            continue

        ## Atualiza a gravidade e a posição do pipoco
        pipoco_speed += gravity
        pipoco_y += pipoco_speed

        ## Cria os logs a cada 100 frames
        if frame_count % 100 == 0:
            height_top = random.randint(50, height - log_gap - 50)
            height_bottom = height - height_top - log_gap
            logs.append((width, height_top, height_bottom))

        ## Move os logs e verifica as colisões
        for i in range(len(logs) - 1, -1, -1):
            log_x, log_top_height, log_bottom_height = logs[i]
            log_x -= 5
            logs[i] = (log_x, log_top_height, log_bottom_height)

            ## Cria retângulos para os logs
            top_log_rect = pygame.Rect(log_x, 0, log_width, log_top_height)
            bottom_log_rect = pygame.Rect(log_x, height - log_bottom_height, log_width, log_bottom_height)

            ## Cria um retângulo de colisão para o pipoco
            pipoco_rect = pygame.Rect(pipoco_x, pipoco_y, pipoco_width, pipoco_height)
            if pipoco_rect.colliderect(top_log_rect) or pipoco_rect.colliderect(bottom_log_rect):
                pipoco_fall_and_shake()
                freeze = True
                break

            ## Remove os logs que já saíram da tela
            if log_x + log_width < 0:
                logs.pop(i)
                score += 1

        frame_count += 1
        draw_pipoco()
        draw_log()

        if pipoco_y < 0 or pipoco_y > height:
            freeze = True

        ## Exibe a pontuação
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(score_text, (10, 10))

        if freeze:
            game_over_logo = pygame.image.load("assets/game-over-1.png")
            screen.blit(pygame.transform.scale(game_over_logo, (300, 165)), (width/2 - 150, 100))

        pygame.display.flip()
        clock.tick(60)


tela_menu()
game_loop()
