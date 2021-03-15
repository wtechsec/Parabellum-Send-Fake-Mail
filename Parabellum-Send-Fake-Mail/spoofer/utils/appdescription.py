from . import logger
from termcolor import colored
from pyfiglet import Figlet


description = """  SEND-FAKE-MAIL- PARA PENTEST (WTECHSEC)  
  MAIL SPOOFING""" 
  

def print_description():
    
    f = Figlet(font='slant')
    print(colored(f.renderText("PARABELLUM"), 'yellow')) #banner
    logger.bright('\n{0}'.format("#"*60))
    logger.header(description) 
    logger.bright('{0}\n'.format('#'*60))


