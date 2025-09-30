from random import randrange

sel = 0
victoria = 0

print("\n\t░▒▓╔══════╗▓▒░\n\t░▒▓║DONUTS║▓▒░\n\t░▒▓╚══════╝▓▒░")

def generarTablero():
    global tablero
    tablero = [[randrange(0, 4) for _ in range(6)] for _ in range(6)]

def pintarTablero():
    n = 1
    print("\n\t    1 2 3 4 5 6")
    print("\t  ╔═════════════╗")
    for row in tablero:
        linea = f"\t{n} ║ "
        for cell in row:
            match cell:
                case 0:
                    linea += "│ "
                case 1:
                    linea += "─ "
                case 2:
                    linea += "/ "
                case 3:
                    linea += "\\ "
                case 4 | 5 | 6 | 7:
                    linea += "× "
                case 8 | 9 | 10 | 11:
                    linea += "○ "
        n+=1
        linea += "║ "
        print(linea)
    print("\t  ╚═════════════╝")

    if jugadaAnterior != None:
        match tablero[jugadaAnterior[0]][jugadaAnterior[1]]:
            case 0 | 4 | 8:
                casilla = "│"
            case 1 | 5 | 9:
                casilla = "─"
            case 2 | 6 | 10:
                casilla = "/"
            case 3 | 7 | 11:
                casilla = "\\"

        print(f"\n\tÚltima casilla: {casilla} ({jugadaAnterior[0]+1}, {jugadaAnterior[1]+1})")


def verificarCasilla(y, x):
    dy = y - jugadaAnterior[0]
    dx = x - jugadaAnterior[1]
    valor_anterior = tablero[jugadaAnterior[0]][jugadaAnterior[1]] % 4
    direcciones = {
        0: [(-1,0), (1,0)],    # │
        1: [(0,-1), (0,1)],    # ─
        2: [(-1,1), (1,-1)],   # /
        3: [(-1,-1), (1,1)]    # \
    }
    
    if (dy, dx) in direcciones[valor_anterior]:
        return True
    else:
        return False


def colocar(n, y, x):
    # n = 1  ->  d negros ×
    # n = 2  ->  d blancos ○ / IA
    permitir = False

    if (x >= 0) and (x < 6) and (y >= 0) and (y < 6):

        if jugadaAnterior == None:
            permitir = True
        else:
            permitir = verificarCasilla(y, x)

        if permitir == True:
            match tablero[y][x]:
                case 0 | 4 | 8:
                    tablero[y][x] = 4
                case 1 | 5 | 9:
                    tablero[y][x] = 5
                case 2 | 6 | 10:
                    tablero[y][x] = 6
                case 3 | 7 | 11:
                    tablero[y][x] = 7
            if n == 2:
                tablero[y][x] += 4

            return True
        else:
            return False

    else:
        return False
    

def verificarVictoria():
    global victoria
    victoria = 0

    y, x = jugadaAnterior
    cell = tablero[y][x]

    if cell in (4, 5, 6, 7):
        cellVal = (4, 5, 6, 7)
        ganador = 1
    elif cell in (8, 9, 10, 11):
        cellVal = (8, 9, 10, 11)
        ganador = 2
    else:
        return

    # vertical │, horizontal ─, diagonal /, diagonal \
    direcciones = [
        (-1, 0), (0, -1), (-1, 1), (-1, -1)
    ]

    for dy, dx in direcciones:
        contador = 1

        ny, nx = y + dy, x + dx
        while 0 <= ny < 6 and 0 <= nx < 6 and tablero[ny][nx] in cellVal:
            contador += 1
            ny += dy
            nx += dx

        ny, nx = y - dy, x - dx
        while 0 <= ny < 6 and 0 <= nx < 6 and tablero[ny][nx] in cellVal:
            contador += 1
            ny -= dy
            nx -= dx

        if contador >= 5:
            victoria = ganador
            return


def empezarJuego(nJ):
    global jugadaAnterior
    jugadaAnterior = None

    generarTablero()
    pintarTablero()

    while victoria == 0:

        valido = False
        while valido == False:
            print("\n\t▀▄█ Donuts negros █▄▀")
            try:
                y = int(input("\tCoordenada vertical: ")) - 1
                x = int(input("\tCoordenada horizontal: ")) - 1
            except:
                y = -1
                x = -1
            if jugadaAnterior != None:
                valido = colocar(1, y, x)
            else:
                colocar(1, y, x)
                valido = True
            if valido == True:
                jugadaAnterior = (y, x)
                pintarTablero()
            else:
                print("\n\tCasilla no válida.")

        valido = False
        if nJ == 1:
            while valido == False:
                y = randrange(0,3)
                x = randrange(0,3)
                valido = colocar(2, y, x)
                if valido == True:
                    print("\n\t░▒▓ Donuts blancos (IA) ▓▒░")
                    jugadaAnterior = (y, x)
                    pintarTablero()
        else:
            while valido == False:
                print("\n\t░▒▓ Donuts blancos ▓▒░")
                try:
                    y = int(input("\tCoordenada vertical: ")) - 1
                    x = int(input("\tCoordenada horizontal: ")) - 1
                except:
                    y = -1
                    x = -1
                valido = colocar(2, y, x)
                if valido == True:
                    jugadaAnterior = (y, x)
                    pintarTablero()
                else:
                    print("\n\tCasilla no válida.")
    if victoria == 1:
        print("¡Ganan los donuts negros!")
    if victoria == 2:
        print("¡Ganan los donuts blancos!")

while not ((sel == 1) or (sel == 2) or (sel == 3) or (sel == 4)):
    print("\n\t1. 1 jugador.")
    print("\t2. 2 jugadores.")
    print("\t3. Leer las reglas.")
    print("\t4. Salir.")
    try:
        sel = int(input("\n\tEscoge una opción: "))
    except:
        sel = 0

    match sel:
        case 1:
            empezarJuego(1)

        case 2:
            empezarJuego(2)

        case 3:
            print("\n\tReglas")

        case 4:
            print("\n\tSaliendo del programa...")

        case _:
            print("\n\tERROR: opción no válida.")