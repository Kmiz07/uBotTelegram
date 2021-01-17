import uPYbot,utime
import machine, esp32, ure
from machine import Pin
from utime import sleep
#######################################################################################
#             EVENTOS BOT (Nombres de eventos definidos al declarar el Bot            #
#######################################################################################

def evento_recepcion(datos_recibidos, miBot):
    
     pass
#         Esta funcion funciona como un evento de recepcion de get_updates.
#         En datos_recibidos, recibimos un objeto mensaje con la siguiente estructura:
#         ok = boolean que define si la respuesta fue satisfactoria.
#         vacio = boolean que dice si el mensaje es vacio 
#         indice = indice del mensaje
#         remite = nombre del remitente
#         remite_id = id del remitente
#         texto = texto del mensaje
#         chat_id = id del canal
#         chat_titulo = si venia de un canal, el titulo del mismo       
#         tipo = sera private si es mensaje privado o supergroup si viene de un canal
#         tiempo = puntero del tiempo del momento de la creacion del mensaje. esta definido desde el 1 de 1 de 2000, normalmente marcara 30 años mas
#         en miBot nos llega una referencia al bot creado.

def bucle_programa(miBot):

    #Esta funcion es el tipico loop de programa, aqui se debe introducir el codigo de manejo de programa
    #normalmente sera utilizado para lectura de pines o sensores
    #Importante no bloquear si no es estrictamente necesario con while true o similares, ya que periodicamente esta funcion sera llamada automaticamente
    #En miBot disponemos de una referencia al bot creado
     pass
    
################################################################################################
#                                 FIN EVENTOS BOT                                              #
################################################################################################
def main():
    
    Bot=uPYbot.uBot(configuracion.Telegram_Bot,'api.telegram.org', configuracion.Chat_Id, evento_recepcion, bucle_programa)
    Bot.send_message(Bot.canal,'Se ha iniciado programa (' + str(utime.time())+' segundos)')
    z=Bot.inicia()

   

                    




