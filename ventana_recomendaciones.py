import PySimpleGUI as sg

class VentanaRecomendaciones():
    def Mostrar():
        botonRegresar = "btn_regresar"
        topPane = sg.Pane([
            sg.Col([[sg.VPush()], [sg.Text("Recomendaciones", font=("Times new roman", 24))], [sg.VPush()]], element_justification="c"),
        ], s=(800,50))

        realGraph = sg.Graph((375,200), (-300,-300), (300,300), background_color="#1a1a1a")
        expectedGraph = sg.Graph((375,200), (-300,-300), (300,300), background_color="#1a1a1a")
        realGraphCol = sg.Col([
            [sg.Text("Real", font=("Times new roman", 24))],
            [realGraph]
        ], element_justification="c")
        expectedGraphCol = sg.Col([
            [sg.Text("Ideal", font=("Times new roman", 24))],
            [expectedGraph]
        ], element_justification="c")


        conclusiones = ""
        layout = [
            [topPane],
            [sg.Push(), realGraphCol, expectedGraphCol, sg.Push()],
            [sg.Frame("Análisis", [[sg.Push(), sg.Text(conclusiones), sg.Push()]], size=(800, 100))]
        ]

        window = sg.Window("Recomendaciones", layout)
        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
                break

        window.close()