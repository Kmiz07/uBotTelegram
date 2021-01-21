uBotTelegram

Script micropython para la creacion de un bot para telegram en un ESP32.
uPYBot.py es el script que genera la conexion con telegram. Se crea un socket ssl y no se cierra a menos que falle la conexion con el servidor .
Este socket, una vez se crea, se mantiene abierto esperando los getupdates del servidor. Recibira un informe con los posibles mensajes y pasados aproximadamente 50segundos, un mensaje vacio si no se recibio ninguno.
En el momento de generar el bot, se le deben proporcionar, ademas del token del bot, el nombre de las dos funciones que funcionaran como receptoras de eventos.
Un evento se generara cada vez que el bot reciba mensajes. y el otro se generara periodicamente a modo de loop de programa, para incluir el runtime del mismo.
en el loop de programa se deben evitar bucles muy largos, y si se han de generar timers se debe usar los que el chip tiene por hardware o punteros de tiempo con if condicionales.
He incluido ademas del script uPYBot, el script conexion. Que es un ejemplo de configuracion del bot.
El bot puede enviar o recibir mensajes de texto multilinea, o puede enviar archivos, como fotos o documentos.
en los archivos, debe incluirse el canal de envio, el path del archivo, el nombre del comando, el nombre que le damos al archivo y el texto que se pondra de comentario.(este ultimo es opcional).
