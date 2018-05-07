from flask import Flask, jsonify, request, _request_ctx_stack
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from jose import jwt

#Roles administrador,yale y seguridad... Rol propietario se maneja diferente
app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.Usuarios

AUTH0_DOMAIN = 'isis2503-dasolano1.auth0.com'
#Para autenticacion
#API_AUDIENCE = "uniandes.edu.co/entrega2"
#Para autorizacion
API_AUDIENCE = "r0ffU9cccUvkV98WC5OB-HtVjbsbNz_F"
ALGORITHMS = ["RS256"]

APP = Flask(__name__)
    

# Error handler    
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    
@APP.errorhandler(AuthError)
def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    print(auth)

    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)
    
    parts = auth.split()
    
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False


class Todo(Resource):

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@requires_auth
    def get(self, correo, clave):
        arreglo = []
        cursor = collection.find({'Correo': (correo)})
        for document in cursor:
            rol = document['Rol'].replace('\\','')
            nombre = document['Nombre'].replace('\\','')
            password = document['Password'].replace('\\','')
            correo = document['Correo'].replace('\\','')
            arreglo=[rol, nombre, password, correo]
        if len(arreglo)> 0:
            if(arreglo[2]== clave):
                print("Inicio de sesion exitoso")
                if(arreglo[0]== 'yale'):

                   print("Seleccione la accion a llevar")
                   print("Gestionar:")
                   print("(1) Unidadades residenciales")
                   print("(2) Inmuebles")
                   print("(3) Hubs")
                   print("(4) Cerraduras")
                   print("(5) Usuarios")
                   print("(6) Claves Cerraduras")
                   print("(7) Horarios de Acceso de propietarios")
                   print("Consultar:")
                   print("(8) Alarmas mensuales por barrio")
                   print("(9) Alarmas en tiempo real")
                   print("(10) Alarmas mensuales por inmueble")
                   print("(11) Alarmas mensuales por Unidad")
                   print("(12) Alarmas en tiempo real de Unidad Residencial")
                   print("(13) Actualizar informacion de usuario")
                   print("(14) Cambiar clave")
                   print("(0) Cerrar sesion")

                   opcion = int(input())

                   if(opcion == 0):
                     print("Sesion finalizada")
                     print("")
                     main()

                   else:
                     print("Estamos en proceso de conectar todo el back con el front")
                     print("")
                     comeBack(correo, clave)
                     
                   

                if(arreglo[0]== 'administrador'):

                   print("Seleccione la accion a llevar")
                   print("Consultar:")
                   print("(1) Alarmas mensuales por Unidad")
                   print("(2) Alarmas en tiempo real de Unidad Residencial")
                   print("(3) Actualizar informacion de usuario")
                   print("(4) Cambiar clave")
                   print("(0) Cerrar sesion")

                   opcion = int(input())

                   if(opcion == 0):
                     print("Sesion finalizada")
                     print("")
                     main()

                   else:
                     print("Estamos en proceso de conectar todo el back con el front")
                     print("")
                     comeBack(correo, clave)
                   

                if(arreglo[0]== 'seguridad'):

                   print("Seleccione la accion a llevar")
                   print("Consultar:")
                   print("(1) Alarmas mensuales por Unidad")
                   print("(2) Alarmas en tiempo real de Unidad Residencial")
                   print("(3) Actualizar informacion de usuario")
                   print("(4) Cambiar clave")
                   print("(0) Cerrar sesion")

                   opcion = int(input())

                   if(opcion == 0):
                     print("Sesion finalizada")
                     print("")
                     main()

                   else:
                     print("Estamos en proceso de conectar todo el back con el front")
                     print("")
                     comeBack(correo, clave)
                   
                
                if(arreglo[0]== 'propietario'):
                   print("Seleccione la accion a llevar")
                   print("Consultar:")
                   print("(1) Alarmas mensuales por inmueble")
                   print("(2) Actualizar informacion de usuario")
                   print("(3) Cambiar clave")
                   print("(0) Cerrar sesion")

                   opcion = int(input())

                   if(opcion == '0'):
                     print("Sesion finalizada")
                     main()

                   else:
                     print("Estamos en proceso de conectar todo el back con el front")
                     print("")
                     comeBack(correo, clave)
                   

            else:
                print("Usuario o Contraseña incorrecta")
                print("")
                main()

        else:
            print("Usuario o Contraseña incorrecta")
            print("")
            main()
        
    
def comeBack(correo, clave):
    p = Todo()
    p.get(correo, clave)
       

def main():

    p = Todo()
    print("Bienvenido a la web de YALE, para ingresar siga estos pasos")
    print("Ingrese su correo")
    correo = input()

    print("Ingrese su clave")
    clave = input()
    p.get(correo, clave)


main()    

   

api.add_resource(Todo, '/usuarios/<correo>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
