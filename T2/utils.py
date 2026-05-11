import math


def calcular_angulo(a, b, c):
    """
    Calculates the angle at point B, formed by segments BA and BC.
    a, b, c are (x, y) tuples.
    Returns angle in degrees [0, 180].
    """
    angulo = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )
    angulo = abs(angulo)

    if angulo > 180:
        angulo = 360 - angulo

    return angulo


def distancia_euclidiana(a, b):
    """
    Calculates the Euclidean distance between two (x, y) points.
    """
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
