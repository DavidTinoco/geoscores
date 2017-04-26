from bottle import *
from lxml import etree
import requests
import os

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


@post('/resultados')
def resultado():
    liga = request.forms.get('liga')
    jornada = request.forms.get('jornada')
    url_base = "http://api.eventful.com/rest"
    k=open("key.txt","r")
    key = k.readline()
    k.close()
    payload = {'app_key':key, 'keywords':cate,'location':city,'date':'Future'}
    r = requests.get(url_base + '/events/search', params=payload)
    if r.status_code == 200:
        doc = etree.fromstring(r.text.encode('utf-8'))
        return template("resultados.tpl",doc=doc,city=city,cate=cate)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='0.0.0.0', port=argv[1])
