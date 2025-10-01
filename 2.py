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


lista = ListaDeFiguras()

t = TrianguloRectangulo(3, 4)
r = Rectangulo(2, 5)

print(t.hipotenusa())
print(t.superficie())
print(r.superficie())

lista.añadir_triangulo(3, 4)
lista.añadir_cuadrado(4)

print(lista.superficie_total())
print(lista.contar_triangulos())