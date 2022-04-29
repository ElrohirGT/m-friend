def FromDictToCSVHeader(diccionario: dict) -> str:
    return ",".join([str(x) for x in diccionario.keys()])

def FromDictToCSVLine(diccionario: dict) -> str:
    return ",".join([str(x) for x in diccionario.values()])

def IsFloat(cadena: str):
    try:
        float(cadena)
        return True
    except(ValueError):
        return False