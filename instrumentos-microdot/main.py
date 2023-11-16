def connect_to( ssid , passwd):

    """
        Conecta el microcontrolador a la red WIFI
        
        ssid (str): Nombre de la red WIFI
        passwd (str): Clave de la red WIFI
        
        returns (str): Retorna la direccion de IP asignada
    """
    import network
    # Creo una instancia para interfaz tipo station
    sta_if = network.WLAN(network.STA_IF)
    # Verifico que no este conectado ya a la red
    if not sta_if.isconnected():
        # Activo la interfaz
        sta_if.active(True)
        # Intento conectar a la red
        sta_if.connect(ssid, passwd)
        # Espero a que se conecte
        while not sta_if.isconnected():
            pass
        # Retorno direccion de IP asignada
    return sta_if.ifconfig()[0]
        
# Importo lo necesario para la aplicacion de Microdot
from microdot import Microdot, send_file

# Creo una instancia de Microdot
app = Microdot()

@app.route("/")
def index(request):
    """
    Funcion asociada a la ruta principal de la aplicacion
    
    request (Request): Objeto que representa la peticion del cliente
    
    returns (File): Retorna un archivo HTML
    """
    return send_file("index.html")


@app.route("/assets/<dir>/<file>")
def assets(request, dir, file):
    """
    Funcion asociada a una ruta que solicita archivos CSS o JS
    
    request (Request): Objeto que representa la peticion del cliente
    dir (str): Nombre del directorio donde esta el archivo
    file (str): Nombre del archivo solicitado
    
    returns (File): Retorna un archivo CSS o JS
    """
    return send_file("/assets/" + dir + "/" + file)

@app.route("/data/update")
def data_update(request):
    """
    Funcion asociada a una ruta que solicida datos del microcontrolador
    
    request (Request): Objeto que representa la peticion del cliente
    
    returns (dict): Retorna un diccionario con los datos leidos
    """
    from machine import Pin, Timer
    import time

    trig_pin = Pin(3, Pin.OUT)  
    echo_pin = Pin(2, Pin.IN)   

    trig_pin.low()
    time.sleep_us(2)
    trig_pin.high()
    time.sleep_us(10)
    trig_pin.low()
    
    while echo_pin.value() == 0:
        pass
    start = time.ticks_us()
    
    while echo_pin.value() == 1:
        pass
    
    end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    distance = 0
    d = 0
    while  d <=10 :  
        distance += (duration / 58)
        d = d +1 
    distance = distance / 10
    print(distance)
    return { "Distance" : distance }
    
    


# Programa principal, verifico que el archivo sea el main.py
if __name__ == "__main__":
    
    try:
        # Me conecto a internet
        ip = connect_to("Red Profesores", "Profes_IMPA_2022")
        # Muestro la direccion de IP
        print("Microdot corriendo en IP/Puerto: " + ip + ":5000")
        # Inicio la aplicacion
        app.run()
    
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")
