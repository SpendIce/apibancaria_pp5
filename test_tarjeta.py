import pytest
from tarjeta import *

class MockCuenta:
    def __init__(self, dni_titular, saldo=0.0):
        self.dni_titular = dni_titular
        self.saldo = saldo
        self.tarjetas = []
    def retirar(self, monto):
        if 0 < monto <= self.saldo:
            self.saldo -= monto
            return
        else:
            raise ValueError("Fondos insuficientes o monto inválido")

class TestTarjetaCreditoDorada:
    def test_init(self):
        tarjeta = TarjetaCreditoDorada("1111 2222 3333 4444", "cuenta")
        assert tarjeta.get_numero() == "1111 2222 3333 4444"
        assert tarjeta.get_deuda() == 0.0

    def test_pagar_y_pagar_deuda(self):
        cuenta = MockCuenta("12345678A", saldo=5000)
        tarjeta = TarjetaCreditoDorada("1111 2222 3333 4444", cuenta)
        tarjeta.pagar(2000)
        assert tarjeta.get_deuda() == 2000.0
        assert cuenta.saldo == 5000

        tarjeta.pagar_deuda(500)
        assert tarjeta.get_deuda() == 1500.0

    def test_pagar_deuda_invalid_amount(self):
        cuenta = MockCuenta("12345678A", saldo=5000)
        tarjeta = TarjetaCreditoDorada("1111 2222 3333 4444", cuenta)
        tarjeta.pagar(2000)
        with pytest.raises(ValueError):
            tarjeta.pagar_deuda(2500)
        with pytest.raises(ValueError):
            tarjeta.pagar_deuda(-100)

class TestTarjetaCreditoBlanca:
    def test_init(self):
        tarjeta = TarjetaCreditoBlanca("5555 6666 7777 8888", "cuenta")
        assert tarjeta.get_numero() == "5555 6666 7777 8888"
        assert tarjeta.get_deuda() == 0.0

    def test_pagar_within_limit(self):
        cuenta = MockCuenta("87654321B", saldo=3000)
        tarjeta = TarjetaCreditoBlanca("5555 6666 7777 8888", cuenta)
        tarjeta.pagar(8000)
        assert tarjeta.get_deuda() == 8000.0

    def test_pagar_exceeding_limit(self):
        cuenta = MockCuenta("87654321B", saldo=3000)
        tarjeta = TarjetaCreditoBlanca("5555 6666 7777 8888", cuenta)
        with pytest.raises(ValueError):
            tarjeta.pagar(12000)
        assert tarjeta.get_deuda() == 0.0

class TestTarjeta:
    def test_init(self):
        cuenta = MockCuenta("11223344C", saldo=2000)
        tarjeta = Tarjeta("9999 8888 7777 6666", cuenta)
        assert tarjeta.get_numero() == "9999 8888 7777 6666"
        assert tarjeta.cuenta == cuenta

    def test_pagar_below_3000(self):
        cuenta = MockCuenta("11223344C", saldo=3000)
        tarjeta = Tarjeta("9999 8888 7777 6666", cuenta)
        tarjeta.pagar(2500)
        assert cuenta.saldo == 3000 - 2500

    def test_pagar_above_3000(self):
        cuenta = MockCuenta("11223344C", saldo=5000)
        tarjeta = Tarjeta("9999 8888 7777 6666", cuenta)
        tarjeta.pagar(4000)
        assert cuenta.saldo == 5000 - (4000 * 0.79)

    def test_pagar_insufficient_funds(self):
        cuenta = MockCuenta("11223344C", saldo=1000)
        tarjeta = Tarjeta("9999 8888 7777 6666", cuenta)
        with pytest.raises(ValueError):
            tarjeta.pagar(1500)