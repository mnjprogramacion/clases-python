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

    def __eq__(self, fraccionb):
        return (self.signo == fraccionb.signo and
                self.numerador == fraccionb.numerador and
                self.denominador == fraccionb.denominador)

    def __add__(self, fraccionb):
        num1 = self.signo * self.numerador
        num2 = fraccionb.signo * fraccionb.numerador
        nuevo_num = num1 * fraccionb.denominador + num2 * self.denominador
        nuevo_den = self.denominador * fraccionb.denominador
        return Fraccion(nuevo_num, nuevo_den)

    def __lt__(self, fraccionb):
        return (self.signo * self.numerador * fraccionb.denominador <
                fraccionb.signo * fraccionb.numerador * self.denominador)

    def __le__(self, fraccionb):
        return self < fraccionb or self == fraccionb

    def __gt__(self, fraccionb):
        return not (self <= fraccionb)

    def __ge__(self, fraccionb):
        return not (self < fraccionb)

class FraccionEnt(Fraccion):

    def __init__(self,num,den,ent):
        super().__init__(num,den)
        pentera=ent

x=Fraccion(1,2)
print(x.numerador)

x1=Fraccion(1,2)
y=FraccionEnt(1,2,3)
#print(y.pentera)
if x == y:
    print("Son iguales")
else: 
    print("Son diferentes")
print(x)