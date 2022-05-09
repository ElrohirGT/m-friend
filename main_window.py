import PySimpleGUI as sg

from models import Movimiento
from ventana_gasto import VentanaGasto
from ventana_ingreso import VentanaIngreso

sg.theme('DarkGreen2') #Tema de la ventana
graphs = [sg.Graph((700,300), (-250, -250), (250,250), background_color="#1a1a1a") for x in range(4)]

top_pane = sg.Pane([
    sg.Col([[sg.VPush()], [sg.Text("M-Friend", font=("Times new roman", 24))], [sg.VPush()]], element_justification="c"),
], s=(800,50))

tabs = sg.TabGroup(tab_location="left", layout=[
    [
        sg.Tab("Gráfica 1", [
            [graphs[0]]
        ]),
        sg.Tab("Gráfica 2", [
            [graphs[1]]
        ]),
        sg.Tab("Gráfica 3", [
            [graphs[2]]
        ]),
        sg.Tab("Gráfica 4", [
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
print("# EJEMPLO DE USO DE CLASE MOVIMIENTO")
monto = movimiento.ObtenerMonto()
if monto.TieneValor():
    print("El monto es:", monto.Valor);
else:
    print("NO TIENE MONTO")
print("# EJEMPLO DE CSV")
print("Monto", "Fecha", "Tipo", sep=",")
print(movimiento.ToCSVLine())
print(movimiento2.ToCSVLine())

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
            print(registros[i][0])
            archivito.write("\n")
def CrearGraficas(movimientos: list[Movimiento], graficas: list[sg.Graph]):
    # Con la circleID se pueden crear animaciones
    circleID = graphs[0].DrawCircle((0,0), 30, line_color="white") 

nombreArchivo = "base_de_datos_mfriend.csv"
movimientos = ObtenerMovimientos(nombreArchivo)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    CrearGraficas(movimientos, graphs)
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
        break

    nuevoMovimiento = None
    if event == botonIngreso:
        nuevoMovimiento = VentanaIngreso.ObtenerIngreso()
    if event == botonGasto:
        nuevoMovimiento = VentanaGasto.ObtenerGasto()
    if nuevoMovimiento != None:
        movimientos.append(nuevoMovimiento.ToCSVLine().split())
        print(movimientos)
    print('You entered ', values[0])

window.close()
GuardarMovimientos(nombreArchivo, movimientos)