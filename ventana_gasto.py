from calendar import c
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
        c = [sg.Text("Monto: ", font=("Mistral", 24)), sg.Input()]
        d = [sg.Text("Fecha: ", font=("Mistral", 24)), sg.Input()]
        e = [sg.Button('Guardar', key=botonGuardar)]
        f = [sg.Button('Regresar', key=botonRegresar)]

        midPane = sg.Pane([
            sg.Col([[sg.VPush()],[sg.Push()], a, b, c, d, e, f, [sg.Push()], [sg.VPush()]], element_justification="c"),
        ], s=(300,400))
          
        

        layout = [

            [topPane],[sg.Push(),midPane,sg.Push()]
        ]
        window = sg.Window("Formluario Gasto", layout)
        
        Lista_de_gastos =[]

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
                break

            nuevoMovimiento = None
            if event == botonGuardar:

                with open("base_de_datod_mfriend.csv", "r") as archivo:
                    titulo = archivo.readline().rstrip().split(",")
        
                    numeros = archivo.readlines()
        
                for i in range(len(numeros)):
                    numeros[i] = numeros[i].rstrip().split(",")
            
                numerosDic = {}
        
            
                for columna in range(len(titulo)):
                    numerosDic[titulo[columna]] = numeros[i][columna]
                
                Lista_de_gastos.append(numerosDic)

                Movimiento = ({
                "Monto": c,
                "Tipo": "Gasto",
                "Fecha": d
                })
                
                Lista_de_gastos.append(Movimiento)

                with open("base_de_datod_mfriend.csv", "w") as archivo:
                    for i in range(len(titulo)):
                        archivo.write(titulo[i])
                    if i < len(titulo) - 1:
                        archivo.write(",")
                    else:
                        archivo.write("\n")
            
                for seriesDic in Lista_de_gastos:
                    for i in range(len(titulo)):
                        archivo.write(numerosDic[titulo[i]])
                        if i < len(titulo) - 1:
                            archivo.write(",")
                        else:
                            archivo.write("\n")

                

            if event == botonRegresar:
                nuevoMovimiento =  VentanaGasto.close()

        window.close()
        return None