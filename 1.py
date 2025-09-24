class Fraccion:

    def __init__(self,num,den):
        self.numerador=num
        self.denominador=den
        if self.denominador == 0 :
            raise ZeroDivisionError("Denominator cannot be zero.")
    
    def __repr__(self):
        return str(self.numerador) + '/' + str(self.denominador)

    def __eq__(self, fraccionb) :
        return (self.numerador == fraccionb.numerador and
        self.denominador == fraccionb.denominador)
    
    

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