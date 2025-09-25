from random import randrange

sel = 0

# Jugador 1 = donuts negros
# Jugador 2 = donuts blancos
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

def verificarCasilla(y, x):
    return True

def colocar(n, y, x):
    # n = 1  ->  d negros
    # n = 2  ->  d blancos
    # n = 3  ->  IA

    if (x >= 0) and (x < 6) and (y >= 0) and (y < 6):
        match n:
            case 1:
                match tablero[y][x]:
                    case 0 | 4 | 8:
                        tablero[y][x] = 4
                    case 1 | 5 | 9:
                        tablero[y][x] = 5
                    case 2 | 6 | 10:
                        tablero[y][x] = 6
                    case 3 | 7 | 11:
                        tablero[y][x] = 7

            case 2:
                match tablero[y][x]:
                    case 0 | 4 | 8:
                        tablero[y][x] = 8
                    case 1 | 5 | 9:
                        tablero[y][x] = 9
                    case 2 | 6 | 10:
                        tablero[y][x] = 10
                    case 3 | 7 | 11:
                        tablero[y][x] = 11

            case 3:
                x = randrange(0,3)
                y = randrange(0,3)
                match tablero[y][x]:
                    case 0 | 4 | 8:
                        tablero[y][x] = 8
                    case 1 | 5 | 9:
                        tablero[y][x] = 9
                    case 2 | 6 | 10:
                        tablero[y][x] = 10
                    case 3 | 7 | 11:
                        tablero[y][x] = 11
                        
        return verificarCasilla(y, x)
    
    else:
            return False
    

def empezarJuego(nJ):
    generarTablero()
    pintarTablero()

    while victoria == 0:

        valido = False
        while valido == False:
            print("\n\t▀▄█ Donuts negros █▄▀")
            y = int(input("\n\tCasilla vertical: ")) - 1
            x = int(input("\tCasilla horizontal: ")) - 1
            valido = colocar(1, y, x)
            if valido == True:
                pintarTablero()
            else:
                print("\n\tCasilla no válida.")

        valido = False
        if nJ == 1:
            while valido == False:
                valido = colocar(3, 0, 0)
                if valido == True:
                    print("\n\tøøø Turno IA øøø")
                    pintarTablero()
        else:
            while valido == False:
                print("\n\t░▒▓ Donuts blancos ▓▒░")
                y = int(input("\tCasilla vertical: ")) - 1
                x = int(input("\n\tCasilla horizontal: ")) - 1
                valido = colocar(2, y, x)
                if valido == True:
                    pintarTablero()
                else:
                    print("\n\tCasilla no válida.")

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