from operator import length_hint
import PySimpleGUI as sg
from tkinter import messagebox
from models import Movimiento
from ventana_gasto import VentanaGasto
from ventana_ingreso import VentanaIngreso
from ventana_recomendaciones import VentanaRecomendaciones
import random
sg.theme('DarkGreen2') #Tema de la ventana
graphs = [sg.Graph((700,300), (-250, -250), (250,250), background_color="#1a1a1a") for x in range(4)]

top_pane = sg.Pane([
    sg.Col([[sg.VPush()], [sg.Text("M-Friend", font=("Times new roman", 24))], [sg.VPush()]], element_justification="c"),
], s=(850,50))

tabs = sg.TabGroup(tab_location="left", layout=[
    [
        sg.Tab("Gráfica \n Barras gastos    ", [
            [graphs[0]]
        ]),
        sg.Tab("Gráfica \n Barras ingreso   ", [
            [graphs[1]]
        ]),
        sg.Tab("Gráfica \n Scatter gastos   ", [
            [graphs[2]]
        ]),
        sg.Tab("Gráfica \n Scatter ingreso  ", [
            [graphs[3]]
        ]),

    ]
])

botonIngreso = "btn_ingreso"
botonGasto = "btn_gasto"
botonRecomendaciones = "btn_recomendaciones"

layout = [
    [top_pane],
    [tabs],
    [
        sg.Push(),
        sg.Button('Registrar Ingreso', key=botonIngreso),
        sg.Button('Registrar Gasto', key=botonGasto),
        sg.Push()
    ],
    [sg.Push(), sg.Button("Recomendaciones", key=botonRecomendaciones), sg.Push()]
]

# Ejemplo de uso de clase movimiento (esta información vendría de un archivo en la app final)
movimiento = Movimiento({
    "Monto": 23.5,
    "Fecha": "2022-04-09",
    "Tipo": "Gasto",
})
movimiento2 = Movimiento({
    "Monto": 23.5,
    "Fecha": "2022-04-09",
    "Tipo": "Gasto",
})
# print("# EJEMPLO DE USO DE CLASE MOVIMIENTO")
# monto = movimiento.ObtenerMonto()
# if monto.TieneValor():
#     print("El monto es:", monto.Valor);
# else:
#     print("NO TIENE MONTO")
# print("# EJEMPLO DE CSV")
# print("Monto", "Fecha", "Tipo", sep=",")
# print(movimiento.ToCSVLine())
# print(movimiento2.ToCSVLine())

# Creación de la ventana
window = sg.Window('M-Friend', layout)
window.Finalize()# Sin esto no se puede dibujar algo en las gráficas

def ObtenerMovimientos(nombreArchivo: str) -> list[Movimiento]:
    with open (nombreArchivo) as archivito:
        lineas = archivito.readlines()
        for i in range(len(lineas)):
            lineas[i] = lineas[i].rstrip().split()
        return lineas
def GuardarMovimientos(nombreArchivo: str, registros: list[Movimiento]):
    with open(nombreArchivo, "w") as archivito:
        for i in range(len(registros)):
            archivito.write(str(registros[i][0]))
            # print(registros[i][0])
            archivito.write("\n")
meses=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
def CrearGraficas(movimientos: list[Movimiento], graficas: list[sg.Graph]):
    # Con la circleID se pueden crear animaciones
    matriz=ObtenerMovimientos(nombreArchivo)
    matrizg=[]
    matrizi=[]
    for i in range(len(matriz)):
        reg=matriz[i][0].split(",")
        if (reg[2]=="Gasto"):
            matrizg.append(reg)
        elif (reg[2]=="Ingreso"):
            matrizi.append(reg)
    barras(matrizg,0)
    barras(matrizi,1)
    disper(matrizg,2)
    disper(matrizi,3)
def disper(matri,s):
    graphs[s].Erase()
    gmeses=[1]*12
    bandera=True
    for i in range(len(matri)):
        registro_temporal=matri[i][1].split("-")
        mes=int(registro_temporal[1])
        gmeses[mes-1]+=int(matri[i][0])
    maxi=max(gmeses)
    valuesy=[0]*13
    for i in range(13):
        valuesy[i]=(maxi/12)*i+1
    graphs[s].draw_line((-225,-210),(243, -210), color='white')
    graphs[s].draw_line((-225,-210),(-225, 200), color='white')
    for i in range(len(matri)):
        registro_temporal=matri[i][1].split("-")
        mes=int(registro_temporal[1])
        graphs[s].DrawCircle(((mes-1)*40+20-230, (int(matri[i][0])*400/maxi)-200),3, fill_color='blue')

    for i in range(12):
        graphs[s].DrawText(text=meses[i], location=(
            i*40+20-230, -230), color='white')
    for i in range(13):graphs[s].DrawText(text=str(int(valuesy[i])), location=(
            -240, 33.3*i-205), color='white')
def barras(matri,s):
    graphs[s].Erase()
    gmeses=[1]*12
    for i in range(len(matri)):
        registro_temporal=matri[i][1].split("-")
        mes=int(registro_temporal[1])
        gmeses[mes-1]+=int(matri[i][0])
    maxi=max(gmeses)
    valuesy=[0]*13
    for i in range(13):
        valuesy[i]=(maxi/12)*i+1
    graphs[s].draw_line((-225,-210),(243, -210), color='white')
    graphs[s].draw_line((-225,-210),(-225, 200), color='white')
    for i in range(12):
        graphs[s].DrawRectangle(top_left=(i*40-220, (int(gmeses[i])*400/maxi)-200),
                            bottom_right=(i*40+20-220, -200), fill_color='blue')
        graphs[s].DrawText(text=meses[i], location=(
            i*40+20-230, -230), color='white')
    for i in range(13):graphs[s].DrawText(text=str(int(valuesy[i])), location=(
            -240, 33.3*i-205), color='white')

nombreArchivo = "base_de_datos_mfriend.csv"
movimientos = ObtenerMovimientos(nombreArchivo)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    CrearGraficas(movimientos, graphs)
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
        break

    if event == botonRecomendaciones:
        VentanaRecomendaciones.Mostrar()

    nuevoMovimiento = None
    if event == botonIngreso:
        nuevoMovimiento = VentanaIngreso.ObtenerIngreso()
    if event == botonGasto:
        nuevoMovimiento = VentanaGasto.ObtenerGasto()
    if nuevoMovimiento != None:
        movimientos.append(nuevoMovimiento.ToCSVLine().split())

window.close()
GuardarMovimientos(nombreArchivo, movimientos)