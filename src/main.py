import pygame
from settings import *
from random import randint
from bloques import *
from colisiones import *
# from interacciones import *
from pygame.locals import *

imagen_de_fondo = pygame.transform.scale(pygame.image.load("./src/assets/images/imagen_de_fondo.png"), SIZE_SCREEN)
personaje = pygame.image.load("./src/assets/images/personaje.png")
enemigo = pygame.image.load("./src/assets/images/enemigo.png")

pygame.init()

#Configurar pantalla inicial
SCREEN = pygame.display.set_mode(SIZE_SCREEN)

#Nombre e Icono del juego
pygame.display.set_caption("Viaje del Rey de la Pradera")
pygame.display.set_icon(pygame.image.load("./src/assets/images/icono.png") )


start_time = pygame.time.get_ticks()
while True:
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
    escudos = 0
    vida_extra = None
    atraviesa_disparo = None
    escudo_extra = None
    bullet = None

    # Oleada
    oleada = 1

    #Config
    clock = pygame.time.Clock()
    delay = 3000

    current_time = pygame.time.get_ticks()
    is_running = True

    # Temporizador para controlar la aparición escalonada de enemigos
    enemy_spawn_timer = 30  # 1 segundo (60 frames)
    enemies_spawned = 0
    flag_no_enemies = False
    wave_start_time = 0

    while is_running:
        #Frames
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running == False
                pygame.quit()
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
                if event.key == K_UP:
                    bullet = bullets.append(create_laser(player["rect"].midtop, "up"))
                elif event.key == K_DOWN:
                    bullet = bullets.append(create_laser(player["rect"].midbottom, "down"))
                elif event.key == K_LEFT:
                    bullet = bullets.append(create_laser(player["rect"].midleft, "left"))
                elif event.key == K_RIGHT:
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
            if bullet:
                if detectar_colision(bullet["rect"], enemy["rect"]):
                    # collision_sound.play()
                    enemies.remove(enemy)
                    #bullet = None
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
                #explosion.play()
                if lives == 0:
                    is_running = False


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
        #Actualizar pantalla
        pygame.display.flip()



























