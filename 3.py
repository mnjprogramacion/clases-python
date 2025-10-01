from random import randrange

class Donuts:
    def __init__(self):
        self.tablero = []
        self.jugadaAnterior = None
        self.victoria = 0

    def generarTablero(self):
        self.tablero = [[randrange(0, 4) for _ in range(6)] for _ in range(6)]

    def pintarTablero(self):
        n = 1
        print("\n\t    1 2 3 4 5 6")
        print("\t  ╔═════════════╗")
        for row in self.tablero:
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

        if self.jugadaAnterior != None:
            match self.tablero[self.jugadaAnterior[0]][self.jugadaAnterior[1]]:
                case 0 | 4 | 8:
                    casilla = "│"
                case 1 | 5 | 9:
                    casilla = "─"
                case 2 | 6 | 10:
                    casilla = "/"
                case 3 | 7 | 11:
                    casilla = "\\"

            print(f"\n\tÚltima casilla: {casilla} ({self.jugadaAnterior[0]+1}, {self.jugadaAnterior[1]+1})")

    def verificarCasilla(self, y, x):
        dy = y - self.jugadaAnterior[0]
        dx = x - self.jugadaAnterior[1]
        valor_anterior = self.tablero[self.jugadaAnterior[0]][self.jugadaAnterior[1]] % 4
        direcciones = {
            0: [(-1,0), (1,0)],
            1: [(0,-1), (0,1)],
            2: [(-1,1), (1,-1)],
            3: [(-1,-1), (1,1)]
        }
        return (dy, dx) in direcciones[valor_anterior]

    def colocar(self, n, y, x):
        permitir = False
        if (x >= 0) and (x < 6) and (y >= 0) and (y < 6):
            if self.jugadaAnterior == None:
                permitir = True
            else:
                permitir = self.verificarCasilla(y, x)
            if permitir == True:
                match self.tablero[y][x]:
                    case 0 | 4 | 8:
                        self.tablero[y][x] = 4
                    case 1 | 5 | 9:
                        self.tablero[y][x] = 5
                    case 2 | 6 | 10:
                        self.tablero[y][x] = 6
                    case 3 | 7 | 11:
                        self.tablero[y][x] = 7
                if n == 2:
                    self.tablero[y][x] += 4
                return True
            else:
                return False
        else:
            return False

    def verificarVictoria(self):
        self.victoria = 0
        y, x = self.jugadaAnterior
        cell = self.tablero[y][x]
        if cell in (4, 5, 6, 7):
            cellVal = (4, 5, 6, 7)
            ganador = 1
        elif cell in (8, 9, 10, 11):
            cellVal = (8, 9, 10, 11)
            ganador = 2
        else:
            return
        direcciones = [
            (-1, 0), (0, -1), (-1, 1), (-1, -1)
        ]
        for dy, dx in direcciones:
            contador = 1
            ny, nx = y + dy, x + dx
            while 0 <= ny < 6 and 0 <= nx < 6 and self.tablero[ny][nx] in cellVal:
                contador += 1
                ny += dy
                nx += dx
            ny, nx = y - dy, x - dx
            while 0 <= ny < 6 and 0 <= nx < 6 and self.tablero[ny][nx] in cellVal:
                contador += 1
                ny -= dy
                nx -= dx
            if contador >= 5:
                self.victoria = ganador
                return

    def empezarJuego(self, nJ):
        self.jugadaAnterior = None
        self.generarTablero()
        self.pintarTablero()
        while self.victoria == 0:
            valido = False
            while valido == False:
                print("\n\t▀▄█ Donuts negros █▄▀")
                try:
                    y = int(input("\tCoordenada vertical: ")) - 1
                    x = int(input("\tCoordenada horizontal: ")) - 1
                except:
                    y = -1
                    x = -1
                if self.jugadaAnterior != None:
                    valido = self.colocar(1, y, x)
                else:
                    self.colocar(1, y, x)
                    valido = True
                if valido == True:
                    self.jugadaAnterior = (y, x)
                    self.pintarTablero()
                else:
                    print("\n\tCasilla no válida.")
            valido = False
            if nJ == 1:
                while valido == False:
                    y = randrange(0,3)
                    x = randrange(0,3)
                    valido = self.colocar(2, y, x)
                    if valido == True:
                        print("\n\t░▒▓ Donuts blancos (IA) ▓▒░")
                        self.jugadaAnterior = (y, x)
                        self.pintarTablero()
            else:
                while valido == False:
                    print("\n\t░▒▓ Donuts blancos ▓▒░")
                    try:
                        y = int(input("\tCoordenada vertical: ")) - 1
                        x = int(input("\tCoordenada horizontal: ")) - 1
                    except:
                        y = -1
                        x = -1
                    valido = self.colocar(2, y, x)
                    if valido == True:
                        self.jugadaAnterior = (y, x)
                        self.pintarTablero()
                    else:
                        print("\n\tCasilla no válida.")
            self.verificarVictoria()
        if self.victoria == 1:
            print("¡Ganan los donuts negros!")
        if self.victoria == 2:
            print("¡Ganan los donuts blancos!")

class Menu:
    def __init__(self):
        self.sel = 0
        self.juego = Donuts()
    def iniciar(self):
        print("\n\t░▒▓╔══════╗▓▒░\n\t░▒▓║DONUTS║▓▒░\n\t░▒▓╚══════╝▓▒░")
        while not ((self.sel == 1) or (self.sel == 2) or (self.sel == 3) or (self.sel == 4)):
            print("\n\t1. 1 jugador.")
            print("\t2. 2 jugadores.")
            print("\t3. Leer las reglas.")
            print("\t4. Salir.")
            try:
                self.sel = int(input("\n\tEscoge una opción: "))
            except:
                self.sel = 0
            match self.sel:
                case 1:
                    self.juego.empezarJuego(1)
                case 2:
                    self.juego.empezarJuego(2)
                case 3:
                    print("\n\tReglas")
                case 4:
                    print("\n\tSaliendo del programa...")
                case _:
                    print("\n\tERROR: opción no válida.")

Menu().iniciar()