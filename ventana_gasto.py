import PySimpleGUI as sg

from models import Movimiento

class VentanaGasto():
    # ¿Qué debe retornar?
    # None: en caso de que le de cancelar o algo así
    # Movimiento({datos}): en caso de que sí le de a guardar
    def ObtenerGasto() -> Movimiento | None:
        topPane = sg.Pane([
            sg.Col([[sg.VPush()], [sg.Text("Formulario Gasto", font=("Mistral", 24))], [sg.VPush()]], element_justification="c"),
        ], s=(800,50))
        botonGuardar = "btn_guardar"
        botonRegresar = "btn_regresar"
        a = [sg.Text("Formulario de", font=("Mistral", 24))]
        b = [sg.Text("ingreso de gastos", font=("Mistral", 24))]
        c = [sg.Text("Monto: ", font=("Mistral", 24)), sg.Input("ingrese el monto")]
        d = [sg.Text("Fecha: ", font=("Mistral", 24)), sg.Input("Año-Mes-Día")]
        e = [sg.Button('Guardar', key=botonGuardar)]
        f = [sg.Button('Regresar', key=botonRegresar)]

        midPane = sg.Pane([
            sg.Col([[sg.VPush()],[sg.Push()], a, b, c, d, e, f, [sg.Push()], [sg.VPush()]], element_justification="c"),
        ], s=(300,400))
            
        

        layout = [

            [topPane],[sg.Push(),midPane,sg.Push()]
        ]
        window = sg.Window("Formluario Gasto", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
                break

        window.close()
        return None