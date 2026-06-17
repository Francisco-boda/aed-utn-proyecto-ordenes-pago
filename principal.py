import os.path
import clase
import pickle


def add_in_order(v, desti0):
    n = len(v)
    pos = n
    izq, der = 0, n - 1
    while izq <= der:
        c = (izq + der) // 2
        if v[c].identificacion_destinatario == desti0.identificacion_destinatario:
            pos = c
            break
        if v[c].identificacion_destinatario > desti0.identificacion_destinatario:
            izq = c + 1
        else:
            der = c - 1

    if izq > der:
        pos = izq
    v[pos:pos] = [desti0]


def cargar_envios():
    v = []
    m = open("envios.csv", encoding='UTF-8')

    for linea in m:
        linea = linea.rstrip("\n\r")
        linea = linea + "\n"
        if linea != "" and linea[-1] == ",":
            linea += "0"
        p = clase.generar_envio(linea)

        monto_base, comision = calcular_comision(p.algoritmo_comision, p.monto_nominal)
        monto_final = calcular_imp(p.algoritmo_impositivo, monto_base)
        p.comision = comision
        p.monto_final = monto_final
        p.moneda_origen = p.obtener_codigo_moneda_origen()
        p.moneda_pago = p.obtener_codigo_moneda_destino()
        add_in_order(v, p)
    m.close()
    i = int(input('Ingrese un valor i: '))
    if 0 <= i < len(v):
        print('r1.1:', v[i].obtener_identificador_pago())
    else:
        print('r1.1:', v[-1].obtener_identificador_pago())

    if i % 2 == 1:
        indice = 3 * i + 1
    else:
        indice = i // 2
    if 0 <= indice < len(v):
        print('r1.2: ', v[indice].obtener_identificador_pago())
    else:
        print('r1.2: ', v[-1].obtener_identificador_pago())
    return v



def calcular_comision(alg, monto):
    comision,monto_base = 0,0


    if alg == 1:#ARS
        comision = monto * 0.09
        monto_base = monto - comision

    elif alg == 2:#USD
        if monto < 0:
            comision = 0
        elif 50000 <= monto < 80000:
            comision = monto * 0.05
        elif monto >= 80000:
            comision = monto * 0.078
        monto_base = monto - comision

    elif alg == 3:#EUR/GBP
        if monto > 25000:
            comision = monto * 0.06
        monto_base = monto - (100 + comision)

    elif alg == 4:#JPY
        if monto <= 100000:
            comision = 500
        elif monto > 100000:
            comision = 1000
        monto_base = monto - comision

    elif alg == 5:#ARS
        if monto < 500000:
            comision = 0
        elif monto >= 500000:
            comision = monto *0.07

        if comision > 50000:
            comision = 50000

        monto_base = monto - comision

    return monto_base, comision


def calcular_imp(alg,monto_base):
    impuesto = 0
    monto_final = monto_base

    if alg == 1:
        if monto_base <= 300000:
            impuesto = 0
        elif monto_base > 300000:
            exc = monto_base-300000
            impuesto = exc * 0.25
        monto_final = monto_base - impuesto

    elif alg == 2:
        if monto_base < 50000:
            impuesto = 50
        elif monto_base >= 50000:
            impuesto = 100
        monto_final = monto_base - impuesto

    elif alg == 3:
        impuesto = monto_base * 0.03
        monto_final = monto_base - impuesto

    return monto_final


def generar_archivo(v):
    monedas = []
    promedios = []
    seleccionados = []
    m = open('archivo.dat', 'wb')

    for i in v:
        if i.moneda_origen not in monedas:
            monedas.append(i.moneda_origen)

    for i in monedas:
        a = c = 0
        for j in v:
            if j.moneda_origen == i:
                a += j.comision
                c += 1
        if c != 0:
            promedio = a / c
            promedios.append(promedio)

    for i in v:
        for j in range(len(monedas)):
            if i.moneda_origen == monedas[j]:
                if i.comision > promedios[j]:
                    seleccionados.append(i)
                break

    for i in seleccionados:
        pickle.dump(i, m)

    m.close()


def mostrar_envios():
    t = os.path.getsize('archivo.dat')
    m = open('archivo.dat', 'rb')

    while m.tell() < t:
        r = pickle.load(m)
        print(r)

    m.close()


def buscar(v):
    n = len(v)
    izq, der, pos = 0, n-1, -1
    iden = str(input('Ingrese el numero de identificador:').strip().upper())

    while izq <= der and pos == -1:
        mid = (izq + der) // 2
        if v[mid].identificacion_destinatario == iden:
            pos = mid
            break

        if v[mid].identificacion_destinatario < iden:
            der = mid - 1
        else:
            izq = mid + 1
    if pos == -1:
        print("r3.1:", 0)
        print("r3.2:", 0)
        return

    mi = v[pos].monto_nominal
    mf = mi * 1.17
    r = mf % 100
    if r >= 50:
        mf = mf - r + 100
    else:
        mf = mf - r
    mf = int(mf)
    v[pos].monto_nominal = mf
    print("r3.1:", mi)
    print("r3.2:", mf)

    generar_archivo(v)


def crear_matriz(v):
    mon_origen = []
    mon_pago = []

    for i in v:
        if i.moneda_origen not in mon_origen:
            mon_origen.append(i.moneda_origen)
        if i.moneda_pago not in mon_pago:
            mon_pago.append(i.moneda_pago)

    mat = [[0]*(len(mon_pago)) for _ in range(len(mon_origen))]

    for e in v:
        ori = e.obtener_codigo_moneda_origen()
        des = e.obtener_codigo_moneda_destino()
        f = 0
        for x in range(len(mon_origen)):
            if mon_origen[x] == ori:
                f = x
                break
        c = 0
        for y in range(len(mon_pago)):
            if mon_pago[y] == des:
                c = y
                break

        if mat[f][c] == 0 or e.monto_final > mat[f][c].monto_final:
            mat[f][c] = e

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] != 0:
                print("r4.1:", mat[i][j].codigo)
            else:
                print("r4.1: ", 0)

    suma, cant = 0, 0
    for i in range(min(len(mon_origen), len(mon_pago))):
        if mat[i][i] != 0:
            suma += mat[i][i].monto_final
            cant += 1

    if cant > 0:
        prom = suma / cant
    else:
        prom = 0

    print("r4.2:", round(prom, 2))


def principal():
    v = []
    op = -1
    while op != 0:
        print("Menu de opciones")
        print("1. Cargar envios ")
        print("2. Mostrar listado")
        print("3. Buscar")
        print("4. Mayores")
        print("0. Salir")
        op = int(input("Ingrese opcion: "))
        if op == 1:
                v = cargar_envios()
        elif op == 2:
            if v:
                generar_archivo(v)
                mostrar_envios()
            else:
                print("El vector no fue cargado todavía...")
        elif op == 3:
            if v:
                buscar(v)
            else:
                print("El vector no fue cargado todavía...")
        elif op == 4:
            if v:
                crear_matriz(v)
            else:
                print("El vector no fue cargado todavía...")
        elif op == 0:
            print("El programa termino")



if __name__ == '__main__':
    principal()
