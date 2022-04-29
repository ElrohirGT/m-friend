import PySimpleGUI as sg

from models import Ingreso, Movimiento

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Uso de clase movimiento
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

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()