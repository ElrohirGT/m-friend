import textwrap
from datetime import datetime
from dateutil.relativedelta import relativedelta
import PySimpleGUI as sg
import pandas as pd

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


        (analisisGeneral, analisisMensual, recomendaciones) = RealizarAnalisisDe("base_de_datos_mfriend.csv")
        texts = [sg.Text(txt) for txt in textwrap.wrap(recomendaciones, 100)]
        frameAnalisis = sg.Frame("Análisis",
            [
                [sg.Push(), sg.Text(analisisGeneral), sg.Text(analisisMensual), sg.Push()],
                [sg.Push(), sg.Text("Recomendaciones: "), sg.Push()],
                *[[sg.Push(), textWidget, sg.Push()] for textWidget in texts]
            ]
        )
        layout = [
            [topPane],
            [sg.Push(), realGraphCol, expectedGraphCol, sg.Push()],
            [sg.Push(), frameAnalisis, sg.Push()]
        ]

        window = sg.Window("Recomendaciones", layout)
        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'): # if user closes window or clicks cancel
                break

        window.close()
    
def RealizarAnalisisDe(nombre_archivo: str) -> str:
    recomendaciones = { # Gastos actuales mayores que sus ingresos?
        True: { # Los gastos subieron respecto al mes pasado?
            True: { # Los ingresos bajaron respecto al mes pasado?
                True: "Lo sentimos, sabemos que manejar dinero es difícil, por eso creamos esta aplicación! Te recomendamos que veas a TwoCents en Youtube.",
                False: "Hey, enfocándonos en lo positivo, tus ingresos subieron respecto al mes pasado! Sin embargo tus gastos también subieron respecto al mes pasado y también gastaste más de lo que ganaste este mes. Recuerda, la diferencia óptima entre gastos e ingresos es de un mínimo del 30%. No porque tengas más dinero significa que tengas que gastar más."
            },
            False: { # Los ingresos bajaron respecto al mes pasado?
                True: "Felicidades! Tus gastos no subieron respecto al mes anterior. Sin embargo, debes recordar que gastaste más de lo que ganaste este mes, por lo que debes intentar mantenerlos más arriba. Tú puedes!",
                False: "Wow, vas mejorando, tus gastos no subieron respecto al mes anterior y tus ingresos subieron. Estas muy cerca! Solo necesitas subir tus ingresos para que sean mayores a tus gastos. Confiamos en tí!"
            }
        },
        False: { # Los gastos subieron respecto al mes pasado?
            True: { # Los ingresos bajaron respecto al mes pasado?
                True: "Hey, todo bien? Por el momento tus gastos son menores que tus ingresos, pero tus gastos subieron y tus ingresos bajaron. Ten cuidado, recuerda que la diferencia mínima óptima entre gastos e ingresos es del 30%",
                False: "Vas bien por el momento, nadie es perfecto. Tus gastos subieron respecto al mes pasado pero tus ingresos no bajaron y tus gastos siguen siendo menor a tus ingresos. Tú puedes!"
            },
            False: { # Los ingresos bajaron respecto al mes pasado?
                True: "Tus ingresos bajaron! Vas muy bien por el momento pues tus gastos no subieron respecto al mes pasado y tus gastos actuales son menores a tus ingresos, tan solo ten cuidado.",
                False: "WOW vas excelente! Continúa así! Recuerda intentar mantener una diferencia del 30% entre tus ingresos y tus gastos."
            }
        }
    }
    fechaActual = datetime.today()
    df = pd.read_csv(nombre_archivo)
    dfGastos = df[df["Tipo"] == "Gasto"]
    dfIngresos = df[df["Tipo"] == "Ingreso"]

    gastosMesActual = dfGastos[df["Fecha"] >= fechaActual.strftime("%Y-%m")]["Monto"]
    mesAnterior = fechaActual - relativedelta(months=1)
    gastosMesAnterior = dfGastos[(df["Fecha"] >= mesAnterior.strftime("%Y-%m")) & (df["Fecha"] < fechaActual.strftime("%Y-%m"))]["Monto"]
    
    ingresosMesActual = dfIngresos[df["Fecha"] >= fechaActual.strftime("%Y-%m")]["Monto"]
    ingresosMesAnterior = dfIngresos[(df["Fecha"] >= mesAnterior.strftime("%Y-%m")) & (df["Fecha"] < fechaActual.strftime("%Y-%m"))]["Monto"]
    
    analisisGeneral = "General:"
    promedioGastos = dfGastos["Monto"].mean()
    analisisGeneral += f"\nEl promedio de tus gastos es: Q. {promedioGastos:.2f}"
    
    promedioIngresos = dfIngresos["Monto"].mean()
    analisisGeneral += f"\nEl promedio de tus ingresos es: Q. {promedioIngresos:.2f}"

    promedioGastoMesActual = gastosMesActual.mean()

    analisisMensual = "Este mes:"
    (promedioGastosActual, gastosRespectoMesAnterior, difGastosFormateado) = EvaluarPromedioDeMesActualYAnterior(gastosMesAnterior, gastosMesActual)
    (promedioIngresosActual, ingresosRespectoMesAnterior, difIngresosFormateado) = EvaluarPromedioDeMesActualYAnterior(ingresosMesAnterior, ingresosMesActual)
    analisisMensual += f"\nEl promedio de gastos es: Q. {promedioGastosActual:.2f} ({difGastosFormateado})"
    analisisMensual += f"\nEl promedio de ingresos es: Q. {promedioIngresosActual:.2f} ({difIngresosFormateado})"

    difGastosEIngresos = promedioIngresosActual - promedioGastosActual
    gastosSonMayores = difGastosEIngresos < 0
    gastosSubieronRespectoAlMesAnterior = gastosRespectoMesAnterior < 0
    ingresosBajaronRespectoAlMesAnterior = ingresosRespectoMesAnterior > 0

    recomendacion = recomendaciones[gastosSonMayores][gastosSubieronRespectoAlMesAnterior][ingresosBajaronRespectoAlMesAnterior]
    
    return (analisisGeneral, analisisMensual, recomendacion)

def EvaluarPromedioDeMesActualYAnterior(mesAnterior, mesActual):
    promedioMesAnterior = mesAnterior.mean()
    promedioMesActual = mesActual.mean()
    porcentajeDiferencia = (1 - promedioMesActual/promedioMesAnterior) * 100
    simbolo = ""
    if porcentajeDiferencia < 0:
        simbolo = "más que el mes anterior"
    elif porcentajeDiferencia > 0:
        simbolo = "menos que el mes anterior"
    
    return (promedioMesActual , porcentajeDiferencia, f"{abs(porcentajeDiferencia):.2f}% {simbolo}")