#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
 
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
 
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

#################################################
# Código creado por https://telegram.me/alfiles #
#################################################

#------------------------------------------------
# Librerías necesarias                          #
#------------------------------------------------
# python3 -m pip install telegram --upgrade 
# python3 -m pip install python-telegram-bot --upgrade
#------------------------------------------------

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, InlineQueryHandler, CallbackQueryHandler)
from telegram import (InlineQueryResultArticle, ParseMode, InputTextMessageContent, MessageEntity, InlineKeyboardButton, InlineKeyboardMarkup)
import telegram	
import logging
from os import remove
from os import environ
from os import scandir, getcwd, rename
import zipfile

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#----------------------------------------------
# Función para descargarse un archivo de 
# internet
#----------------------------------------------
def DownloadFile(url, ruta, filename):
	import urllib.request
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	urllib.request.install_opener(opener)
	urllib.request.urlretrieve(url, ruta+filename)

#----------------------------------------------
# Función para leer los archivos de un 
# directorio
#----------------------------------------------
def ls(ruta = getcwd()):
	return [arch.name for arch in scandir(ruta) if arch.is_file()]

#----------------------------------------------
# Función para quitar los ' ' del nombre de
# los archivos
#----------------------------------------------	

def rename_files(ruta):
	for archivos in ls(ruta):
		if archivos.startswith("'") and archivos.endswith("'"):
			rename(archivos, archivos[1:-1])

#----------------------------------------------
# Función para contar los usuarios y/o grupos
# que se han añadido en la variables a la hora
# de inicializar el contenedor
#----------------------------------------------

def calcular(miembros):
	total=0
	contador=1
	while True:
		try:
			if environ[miembros+str(contador)]:
				total+=1
				contador+=1
		except:
			break
	return total

#----------------------------------------------
# Función para descargar .torrent y enviarlos 
# a una carpeta
#----------------------------------------------

def descargar_archivos(bot, update):
	
	#Añadimos los ID de usuarios a la lista "miembros_permitidos"
	if calcular("usuario") > 0:
		miembros_permitidos=[]
		for i in range (1,calcular("usuario")+1):
			miembros_permitidos.append(int(environ['usuario'+str(i)]))

	#Añadimos los ID de grupos a la lista "miembros_permitidos"
	if calcular("grupo") > 0:
		for i in range (1,calcular("grupo")+1):
			miembros_permitidos.append(int(environ['grupo'+str(i)]))

	m=update.message

	if int(m.chat.id) in miembros_permitidos:			

		ruta='/home/descargas/' 
		tmp='/zip/'

		filename=m.document.file_name	
		archivo = bot.getFile(m.document.file_id)	

		if filename.endswith('.zip'):				
			DownloadFile(archivo.file_path, tmp, filename)				
			zf = zipfile.ZipFile(tmp+filename, "r")
			for torrents in zf.namelist():
				if os.path.dirname(torrents)=='' and torrents.endswith('.torrent'):
					zf.extract(torrents, ruta)					
			zf.close()		
			rename_files()
			remove(tmp+filename)		
			bot.send_message(chat_id=m.chat.id, text="Se han guardado los archivos de <b>"+filename+"</b> en la carpeta", parse_mode="HTML") 			

		if filename.endswith('.torrent'):		
			DownloadFile(archivo.file_path, ruta, filename)
			bot.send_message(chat_id=m.chat.id, text="El archivo <b>"+filename+"</b> se ha guardado en la carpeta", parse_mode="HTML") 

	else:
		bot.send_message(chat_id=m.chat.id, text="No tienes permisos suficientes para utilizar el bot", parse_mode="HTML") 

#----------------------------------------------
# Función para descargar .torrent desde URL y 
# enviarlos a una carpeta
#----------------------------------------------

def descargar_archivos_url(bot, update, args):
	
	#Añadimos los ID de usuarios a la lista "miembros_permitidos"
	if calcular("usuario") > 0:
		miembros_permitidos=[]
		for i in range (1,calcular("usuario")+1):
			miembros_permitidos.append(int(environ['usuario'+str(i)]))

	#Añadimos los ID de grupos a la lista "miembros_permitidos"
	if calcular("grupo") > 0:
		for i in range (1,calcular("grupo")+1):
			miembros_permitidos.append(int(environ['grupo'+str(i)]))

	m=update.message

	if int(m.chat.id) in miembros_permitidos:			

		ruta='/home/descargas/' 
		tmp='/zip/'

		url = " ".join(args)
		
		if len(url)>0:
    		
			filename = url[url.rfind("/")+1:]

			if filename.endswith('.zip'):				
				DownloadFile(url, tmp, filename)
				zf = zipfile.ZipFile(tmp+filename, "r")
				for torrents in zf.namelist():
					if os.path.dirname(torrents)=='' and torrents.endswith('.torrent'):
						zf.extract(torrents, ruta)					
				zf.close()		
				rename_files()
				remove(tmp+filename)		
				bot.send_message(chat_id=m.chat.id, text="Se han guardado los archivos de <b>"+filename+"</b> en la carpeta", parse_mode="HTML") 			

			if filename.endswith('.torrent'):			
				DownloadFile(url, ruta, filename)
				bot.send_message(chat_id=m.chat.id, text="El archivo <b>"+filename+"</b> se ha añadido guardado en la carpeta", parse_mode="HTML") 
				
		else:
			bot.send_message(chat_id=m.chat.id, text="Debes indicar una URL", parse_mode="HTML") 

	else:
		bot.send_message(chat_id=m.chat.id, text="No tienes permisos suficientes para utilizar el bot", parse_mode="HTML") 


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.

	updater = Updater(environ['token'])
	dp = updater.dispatcher

	dp.add_handler(MessageHandler(Filters.document, descargar_archivos)) 
	dp.add_handler(CommandHandler("addtorrent", descargar_archivos_url, pass_args=True), group = 1) 	
	
    # Get the dispatcher to register handlers



    # log all errors
	dp.add_error_handler(error)

    # Start the Bot
	updater.start_polling(clean=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
