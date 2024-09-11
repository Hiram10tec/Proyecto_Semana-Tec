"""Pacman, juego clásico de arcade."""

from random import choice
from turtle import Turtle, bgcolor, clear, up, goto, dot, update, ontimer
from turtle import setup, hideturtle, tracer, listen, onkey, done
from freegames import floor, vector

# Estado del juego con el puntaje
state = {'score': 0}

# Creación de las tortugas para dibujar y mostrar el puntaje
path = Turtle(visible=False)
writer = Turtle(visible=False)

# Dirección inicial de Pacman
aim = vector(5, 0)

# Posición inicial de Pacman
pacman = vector(-40, -80)

# Lista de fantasmas con sus posiciones y direcciones iniciales
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# Mapa del tablero, donde 0 es una pared y 1 es un espacio con puntos
    # Tablero en una lista 1D,cada valor es un espacio del mapa
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0,
    0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0,
    0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
def square(x, y):
    """Dibuja un cuadrado azul en la posición (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    # Dibuja un cuadrado de 4 lados
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Retorna el índice correspondiente al punto en el mapa tiles."""
    x = (floor(point.x, 20) + 200) // 20
    y = (180 - floor(point.y, 20)) // 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    if 0 <= index < len(tiles):
        if tiles[index] == 0:
            return False

        index = offset(point + vector(19, 0))
        if 0 <= index < len(tiles):
            if tiles[index] == 0:
                return False

        index = offset(point + vector(0, 19))
        if 0 <= index < len(tiles):
            if tiles[index] == 0:
                return False

        return point.x % 20 == 0 or point.y % 20 == 0
    return False


def world():
    """Dibuja el tablero de juego."""
    bgcolor('black')
    path.color('blue')

    # Recorre cada celda del tablero y la dibuja
    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            # Dibuja los puntos que Pacman debe comer
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Mueve a Pacman y a los fantasmas en cada ciclo de juego."""
    writer.undo()
    writer.write(state['score'])

    clear()

    # Verifica si Pacman puede moverse en la dirección actual
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    # Si Pacman come un punto, actualiza el tablero y el puntaje
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    # Dibuja a Pacman
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Mueve a los fantasmas y los redibuja
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # Si el camino no es válido,el fantasma cambia de dirección al azar
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    # Si Pacman y un fantasma colisionan, termina el juego
    for point, _ in ghosts:
        if abs(pacman - point) < 20:
            return

    # Programa el siguiente ciclo de movimiento
    ontimer(move, 100)


def change(x, y):
    """Cambia la dirección de Pacman si es válida."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Configuración inicial de la ventana del juego
setup(420, 420, 370, 0)
hideturtle()
tracer(False)

# Configura la posición del contador de puntaje
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])

# Configura las teclas de control para mover a Pacman
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

# Dibuja el mundo inicial y comienza el ciclo de movimiento
world()
move()
done()
