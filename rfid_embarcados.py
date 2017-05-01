#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import signal

"""
    Lista com relação dos IDs autorizados 
"""
acessos_autorizados = [[227,41,93,116,227], [201,39,92,115,201], [225,95,12,103,225]]

"""
    Vou tentar importar os modulos abaixo, caso algum problema ocorra,
    sera lançada a exceção na sequencia
"""
try:
    import MFRC522
    import RPi.GPIO as GPIO
except ImportError as ie:
    print("Problema ao importar modulo {0}").format(ie)
    sys.exit()

"""
    Funcao que irá garantir que o root ou usuario com permissão de
    super-usuario irá executar a aplicação
"""
def check_user():
    if os.geteuid() != 0:
        print("Você deve executar o programa como super-usuario!")
        #print "Exemplo:\nsudo python {0}".format(os.path.realpath(__file__))
        print("Exemplo:\nsudo python {0}").format(__file__)
        sys.exit()


"""
    Captura o sinal gerado, no caso o que nos interessa é o sinal
    SIGINT(Interrupção do Terminal ou processo) e irá encerrar a aplicação
"""
def finalizar_app(signal,frame):
    global continue_reading
    print("\nCtrl+C pressionado, encerrando aplicação...")
    continue_reading = False
    GPIO.cleanup()


continue_reading = True

def main():

    check_user()

    # Handler do sinal SIGINT
    signal.signal(signal.SIGINT, finalizar_app)

    # Cria o objeto da class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    print("Portal Embarcados - Python é sucesso!")
    print("Pressione Ctrl-C para encerrar a aplicação.")

    while continue_reading:
        # Scan for cards    
        #(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)


        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            if uid in acessos_autorizados:
                    print("Acesso liberado!")
            else:
                    print("Sem acesso!")




if __name__ == "__main__":
    main()
