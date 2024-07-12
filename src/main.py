import pygame
from settings import *
from random import randint
from bloques import *
from colisiones import *
from estructura import *
from pygame.locals import *

pygame.init()

#Fuente
fuente = pygame.font.Font("./src/assets/fonts/dash-horizon.otf", 32)

#Imagenes
imagen_de_fondo = pygame.transform.scale(pygame.image.load("./src/assets/images/imagen_de_fondo.png"), SIZE_SCREEN)
personaje = pygame.image.load("./src/assets/images/personaje.png")
enemigo = pygame.image.load("./src/assets/images/enemigo.png")
imagen_fondo_inicio = pygame.transform.scale(pygame.image.load("./src/assets/images/fondo_inicio.jpg"), SIZE_SCREEN)
start_button = pygame.transform.scale(pygame.image.load("./src/assets/images/start_button.png"), BUTTON_SIZE)
exit_button = pygame.transform.scale(pygame.image.load("./src/assets/images/exit_button.png"), BUTTON_SIZE)
vida_extra = pygame.image.load("./src/assets/images/imagen_vida.png")
speed_up = pygame.image.load("./src/assets/images/imagen_poder.png")

#Sonidos
disparo = pygame.mixer.Sound("./src/assets/sounds/disparo.wav")
impacto_enemigo =pygame.mixer.Sound("./src/assets/sounds/impacto.ogg")
game_over = pygame.mixer.Sound("./src/assets/sounds/game_over.wav")
hit_live = pygame.mixer.Sound("./src/assets/sounds/hit.wav")

#Musica fondo
pygame.mixer.music.load("./src/assets/music/musica_fondo.wav")

#Volumen
disparo.set_volume(0.045)
impacto_enemigo.set_volume(0.045)
hit_live.set_volume(0.3)
pygame.mixer.music.set_volume(0.05)

#Configurar pantalla inicial
SCREEN = pygame.display.set_mode(SIZE_SCREEN)

#Nombre e Icono del juego
pygame.display.set_caption("Viaje del Rey de la Pradera")
pygame.display.set_icon(pygame.image.load("./src/assets/images/icono.png") )

while True:
    config = cargar_json("config")
    playing_music = config[0]["mute"]
    records = cargar_csv("records")

    #Pantalla de inicio
    SCREEN.blit(imagen_fondo_inicio, ORIGIN)
    rect_start_button = start_button.get_rect(center= POS_START)
    rect_exit_button = exit_button.get_rect(center= POS_EXIT)
    SCREEN.blit(start_button, rect_start_button)
    SCREEN.blit(exit_button, rect_exit_button)
    pygame.display.flip()
    esperar_click_jugador(rect_start_button, rect_exit_button)


    #Jugador
    player = create_player(personaje)

    #Enemigo y balas
    enemies = []
    bullets = []

    #Direcciones
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    # Puntajes y bonus
    lives = 3
    velocidad_arriba = None
    vida = None
    bullet = None
    GENERAR_BONUS = pygame.USEREVENT + 1
    pygame.time.set_timer(GENERAR_BONUS, TIME_BONUS)

    # Oleada
    oleada = 1

    #Config
    clock = pygame.time.Clock()
    is_running = True

    #Temporizador y bonus
    start_time_speed_up = 0
    start_time = pygame.time.get_ticks()

    #Temporizador para controlar la aparición escalonada de enemigos
    enemy_spawn_timer = 30
    enemies_spawned = 0
    flag_no_enemies = False
    wave_start_time = 0

    #Musica
    pygame.mixer.music.play(-1)
    playing_music = True

    while is_running:
        #Frames
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False
                terminar()
            #Detecta cuandos se apreta una tecla
            if event.type == KEYDOWN:
                if event.key == K_s:
                        move_down = True
                        move_up = False
                if event.key == K_w:
                        move_up = True
                        move_down = False
                if event.key == K_a:
                        move_left = True
                        move_right = False
                if event.key == K_d:
                        move_right = True
                        move_left = False
                if event.key == K_m:
                    if playing_music:
                        pygame.mixer_music.pause()
                    else:
                        pygame.mixer_music.unpause()
                    playing_music = not playing_music
                if event.key == K_UP:
                    disparo.play()
                    bullet = bullets.append(create_laser(player["rect"].midtop, "up"))
                elif event.key == K_DOWN:
                    disparo.play()
                    bullet = bullets.append(create_laser(player["rect"].midbottom, "down"))
                elif event.key == K_LEFT:
                    disparo.play()
                    bullet = bullets.append(create_laser(player["rect"].midleft, "left"))
                elif event.key == K_RIGHT:
                    disparo.play()
                    bullet = bullets.append(create_laser(player["rect"].midright, "right"))
            
            #Detecta cuando se deja de presionar una tecla
            if event.type == KEYUP:
                if event.key == K_s:
                    move_down = False
                if event.key == K_w:
                    move_up = False
                if event.key == K_a:
                    move_left = False
                if event.key == K_d:
                    move_right = False
            
            if event.type == GENERAR_BONUS:
                opcion = 2
                if opcion == 1:
                    vida = crear_bonus(vida_extra)
                else:
                    velocidad_arriba = crear_bonus(speed_up)

        # actiualizar elementos

        #muevo el personaje segun sus direcciones y hago tope en los arbustos
        if move_left and player["rect"].left > 0:
            player["rect"].x -= SPEED
            if player["rect"].left < 45:
                player["rect"].left = 45
        if move_right and player["rect"].right < WIDTH:
            player["rect"].x += SPEED
            if player["rect"].right > WIDTH - 45:
                player["rect"].right = WIDTH - 45
        if move_up and player["rect"].top > 0:
            player["rect"].y -= SPEED
            if player["rect"].top < 45:
                player["rect"].top = 45
        if move_down and player["rect"].bottom < HEIGHT:
            player["rect"].y += SPEED
            if player["rect"].bottom > HEIGHT - 45:
                player["rect"].bottom = HEIGHT - 45

        # Lógica para la aparición escalonada de enemigos
        if enemy_spawn_timer > 0:
            enemy_spawn_timer -= 1
        else:
            if enemies_spawned < INITIALS_ENEMYS:
                new_enemy = create_enemy(enemigo)
                enemies.append(new_enemy)
                enemies_spawned += 1
                enemy_spawn_timer = 30 

        #El enemigo persigue al personaje
        for enemy in enemies[:]:
            if enemy["rect"].x < player["rect"].x:
                enemy["rect"].x += 2
            if enemy["rect"].x > player["rect"].x:
                enemy["rect"].x -= 2
            if enemy["rect"].y < player["rect"].y:
                enemy["rect"].y += 2
            if enemy["rect"].y > player["rect"].y:
                enemy["rect"].y -= 2

        #Direcccion de disparo
        for bullet in bullets[:]:
            if bullet["direction"] == "left":
                bullet["rect"].x -= bullet["speed"]
            elif bullet["direction"] == "right":
                bullet["rect"].x += bullet["speed"]
            elif bullet["direction"] == "up":
                bullet["rect"].y -= bullet["speed"]
            elif bullet["direction"] == "down":
                bullet["rect"].y += bullet["speed"]

        # Destruir la bala si sale de la pantalla
            if bullet["rect"].right < 0 or bullet["rect"].left > WIDTH or bullet["rect"].bottom < 0 or bullet["rect"].top > HEIGHT:
                bullets.remove(bullet)

        # Detectar colisiones entre balas y enemigos
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if bullet:
                    if detectar_colision(bullet["rect"], enemy["rect"]):
                        impacto_enemigo.play()
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        if len(enemies) == 0:
                            wave_start_time = pygame.time.get_ticks()
                            flag_no_enemies = True

        if flag_no_enemies:
            if pygame.time.get_ticks() - wave_start_time >= 3000:
                oleada += 1
                INITIALS_ENEMYS += 1
                enemies_spawned = 0
                flag_no_enemies = False

        if not flag_no_enemies:
            if enemy_spawn_timer > 0:
                    enemy_spawn_timer -= 1
            else:
                if enemies_spawned < INITIALS_ENEMYS:
                    new_enemy = create_enemy(enemigo)
                    enemies.append(new_enemy)
                    enemies_spawned += 1
                    enemy_spawn_timer = 30

        for enemy in enemies[:]:
            if dectectar_colision_circulos(player["rect"], enemy["rect"]):
                enemies.remove(enemy)
                lives -= 1
                hit_live.play()
                if lives == 0:
                    game_over.play()
                    is_running = False

        if vida:
            if detectar_colision(vida["rect"], player["rect"]):
                lives += 1
                vida = None
        
        if velocidad_arriba:
            if detectar_colision(velocidad_arriba["rect"],player["rect"]):
                start_time_speed_up = pygame.time.get_ticks()
                SPEED += 1

        if start_time_speed_up and pygame.time.get_ticks() - start_time_speed_up <= TIME_SPEED_UP:
            velocidad_arriba = None
            SPEED = 4

        #Calcular el tiempo transcurrido
        tiempo_transcurrido = (pygame.time.get_ticks() - start_time) / 1000
        min_transcurridos = int(tiempo_transcurrido // 60)
        seg_transcurridos = int(tiempo_transcurrido % 60)
        tiempo = f"{min_transcurridos:02}:{seg_transcurridos:02}"
        # Dibujar pantalla, mostrar enemigos y balas, etc.

        #Dibujar pantalla
        SCREEN.blit(imagen_de_fondo, ORIGIN)
        SCREEN.blit(player["img"], player["rect"])
        
        #Muestro enemigos
        for enemy in enemies:
            SCREEN.blit(enemy["img"], enemy["rect"])
        
        #Muestro balas
        for bullet in bullets:
            pygame.draw.rect(SCREEN, bullet["color"], bullet["rect"])

        if vida:
            SCREEN.blit(vida["img"], vida["rect"])

        if velocidad_arriba:
            SCREEN.blit(velocidad_arriba["img"], velocidad_arriba["rect"])

        mostrar_texto(SCREEN, POS_OLEADAS, f"Oleada: {oleada}", fuente, WHITE, BLACK)
        mostrar_texto(SCREEN, POS_VIDAS, f"Lives: {lives}", fuente, WHITE, BLACK)
        #Actualizar pantalla
        pygame.display.flip()
    config[0]["mute"] = playing_music
    guardar_json("config", config)
    new_record = {"puesto":None, "oleada":oleada, "tiempo":tiempo}
    records.append(new_record)
    #orden_lista(lambda rec_uno,rec_dos: int(rec_uno["tiempo"].replace(":", "")) < int(rec_dos["tiempo"].replace(":", "")),records)



























