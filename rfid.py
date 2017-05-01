#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

"""
Função que é chamada assim que Ctrl+C é pressionado
"""
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

"""
Responsável por capturar o SIGINT gerado (Ctrl+C) e chamar a função end_read
"""
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

"""
Criando um objecto da class MFRC522
"""
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

"""
Entra em um loop infinito baseado na variavel global :( continue_reading, que ira mudar o seu valor assim que
a aplicação for interrompida e a função end_read() irá setar como False
"""
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    """
    Maioria das chamadas abaixo falam por si só, irei comentar as que achar interessante
    """
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    """
    Agora iremos receber o ID RFID e o status, e o nome Anticoll é baseado no proprio protocolo
    no Registrador ErrorReg bit3 verifica se houve colisão dos dados
    """
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    
        """
        Uma camada de segurança a mais, onde além de verificar o ID que recebemos podemos enviar a key dos chaveiros e tags
        e aguardar a autenticação
        Veja no datasheet MF1S70yyX.pdf Pagina: 11 - 8.6.3 Sector trailer
        E as rotinas para esta checagem segue abaixo.

        Usando a key abaixo é a chave de 6 bytes utilizada para 
        autenticar a comunicação maneira esta usando o MFAuthent 
        endereço 0x60 a 0x61

        OBS: Não irei utilizar isso em nossa aplicação!
        """
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
     
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        """
        Aqui é enviado a key do "fabricante", modo de autenticação 0x60 ou 0x61, Block Address e nosso uid
        """
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
