class Tarjeta:
    def __init__(self, numero, cuenta):
        self.numero = numero
        self.cuenta = cuenta

    def get_numero(self):
        return self.numero

    def pagar(self, monto):
        if monto < 3000:
            self.cuenta.retirar(monto)
            return
        else:
            monto = monto * 0.79 # Descontar el 21% de IVA
            self.cuenta.retirar(monto)

class TarjetaCreditoDorada(Tarjeta):
    def __init__(self, numero, cuenta):
        super().__init__(numero, cuenta)
        self.deuda = 0.0

    def get_deuda(self):
        return self.deuda

    def pagar(self, monto):
        self.deuda += monto
        return

    def pagar_deuda(self, monto):
        if monto > 0 and monto <= self.deuda:
            self.deuda -= monto
            return
        else:
            raise ValueError("Monto inválido para pagar la deuda")

class TarjetaCreditoBlanca(TarjetaCreditoDorada):
    def __init__(self, numero, cuenta):
        super().__init__(numero, cuenta)
        self.limite_credito = 10000.0

    def pagar(self, monto):
        if self.deuda + monto <= self.limite_credito:
            self.deuda += monto
            return
        else:
            raise ValueError("Límite de crédito excedido")