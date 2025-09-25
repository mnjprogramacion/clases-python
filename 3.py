from random import randrange

tablero = []

print("\n╔══════╗\n║DONUTS║\n╚══════╝")

def generarTablero():
    tablero = [[randrange(0, 4) for _ in range(6)] for _ in range(6)]
    return tablero

def pintarTablero(tablero):
    print("\n╔══════╗")
    for row in tablero:
        linea = "║"
        for cell in row:
            if cell == 0:
                linea += "│"
            elif cell == 1:
                linea += "─"
            elif cell == 2:
                linea += "/"
            elif cell == 3:
                linea += "\\"
            elif (cell == 4) or (cell == 5) or (cell == 6) or (cell == 7):
                linea += "×"
            elif (cell == 8) or (cell == 9) or (cell == 10) or (cell == 11):
                linea += "○"
            else:
                linea += "░"
        linea += "║"
        print(linea)
    print("╚══════╝")

tablero = generarTablero()
pintarTablero(tablero)