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
dbPropetarios = db.propetarios
dbPermisos = db.permisos
dbHorarios = db.horarios
dbCerraduras = db.cerraduras

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

class Propetario(Resource):

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self):
        json_data = request.get_json(force = True)
        idP = json_data['idP']
        informacion = json_data['informacion']
        guardar ={
            'idP' : idP,
            'Informacion' : informacion
            }
        dbPropetarios.insert_one(guardar).inserted_id
        return jsonify(idP = idP, Informacion = informacion)

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self):
        x = {}
        cursor = dbPropetarios.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
            x['Propetario#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idP':v[0], 'Informacion':v[1]}} for k,v in x.items()])
        return thejson

class PropetarioID(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idP):
        arreglo = []
        cursor = dbPropetarios.find({"idP": (idP)})
        for document in cursor:
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el id ' + idP})
            return thejson
        return thejson

    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idP):
        json_data = request.get_json(force = True)
        informacion = json_data['informacion']
        result = dbPropetarios.update_one(
                {'idP' : idP},
                {
                    "$set":{
                        'Informacion': informacion
                    }
                },
                upsert=False
            )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario que se va actualizar con el id ' + idP})
            return thejson
        else:    
            return jsonify(idP = idP, Informacion = informacion)
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idP):
        arreglo = []
        cursor = dbPropetarios.find({"idP": (idP)})
        try:
            for document in cursor:
                idP = document['idP'].replace('\\','')
                informacion = document['Informacion'].replace('\\','')
                arreglo=[idP, informacion]
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
            dbPropetarios.remove({"idP": idP})
            result = dbCerraduras.update(
                        {},
                        {
                            "$pull":{'Propetarios':{
                                "idP"+str(idP):idP
                            }
                        }
                        }
                    )
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario que se va eliminar con el id ' + idP})
            return thejson
class Horario(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self):
        json_data = request.get_json(force = True)
        idH = json_data['idH']
        dia = json_data['dia']
        horaP = json_data['hora1']
        horaS = json_data['hora2']
        timeZone = json_data['timeZone']
        guardar ={
            'idH': idH,
            'Dia': dia,
            'Hora1': horaP,
            'Hora2': horaS,
            'TimeZone': timeZone
            }
        dbHorarios.insert_one(guardar).inserted_id
        return jsonify(idH = idH, Dia = dia, Hora1 = horaP, Hora2 = horaS, TimeZone = timeZone)
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self):
        x = {}
        cursor = dbHorarios.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idH = document['idH'].replace('\\','')
            dia = document['Dia'].replace('\\','')
            horaP = document['Hora1'].replace('\\','')
            horaS = document['Hora2'].replace('\\','')
            timeZone = document['TimeZone'].replace('\\','')
            arreglo=[idH, dia, horaP, horaS, timeZone]
            x['Dia#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idH:':v[0], 'Dia:':v[1], 'Hora1:':v[2], 'Hora2:':v[3], 'TimeZone:':v[4]}} for k,v in x.items()])
        return thejson
class HorarioID(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idD):
        arreglo = []
        cursor = dbHorarios.find({"idH": (idD)})
        for document in cursor:
            idH = document['idH'].replace('\\','')
            dia = document['Dia'].replace('\\','')
            horaP = document['Hora1'].replace('\\','')
            horaS = document['Hora2'].replace('\\','')
            timeZone = document['TimeZone'].replace('\\','')
            arreglo=[idH, dia, horaP, horaS, timeZone]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idH:':arreglo[0], 'Dia:':arreglo[1], 'Hora1:':arreglo[2], 'Hora2:':arreglo[3], 'TimeZone:':arreglo[4]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe el Dia con el id ' + idD})
            return thejson
        return thejson
    # Aca se indica que este servicio requiere de autorización.
   # @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idD):
        json_data = request.get_json(force = True)
        dia = json_data['dia']
        horaP = json_data['hora1']
        horaS = json_data['hora2']
        timeZone = json_data['timeZone']
        result = dbHorarios.update_one(
                {'idH' : idD},
                {
                    "$set":{
                        'Dia': dia,
                        'Hora1': horaP,
                        'Hora2': horaS,
                        'TimeZone': timeZone
                    }
                },
                upsert=False
            )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Dia que se va actualizar con el id ' + idD})
            return thejson
        else:    
            return jsonify(idD = idD, Dia = dia, Hora1 = horaP, Hora2 = horaS, timeZone = timeZone)
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idD):
        arreglo = []
        cursor = dbHorarios.find({"idH": (idD)})
        try:
            for document in cursor:
                idD = document['idH'].replace('\\','')
                dia = document['Dia'].replace('\\','')
                horaP = document['Hora1'].replace('\\','')
                horaS = document['Hora2'].replace('\\','')
                timeZone = document['TimeZone'].replace('\\','')
                arreglo=[idD, dia, horaP, horaS, timeZone]
            thejson = json.dumps([{'idH:':arreglo[0], 'Dia:':arreglo[1], 'Hora1:':arreglo[2], 'Hora2:':arreglo[3], 'TimeZone:':arreglo[4]}])
            dbHorarios.remove({"idH": idD})
            result = dbCerraduras.update(
                        {},
                        {
                            "$pull":{'Horarios':{
                                "idH"+str(idD):idD
                            }
                        }
                        }
                    )
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Horario que se va eliminar con el id ' + idD})
            return thejson
class Cerradura(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self):
        json_data = request.get_json(force = True)
        idC = json_data['idC']
        estadoActual = json_data['EstadoActual']
        healthCheck = json_data['HealthCheck']
        horarios = json_data['Horarios']
        propetarios = json_data['Propetarios']
        guardar ={
            'idC': idC,
            'EstadoActual': estadoActual,
            'HealthCheck': healthCheck,
            'Horarios': horarios,
            'Propetarios': propetarios
            }
        dbCerraduras.insert_one(guardar).inserted_id
        return jsonify(idH = idC, EstadoActual = estadoActual, HealthCheck = healthCheck, Horarios = horarios, Propetarios = propetarios)
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self):
        x = {}
        cursor = dbCerraduras.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idC = document['idC'].replace('\\','')
            estadoActual = document['EstadoActual'].replace('\\','')
            healthCheck = document['HealthCheck'].replace('\\','')
            horarios = document['Horarios']
            propetarios = document['Propetarios']
            arreglo=[idC, estadoActual, healthCheck, horarios, propetarios]
            x['Cerradura#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idC:':v[0], 'EstadoActual:':v[1], 'HealthCheck:':v[2], 'Horarios:':v[3], 'Propetarios:':v[4]}} for k,v in x.items()])
        return thejson
class CerraduraID(Resource):
    # Aca se indica que este servicio requiere de autorización.
   # @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idC):
        arreglo = []
        cursor = dbCerraduras.find({"idC": (idC)})
        for document in cursor:
            idH = document['idC'].replace('\\','')
            estadoActual = document['EstadoActual'].replace('\\','')
            healthCheck = document['HealthCheck'].replace('\\','')
            horarios = document['Horarios']
            propetarios = document['Propetarios']
            arreglo=[idC, estadoActual, healthCheck, horarios, propetarios]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idC:':arreglo[0], 'EstadoActual:':arreglo[1], 'HealthCheck:':arreglo[2], 'Horarios:':arreglo[3], 'Propetarios:':arreglo[4]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el id ' + idC})
            return thejson
        return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idC):
        json_data = request.get_json(force = True)
        estadoActual = json_data['EstadoActual']
        healthCheck = json_data['HealthCheck']
        result = dbCerraduras.update_one(
                {'idC' : idC},
                {
                    "$set":{
                        'EstadoActual': estadoActual,
                        'HealthCheck': healthCheck
                    }
                },
                upsert=False
            )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe la cerradura que se va actualizar con el id ' + idC})
            return thejson
        else:    
            return jsonify(idC = idC, EstadoActual = estadoActual, HealthCheck = healthCheck)
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idC):
        arreglo = []
        cursor = dbCerraduras.find({"idC": (idC)})
        try:
            for document in cursor:
                idC = document['idC'].replace('\\','')
                estadoActual = document['EstadoActual'].replace('\\','')
                healthCheck = document['HealthCheck'].replace('\\','')
                horarios = document['Horarios']
                propetarios = document['Propetarios']
                arreglo=[idC, estadoActual, healthCheck, horarios, propetarios]
            thejson = json.dumps([{'idC:':arreglo[0], 'EstadoActual:':arreglo[1], 'HealthCheck:':arreglo[2], 'Horarios:':arreglo[3], 'Propetarios:':arreglo[4]}])
            dbCerraduras.remove({"idC": idC})
            result = dbPermisos.update(
                        {},
                        {
                            "$pull":{'Cerraduras':{
                                "idC"+str(idC):idC
                            }
                        }
                        }
                    )
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe la cerradura que se va eliminar con el id ' + idD})
            return thejson
class CerraduraIDHorarios(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self, idC):
        json_data = request.get_json(force = True)
        idH = json_data['id']
        cursor = dbHorarios.find({"idH": idH}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Horario con el id ' + idH})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Horarios.idH"+str(idH):idH}).count()
            if cursor > 0:
                thejson = json.dumps({'Respuesta': 'Ya existe el Horario con el id ' + idH + ' en la cerradura ' +idC})
                return thejson
            else:
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Horarios':{
                                "idH"+str(idH):idH
                            }
                        }
                        }
                    )
                    return jsonify(idH = idH)
                except:
                    thejson = json.dumps({'ERROR': "ERROR"})
                    return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idC):
        arreglo = []
        cursor = dbCerraduras.find(
                {"idC": (idC)},
            )
        for document in cursor:
            idC = document['idC'].replace('\\','')
            horarios = document['Horarios']
            arreglo=[idC, horarios]
        thejson = json.dumps([{'idC:':arreglo[0], 'Horarios:':arreglo[1]}])
        return thejson
class CerraduraIDHorariosID(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idC, idH):
        arreglo = []
        cursor = dbCerraduras.find(
                {"idC": (idC), "Horarios.idH" + str(idH):(idH)},
                {"idC":1, "Horarios":1}
            )
        try:
            for document in cursor:
                Horarios = document['Horarios']
                for horario in Horarios:
                    idH = horario["idH" + str(idH)]
                    arreglo=[idC, idH]
            thejson = json.dumps([{'idC':arreglo[0], 'idH':arreglo[1]}])
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Horario con el id ' + idH + ' en la cerradura con el id ' + idC})
            return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idC, idH):
        json_data = request.get_json(force = True)
        idN = json_data['id']
        cursor = dbHorarios.find({"idH":idH}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Horario con el id ' + idH})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Horarios.idH"+str(idH): idH}).count()
            if cursor == 0:
                thejson = json.dumps({'Respuesta': 'No existe el Horario con el id ' + idH + ' en la cerradura con id '+ idC})
                return thejson
            else:       
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            '$pull':{
                                'Horarios': {'idH'+str(idH):idH}
                             }
                         }
                    )
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Horarios':{
                                "idH"+str(idN):idN
                            }
                        }
                        }
                    )
                    thejson = json.dumps([{'idC':idC, 'idH':idN}])
                    return thejson
                except:
                    thejson = json.dumps({'ERROR': 'ERROR'})
                    return thejson
     # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idC, idH):
        cursor = dbCerraduras.find({"idC":idC, "Horarios.idH"+str(idH):idH}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el id ' + idC + ' y el horario a borrar con el id ' + idH})
            return thejson
        else:
            try:
                result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$pull":{'Horarios':{
                                "idH"+str(idH):idH
                            }
                        }
                        }
                    )
                thejson = json.dumps([{'idC':idC, 'idH':idH}])
                return thejson
            except:
                thejson = json.dumps({'ERROR': 'ERROR'})
                return thejson
class CerraduraIDPropetarios(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self, idC):
        json_data = request.get_json(force = True)
        idP = json_data['id']
        cursor = dbPropetarios.find({"idP": idP}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Propetaario con el id ' + idP})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Propetarios.idP"+str(idP):idP}).count()
            if cursor > 0:
                thejson = json.dumps({'Respuesta': 'Ya existe el Propetario con el id ' + idP + ' en la cerradura ' +idC})
                return thejson
            else:
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Propetarios':{
                                "idP"+str(idP):idP
                            }
                        }
                        }
                    )
                    return jsonify(idP = idP)
                except:
                    thejson = json.dumps({'ERROR': "ERROR"})
                    return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idC):
        arreglo = []
        cursor = dbCerraduras.find(
                {"idC": (idC)},
            )
        for document in cursor:
            propetarios = document['Propetarios']
            arreglo=[idC, propetarios]
        thejson = json.dumps([{'idC:':arreglo[0], 'Propetarios:':arreglo[1]}])
        return thejson
class CerraduraIDPropetariosID(Resource):
     # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idC, idP):
        arreglo = []
        cursor = dbCerraduras.find(
                {"idC": (idC), "Propetarios.idP" + str(idP):(idP)},
                {"idC":1, "Propetarios":1}
            )
        try:
            for document in cursor:
                propetarios = document['Propetarios']
                for propetario in propetarios:
                    idP = propetario["idP" + str(idP)]
                    arreglo=[idC, idP]
            thejson = json.dumps([{'idC':arreglo[0], 'idP':arreglo[1]}])
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el id ' + idP + ' en la cerradura con el id ' + idC})
            return thejson
     # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idC, idP):
        json_data = request.get_json(force = True)
        idN = json_data['id']
        cursor = dbPropetarios.find({"idP":idP}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el id ' + idP})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Propetarios.idP"+str(idP): idP}).count()
            if cursor == 0:
                thejson = json.dumps({'Respuesta': 'No existe el Propetario con el id ' + idP + ' en la cerradura con id '+ idC})
                return thejson
            else:       
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            '$pull':{
                                'Propetarios': {'idP'+str(idP):idP}
                             }
                         }
                    )
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Propetarios':{
                                "idP"+str(idN):idN
                            }
                        }
                        }
                    )
                    thejson = json.dumps([{'idC':idC, 'idP':idN}])
                    return thejson
                except:
                    thejson = json.dumps({'ERROR': 'ERROR'})
                    return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idC, idP):
        cursor = dbCerraduras.find({"idC":idC, "Propetarios.idP"+str(idP):idP}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el id ' + idC + ' y el Propetario a borrar con el id ' + idP})
            return thejson
        else:
            try:
                result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$pull":{'Propetarios':{
                                "idP"+str(idP):idP
                            }
                        }
                        }
                    )
                thejson = json.dumps([{'idC':idC, 'idP':idP}])
                return thejson
            except:
                thejson = json.dumps({'ERROR': 'ERROR'})
                return thejson
class Permisos(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self):
        json_data = request.get_json(force = True)
        idV = json_data['idV']
        dirrecion = json_data['Dirrecion']
        cerraduras = json_data['Cerraduras']
        guardar ={
            'idV': idV,
            'Dirrecion': dirrecion,
            'Cerraduras': cerraduras
            }
        dbPermisos.insert_one(guardar).inserted_id
        return jsonify(idV = idV, Dirrecion = dirrecion, Cerraduras = cerraduras)
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self):
        x = {}
        cursor = dbPermisos.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idV = document['idV'].replace('\\','')
            dirrecion = document['Dirrecion'].replace('\\','')
            cerraduras = document['Cerraduras']
            arreglo=[idV, dirrecion, cerraduras]
            x['Permiso#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idV:':v[0], 'dirrecion:':v[1], 'cerraduras:':v[2]}} for k,v in x.items()])
        return thejson
class PermisosID(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idV):
        arreglo = []
        cursor = dbPermisos.find({"idV": (idV)})
        for document in cursor:
            idV = document['idV'].replace('\\','')
            dirrecion = document['Dirrecion'].replace('\\','')
            cerraduras = document['Cerraduras']
            arreglo=[idV, dirrecion, cerraduras]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idV:':arreglo[0], 'Dirrecion:':arreglo[1], 'Cerraduras:':arreglo[2]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe el Permiso con el id ' + idV})
            return thejson
        return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idV):
        json_data = request.get_json(force = True)
        dirrecion = json_data['Dirrecion']
        result = dbPermisos.update_one(
                {'idV' : idV},
                {
                    "$set":{
                        'Dirrecion': dirrecion
                    }
                },
                upsert=False
            )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe el permiso que se va actualizar con el id ' + idV})
            return thejson
        else:    
            return jsonify(idV = idV, Dirrecion = dirrecion)
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idV):
        arreglo = []
        cursor = dbPermisos.find({"idV": (idV)})
        try:
            for document in cursor:
                idV = document['idV'].replace('\\','')
                dirrecion = document['Dirrecion'].replace('\\','')
                cerraduras = document['Cerraduras']
                arreglo=[idV, dirrecion, cerraduras]
            thejson = json.dumps([{'idV:':arreglo[0], 'dirrecion:':arreglo[1], 'cerraduras:':arreglo[2]}])
            dbPermisos.remove({"idV": idV})
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el permiso que se va eliminar con el id ' + idP})
            return thejson
class PermisosIDCerradura(Resource):
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def post(self, idV):
        json_data = request.get_json(force = True)
        idC = json_data['id']
        cursor = dbCerraduras.find({"idC": idC}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el id ' + idC})
            return thejson
        else:
            cursor = dbCerraduras.find({"idV":idV, "Cerraduras.idC"+str(idC):idC}).count()
            if cursor > 0:
                thejson = json.dumps({'Respuesta': 'Ya existe la Cerradura con el id ' + idC + ' en el permiso' +idV})
                return thejson
            else:
                try:
                    result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            "$push":{'Cerraduras':{
                                "idC"+str(idC):idC
                            }
                        }
                        }
                    )
                    return jsonify(idC = idC)
                except:
                    thejson = json.dumps({'ERROR': "ERROR"})
                    return thejson
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idV):
        arreglo = []
        cursor = dbPermisos.find(
                {"idV": (idV)},
            )
        for document in cursor:
            cerraduras = document['Cerraduras']
            arreglo=[idV, cerraduras]
        thejson = json.dumps([{'idV:':arreglo[0], 'Cerraduras:':arreglo[1]}])
        return thejson
class PermisosIDCerraduraID(Resource):
    # Aca se indica que este servicio requiere de autorización.
    #@app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def get(self, idV, idC):
        arreglo = []
        cursor = dbPermisos.find(
                {"idV": (idV), "Cerraduras.idC" + str(idC):(idC)},
                {"idV":1, "Cerraduras":1}
            )
        try:
            for document in cursor:
                cerraduras = document['Cerraduras']
                for cerradura in cerraduras:
                    idC = cerradura["idC" + str(idC)]
                    arreglo=[idV, idC]
            thejson = json.dumps([{'idV':arreglo[0], 'idC':arreglo[1]}])
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Cerradura con el id ' + idC + ' en la Permiso con el id ' + idV})
            return thejson
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def put(self, idV, idC):
        json_data = request.get_json(force = True)
        idN = json_data['id']
        cursor = dbCerraduras.find({"idC":idC}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Cerraduras con el id ' + idC})
            return thejson
        else:
            cursor = dbPermisos.find({"idV":idV, "Cerraduras.idC"+str(idC): idC}).count()
            if cursor == 0:
                thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el id ' + idC + ' en el Permiso con id '+ idV})
                return thejson
            else:       
                try:
                    result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            '$pull':{
                                'Cerraduras': {'idC'+str(idC):idC}
                             }
                         }
                    )
                    result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            "$push":{'Cerraduras':{
                                "idC"+str(idN):idN
                            }
                        }
                        }
                    )
                    thejson = json.dumps([{'idV':idV, 'idC':idN}])
                    return thejson
                except:
                    thejson = json.dumps({'ERROR': 'ERROR'})
                    return thejson
    # Aca se indica que este servicio requiere de autorización.
    @app.route("/api/private")
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @requires_auth
    def delete(self, idV, idC):
        cursor = dbPermisos.find({"idV":idV, "Cerraduras.idC"+str(idC):idC}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el id ' + idC + ' en el Permiso a borrar con el id ' + idV})
            return thejson
        else:
            try:
                result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            "$pull":{'Cerraduras':{
                                "idC"+str(idC):idC
                            }
                        }
                        }
                    )
                thejson = json.dumps([{'idV':idV, 'idC':idC}])
                return thejson
            except:
                thejson = json.dumps({'ERROR': 'ERROR'})
                return thejson
api.add_resource(Propetario, '/propetarios')
api.add_resource(PropetarioID, '/propetarios/<idP>')
api.add_resource(Horario, '/horarios')
api.add_resource(HorarioID, '/horarios/<idD>')
api.add_resource(Cerradura, '/cerraduras')
api.add_resource(CerraduraID, '/cerraduras/<idC>')
api.add_resource(CerraduraIDHorarios, '/cerraduras/<idC>/horarios')
api.add_resource(CerraduraIDHorariosID, '/cerraduras/<idC>/horarios/<idH>')
api.add_resource(CerraduraIDPropetarios, '/cerraduras/<idC>/propetarios')
api.add_resource(CerraduraIDPropetariosID, '/cerraduras/<idC>/propetarios/<idP>')
api.add_resource(Permisos, '/permisos')
api.add_resource(PermisosID, '/permisos/<idV>')
api.add_resource(PermisosIDCerradura, '/permisos/<idV>/cerraduras')
api.add_resource(PermisosIDCerraduraID, '/permisos/<idV>/cerraduras/<idC>')


if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
