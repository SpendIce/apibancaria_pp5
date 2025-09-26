class Banco:
    def __init__(self):
        self.cuentas = []

    def adicionar_cliente(self, cuenta):
        self.cuentas.append(cuenta)

    def remover_cliente(self, cuenta):
        if cuenta in self.cuentas:
            self.cuentas.remove(cuenta)

    def buscar_cliente(self, dni):
        for cuenta in self.cuentas:
            if cuenta.get_dni_titular() == dni:
                return cuenta
            else:
                raise IndexError("Cliente no encontrado")

    def consumir(self, tarjeta, monto):
        for cuenta in self.cuentas:
            if cuenta.has_tarjeta(tarjeta):
                cuenta.get_tarjeta(tarjeta).pagar(monto)
                print("Pago realizado con éxito")
                return
        print("Tarjeta no encontrada en el banco")

    def consultar_saldo(self, dni):
        cuenta = self.buscar_cliente(dni)
        return cuenta.get_saldo()

    def consultar_deuda(self, dni):
        cuenta = self.buscar_cliente(dni)
        return cuenta.get_deuda()

    def mejor_cliente(self):
        if not self.cuentas:
            return None
        mejor = max(self.cuentas, key=lambda cuenta: cuenta.get_deuda())
        return mejor.get_dni_titular()