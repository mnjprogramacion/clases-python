from random import randrange

class Donuts:
    def __init__(self):
        self.tablero = []
        self.jugadaAnterior = None
        self.victoria = 0

    def generarTablero(self):
        # Genera un array con números del 0 al 3, cada uno corresponde con una dirección
        self.tablero = [[randrange(0, 4) for _ in range(6)] for _ in range(6)]

    def pintarTablero(self):
        # Pinta el tablero con diseño ASCII, según el array generado
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

    def movimientosValidos(self):
        """
        Devuelve una lista de posiciones válidas para colocar un donut, siguiendo el orden de prioridades:
        - Casillas contiguas
        - Línea de casillas desde borde
        - Libertad total
        """
        if self.jugadaAnterior is None:
            # Primera jugada: cualquier casilla libre
            return [(y, x) for y in range(6) for x in range(6) if self.tablero[y][x] in (0,1,2,3)]

        y0, x0 = self.jugadaAnterior
        valor_anterior = self.tablero[y0][x0] % 4
        direcciones = {
            0: [(-1,0),(1,0)],       # vertical
            1: [(0,-1),(0,1)],       # horizontal
            2: [(-1,1),(1,-1)],      # diagonal /
            3: [(-1,-1),(1,1)]       # diagonal \
        }

        # Comprobación de casillas vacías
        def es_libre(y, x):
            return 0 <= y < 6 and 0 <= x < 6 and self.tablero[y][x] in (0,1,2,3)

        dir1, dir2 = direcciones[valor_anterior]

        # Comprueba las casillas contiguas
        n1 = (y0 + dir1[0], x0 + dir1[1])
        n2 = (y0 + dir2[0], x0 + dir2[1])

        libre1 = es_libre(*n1)
        libre2 = es_libre(*n2)

        # 1. casillas contiguas
        if libre1 and libre2:
            return [n1, n2]

        # 2. linea desde borde
        linea = []

        # Dirección 1
        dy, dx = dir1
        ny, nx = y0 + dy, x0 + dx
        while 0 <= ny < 6 and 0 <= nx < 6:
            if self.tablero[ny][nx] in (0,1,2,3):
                linea.append((ny, nx))
            ny += dy
            nx += dx

        # Dirección 2
        dy, dx = dir2
        ny, nx = y0 + dy, x0 + dx
        while 0 <= ny < 6 and 0 <= nx < 6:
            if self.tablero[ny][nx] in (0,1,2,3):
                linea.append((ny, nx))
            ny += dy
            nx += dx

        if linea:
            return linea

        # 3. Libertad total
        return [(y, x) for y in range(6) for x in range(6) if self.tablero[y][x] in (0,1,2,3)]

    def verificarCasilla(self, y, x):
        # Devuelve True si la jugada (y,x) es válida según el orden de prioridades.
        return (y, x) in self.movimientosValidos()

    def colocar(self, n, y, x):
        # Comprobación contigua
        if not (0 <= x < 6 and 0 <= y < 6):
            return False

        # Comprobación casilla vacía
        if self.tablero[y][x] not in (0,1,2,3):
            return False

        # Si es la primera jugada, cualquier casilla es válida
        if self.jugadaAnterior is None:
            permitir = True
        else:
            validas = self.movimientosValidos()
            permitir = (y, x) in validas

        if not permitir:
            return False

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

    def verificarVictoria(self):
        self.victoria = 0
        # vertical, horizontal, diagonal \, diagonal /
        direcciones = [(1,0), (0,1), (1,1), (1,-1)]
        for y in range(6):
            for x in range(6):
                val = self.tablero[y][x]
                if val not in (4,5,6,7,8,9,10,11):
                    continue
                jugador = 1 if val in (4,5,6,7) else 2
                grupo = (4,5,6,7) if jugador == 1 else (8,9,10,11)
                for dy, dx in direcciones:
                    contador = 1
                    ny, nx = y + dy, x + dx
                    while 0 <= ny < 6 and 0 <= nx < 6 and self.tablero[ny][nx] in grupo:
                        contador += 1
                        ny += dy
                        nx += dx
                    if contador >= 5:
                        self.victoria = jugador
                        return

    def tableroLleno(self):
        # Detecta si al tablero no le queda ninguna casilla vacía
        return all(celda not in (0, 1, 2, 3) for fila in self.tablero for celda in fila)

    def capturarFichas(self, jugador, y, x):
        pares_direcciones = [
            [(-1, 0), (1, 0)],       # vertical
            [(0, -1), (0, 1)],       # horizontal
            [(-1, -1), (1, 1)],      # diagonal \
            [(1, -1), (-1, 1)]       # diagonal /
        ]

        if jugador == 1:
            rival = (8, 9, 10, 11)
        else:
            rival = (4, 5, 6, 7)

        for (dy1, dx1), (dy2, dx2) in pares_direcciones:
            ny1, nx1 = y + dy1, x + dx1
            ny2, nx2 = y + dy2, x + dx2
            
            if (0 <= ny1 < 6 and 0 <= nx1 < 6 and self.tablero[ny1][nx1] in rival and
                0 <= ny2 < 6 and 0 <= nx2 < 6 and self.tablero[ny2][nx2] in rival):
                
                for cy, cx in [(ny1, nx1), (ny2, nx2)]:
                    forma = self.tablero[cy][cx] % 4
                    if jugador == 1:
                        self.tablero[cy][cx] = 4 + forma
                    else:
                        self.tablero[cy][cx] = 8 + forma

    def empezarJuego(self, nJ):
        self.victoria = 0
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
                    self.capturarFichas(1, y, x)
                    self.pintarTablero()
                else:
                    print("\n\tCasilla no válida.")
            valido = False
            if nJ == 1:
                validas = self.movimientosValidos()
                if validas:
                    y, x = validas[randrange(len(validas))]
                    self.colocar(2, y, x)
                    self.jugadaAnterior = (y, x)
                    self.capturarFichas(2, y, x)
                    print("\n\t░▒▓ Donuts blancos (IA) ▓▒░")
                    self.pintarTablero()
                else:
                    print("\n\t¡Empate!")
                    break
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
                        self.capturarFichas(2, y, x)
                        self.pintarTablero()
                    else:
                        print("\n\tCasilla no válida.")
            self.verificarVictoria()

            if self.tableroLleno():
                print("\n\t¡Empate!")
                break
        if self.victoria == 1:
            print("\n¡Ganan los donuts negros!")
        if self.victoria == 2:
            print("\n¡Ganan los donuts blancos!")



class Menu:
    def __init__(self):
        self.sel = 0
        self.juego = Donuts()
    def iniciar(self):
        while not (self.sel == 4):
            print("\n\t░▒▓╔══════╗▓▒░\n\t░▒▓║DONUTS║▓▒░\n\t░▒▓╚══════╝▓▒░")
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
                    print("\n\tDonuts es un juego similar al 3 en raya.")
                    print("\tDebes colocar 5 donuts consecutivos en una línea antes que tu oponente.")
                    print("\n\tSe genera un tablero nuevo aleatorio cada partida.")
                    print("\tSolo puedes colocar tu donut en las casillas contiguas la última casilla ocupada por tu oponente, en la dirección marcada por la línea.")
                    print("\t│ = arriba o abajo   ─ = izquierda o derecha   / = arriba a la derecha o abajo a la izquierda   \\ = arriba a la izquierda o abajo a la derecha")
                    print("\n\tSi una o las dos posibles casillas están bloqueadas, el siguiente jugador puede colocar en toda la línea de casillas indicada por la línea.")
                    print("\tSi ninguna de las dos opciones anteriores es posible, el jugador puede colocar su donut donde quiera.")
                    print("\n\tSi rodeas los donuts de tu contrincante en línea recta, pasan a ser tuyos.")
                    print("\n\tPuedes jugar contra la IA o contra un amigo.")
                case 4:
                    print("\n\tSaliendo del programa...")
                case _:
                    print("\n\tERROR: opción no válida.")

Menu().iniciar()