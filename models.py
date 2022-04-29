from datetime import date
from helperMethods import FromDictToCSVLine, IsFloat

class Resultado():
    def __init__(self, valor, error = None) -> None:
        Valor = valor
        Error = error

    def HasValue(self):
        return self.Valor != None

    Valor: any = None
    Error: any = None

class Movimiento():
    LLAVE_MONTO = "Monto"
    LLAVE_TIPO = "Tipo"
    LLAVE_FECHA = "Fecha"
    _current: dict

    def __init__(self, diccionario: dict) -> None:
        self._current = diccionario

    def ObtenerTipo(self) -> Resultado:
        if self.LLAVE_TIPO in self._current:
            return Resultado(self._current[self.LLAVE_TIPO])
        return Resultado(None, "Error al obtener tipo de movimiento")
    def CambiarTipo(self, nuevoTipo: str):
        if self.LLAVE_TIPO in self._current:
            self._current[self.LLAVE_TIPO] = nuevoTipo

    def ObtenerMonto(self) -> Resultado:
        if self.LLAVE_MONTO in self._current and IsFloat(self._current[self.LLAVE_MONTO]):
            return Resultado(float(self._current[self.LLAVE_MONTO]))
        return Resultado(None, "Error al obtener monto")
    
    def CambiarMonto(self, newValue: float):
        if self.LLAVE_MONTO in self._current:
            self._current[self.LLAVE_MONTO] = newValue

    def ObtenerFecha(self) -> Resultado:
        if self.LLAVE_FECHA in self._current:
            fecha = date.fromisoformat(self._current[self.LLAVE_FECHA])
            return Resultado(fecha)
        return Resultado(None, "Error al obtener fecha")

    def CambiarFecha(self, newValue: date):
        if self.LLAVE_FECHA in self._current:
            self._current[self.LLAVE_FECHA] = newValue.isoformat()
    
    def ToCSVLine(self) -> str:
        return FromDictToCSVLine(self._current)