from flask import Flask, jsonify, request, _request_ctx_stack
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from jose import jwt

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.alertas

AUTH0_DOMAIN = 'isis2503-dasolano1.auth0.com'
API_AUDIENCE = "uniandes.edu.co/entrega2"
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

class HelloWorld(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            activo = document['Activo'].replace('\\','')
            tipo = document['Tipo'].replace('\\','')
            conjunto = document['Conjunto'].replace('\\','')
            torre = document['Torre'].replace('\\','')
            piso = document['Piso'].replace('\\','')
            apartamento = document['Apartamento'].replace('\\','')
            hora = document['Hora']
            arreglo=[activo, tipo, conjunto, torre, piso, apartamento, str(hora).replace('\\','')]
            x['Alerta' + str(i)] = arreglo
            i+=1
        thejson = json.dumps([{k :{ 'Activo':v[0], 'Tipo':v[1], 'Conjunto': v[2], 'Torre': v[3], 'Piso': v[4], 'Apartamento': v[5], 'Hora': v[6]}} for k,v in x.items()])
        return thejson

    @app.route("/admin/<name>")
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def getAdmin(name):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            activo = document['Activo'].replace('\\','')
            tipo = document['Tipo'].replace('\\','')
            conjunto = document['Conjunto'].replace('\\','')
            torre = document['Torre'].replace('\\','')
            piso = document['Piso'].replace('\\','')
            apartamento = document['Apartamento'].replace('\\','')
            hora = document['Hora']
            arreglo=[activo, tipo, conjunto, torre, piso, apartamento, str(hora).replace('\\','')]
            if arreglo[2] == (name) :
               thejson = json.dumps([{ 'Activo':arreglo[0], 'Tipo':arreglo[1], 'Conjunto': arreglo[2], 'Torre': arreglo[3], 'Piso': arreglo[4], 'Apartamento': arreglo[5], 'Hora': arreglo[6]}])
            else: 
                i+=1
        return thejson

    @app.route("/propietario/<conjunto>/<torre>/<piso>/<apartamento>")
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def getPropietario(conjunto, torre, piso, apartamento):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            activo = document['Activo'].replace('\\','')
            tipo = document['Tipo'].replace('\\','')
            conjunto = document['Conjunto'].replace('\\','')
            torre = document['Torre'].replace('\\','')
            piso = document['Piso'].replace('\\','')
            apartamento = document['Apartamento'].replace('\\','')
            hora = document['Hora']
            arreglo=[activo, tipo, conjunto, torre, piso, apartamento, str(hora).replace('\\','')]
            if arreglo[2] == (conjunto) and arreglo[3] == (torre) and arreglo[4] == (piso) and arreglo[5] == (apartamento) :
               thejson = json.dumps([{ 'Activo':arreglo[0], 'Tipo':arreglo[1], 'Conjunto': arreglo[2], 'Torre': arreglo[3], 'Piso': arreglo[4], 'Apartamento': arreglo[5], 'Hora': arreglo[6]}])
            i+=1
        return thejson

    
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth    
    def post(self):
        json_data = request.get_json(force = True)
        activo = json_data['Activo']
        tipo = json_data['Tipo']
        conjunto = json_data['Conjunto']
        torre = json_data['Torre']
        piso = json_data['Piso']
        apartamento = json_data['Apartamento']
        hora = datetime.datetime.utcnow()
        guardar ={
            'Activo' : activo,
            'Tipo' : tipo,
            'Conjunto' : conjunto,
            'Torre' : torre,
            'Piso' : piso,
            'Apartamento' : apartamento,
            'Hora' : hora
            }
        collection.insert_one(guardar).inserted_id
        return jsonify(activo = activo, tipo = tipo, conjunto = conjunto, torre = torre, piso = piso, apartamento = apartamento, hora = hora)                                        
api.add_resource(HelloWorld, '/alertas')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
