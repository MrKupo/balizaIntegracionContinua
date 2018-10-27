#Archivo main del ESP32
from ConfiguracionBaliza import ConfiguracionBaliza

#Instanciamos el singleton de configuracion
configuracionBaliza = ConfiguracionBaliza()

#Hardcodeamos las configuraciones
#Configuracion de Travis
TRAVIS_API_URL = "http://192.168.0.18:8080"
TOKEN = "9cHb1xMQyaGSSSsi6xTW5Q"
REPOSITORIO = "dyasc-2018"
USUARIO = "MrKupo"

#Configuracion de Red
SSID = "Fibertel WiFi589 2.4GHz"
CLAVE = "00438829825"

ConfiguracionBaliza.instancia.get_configuracion_travis().configurar(
    USUARIO,
    REPOSITORIO,
    TOKEN#,
    #TRAVIS_API_URL #COMENTAMOS PARA QUE USE LA API DE TRAVIS
)

config_red = ConfiguracionBaliza.instancia.get_configuracion_red()

config_red.configurar(
    SSID,
    CLAVE
)

import time
network_importada = True
try:
    import network
except:
    network_importada = False

if(network_importada):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    cantidad_intentos_conexion = 1
    while(not sta_if.isconnected()):
        print("Tratando de conectarse a la red",config_red.get_SSID(),"\nIntento número",cantidad_intentos_conexion)
        sta_if.connect(config_red.get_SSID(), config_red.get_clave())
        if(sta_if.isconnected()):
            print("Se ha establecido la conexión con la red:",config_red.get_SSID())
            break
        cantidad_intentos_conexion += 1
        time.sleep(1)


import LoopPrincipal