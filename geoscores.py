from bottle import *
from lxml import etree
import requests
import os
from sys import argv

futbolkey = os.environ["futbolkey"]

#Página de inicio de la aplicación
@route('/')
def consulta():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'matchsday', 'country':'es', 'limit':'4'}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("inicio.tpl", doc=doc)

#Página dónde realizaremos la consulta de la liga y la jornada que queremos localizar
@route('/localizalo')
def peticion():
    return template("peticion.tpl")

#Página dónde aparecerá la clasificación de primera división
@route('/clasificacion/ligasantander')
def clasificacion1():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'1'}
    r = requests.get(url_base, params = payload)
    if r.status_code==200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion1.tpl",doc=doc)

##Página dónde aparecerá la clasificación de segundo división
@route('/clasificacion/liga123')
def clasificacion2():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'2'}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion2.tpl", doc=doc)

#Página en la cual aparecerá la jornada Geolocalizada
@post('/localizados')
def resultado():
    #Recibimos los parámetros liga y jornada que el usario desea geolocalizar
    liga = request.forms.get('liga')
    jornada = request.forms.get('jornada')
    #Url's base de las apis a utilizar en ésta consulta
    url_base_mapa="maps.google.com/maps/api/geocode/xml?address="
    url_base_futbol = "http://apiclient.resultados-futbol.com/scripts/api/api.php"
    #Payload que necesitaremos para la consulta principal, que son los partidos de la jornada requerida por el usuario
    payload_futbol = {'key':futbolkey, 'format':'xml','req':'matchs','league':liga, 'round':jornada}
    #Variables que vamos a necesitar para construir la página y el mapa
    latitud=[]
    longitud=[]
    local=[]
    visitante=[]
    fecha=[]
    hora=[]
    resultado=[]
    #Realizamos la consulta a la api de resultados-fútbol
    r = requests.get(url_base_futbol, params=payload_futbol)
    #Si no devuelve que ha encontrado lo solicitado
    if r.status_code == 200:
        #Guardamos en doc la consulta para recorrer
        doc = etree.fromstring(r.text.encode('utf-8'))
        #Vamos a necesitar el equipo local, visitante, la fecha y hora y el resultado
        for l,v,f,h,m,q in zip(doc.xpath("//local"),doc.xpath("//visitor"),doc.xpath("//date"),doc.xpath("//hour"),doc.xpath("//minute"),doc.xpath("//result")):
            #Necesitamos las coordenadas del estadio, para ello haremos la consulta a Google Maps del Estadio "local"
            busqueda = 'Estadio+'+l.text.replace(" ","+")
            s = requests.get(url_base_mapa+busqueda)
            doc2 = etree.fromstring(s.text.encode('utf-8'))
            #Vamos almacenando en las listas los valores que luego utilizaremos
            latitud.append(doc2.xpath("//geometry/lat").text)
            longitud.append(doc2.xpath("//geometry/lng").text)
            local.append(l.text)
            visitante.append(v.text)
            fecha.append(f.text)
            hora.append(h.text+":"+m.text)
            resultado.append(q.text)
        #Le pasamos a la página los parámetro que va a necesitar para formarla    
        return template("localizados.tpl",lat=latitud, lng=longitud, local=local, visitante=visitante, fecha=fecha, hora=hora, resultado=resultado)
    else:
        #Si no encontró lo solicitado, devolvemos un mensaje para que el usuario sea consciente de lo ocurrido.
        return template("jornadanotfound.tpl")

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='0.0.0.0', port=8081)
