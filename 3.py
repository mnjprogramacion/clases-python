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

    def verificarContiguas(self, y, x):
        """Devuelve True si (y,x) es contigua a la última ficha según la dirección de la casilla."""
        if self.jugadaAnterior is None:
            return True  # Primera jugada

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
        """Devuelve True si (y,x) está en la línea libre de un borde según la dirección de la última ficha."""
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

        # las dos direcciones
        dir1, dir2 = direcciones[valor_anterior]

        # función auxiliar: recorre desde (y0,x0) en direction (dy,dx) y busca (y,x) entre casillas vacías
        def recorrer(dy, dx):
            ny, nx = y0 + dy, x0 + dx
            while 0 <= ny < 6 and 0 <= nx < 6:
                if self.tablero[ny][nx] in (0,1,2,3):
                    if (ny, nx) == (y, x):
                        return True
                ny += dy
                nx += dx
            return False

        # Si dir1 está bloqueada, la línea libre es dir2 (recorremos dir2).
        dy1, dx1 = dir1
        dy2, dx2 = dir2
        bloqueada1 = not (0 <= y0 + dy1 < 6 and 0 <= x0 + dx1 < 6)
        bloqueada2 = not (0 <= y0 + dy2 < 6 and 0 <= x0 + dx2 < 6)

        if bloqueada1 and not bloqueada2:
            return recorrer(dy2, dx2)
        if bloqueada2 and not bloqueada1:
            return recorrer(dy1, dx1)

        # Si ninguna está bloqueada o ambas están bloqueadas (esquina muy rara), no aplica "línea de borde"
        return False



    def verificarCasilla(self, y, x):
        """
        Devuelve True si la jugada (y,x) es válida según el orden de prioridades:
        1️⃣ Contiguas
        2️⃣ Línea de borde
        3️⃣ Libertad total se maneja en movimientosValidos()
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

        # 1️⃣ Contiguas
        for y in range(6):
            for x in range(6):
                if self.verificarContiguas(y,x):
                    posiciones.append((y,x))
        if posiciones:
            return posiciones

        # 2️⃣ Línea de borde
        for y in range(6):
            for x in range(6):
                if self.verificarLineaBorde(y,x):
                    posiciones.append((y,x))
        if posiciones:
            return posiciones

        # 3️⃣ Libertad total
        for y in range(6):
            for x in range(6):
                if self.tablero[y][x] in (0,1,2,3):
                    posiciones.append((y,x))

        return posiciones


    def colocar(self, n, y, x):
        # Comprobaciones de frontera
        if not (0 <= x < 6 and 0 <= y < 6):
            return False

        # La casilla debe estar vacía siempre
        if self.tablero[y][x] not in (0,1,2,3):
            return False

        # Si es la primera jugada, cualquier casilla vacía es válida
        if self.jugadaAnterior is None:
            permitir = True
        else:
            # Obtener la lista oficial de movimientos válidos (respeta prioridades)
            validas = self.movimientosValidos()
            # Si no hay movimientos válidos, validas será [] (tablero lleno → empate)
            # pero normalmente se pasa por aqui porque antes se comprueba validas al llamar IA.
            permitir = (y, x) in validas

        if not permitir:
            return False

        # Colocar la ficha según la forma original de la casilla
        match self.tablero[y][x]:
            case 0 | 4 | 8:
                self.tablero[y][x] = 4
            case 1 | 5 | 9:
                self.tablero[y][x] = 5
            case 2 | 6 | 10:
                self.tablero[y][x] = 6
            case 3 | 7 | 11:
                self.tablero[y][x] = 7
        # Si es jugador 2 (IA) añade +4 (manteniendo la semántica de tu código)
        if n == 2:
            self.tablero[y][x] += 4

        return True
    

    def verificarVictoria(self):
        """
        Busca en todo el tablero si existe una línea de 5 (o más) consecutivas
        de donuts negros (4..7) o blancos (8..11). Si encuentra, pone self.victoria
        en 1 o 2 y devuelve.
        """
        self.victoria = 0

        # funciones helper para comprobar si una celda pertenece a jugador 1 o 2
        def es_negro(val):
            return val in (4,5,6,7)
        def es_blanco(val):
            return val in (8,9,10,11)

        # direcciones: vertical, horizontal, diagonal \, diagonal /
        direcciones = [(1,0), (0,1), (1,1), (1,-1)]

        for y in range(6):
            for x in range(6):
                val = self.tablero[y][x]
                if not (es_negro(val) or es_blanco(val)):
                    continue

                # determinar a qué jugador pertenece esta celda
                es_j1 = es_negro(val)
                # recorrer 4 direcciones desde esta celda
                for dy, dx in direcciones:
                    contador = 1
                    ny, nx = y + dy, x + dx
                    while 0 <= ny < 6 and 0 <= nx < 6:
                        nv = self.tablero[ny][nx]
                        if es_j1 and es_negro(nv):
                            contador += 1
                        elif (not es_j1) and es_blanco(nv):
                            contador += 1
                        else:
                            break
                        ny += dy
                        nx += dx

                    # si contamos 5 o más → victoria
                    if contador >= 5:
                        self.victoria = 1 if es_j1 else 2
                        return
        # si no encuentra nada, self.victoria queda en 0


    def tableroLleno(self):
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