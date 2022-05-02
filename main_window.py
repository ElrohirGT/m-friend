import PySimpleGUI as sg

from models import Movimiento
from ventana_ingreso import VentanaIngreso

sg.theme('DarkGreen2') #Tema de la ventana
graphs = [sg.Graph((700,300), (-250, -250), (250,250), background_color="#1a1a1a") for x in range(4)]

top_pane = sg.Pane([
    sg.Col([[sg.VPush()], [sg.Text("M-Friend", font=("Mistral", 24))], [sg.VPush()]], element_justification="c"),
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
    "Tipo": "Gasto",
    "Fecha": "2022-04-09"
})

monto = movimiento.ObtenerMonto()
if monto.TieneValor():
    print("El monto es:", monto.Valor);
else:
    print("NO TIENE MONTO")

# Creación de la ventana
window = sg.Window('M-Friend', layout)
window.Finalize()# Sin esto no se puede dibujar algo en las gráficas
# Event Loop to process "events" and get the "values" of the inputs
circleID = graphs[0].DrawCircle((0,0), 30, line_color="white")
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
        break

    if event == botonIngreso:
        nuevoIngreso = VentanaIngreso.ObtenerIngreso()
    print('You entered ', values[0])

window.close()