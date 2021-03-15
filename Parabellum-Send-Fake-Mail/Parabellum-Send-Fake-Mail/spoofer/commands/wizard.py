from colorama import Fore
from getpass import getpass
from ..utils import logger, appdescription
from ..utils.userinput import prompt, get_required, get_optional, get_yes_no
from ..models.smtpconnection import SMTPConnection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os.path



def run(args):
    appdescription.print_description()

    host = get_required('SMTP host: ')
    port = None;

    while not port:
        try:
            port = int(get_required('SMTP port: '))
            if port < 0 or port > 65535:
                logger.error('Porta SMTP fora do intervalo(0-65535)')
                port = None
        except ValueError:
            logger.error('Porta SMTP sem conexão')
            port = None

    # Connect to SMTP over TLS
    connection = SMTPConnection(host, str(port))

    # Attempt login
    if not get_yes_no("Desabilitar Login(Y/N)?: ", 'n'):
        success = False
        while not success:
            success = connection.login(
                get_required('Usuario smtp: '),
                getpass()
            )
        logger.success('Sucesso Login efetuado no servidor SMTP')

    sender = get_required('Email de envio: ')
    sender_name = get_required('nome: ');

    recipients = [get_required('Email alvo: ')]
    if get_yes_no('Entre com outros alvos (Y/N)?: ', 'n'):
        recipient = True;
        while recipient:
            recipient = get_optional('Email alvo: ', None)
            if recipient:
                recipients.append(recipient)

    subject = get_required('Assunto: ')

    html = ''
    if get_yes_no('Carregar Template HTML (Y/N)?: ', 'n'):
        filename = get_required('Nome do arquivo HTML: ')
        with open(filename) as f:
            html = f.read()

    
    img = ''      
    if get_yes_no('Anexar Logo no corpo do email (Y/N)?: ', 'n'):         
        logo_filename = get_required('Nome do arquivo png: ')
        with open(logo_filename, 'rb') as f:
            img = f.read()
    
    else:
        logger.info('Linha de comando HTML')
        logger.info('Para sair, pressione CTRL+D')
        while True:
            try:
                line = prompt('>| ', Fore.LIGHTBLACK_EX)
                html += line + '\n'
            except EOFError:
                logger.success('Upload HTML efetuado')
                break

    # Compose MIME message
    message = connection.compose_message(
        sender,
        sender_name,
        recipients,
        subject,
        html
        
        
        
    )

    if get_yes_no('Enviar Email (Y/N)?: ', None):
        connection.send_mail(message)
