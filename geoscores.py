#-*-coding:utf-8-*-
from bottle import *
from lxml import etree
import requests
import os
from sys import argv
import sys
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

futbolkey = os.environ["futbolkey"]
twitterkey = os.environ["consumerkey"]
twittersecret = os.environ["consumersecret"]

TOKENS = {}

url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'

def get_request_token():
    oauth = OAuth1(twitterkey, 
        client_secret = twittersecret,
        )
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    sys.stdout.write('Request token madafaka')
    sys.stdout.write(r.content)
    TOKENS["request_token"] = credentials.get('oauth_token')[0]
    TOKENS["request_token_secret"] = credentials.get('oauth_token_secret')[0]

def get_access_token(TOKENS):
    oauth = OAuth1(twitterkey,
        client_secret=twittersecret,
        resource_owner_key = TOKENS["request_token"],
        resource_owner_secret = TOKENS["request_token_secret"],
        verifier=TOKENS["verifier"])
    
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    TOKENS["access_token"] = credentials.get('oauth_token')[0]
    TOKENS["access_token_secret"] = credentials.get('oauth_token_secret')[0]


#Pagina de inicio de la aplicacion
@route('/')
def consulta():
    payload = {'key':futbolkey, 'format':'xml','req':'matchsday', 'country':'es', 'limit':'4'}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("inicio.tpl", doc=doc)

#Pagina donde realizaremos la consulta de la liga y la jornada que queremos localizar
@route('/localizalo')
def peticion():
    return template("peticion.tpl")

#Pagina donde aparecera la clasificacion de primera division
@post('/clasificacion/ligasantander')
@route('/clasificacion/ligasantander')
def clasificacion1():
    if request.method == "GET":
        payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'1'}
        jornada = 'Actual'
    elif request.method == "POST":
        jornada = request.forms.get('jornada')
        payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'1', 'round':jornada}
    r = requests.get(url_base, params = payload)
    if r.status_code==200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion1.tpl",doc=doc,jornada=jornada)

##Pagina donde aparecera la clasificacion de segunda division
@post('/clasificacion/liga123')
@route('/clasificacion/liga123')
def clasificacion2():
    if request.method == "GET":
        jornada = 'Actual'
        payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'2'}
    elif request.method == "POST":
        jornada = request.forms.get('jornada')
        payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'2', 'round':jornada}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion2.tpl", doc=doc, jornada=jornada)

#Pagina en la cual aparecera la jornada Geolocalizada
@post('/localizados')
def localizados():
    #Recibimos los parametros liga y jornada que el usario desea geolocalizar
    liga = request.forms.get('liga')
    jornada = request.forms.get('jornada')
    #Url's base de las apis a utilizar en esta consulta
    url_base_mapa="http://maps.google.com/maps/api/geocode/xml?address="
    #Payload que necesitaremos para la consulta principal, que son los partidos de la jornada requerida por el usuario
    payload_futbol = {'key':futbolkey, 'format':'xml','req':'matchs','league':liga, 'round':jornada}
    #Variables que vamos a necesitar para construir la pagina y el mapa
    latitud=[]
    longitud=[]
    local=[]
    visitante=[]
    fecha=[]
    hora=[]
    resultado=[]
    #Realizamos la consulta a la api de resultados-futbol
    r = requests.get(url_base, params=payload_futbol)
    #Si no devuelve que ha encontrado lo solicitado
    if r.status_code == 200:
        #Guardamos en doc la consulta para recorrer
        doc = etree.fromstring(r.text.encode('utf-8'))
        #Vamos a necesitar el equipo local, visitante, la fecha y hora y el resultado
        for l,v,f,h,m,q in zip(doc.xpath("//local"),doc.xpath("//visitor"),doc.xpath("//date"),doc.xpath("//hour"),doc.xpath("//minute"),doc.xpath("//result")):
            #Necesitamos las coordenadas del estadio, para ello haremos la consulta a Google Maps del Estadio "local"
            if l.text[1:] == 'Sporting':
                busqueda = 'Estadio+Sporting+Gijon'
            elif l.text[1:] =='Deportivo':
                busqueda = 'Estadio+Deportivo+Coruña'
            else:
                busqueda = 'Estadio+'+l.text.replace(" ","+")[1:]
            s = requests.get(url_base_mapa+busqueda)
            doc2 = etree.fromstring(s.text.encode('utf-8'))
            #Vamos almacenando en las listas los valores que luego utilizaremos
            latitud.append(float(doc2.xpath("//geometry/location/lat")[0].text))
            longitud.append(float(doc2.xpath("//geometry/location/lng")[0].text))
            local.append(l.text[1:].encode("utf-8"))
            visitante.append(v.text[1:].encode("utf-8"))
            fecha.append(f.text[-2:]+"/"+f.text[-5:-2]+f.text[1:5])
            hora.append(h.text[1:]+":"+m.text[1:])
            resultado.append(q.text[1:])
        #Le pasamos a la pagina los parametros que va a necesitar para formarla    
        return template("localizados.tpl",lat=latitud, lng=longitud, local=local, visitante=visitante, fecha=fecha, hora=hora, resultado=resultado)
    else:
        #Si no encontro lo solicitado, devolvemos un mensaje para que el usuario sea consciente de lo ocurrido.
        return template("jornadanotfound.tpl")


@get('/twit/<twit>')
def twit(twit):
    get_request_token()
    authorize_url = AUTHENTICATE_URL + TOKENS["request_token"]
    response.set_cookie("twit", twit,secret="some-secret-key")
    response.set_cookie("request_token", TOKENS["request_token"], secret="some-secret-key")
    response.set_cookie("request_token_secret", TOKENS["request_token_secret"], secret="some-secret-key")
    redirect(authorize_url)

@get('/callback')
def get_verifier():
    TOKENS["request_token"]=request.get_cookie("request_token", secret='some-secret-key')
    TOKENS["request_token_secret"]=request.get_cookie("request_token_secret", secret='some-secret-key')
    TOKENS["verifier"] = request.query.oauth_verifier
    get_access_token(TOKENS)
    response.set_cookie("access_token", TOKENS["access_token"],secret='some-secret-key')
    response.set_cookie("access_token_secret", TOKENS["access_token_secret"],secret='some-secret-key')
    redirect('/twitit')

@route('/twitit')
def enviar_tweet():
    cuerpo = request.get_cookie("twit", secret='some-secret-key')
    TOKENS["access_token"]=request.get_cookie("access_token", secret='some-secret-key')
    TOKENS["access_token_secret"]=request.get_cookie("access_token_secret", secret='some-secret-key')
    oauth = OAuth1(twitterkey,
        client_secret=twittersecret,
        resource_owner_key=TOKENS["access_token"],
        resource_owner_secret=TOKENS["access_token_secret"])
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    r = requests.post(url=url,
        data={"status":cuerpo},
        auth=oauth)
    if r.status_code == 200:
        redirect('/')
    else:
        return template("twitnotsend.tpl")



@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='0.0.0.0', port=argv[1])
