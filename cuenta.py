from tarjeta import *

class Cuenta:
    def __init__(self, titular, dni_titular, numero_tarjeta, saldo_inicial=0.0):
        self.titular = titular
        self.dni_titular = dni_titular
        self.tarjeta_debito = Tarjeta(numero_tarjeta, self)
        self.tarjetas_credito = []
        self.saldo = saldo_inicial

    def get_saldo(self):
        return self.saldo

    def get_deuda(self):
        total_deuda = 0.0
        for tarjeta in self.tarjetas_credito:
            total_deuda += tarjeta.get_deuda()
        return total_deuda

    def get_dni_titular(self):
        return self.dni_titular

    def has_tarjeta(self, numero):
        if self.tarjeta_debito.get_numero() == numero:
            return True
        for tarjeta in self.tarjetas_credito:
            if tarjeta.get_numero() == numero:
                return True
        return False


    def get_tarjeta(self, numero):
        if self.tarjeta_debito.get_numero() == numero:
            return self.tarjeta_debito
        for tarjeta in self.tarjetas_credito:
            if tarjeta.get_numero() == numero:
                return tarjeta
        raise ValueError("Tarjeta no encontrada")

    def agregar_tarjeta_credito(self, tipo, numero):
        if tipo == "dorada":
            tarjeta = TarjetaCreditoDorada(numero, self)
        elif tipo == "blanca":
            tarjeta = TarjetaCreditoBlanca(numero, self)
        else:
            raise ValueError("Tipo de tarjeta de crédito inválido")
        self.tarjetas_credito.append(tarjeta)
        return tarjeta

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            return True
        else:
            raise ValueError("Monto de depósito inválido")

    def retirar(self, monto):
        if 0 < monto <= self.saldo:
            self.saldo -= monto
            return
        else:
            raise ValueError("Fondos insuficientes o monto inválido")

