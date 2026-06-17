__author__ = "Cátedra de Algoritmos y Estructuras de Datos"


class Envio:
    def __init__(self, codigo, identificacion_destinatario,
                 nombre_destinatario, tasa, monto_nominal,
                 algoritmo_comision, algoritmo_impositivo):
        self.codigo = codigo
        self.identificacion_destinatario = identificacion_destinatario
        self.nombre_destinatario = nombre_destinatario
        self.tasa = tasa
        self.monto_nominal = monto_nominal
        self.algoritmo_comision = algoritmo_comision
        self.algoritmo_impositivo = algoritmo_impositivo

    def obtener_identificador_pago(self):
        identificador_pago = self.codigo.split("|")
        return identificador_pago[2]

    def obtener_codigo_moneda_origen(self):
        moneda_origen = self.codigo.split("|")
        return int(moneda_origen[0])

    def obtener_codigo_moneda_destino(self):
        moneda_destino = self.codigo.split("|")
        return int(moneda_destino[1])

    def __str__(self):
        return (
            f"Identificador de pago: {self.obtener_identificador_pago()} - Identificación: {self.identificacion_destinatario} -"
            f" Nombre: {self.nombre_destinatario} - Tasa: {self.tasa} - Monto nominal: {self.monto_nominal}")


def generar_envio(token):
    datos_base = token[:-1]
    datos_base = datos_base.split(",")
    codigo = datos_base[0]
    identificacion_destinatario = datos_base[1]
    nombre_destinatario = datos_base[2]
    tasa = float(datos_base[3])
    monto_nominal = int(datos_base[4])
    algoritmo_comision = int(datos_base[5])
    algoritmo_impositivo = int(datos_base[6])
    return Envio(codigo, identificacion_destinatario, nombre_destinatario, tasa, monto_nominal, algoritmo_comision,
                 algoritmo_impositivo)


if __name__ == "__main__":
    envio_base = "05|04|4616A0743D75FC8C,AF188371E36A,Shansa B. Alexis,1,11374056,4,2\n"
    envio = generar_envio(envio_base)
    print(envio)
    print(envio.obtener_identificador_pago())
    print(envio.obtener_codigo_moneda_origen())
    print(envio.obtener_codigo_moneda_destino())
