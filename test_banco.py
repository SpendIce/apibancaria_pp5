import pytest
from banco import Banco

class MockCuenta:
    def __init__(self, dni, saldo=0):
        self.dni = dni
        self.saldo = saldo
        self.debito = MockTarjeta("1234 5678 9012 3456", self)
        self.tarjetas = []

    def get_dni_titular(self):
        return self.dni

    def get_saldo(self):
        return self.saldo

    def has_tarjeta(self, numero):
        if self.debito.get_numero() == numero:
            return True
        for tarjeta in self.tarjetas:
            if tarjeta.get_numero() == numero:
                return True
        return False

    def get_tarjeta(self, numero):
        if self.debito.get_numero() == numero:
            return self.debito
        for tarjeta in self.tarjetas:
            if tarjeta.get_numero() == numero:
                return tarjeta
        raise ValueError("Tarjeta no encontrada")

    def retirar(self, monto):
        if 0 < monto <= self.saldo:
            self.saldo -= monto
            return
        else:
            raise ValueError("Fondos insuficientes o monto inválido")

    def get_deuda(self):
        total_deuda = 0
        for tarjeta in self.tarjetas:
            total_deuda += tarjeta.get_deuda()
        return total_deuda

    def add_tarjeta(self, tarjeta):
        self.tarjetas.append(tarjeta)

class MockTarjeta:
    def __init__(self, numero, cuenta):
        self.numero = numero
        self.cuenta = cuenta

    def pagar(self, monto):
        self.cuenta.retirar(monto)

    def get_numero(self):
        return self.numero

class MockTarjetaCredito:
    def __init__(self, numero, cuenta, deuda=0):
        self.numero = numero
        self.cuenta = cuenta
        self.deuda = deuda

    def get_numero(self):
        return self.numero

    def get_deuda(self):
        return self.deuda

    def pagar(self, monto):
        self.deuda += monto

class TestBanco:
    def test_init(self):
        banco = Banco()
        assert banco.cuentas == []

    def test_adicionar_cliente(self):
        banco = Banco()
        cuenta = MockCuenta("12345678A")
        banco.adicionar_cliente(cuenta)
        assert cuenta in banco.cuentas

    def test_retirar_cliente(self):
        banco = Banco()
        cuenta = MockCuenta("12345678A")
        banco.adicionar_cliente(cuenta)
        banco.remover_cliente(cuenta)
        assert cuenta not in banco.cuentas

    def test_buscar_cliente(self):
        banco = Banco()
        cuenta = MockCuenta("12345678A")
        banco.adicionar_cliente(cuenta)
        assert banco.buscar_cliente("12345678A") == cuenta
        with pytest.raises(IndexError):
            banco.buscar_cliente("87654321B")

    def test_consumir(self):
        banco = Banco()
        cuenta = MockCuenta("38123456", saldo=1000)
        tarjeta_credito = MockTarjetaCredito("9012 3456 1234 5678", cuenta)
        cuenta.add_tarjeta(tarjeta_credito)
        banco.adicionar_cliente(cuenta)

        banco.consumir("1234 5678 9012 3456", 300)
        assert cuenta.get_saldo() == 700

        banco.consumir("9012 3456 1234 5678", 500)
        assert tarjeta_credito.get_deuda() == 500

        with pytest.raises(ValueError):
            banco.consumir("1234 5678 9012 3456", 1000)

    def test_consultar_saldo(self):
        banco = Banco()
        cuenta = MockCuenta("38123456", saldo=500)
        banco.adicionar_cliente(cuenta)
        assert banco.consultar_saldo("38123456") == 500

    def test_consultar_deuda(self):
        banco = Banco()
        cuenta = MockCuenta("38123456")
        tarjeta_credito = MockTarjetaCredito("9012 3456 1234 5678", cuenta, deuda=300)
        tarjeta_credito2 = MockTarjetaCredito("5678 1234 9012 3456", cuenta, deuda=200)
        cuenta.add_tarjeta(tarjeta_credito2)
        cuenta.add_tarjeta(tarjeta_credito)
        banco.adicionar_cliente(cuenta)
        assert banco.consultar_deuda("38123456") == 500

    def test_mejor_cliente(self):
        banco = Banco()
        cuenta1 = MockCuenta("38123456", saldo=500)
        tarjeta_credito = MockTarjetaCredito("5678 1234 9012 3456", cuenta1, deuda=200)
        cuenta1.add_tarjeta(tarjeta_credito)
        cuenta2 = MockCuenta("12345678", saldo=1500)
        banco.adicionar_cliente(cuenta1)
        banco.adicionar_cliente(cuenta2)
        assert banco.mejor_cliente() == "38123456"