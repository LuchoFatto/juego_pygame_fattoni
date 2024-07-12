import pygame
from random import randint
from settings import *

def create_block(imagen:pygame.Surface= None, left = 0, top = 0, width = 50, height = 50,
                color = (255, 255, 255), dir = 3, borde = 0, radio = -1)->dict:
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))

    return {"rect": pygame.Rect(left, top, width, height),"color": color,
            "dir": dir, "borde": borde, "radio": radio, "img": imagen}

def create_player(imagen:pygame.Surface= None):
    return create_block(imagen, MID_WIDTH_SCREEN, MID_HEIGHT_SCREEN, PLAYER_W, PLAYER_H, BLUE, 0, 0, 0)

def create_enemy(imagen: pygame.Surface = None):
    left, top = spawn[randint(1, 4)]
    return create_block(imagen, left, top, PLAYER_W, PLAYER_H, BLUE, 0, 0, 0)

def create_laser(midBottom:tuple[int, int], direction:str, color:tuple[int, int, int]=GREY):
    block = {"rect": pygame.Rect(0, 0, BALA_W, BALA_H), "color": color, "speed": BALA_SPEED, "direction": direction}
    block["rect"].midbottom = midBottom
    return block

def load_enemy_list(lista: list, cant_enemys: int, imagen: pygame.Surface = None):
    for _ in range(cant_enemys):
        lista.append(create_enemy(imagen))