#!/bin/python

# costanti

VID1 = 0
TMP = 1
BAR = 2
GEI = 3

# Controllo esecuzione come root
import os
if os.geteuid() != 0:
    print "program must be run at root. (How else could I talk to devices?)"
    exit()



# Impostazione servizio di logging. Da qui in poi i print vanno solo in terminale; ogni informazione rilevante va loggata con logger.info
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("root")

handler = logging.FileHandler('logs/log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)



# Attivazione computer di bordo, caricamento interfaccia

logger.info("STARTING ONBOARD COMPUTER...")

import datetime
import time

logger.info(time.strftime("%Y-%m-%d %H:%M:%S"))

print '''
mmmmmm    mmmmmm   mmmmmm       mm mmmmmm    mmmmmm       mm     mmmmmm  mmm   mm 
##""""##  ##""""#m ""##""      ##  ##""""##  ##""""##    ####    ""##""  ###   ## 
##    ##  ##    ##   ##       ##   ##    ##  ##    ##    ####      ##    ##"#  ## 
#######   ######"    ##      ##    #######   #######    ##  ##     ##    ## ## ## 
##  "##m  ##         ##     m#"    ##    ##  ##  "##m   ######     ##    ##  #m## 
##    ##  ##       mm##mm  m#"     ##mmmm##  ##    ##  m##  ##m  mm##mm  ##   ### 
""    """ ""       """""" m#"      """""""   ""    """ ""    ""  """"""  ""   """ '''

print ""

print "-----------------------------------------------------------"

logger.info("loading interfacing submodule...")

try:
    import interface
except ImportError:
    logger.error("FATAL ERROR: interface.py submodule was NOT found. Machine operation is impossible, shutting down.", exc_info=True)
    exit()

logger.info("DONE!")



interface.startup(range(4))

logger.info("DONE.")

logger.info("This is RPI/BRAIN now ready to acquire data. It's "+time.strftime("%Y-%m-%d %H:%M:%S")+" and we are about to launch. Temperature is "+interface.get_reading(1)+" and it's a glorious day.")

#interface.take_still("test")

# importante: aggiunge una riga di separazione da i dati da acquisizioni precedenti

f = open("data/tmp","a")
f.write("-----------------------\n")
f.close()

f = open("data/bar","a")
f.write("-----------------------\n")
f.close()

f = open("data/gei","a")
f.write("-----------------------\n")
f.close()




logger.info("Beginning datalogging loop.")
logger.info("")


while True:

    
    # Genera la stringa di tempo corrispondente ad ora. Sul raspi questo codice non ha l'interpretazione di numero di secondi dall'epoca
    timehuman = time.strftime("%Y-%m-%d %H:%M:%S")
    t = str(time.time())



    # Fai una foto con VID1
    interface.take_still(t)

    
    # Salva i dati
    f = open("data/tmp","a")
    f.write(t+"\t"+interface.get_reading(TMP)+"\n")
    f.close()

    f = open("data/bar","a")
    f.write(t+"\t"+interface.get_reading(BAR)+"\n")
    f.close()

    f = open("data/gei","a")
    f.write(t+"\t"+interface.get_reading(GEI)+"\n")
    f.close()



    # Stampa una riga di feedback con i dati
    logger.info(timehuman+"\t"+interface.get_reading(1)+"degC\t"+interface.get_reading(2)+"atm\t" + interface.get_reading(3)+" uSv/h")



    time.sleep(2.5)
    time.sleep(2.5)


