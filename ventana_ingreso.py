import PySimpleGUI as sg

from models import Movimiento

class VentanaIngreso():
    def ObtenerIngreso() -> Movimiento:
        topPane = sg.Pane([
            sg.Col([[sg.VPush()], [sg.Text("Formulario Ingreso", font=("Mistral", 24))], [sg.VPush()]], element_justification="c"),
        ], s=(800,50))

        layout = [
            [topPane],
        ]
        window = sg.Window("Formluario Ingreso", layout)
        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
                break

        window.close()
        return Movimiento()