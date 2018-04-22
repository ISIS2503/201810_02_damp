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
collection = db.CERRADURAS

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


class TodoList(Resource):
    def post(self):
        json_data = request.get_json(force = True)
        idP = json_data['idP']
        informacion = json_data['Informacion']
        guardar ={
            'idP' : idP,
            'Informacion' : informacion
            }
        collection.insert_one(guardar).inserted_id
        return jsonify(idP = idP, Informacion = informacion)
    def get(self):
        x = {}
        cursor = collection.find({})
        i = 1
        for document in cursor:
            arreglo = []
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
            x['Cerradura#' + str(i)] = arreglo
            i+=1
        thejson = json.dumps([{k :{ 'idP':v[0], 'Informacion':v[1]}} for k,v in x.items()])
        return thejson
class Todo(Resource):

    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idP):
        arreglo = []
        cursor = collection.find({"idP": (idP)})
        for document in cursor:
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
        else:
            thejson=[]
        return thejson
    def put(self, idP):
        json_data = request.get_json(force = True)
        informacion = json_data['Informacion']
        collection.update_one(
                {'idP' : idP},
                {"$set": {'Informacion': informacion}},
                upsert=False
            )
        return jsonify(idP = idP, Informacion = informacion)
    def delete(self, idP):
        arreglo = []
        cursor = collection.find({"idP": (idP)})
        try:
            for document in cursor:
                idP = document['idP'].replace('\\','')
                informacion = document['Informacion'].replace('\\','')
                arreglo=[idP, informacion]
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
            collection.remove({"idP": idP})
            return thejson
        except:
            print ("No se encuentra el idP en la BD")
api.add_resource(TodoList, '/cerraduras')
api.add_resource(Todo, '/cerraduras/<idP>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
