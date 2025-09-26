import pytest
from cuenta import Cuenta

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

class TestCuenta:
    def test_init(self):
        cuenta = Cuenta("Pedro", "12345678A", "1234 5678 9012 3456", 1000)
        assert cuenta.titular == "Pedro"
        assert cuenta.get_dni_titular() == "12345678A"
        assert cuenta.get_saldo() == 1000
        assert cuenta.get_deuda() == 0.0
        assert cuenta.has_tarjeta("1234 5678 9012 3456") is True
        assert cuenta.tarjetas_credito == []

    def test_depositar(self):
        cuenta = Cuenta("Pedro", "12345678A", "1234 5678 9012 3456", 500)
        cuenta.depositar(300)
        assert cuenta.get_saldo() == 800
        with pytest.raises(ValueError):
            cuenta.depositar(-100)

    def test_retirar(self):
        cuenta = Cuenta("Pedro", "12345678A", "1234 5678 9012 3456", 1000)
        cuenta.retirar(400)
        assert cuenta.get_saldo() == 600
        with pytest.raises(ValueError):
            cuenta.retirar(700)
        with pytest.raises(ValueError):
            cuenta.retirar(-50)

    def test_add_tarjeta_and_has_tarjeta(self):
        cuenta = Cuenta("Pedro", "12345678A", "1234 5678 9012 3456", 1000)
        assert cuenta.has_tarjeta("5555 6666 7777 8888") is False

    def test_get_deuda_with_credit_cards(self):
        cuenta = Cuenta("Pedro", "12345678A", "1234 5678 9012 3456", 1000)
        tarjeta1 = MockTarjetaCredito("5555 6666 7777 8888", cuenta, deuda=200)
        cuenta.tarjetas_credito.append(tarjeta1)
        assert cuenta.get_deuda() == 200.0