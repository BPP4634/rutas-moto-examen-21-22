from datetime import datetime

def parsea_fecha(fecha):
    if fecha=='':
        return datetime.today().date()
    else:
        return datetime.strptime(fecha, '%m/%d/%Y')