from random import shuffle
from turtle import up, goto, down, color, begin_fill, forward, left, end_fill, clear
from turtle import shape, stamp, write, update, ontimer, setup, addshape, hideturtle, tracer, onscreenclick, done
from freegames import path

#Imagen del carro
car = path('car.gif')

#Inicialización del juego
tiles = list(range(32)) * 2
state = {'mark': None}
hide = [True] * 64

#Contador de taps
taps=0

def square(x, y):
    # Dibuja un cuadrado blanco en (x, y)
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    # Convierte las coordenadas (x, y) en un indice de tile
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    #Convierte el dinde de tile a coordenadas (x, y)
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    # Actualiza el estado de las marcas y tiles ocultos basados en el tap

    # Saca la variable taps del local"
    global taps
    #Agrega 1 por cada tap"
    taps= taps+1
    spot = index(x, y)
    mark = state['mark']
    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None


def draw():
    #Dibuja la imagen, tiles y cuenta el numero de taps
    clear()
    goto(0, 0)
    shape(car)
    stamp()
    # Dibuja el grid de tiles
    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    # Dibuja el numero en el tile marcado
    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))
    #Muestra los taps
    up()
    goto(-200, -250)
    color("black")
    write(f'Taps: {taps}')

    #Detecta si todos los cuadros han sido destapados
    if True not in hide:
        goto(-50,0)
        write("Lo lograste!")

    update()
    ontimer(draw, 100)

#Config del juego
shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()