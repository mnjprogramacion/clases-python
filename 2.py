import math

class FiguraGeometrica:
    def superficie(self):
        return 0

class TrianguloRectangulo(FiguraGeometrica):
    def __init__(self, cateto1, cateto2):
        self.cateto1 = cateto1
        self.cateto2 = cateto2

    def hipotenusa(self):
        return math.sqrt(self.cateto1**2 + self.cateto2**2)

    def superficie(self):
        return (self.cateto1 * self.cateto2) / 2


class Rectangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def superficie(self):
        return self.base * self.altura

class ListaDeFiguras:
    def __init__(self):
        self.figuras = []

    def añadir_triangulo(self, cateto1, cateto2):
        self.figuras.append(TrianguloRectangulo(cateto1, cateto2))

    def añadir_cuadrado(self, lado):
        self.figuras.append(Rectangulo(lado, lado))

    def superficie_total(self):
        return sum(figura.superficie() for figura in self.figuras)

    def contar_triangulos(self):
        return sum(isinstance(figura, TrianguloRectangulo) for figura in self.figuras)


# Ejemplo de uso
if __name__ == "__main__":
    lista = ListaDeFiguras()
    lista.añadir_triangulo(3, 4)  # triángulo rectángulo
    lista.añadir_cuadrado(5)      # cuadrado de lado 5
    lista.añadir_triangulo(6, 8)  # otro triángulo

    print("Superficie total:", lista.superficie_total())
    print("Número de triángulos:", lista.contar_triangulos())
