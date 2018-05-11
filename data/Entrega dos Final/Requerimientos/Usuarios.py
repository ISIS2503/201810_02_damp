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


class TodoList(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    #@requires_auth
    def post(self):
        json_data = request.get_json(force = True)       
        rol = json_data['Rol']
        nombre = json_data['Nombre']
        password = json_data['Password']
        correo = json_data['Correo']
        guardar ={
            'Rol' : rol,
            'Nombre' : nombre,
            'Password' : password,
            'Correo' : correo
            }
        collection.insert_one(guardar).inserted_id
        return jsonify(Rol = rol, Nombre = nombre, Password = password, Correo = correo)

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@requires_auth
    def get(self):
        x = {}
        cursor = collection.find({})
        i = 1
        for document in cursor:
            arreglo = []
            rol = document['Rol'].replace('\\','')
            nombre = document['Nombre'].replace('\\','')
            password = document['Password'].replace('\\','')
            correo = document['Correo'].replace('\\','')
            arreglo=[rol, nombre, password, correo]
            x['Usuario#' + str(i)] = arreglo
            i+=1
        thejson = json.dumps([{k :{ 'Rol':v[0], 'Nombre':v[1], 'Password':v[2], 'Correo':v[3]}} for k,v in x.items()])
        return thejson


class Todo(Resource):

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@requires_auth
    def get(self, correo):
        arreglo = []
        cursor = collection.find({'Correo': (correo)})
        for document in cursor:
            rol = document['Rol'].replace('\\','')
            nombre = document['Nombre'].replace('\\','')
            password = document['Password'].replace('\\','')
            correo = document['Correo'].replace('\\','')
            arreglo=[rol, nombre, password, correo]
        if len(arreglo)> 0:
            thejson = json.dumps([{'Rol':arreglo[0], 'Nombre': arreglo[1], 'Password':arreglo[2], 'Correo':arreglo[3]}])
        else:
            thejson=[]   
        return thejson

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@requires_auth
    def put(self, correo):
        json_data = request.get_json(force = True)
        rol = json_data['Rol']
        nombre = json_data['Nombre']
        password = json_data['Password']
        collection.update_one(
                {'Correo' : correo},
                {
                    "$set":{
                        'Rol': rol,
                        'Nombre': nombre,
                        'Password': password
                    }
                },
                upsert=False
            )
        return jsonify(Rol = rol, Nombre = nombre, Password = password, Correo = correo)

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@requires_auth
    def delete(self, correo):
        arreglo = []
        cursor = collection.find({'Correo': (correo)})
        try:
            for document in cursor:
                rol = document['Rol'].replace('\\','')
                nombre = document['Nombre'].replace('\\','')
                password = document['Password'].replace('\\','')
                correo = document['Correo'].replace('\\','')
                arreglo=[rol, nombre, password, correo]
            thejson = json.dumps([{'Rol':arreglo[0], 'Nombre': arreglo[1], 'Password':arreglo[2], 'Correo':arreglo[3]}])
            collection.remove({"Correo": correo})
            return thejson
        except:
            print ("No se encuentra el correo en la BD")


class Roles(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    #@cross_origin(headers=['Content-Type', 'Authorization'])
    #@requires_auth
    def get(self, role):
        x = {}
        cursor = collection.find({})
        i = 0
        j = 1
        for document in cursor:
            arreglo = []
            rol = document['Rol'].replace('\\','')
            nombre = document['Nombre'].replace('\\','')
            password = document['Password'].replace('\\','')
            correo = document['Correo'].replace('\\','')           
            arreglo=[rol, nombre, password, correo]
            if arreglo[0] == (role) :
               
               thejson = json.dumps([{ 'Rol':arreglo[0], 'Nombre':arreglo[1], 'Password': arreglo[2], 'Correo': arreglo[3]}])               
               x['Usuario ' + role + ' #' + str(j)] = arreglo
               j+=1
            
            i+=1
        return x
        
    
api.add_resource(TodoList, '/usuarios')
api.add_resource(Todo, '/usuarios/<correo>')
api.add_resource(Roles, '/usuarios/rol/<role>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
