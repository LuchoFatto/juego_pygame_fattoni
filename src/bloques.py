import pygame
from random import randint
from settings import *

def create_block(imagen: pygame.Surface = None, left: int = 0, top: int = 0, width: int = 50, height: int = 50,
                color: tuple = (255, 255, 255), dir: int = 3, borde: int = 0, radio: int = -1) -> dict:
    """
    Crea un bloque con las características especificadas.

    Args:
        imagen (pygame.Surface, opcional): La imagen del bloque. Si se proporciona, se redimensionará a las dimensiones especificadas.
        left (int, opcional): La coordenada x de la esquina superior izquierda del bloque. Por defecto es 0.
        top (int, opcional): La coordenada y de la esquina superior izquierda del bloque. Por defecto es 0.
        width (int, opcional): El ancho del bloque. Por defecto es 50.
        height (int, opcional): La altura del bloque. Por defecto es 50.
        color (tuple, opcional): El color del bloque en formato RGB. Por defecto es blanco (255, 255, 255).
        dir (int, opcional): La dirección del bloque. El valor por defecto es 3.
        borde (int, opcional): El grosor del borde del bloque. Por defecto es 0.
        radio (int, opcional): El radio del borde redondeado del bloque. Si es -1, no hay borde redondeado. Por defecto es -1.

    Returns:
        dict: Un diccionario que contiene el rectángulo del bloque (`rect`), el color (`color`), la dirección (`dir`), 
            el grosor del borde (`borde`), el radio del borde redondeado (`radio`) y la imagen (`img`).
    """
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))

    return {"rect": pygame.Rect(left, top, width, height), "color": color,
            "dir": dir, "borde": borde, "radio": radio, "img": imagen}

def create_player(imagen: pygame.Surface = None) -> dict:
    """
    Crea un jugador con las características especificadas.

    Args:
        imagen (pygame.Surface, opcional): La imagen del jugador. Si se proporciona, se redimensionará a las dimensiones especificadas.

    Returns:
        dict: Un diccionario que contiene el rectángulo del jugador (`rect`), el color (`color`), la dirección (`dir`), 
            el grosor del borde (`borde`), el radio del borde redondeado (`radio`) y la imagen (`img`).
    """
    return create_block(imagen, MID_WIDTH_SCREEN, MID_HEIGHT_SCREEN, PLAYER_W, PLAYER_H, BLUE, 0, 0, 0)

def create_enemy(imagen: pygame.Surface = None) -> dict:
    """
    Crea un enemigo con las características especificadas.

    Args:
        imagen (pygame.Surface, opcional): La imagen del enemigo. Si se proporciona, se redimensionará a las dimensiones especificadas.

    Returns:
        dict: Un diccionario que contiene el rectángulo del enemigo (`rect`), el color (`color`), la dirección (`dir`), 
            el grosor del borde (`borde`), el radio del borde redondeado (`radio`) y la imagen (`img`).

    Nota:
        La posición inicial del enemigo se determina aleatoriamente a partir de un conjunto de posibles posiciones de spawn.
    """
    left, top = spawn[randint(1, 4)]
    return create_block(imagen, left, top, PLAYER_W, PLAYER_H, BLUE, 0, 0, 0)

def create_bullet(midBottom: tuple[int, int], direction: str, color: tuple[int, int, int] = GREY) -> dict:
    """
    Crea una bala con las características especificadas.

    Args:
        midBottom (tuple[int, int]): La posición (x, y) del punto medio de la base inferior de la bala.
        direction (str): La dirección en la que se moverá la bala.
        color (tuple[int, int, int], opcional): El color de la bala en formato RGB. Por defecto es gris (GREY).

    Returns:
        dict: Un diccionario que contiene el rectángulo de la bala (`rect`), el color (`color`), 
            la velocidad (`speed`) y la dirección (`direction`).
    """
    block = {"rect": pygame.Rect(0, 0, BALA_W, BALA_H), "color": color, "speed": BALA_SPEED, "direction": direction}
    block["rect"].midbottom = midBottom
    return block

def crear_bonus(img: pygame.Surface) -> dict:
    """
    Crea un bloque que representa un bono con la imagen y velocidad proporcionadas.

    Args:
        img (pygame.Surface): La imagen que se usará para el bono.
        speed (int): La velocidad del bono en el eje y.

    Returns:
        dict: Un diccionario que representa el bonus creado.
    """
    block = create_block(img, randint(MIN_WIDTH_SALIDA_B, MAX_WIDTH_SALIDA_B - BONUS_W),
                        randint(MIN_HEIGHT_SALIDA_B, MAX_HEIGHT_SALIDA_B - BONUS_H), BONUS_W, BONUS_H, YELLOW, 0, 0, 0)
    return block