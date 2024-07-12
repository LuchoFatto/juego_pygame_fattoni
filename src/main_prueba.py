import pygame
from settings import *
from random import randint
from bloques import *
from colisiones import *
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Configurar pantalla inicial
SCREEN = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Viaje del Rey de la Pradera")
pygame.display.set_icon(pygame.image.load("./src/assets/images/icono.png"))

# Cargar imágenes
imagen_de_fondo = pygame.transform.scale(pygame.image.load("./src/assets/images/imagen_de_fondo.png"), SIZE_SCREEN)
personaje = pygame.image.load("./src/assets/images/personaje.png")
enemigo = pygame.image.load("./src/assets/images/enemigo.png")

def main():
    INITIALS_ENEMYS = 6
    # Jugador
    player = create_player(personaje)

    # Enemigos y balas
    enemies = []
    bullets = []
    load_enemy_list(enemies, INITIALS_ENEMYS, enemigo)

    # Direcciones
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    # Puntajes y bonus
    lives = 3
    escudos = 0

    # Nivel u oleada
    nivel = 1

    # Temporizador y contador de enemigos
    enemies_spawned = 0
    enemy_spawn_timer = 60  # 1 segundo (60 frames)

    # Config
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        clock.tick(FPS)

        # Gestión de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    move_down = True
                    move_up = False
                elif event.key == K_w:
                    move_up = True
                    move_down = False
                elif event.key == K_a:
                    move_left = True
                    move_right = False
                elif event.key == K_d:
                    move_right = True
                    move_left = False
                elif event.key == K_UP:
                    bullets.append(create_laser(player["rect"].midtop, "up"))
                elif event.key == K_DOWN:
                    bullets.append(create_laser(player["rect"].midbottom, "down"))
                elif event.key == K_LEFT:
                    bullets.append(create_laser(player["rect"].midleft, "left"))
                elif event.key == K_RIGHT:
                    bullets.append(create_laser(player["rect"].midright, "right"))
            elif event.type == KEYUP:
                if event.key == K_s:
                    move_down = False
                elif event.key == K_w:
                    move_up = False
                elif event.key == K_a:
                    move_left = False
                elif event.key == K_d:
                    move_right = False

        # Actualizar jugador según las direcciones y limitaciones
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
                enemy_spawn_timer = 60  # Reinicia el temporizador a 1 segundo (60 frames)

        # El enemigo persigue al jugador
        for enemy in enemies:
            if enemy["rect"].x < player["rect"].x:
                enemy["rect"].x += 2
            if enemy["rect"].x > player["rect"].x:
                enemy["rect"].x -= 2
            if enemy["rect"].y < player["rect"].y:
                enemy["rect"].y += 2
            if enemy["rect"].y > player["rect"].y:
                enemy["rect"].y -= 2

        # Dirección de las balas y destrucción si salen de pantalla
        for bullet in bullets[:]:
            if bullet["direction"] == "left":
                bullet["rect"].x -= bullet["speed"]
            elif bullet["direction"] == "right":
                bullet["rect"].x += bullet["speed"]
            elif bullet["direction"] == "up":
                bullet["rect"].y -= bullet["speed"]
            elif bullet["direction"] == "down":
                bullet["rect"].y += bullet["speed"]

            if bullet["rect"].right < 0 or bullet["rect"].left > WIDTH or bullet["rect"].bottom < 0 or bullet["rect"].top > HEIGHT:
                bullets.remove(bullet)

        # Detectar colisiones entre balas y enemigos y eliminar ambos
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if detectar_colision(bullet["rect"], enemy["rect"]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        # Si no hay más enemigos en pantalla, iniciar nueva oleada
        if not enemies and enemies_spawned == INITIALS_ENEMYS:
            nivel += 1  # Incrementar el nivel
            INITIALS_ENEMYS += 1  # Aumentar la cantidad de enemigos para la siguiente oleada
            enemies_spawned = 0  # Reiniciar el contador de enemigos aparecidos
            enemy_spawn_timer = 60  # Reinicia el temporizador a 1 segundo (60 frames)
            load_enemy_list(enemies, INITIALS_ENEMYS, enemigo)  # Cargar nuevos enemigos

        # Dibujar elementos en pantalla
        SCREEN.blit(imagen_de_fondo, ORIGIN)
        SCREEN.blit(player["img"], player["rect"])
        for enemy in enemies:
            SCREEN.blit(enemy["img"], enemy["rect"])
        for bullet in bullets:
            pygame.draw.rect(SCREEN, bullet["color"], bullet["rect"])
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
