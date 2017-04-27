from bottle import *
from lxml import etree
import requests
import os
from sys import argv

futbolkey = os.environ["futbolkey"]

#Pagina de inicio de la aplicacion
@route('/')
def consulta():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
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
@route('/clasificacion/ligasantander')
def clasificacion1():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'1'}
    r = requests.get(url_base, params = payload)
    if r.status_code==200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion1.tpl",doc=doc)

##Pagina donde aparecera la clasificacion de segundo division
@route('/clasificacion/liga123')
def clasificacion2():
    url_base = ' http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'2'}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion2.tpl", doc=doc)

#Pagina en la cual aparecera la jornada Geolocalizada
@post('/localizados')
def localizados():
    #Recibimos los parametros liga y jornada que el usario desea geolocalizar
    liga = "1"
    jornada = "20"
    #Url's base de las apis a utilizar en esta consulta
    url_base_mapa="http://maps.google.com/maps/api/geocode/xml?address="
    url_base_futbol = "http://apiclient.resultados-futbol.com/scripts/api/api.php"
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
    r = requests.get(url_base_futbol, params=payload_futbol)
    #Si no devuelve que ha encontrado lo solicitado
    if r.status_code == 200:
        #Guardamos en doc la consulta para recorrer
        doc = etree.fromstring(r.text.encode('utf-8'))
        #Vamos a necesitar el equipo local, visitante, la fecha y hora y el resultado
        for l,v,f,h,m,q in zip(doc.xpath("//local"),doc.xpath("//visitor"),doc.xpath("//date"),doc.xpath("//hour"),doc.xpath("//minute"),doc.xpath("//result")):
            #Necesitamos las coordenadas del estadio, para ello haremos la consulta a Google Maps del Estadio "local"
            busqueda = 'Estadio+'+l.text.replace(" ","+")[1:]
            s = requests.get(url_base_mapa+busqueda)
            doc2 = etree.fromstring(s.text.encode('utf-8'))
            #Vamos almacenando en las listas los valores que luego utilizaremos
            latitud.append(doc2.xpath("//geometry/location/lat")[0].text)
            longitud.append(doc2.xpath("//geometry/location/lng")[0].text)
            local.append(l.text[1:])
            visitante.append(v.text[1:])
            fecha.append(f.text[1:])
            hora.append(h.text[1:]+":"+m.text[1:])
            resultado.append(q.text[1:])
        #Le pasamos a la pagina los parametros que va a necesitar para formarla    
        return template("localizados.tpl",lat=latitud, lng=longitud, local=local, visitante=visitante, fecha=fecha, hora=hora, resultado=resultado)
    else:
        #Si no encontrp lo solicitado, devolvemos un mensaje para que el usuario sea consciente de lo ocurrido.
        return template("jornadanotfound.tpl")

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='0.0.0.0', port=argv[1])
