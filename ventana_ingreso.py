from calendar import c
from tkinter import messagebox
import PySimpleGUI as sg

from models import Movimiento

class VentanaIngreso():
    # ¿Qué debe retornar?
    # None: en caso de que le de cancelar o algo así
    # Movimiento({datos}): en caso de que sí le de a guardar
    def ObtenerIngreso() -> Movimiento | None:
        topPane = sg.Pane([
            sg.Col([[sg.VPush()], [sg.Text("Formulario Ingreso", font=("Times new roman", 24))], [sg.VPush()]], element_justification="c"),
        ], s=(800,50))
        botonGuardar = "btn_guardar"
        botonRegresar = "btn_regresar"
        a = [sg.Text("Formulario de", font=("Times new roman", 24))]
        b = [sg.Text("ingresos", font=("Times new roman", 24))]
        c = [sg.Text("Monto: ", font=("Times new roman", 24)), sg.Input(key="inputmonto")]
        d = [sg.Text("Fecha: ", font=("Times new roman", 24)), sg.Input(key="inputfecha")]
        e = [sg.Button('Guardar', key=botonGuardar)]
        f = [sg.Button('Regresar', key=botonRegresar)]

        midPane = sg.Pane([
            sg.Col([[sg.VPush()],[sg.Push()], a, b, c, d, e, f, [sg.Push()], [sg.VPush()]], element_justification="c"),
        ], s=(300,400))
          

        layout = [

            [topPane],[sg.Push(),midPane,sg.Push()]
        ]
        window = sg.Window("Formulario Ingresos", layout)
        
        nuevoMovimiento = None

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
                break

            elmonto = values["inputmonto"]
            lafecha = values["inputfecha"]
            xd = elmonto.isnumeric()
            l = ["0000", "00"," 00"]
            xd2 = lafecha.split("-")
            xd3 = lafecha.isalpha()
            if len(xd2) == 3:
                l = [int(xd2[0]), int(xd2[1]),int(xd2[2])]
                if xd == True and xd3 == False and l[0] > 2020 and l[1] > 0 and l[1] < 13 and l[2] > 0 and l[2] < 32:
                    if event == botonGuardar:
                        movimiento = {
                        "Monto": elmonto,
                        "Fecha": lafecha,
                        "Tipo": "Ingreso"
                        }
                    # print(movimiento)
                    nuevoMovimiento = Movimiento(movimiento)
                    break 
                else:
                    pass
            elif event == botonRegresar: 
                break
            else:
                messagebox.showerror("Error","Los datos ingresados son incorrectos")
                # print("error")
            

        window.close()
        return nuevoMovimiento