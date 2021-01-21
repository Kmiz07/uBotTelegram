import network,gc,utime,ujson,machine
import usocket as socket
import ussl,ure,uerrno
import ubinascii
import uos
import utime
from machine import Pin
from utime import sleep
import esp32
class uBot():
    def chip_reset(self):
        self.resetear=True
            
    def usock_ssl(self):
#         inicia un socket ssl. si todo va bien retorna el socket, sino retorna None
        if network.WLAN(network.STA_IF).isconnected():
            addr = socket.getaddrinfo(self.host, 443)[0][-1]
            s0 = socket.socket()
            s0.connect(addr)
            s0.setblocking(False)
            print(gc.mem_free())
            s = ussl.wrap_socket(s0)
            return s
        else:
            return None
    
    def __init__(self,token , host,   funcion, bucle):
#         inicia un bot. precisa el token de telegram  y dos funciones
#         la funcion 'funcion' es la que sera llamada cuando se reciban datos
#         la funcion bucle es llamada a cada ciclo de lectura de datos, por lo que sera usada a modo de loop de programa
        self.token = token
        self.host = host
        self.datos_recibidos = ''
        self.funcion = funcion
        self.id_update = 0
        self.usock = self.usock_ssl()
        self.timeout = 50
        self.limit = 1
        self.bucle = bucle
        self.puntero_tiempo = utime.time()
        self.resetear = False

    def send_message(self,id_canal,mensaje):
#         envia mensaje de texto al canal/usuario elegido
        peticion = b'GET /bot%s/sendMessage?chat_id=%s&parse_mode=HTML&text=%s HTTP/1.1\r\nHost: api.telegram.org\r\n\r\n' %(self.token, id_canal, mensaje)      
        self.usock.write(peticion)
        data = self.usock.read()
        bufer=b'' 
        while data:
            bufer += data
            data = self.usock.read()
        return bufer
     
    def procesa_entrada(self,bufer_de_entrada):
#         procesa la cabecera y retorna el json de la respuesta de servidor
        separa_por_lineas = ure.compile('[\r\n]')
        separa_por_espacios = ure.compile('\s')
        lineas=separa_por_lineas.split(bufer_de_entrada.decode())
        fin_cabecera = 0#para asegurar que fue el fin de cabecera
        for linea in lineas:
            partes_de_linea = separa_por_espacios.split(linea)
            if partes_de_linea[0] == 'HTTP/1.1':
                codigo_pagina = partes_de_linea[1]
                print('codigo pagina = ',codigo_pagina)
            if partes_de_linea[0] == 'Content-Length:':
                longitud_respuesta = int(partes_de_linea[1])
                print('longitud de respuesta = ',str(longitud_respuesta))
            if partes_de_linea[0] == '':
                fin_cabecera +=1
                if fin_cabecera == 2:
#                     retorna la informacion interesante para el bot(el json del mensaje)
                    return self.usock.read(longitud_respuesta)
            else:
                fin_cabecera = 0
                
    def inicia(self):
#         comienza la comunicacion con telegram y espera mensajes
        esperando_update = False
        while True:
            if esperando_update == False:
                try:
                    gc.collect()
                    self.puntero_tiempo = utime.time()#marca tiempo de peticion para comprobar correcto timeout
                    peticion = b"GET /bot%s/getUpdates?offset=%s&timeout=%s&limit=%s  HTTP/1.1\r\nHost: api.telegram.org\r\n\r\n" %(self.token, str(self.id_update), str(self.timeout), str(self.limit))                       
                    print(peticion)
                    self.usock.write(peticion)
                    esperando_update=True#Ahora si esta esperando update
                except OSError as exc:
                    print(exc.args[0])
                    print('error enviando peticion')
                    self.usock = self.usock_ssl()
                    esperando_update = False
                    print('------------------------------------------------------------------error de envio--------------------------------------------------------------')
                    self.usock.write(peticion)
 
            try:
                data = self.usock.readline()
                bufer = b''
                while True:
                    if data == b'' or data == b'\r\n' or data == None:
                        break
                    bufer += data
                    data = self.usock.readline()
                if bufer != b'':
                    mensaje_util = self.procesa_entrada(bufer)
                    print('-------------------respuesta------------------------',utime.time())
                    print(mensaje_util)
                    print('--------------------------------------------------')
                    bufer = mensaje_util
            except OSError as exc:
                print('error recibiendo datos')
                machine.reset()            
            if bufer != b'' and bufer != None:
                try:
                    retorno = self.obj_msg(ujson.loads(bufer))
                except:
                    print('fallo en json')
                    retorno.vacio = True
                esperando_update= False
                if retorno.vacio == False:
                    print(retorno.vacio)
                    print(retorno.indice)
                    if retorno.indice != 0:
                        self.id_update = retorno.indice + self.limit
                    self.funcion(retorno, self)#llama al evento de recepcion de datos
            if utime.time() - 55 > self.puntero_tiempo:#si se desbordo oftime.... se resetea el chip(por desarrollar este punto)
                self.usock = self.usock_ssl()
                esperando_update = False
                print('----------------------------------------------------------------------timeout-------------------------------------------------------------------------')


            self.bucle(self)
            
    class mensaje():
        ok = False
        vacio = True 
        indice = 0
        remite = '' 
        remite_id = 0
        texto = ''
        chat_id = 0
        chat_titulo = ''        
        tipo = ''
        tiempo = 0
    def obj_msg(self,z):
        mensaje = self.mensaje()       
        if z['ok']:
            mensaje.ok = True
            try:
                if z['result'] != []:
                    mensaje.vacio = False
                    mensaje.indice = z['result'][0]['update_id']
                    mensaje.remite = z['result'][0]['message']['from']['username']
                    mensaje.remite_id = z['result'][0]['message']['from']['id']
                    mensaje.texto = z['result'][0]['message']['text']
                    mensaje.chat_id = z['result'][0]['message']['chat']['id']
                    mensaje.tipo = z['result'][0]['message']['chat']['type']
                    mensaje.tiempo = z['result'][0]['message']['date']
                    if z['result'][0]['message']['chat']['type'] == 'supergroup':
                        mensaje.chat_titulo = z['result'][0]['message']['chat']['title']
                    else:
                        mensaje.chat_titulo = ''
                
                    if 'update_id' in z['result'][0] == False: mensaje.vacio = True
                        
                else:
                    mensaje.vacio = True
            except:
                pass
        else:
            mensaje.ok = False
        return mensaje

    def envia_archivo_multipart(self,canal_id,arch,comando,nombre,comentario=''):
        limite = ubinascii.hexlify(uos.urandom(16)).decode('ascii')
        cadenados = b'--'
        cadenados += limite
        cadenados += '\r\n'
        cadenados += b'content-disposition: form-data; name= "chat_id"\r\n\r\n'
        cadenados += canal_id
        cadenados += b'\r\n--'
        cadenados += limite
        cadenados += b'\r\n'
        if comentario != '':
            cadenados += b'content-disposition: form-data; name= "caption"\r\n\r\n'
            cadenados += comentario
            cadenados += b'\r\n--'
            cadenados += limite
            cadenados += b'\r\n'    
        cadenados += b'content-disposition: form-data; name= "'
        cadenados += nombre
        cadenados += b'"; filename= "file.jpg"\r\n'
        cadenados += b'Content-Type: image-jpeg\r\n\r\n'
        cadenatres= b'\r\n--'
        cadenatres += limite
        cadenatres += b'--\r\n'
        gc.collect()
        x = uos.stat(arch)
        tamarch = x[6]
        Tamanyo_total=str(tamarch+len(cadenados)+len(cadenatres))
        archivo = ""
        gc.collect()
        cadenainicio = b'POST /bot'
        cadenainicio += self.token
        cadenainicio += b'/'
        cadenainicio += comando
        cadenainicio += b' HTTP/1.1\r\n'
        cadenainicio += b'Host: api.telegram.org\r\n'
        cadenainicio += b'User-Agent: KmiZbot/v1.0\r\n'
        cadenainicio += b'Accept: */*\r\n'
        cadenainicio += b'Content-Length: '
        cadenainicio += Tamanyo_total
        cadenainicio += b'\r\n'
        cadenainicio += b'Content-Type: multipart/form-data; boundary='
        cadenainicio += limite
        cadenainicio += b'\r\n\r\n'
        self.usock.write(cadenainicio)                                                  
        self.usock.write(cadenados)                                                      
        f = open(arch, "rb")
        contenido = bytearray(f.read(512),'utf-8')
        while contenido:
            self.usock.write(contenido)
            contenido = bytearray(f.read(512),'utf-8')
            gc.collect()
        f.close()
        self.usock.write(cadenatres)
        gc.collect()
        data = self.usock.readline()
        while data:
#             if '200 OK' in data:break
            data = self.usock.readline()
#         print(data)

    