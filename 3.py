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

    def verificarContiguas(self, y, x):
        # Devuelve True si (y,x) es contigua a la última ficha según la dirección de la casilla
        if self.jugadaAnterior is None:
            return True

        y0, x0 = self.jugadaAnterior
        valor_anterior = self.tablero[y0][x0] % 4
        direcciones = {
            0: [(-1,0),(1,0)],       # vertical
            1: [(0,-1),(0,1)],       # horizontal
            2: [(-1,1),(1,-1)],      # diagonal /
            3: [(-1,-1),(1,1)]       # diagonal \
        }

        for dy, dx in direcciones[valor_anterior]:
            ny, nx = y0 + dy, x0 + dx
            if 0 <= ny < 6 and 0 <= nx < 6 and self.tablero[ny][nx] in (0,1,2,3):
                if (ny, nx) == (y, x):
                    return True
        return False

    def verificarLineaBorde(self, y, x):
        # Devuelve True si (y,x) está en la línea libre de un borde según la dirección de la última ficha
        if self.jugadaAnterior is None:
            return False

        y0, x0 = self.jugadaAnterior
        valor_anterior = self.tablero[y0][x0] % 4
        direcciones = {
            0: [(-1,0),(1,0)],
            1: [(0,-1),(0,1)],
            2: [(-1,1),(1,-1)],
            3: [(-1,-1),(1,1)]
        }

        dir1, dir2 = direcciones[valor_anterior]

        def recorrer(dy, dx):
            ny, nx = y0 + dy, x0 + dx
            while 0 <= ny < 6 and 0 <= nx < 6:
                if self.tablero[ny][nx] in (0,1,2,3):
                    if (ny, nx) == (y, x):
                        return True
                ny += dy
                nx += dx
            return False

        dy1, dx1 = dir1
        dy2, dx2 = dir2
        bloqueada1 = not (0 <= y0 + dy1 < 6 and 0 <= x0 + dx1 < 6)
        bloqueada2 = not (0 <= y0 + dy2 < 6 and 0 <= x0 + dx2 < 6)

        if bloqueada1 and not bloqueada2:
            return recorrer(dy2, dx2)
        if bloqueada2 and not bloqueada1:
            return recorrer(dy1, dx1)

        return False

    def verificarCasilla(self, y, x):
        """
        Devuelve True si la jugada (y,x) es válida según el orden de prioridades:
        - Casillas contiguas
        - Línea de casillas desde borde
        - Libertad total
        """
        if self.tablero[y][x] not in (0,1,2,3):
            return False
        if self.verificarContiguas(y,x):
            return True
        if self.verificarLineaBorde(y,x):
            return True
        return False

    def movimientosValidos(self):
        posiciones = []

        # Contiguas
        for y in range(6):
            for x in range(6):
                if self.verificarContiguas(y,x):
                    posiciones.append((y,x))
        if posiciones:
            return posiciones

        # Línea desde borde
        for y in range(6):
            for x in range(6):
                if self.verificarLineaBorde(y,x):
                    posiciones.append((y,x))
        if posiciones:
            return posiciones

        # Libertad total
        for y in range(6):
            for x in range(6):
                if self.tablero[y][x] in (0,1,2,3):
                    posiciones.append((y,x))

        return posiciones

    def colocar(self, n, y, x):
        # Comprobación contigua
        if not (0 <= x < 6 and 0 <= y < 6):
            return False

        # Comprobación casilla vaía
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

        def det_negro(val):
            return val in (4,5,6,7)
        def det_blanco(val):
            return val in (8,9,10,11)

        # vertical, horizontal, diagonal \, diagonal /
        direcciones = [(1,0), (0,1), (1,1), (1,-1)]

        for y in range(6):
            for x in range(6):
                val = self.tablero[y][x]
                if not (det_negro(val) or det_blanco(val)):
                    continue

                # determinar a qué jugador pertenece esta celda
                es_j1 = det_negro(val)

                for dy, dx in direcciones:
                    contador = 1
                    ny, nx = y + dy, x + dx
                    while 0 <= ny < 6 and 0 <= nx < 6:
                        nv = self.tablero[ny][nx]
                        if es_j1 and det_negro(nv):
                            contador += 1
                        elif (not es_j1) and det_blanco(nv):
                            contador += 1
                        else:
                            break
                        ny += dy
                        nx += dx

                    if contador >= 5:
                        self.victoria = 1 if es_j1 else 2
                        return

    def tableroLleno(self):
        # Detecta si al tablero no le queda ninguna casilla vacía
        return all(celda not in (0, 1, 2, 3) for fila in self.tablero for celda in fila)

    def capturarFichas(self, jugador, y, x):
        direcciones = [
            (-1, 0), (1, 0),       # vertical
            (0, -1), (0, 1),       # horizontal
            (-1, -1), (-1, 1),     # diagonales
            (1, -1), (1, 1)
        ]

        if jugador == 1:
            propio = (4, 5, 6, 7)
            rival = (8, 9, 10, 11)
        else:
            propio = (8, 9, 10, 11)
            rival = (4, 5, 6, 7)

        for dy, dx in direcciones:
            ny, nx = y + dy, x + dx
            fichas_capturadas = []

            while 0 <= ny < 6 and 0 <= nx < 6 and self.tablero[ny][nx] in rival:
                fichas_capturadas.append((ny, nx))
                ny += dy
                nx += dx

            if 0 <= ny < 6 and 0 <= nx < 6 and self.tablero[ny][nx] in propio and len(fichas_capturadas) > 0:
                for cy, cx in fichas_capturadas:
                    forma = self.tablero[cy][cx] % 4
                    if jugador == 1:
                        self.tablero[cy][cx] = 4 + forma
                    else:
                        self.tablero[cy][cx] = 8 + forma

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
                    print("\n\tSi colocas dos donuts a los lados de tu contrincante, su ficha pasa a ser tuya.")
                    print("\tSi un jugador coloca un donut en un borde del tablero, el contrincante puede colocar su donut en toda la línea de casillas que indica la dirección, sin ser contigua.")
                    print("\n\tPuedes jugar contra la IA o contra un amigo.")
                case 4:
                    print("\n\tSaliendo del programa...")
                case _:
                    print("\n\tERROR: opción no válida.")

Menu().iniciar()