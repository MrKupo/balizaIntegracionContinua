from json import loads
from ClienteCI import *
from EstadoBuild import EstadoBuild
from gc import collect
import HttpRequests
from ConfiguracionCI import ConfiguracionCI
collect()

class ClienteTravis(ClienteCI):    

    def __init__(self, configuracion_ci):
        self.set_configuracion_ci(configuracion_ci)

    def set_configuracion_ci(self, configuracion_ci):
        self.__configuracion_ci = configuracion_ci

    def get_configuracion_ci(self):
        return self.__configuracion_ci

    def __consultar_estado(self):
        #Definimos los headers para el request
        headers = {
            "Travis-API-Version": "3",
            "Authorization": "token " + self.__configuracion_ci.get_token()
        }
        request_url = (self.__configuracion_ci.get_api_url() + "/repo/" +
                            self.__configuracion_ci.get_usuario() +"%2F"+ self.__configuracion_ci.get_repositorio() +
                            "/builds?limit=1&sort_by=finished_at:desc")
        response = HttpRequests.get(request_url, headers=headers)
        return response.text

    def __parsear_estado(self, response_json):
        #Traemos el string que representa el estado del build
        estado = response_json['builds'][0]['state']
        #Si paso los tests
        if(estado == "passed"):
            return EstadoBuild.PASSED
        #Si fallo los tests
        elif(estado == "failed"):
            return EstadoBuild.FAILED
        #Si en este momento esta corriendo los tests
        else:            
            return EstadoBuild.RUNNING

    def __obtener_estado(self, response):
        #Si existe algun problema de credenciales
        if(response == "access denied"):         
            return EstadoBuild.ACCESS_DENIED
        #Transformamos el response a JSON
        response_json = loads(response)
        #Cuando ocurre un error al estar mal el nombre de usuario o el repositorio
        if('error_type' in response_json):
            return EstadoBuild.CONNECTION_ERROR
        if('builds' in response_json):
            #Si no fue compilado nunca
            if(len(response_json['builds']) == 0):
                return EstadoBuild.NOT_YET_BUILT
            return self.__parsear_estado(response_json)
        #Si no es ninguno
        return EstadoBuild.CONNECTION_ERROR

    def get_estado(self):
        if(not self.__configuracion_ci.esta_configurada()):
            return EstadoBuild.CONNECTION_ERROR
        try:
            response = self.__consultar_estado()
        except HttpRequests.ConnectionError:
            #Si existe error de conexion
            return EstadoBuild.CONNECTION_ERROR
        estado = self.__obtener_estado(response)
        #Ejecutamos el Garbage Collector
        collect()
        return estado