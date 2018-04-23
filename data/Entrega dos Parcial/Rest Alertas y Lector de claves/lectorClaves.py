from flask import Flask, jsonify, request, _request_ctx_stack
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from jose import jwt
import paho.mqtt.client as mqtt

app = Flask(_name_)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['claves']
collection = db.clavesistema

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


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client();
client.on_connect=on_connect;
client.connect_async("172.24.41.200",8083,60);
client.reconnect();

class Claves(Resource):
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self):
        return ("GET")
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self):
        try:
            json_data = request.get_json(force=True)
            app.logger.info(json_data['clave'])
            passw = json_data['clave']
            if(len(passw)==4):
                if(passw.isnumeric()):
                    if(collection.count()<20):
                        if(collection.find({"clave" : passw}).count()==0):
                            app.logger.info(collection.find({"clave" : passw}).count())
                            collection.insert_one({"clave": passw}).inserted_id
                            stringArmada = "creacionclave::"+str(passw)
                            client.publish("claves/", stringArmada)
                            return ("La clave fue guardada satisfactoriamente")
                        else:
                            return ("Ya hay una clave igual")
                    else:
                        return ("Se llegó a un máximo de claves")
                else:
                    return ("La clave debe ser totalmente numerica")
            else:
                return ("La clave tiene un tamaño no permitido. Debe ser de 4")
        except Exception as e:
            return ("Ocurrio un problema: "+str(e))
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self):
        try:
            json_data = request.get_json(force=True)
            que = json_data['que']
            passw = json_data['clave']
            if(que=='todo'):
                collection.remove({})
                client.publish("claves/", "eliminar:todo")
                return ("Se eliminaron todas las claves")
            elif(que=='clave'):
                if(collection.find({"clave" : passw}).count()==1):
                    db.clavesistema.remove({"clave": passw})
                    stringArmada = "eliminar::"+str(passw)
                    client.publish("claves/", stringArmada)
                    return ("Se elimino la clave")
                else:
                    return("No existe dicha clave")
        except Exception as e:
            return ("Ocurrio un problema: "+str(e))
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self):
        try:
            json_data = request.get_json(force=True)
            passw = json_data['claveAntigua']
            passwN = json_data['claveNueva']
            if(collection.find({"clave" : passw}).count()==1):
                db.clavesistema.update_one({"clave":passw}, {"$set": {"clave": passwN}})
                stringArmada = "actualizar::"+str(passw)+"&"+str(passwN)
                client.publish("claves/", stringArmada)
                return ("Se actualizo la clave")
            else:
                return("No existe dicha clave")
        except Exception as e:
            return ("Ocurrio un problema: "+str(e))

api.add_resource(Claves, '/claves')

if _name_ == '_main_':
    app.run(debug=True, port = 8001)
