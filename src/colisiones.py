import pygame

def punto_en_rectangulo(punto: tuple[int, int], rect: pygame.Rect) -> bool:
    """
    Verifica si un punto está dentro de un rectángulo.

    Args:
        punto (tuple[int, int]): Una tupla que representa las coordenadas (x, y) del punto a verificar.
        rect (pygame.Rect): Un objeto pygame.Rect que define el rectángulo.

    Returns:
        bool: True si el punto está dentro del rectángulo, False en caso contrario.
    """
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def detectar_colision(rect_1: pygame.Rect, rect_2: pygame.Rect) -> bool:
    """
    Detecta si hay una colisión entre dos rectángulos.

    Esta función verifica si algún punto de `rect_1` está dentro de `rect_2` o si algún punto de `rect_2`
    está dentro de `rect_1`.

    Args:
        rect_1 (pygame.Rect): El primer rectángulo a verificar.
        rect_2 (pygame.Rect): El segundo rectángulo a verificar.

    Returns:
        bool: True si hay una colisión entre los dos rectángulos, False en caso contrario.
    """
    # Revisa si algún punto del rect_1 está dentro de rect_2
    if (punto_en_rectangulo(rect_1.topleft, rect_2) or
        punto_en_rectangulo(rect_1.topright, rect_2) or
        punto_en_rectangulo(rect_1.bottomleft, rect_2) or
        punto_en_rectangulo(rect_1.bottomright, rect_2)):
        return True
    
    # Revisa si algún punto del rect_2 está dentro de rect_1
    if (punto_en_rectangulo(rect_2.topleft, rect_1) or
        punto_en_rectangulo(rect_2.topright, rect_1) or
        punto_en_rectangulo(rect_2.bottomleft, rect_1) or
        punto_en_rectangulo(rect_2.bottomright, rect_1)):
        return True
    
    # Si no encuentra ninguna colisión, devuelve False
    return False

def distancia_entre_puntos(pto_1: tuple[int, int], pto_2: tuple[int, int]) -> float:
    """
    Calcula la distancia entre dos puntos en un plano cartesiano.

    Args:
        pto_1 (tuple[int, int]): Las coordenadas (x, y) del primer punto.
        pto_2 (tuple[int, int]): Las coordenadas (x, y) del segundo punto.

    Returns:
        float: La distancia entre los dos puntos calculada usando el teorema de Pitágoras.
    """
    return ((pto_1[0] - pto_2[0]) ** 2 + (pto_1[1] - pto_2[1]) ** 2) ** 0.5

def calcular_radio(rect: pygame.Rect) -> int:
    """
    Calcula el radio de un círculo inscrito en un rectángulo.

    Args:
        rect (pygame.Rect): El rectángulo del cual se calculará el radio.

    Returns:
        int: El radio del círculo inscrito.
    """
    return rect.width // 2

def dectectar_colision_circulos(rect_1: pygame.Rect, rect_2: pygame.Rect) -> bool:
    """
    Detecta si hay una colisión entre dos círculos inscritos en rectángulos dados.

    Args:
        rect_1 (pygame.Rect): El primer rectángulo que contiene al primer círculo.
        rect_2 (pygame.Rect): El segundo rectángulo que contiene al segundo círculo.

    Returns:
        bool: True si hay colisión entre los círculos, False en caso contrario.
    """
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

