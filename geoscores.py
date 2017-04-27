from bottle import *
from lxml import etree
import requests
import os
from sys import argv

futbolkey = os.environ["futbolkey"]

@route('/')
def consulta():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'matchsday', 'country':'es', 'limit':'4'}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("inicio.tpl", doc=doc)

@route('/localizalo')
def peticion():
    return template("peticion.tpl")

@route('/clasificacion/ligasantander')
def clasificacion1():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'1'}
    r = requests.get(url_base, params = payload)
    if r.status_code==200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion1.tpl",doc=doc)

@route('/clasificacion/liga123')
def clasificacion2():
    url_base = 'http://apiclient.resultados-futbol.com/scripts/api/api.php'
    payload = {'key':futbolkey, 'format':'xml','req':'tables', 'league':'2'}
    r = requests.get(url_base, params = payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("clasificacion2.tpl", doc=doc)


@post('/localizados')
def resultado():
    liga = request.forms.get('liga')
    jornada = request.forms.get('jornada')
    url_base_mapa="maps.google.com/maps/api/geocode/xml"
    url_base_futbol = "http://apiclient.resultados-futbol.com/scripts/api/api.php"
    payload_futbol = {'key':futbolkey, 'format':'xml','req':'matchs','league':liga, 'round':jornada}
    latitud=[]
    longitud=[]
    local=[]
    visitante=[]
    fecha=[]
    hora=[]
    resultado=[]
    r = requests.get(url_base_futbol, params=payload_futbol)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        for l,v,f,h,m,q in zip(doc.xpath("//local"),doc.xpath("//visitor"),doc.xpath("//date"),doc.xpath("//hour"),doc.xpath("//minute"),doc.xpath("//result")):
            busqueda = 'Estadio+'+l.text.replace(" ","+")
            s = requests.get(url_base_mapa+'?address='+busqueda)
            doc2 = etree.fromstring(s.text.encode('utf-8'))
            latitud.append(doc2.xpath("//geometry/lat").text)
            longitud.append(doc2.xpath("//geometry/lng").text)
            local.append(l.text)
            visitante.append(v.text)
            fecha.append(f.text)
            hora.append(h.text+":"+m.text)
            resultado.append(q.text)
            print latitud

        return template("localizados.tpl",lat=latitud, lng=longitud, local=local, visitante=visitante, fecha=fecha, hora=hora, resultado=resultado)
    else:
        return template("jornadanotfound.tpl")

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='0.0.0.0', port=8081)
