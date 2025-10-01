from math import gcd

class Fraccion:

    def __init__(self, num, den):
        self.numerador = num
        self.denominador = den
        if self.denominador == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        self.signo = -1 if self.numerador * self.denominador < 0 else 1

        self.numerador, self.denominador = abs(self.numerador), abs(self.denominador)

        divisor = gcd(self.numerador, self.denominador)
        self.numerador //= divisor
        self.denominador //= divisor

    def __repr__(self):
        signo_str = "-" if self.signo < 0 else ""
        return signo_str + str(self.numerador) + '/' + str(self.denominador)

    def __eq__(self, fb):
        return (self.signo == fb.signo and
                self.numerador == fb.numerador and
                self.denominador == fb.denominador)

    def __add__(self, fb):
        num1 = self.signo * self.numerador
        num2 = fb.signo * fb.numerador
        nuevo_num = num1 * fb.denominador + num2 * self.denominador
        nuevo_den = self.denominador * fb.denominador
        return Fraccion(nuevo_num, nuevo_den)

    def __lt__(self, fb):
        return (self.signo * self.numerador * fb.denominador <
                fb.signo * fb.numerador * self.denominador)

    def __le__(self, fb):
        return self < fb or self == fb

    def __gt__(self, fb):
        return not (self <= fb)

    def __ge__(self, fb):
        return not (self < fb)

class FraccionEnt(Fraccion):

    def __init__(self,num,den,ent):
        super().__init__(num,den)
        pentera=ent

x=Fraccion(1,2)
print(x.numerador)


f1 = Fraccion(2, 4)
f2 = Fraccion(1, 2)
f3 = Fraccion(3, 4)

print(f1)
print(f1 == f2)
print(f1 + f3)
print(f1 < f3)
print(f1 <= f2)
print(f3 > f1)
print(f2 >= f1)