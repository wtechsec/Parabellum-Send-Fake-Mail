import smtplib
import traceback
from socket import gaierror
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..utils import logger

class SMTPConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket  = host + ':' + port
        self.server  = None
        self.sender = None
        self.recipients = None

        self.__connect()
        self.__start_tls()
        self.__eval_server_features()

    def __ehlo(self):
        try:
            self.server.ehlo()
            if not self.server.does_esmtp:
                logger.error('O servidor não suporta ESMTP')
                exit(1)
        except smtplib.SMTPHeloError:
            logger.error('O servidor não respondeu corretamente à saudação EHLO / HELO.')
            exit(1)

    def __connect(self):
        try:
            logger.info('Conectando ao socket SMTP (' + self.socket + ')...')
            self.server = smtplib.SMTP(self.host, self.port)
        except (gaierror, OSError):
            logger.error('Não foi possível estabelecer conexão com o soquete SMTP.')
            exit(1)

    def __start_tls(self):
        self.__ehlo()
        if not self.server.has_extn('starttls'):
            logger.error('O servidor MTP não oferece suporte a TLS.')
            exit(1)
        else:
            try:
                logger.info('Iniciando sessão TLS...')
                self.server.starttls()
            except RuntimeError:
                logger.error('O suporte SSL / TLS não está disponível para o seu interpretador Python.')
                exit(1)

    def __eval_server_features(self):
        self.__ehlo()

        if not self.server.has_extn('auth'):
            logger.error('Nenhum tipo AUTH detectado.')
            exit(1)

        server_auth_features = self.server.esmtp_features.get('auth').strip().split()
        supported_auth_features = { auth_type for auth_type in {'PLAIN', 'LOGIN'} if auth_type in server_auth_features }

        if not supported_auth_features:
            logger.error('O servidor SMTP não suporta AUTH PLAIN ou AUTH LOGIN. ')
            exit(1)

    def login(self, username, password):
        try:
            return self.server.login(username, password)
        except smtplib.SMTPAuthenticationError:
            logger.error('O servidor não aceitou a combinação de nome de usuário / senha.')
            return False
        except smtplib.SMTPNotSupportedError:
            logger.error('O comando AUTH não é compatível com o servidor.')
            exit(1)
        except smtplib.SMTPException:
            logger.error('Foi encontrado um erro durante a autenticação.')
            exit(1)

    def compose_message(self, sender, name, recipients, subject, html):
        self.sender = sender
        self.recipients = recipients

        message = MIMEMultipart('alternative')
        message.set_charset("utf-8")

        message["From"] = name + "<" +  self.sender + ">"
        message['Subject'] = subject
        message["To"] = ', '.join(self.recipients)

        body = MIMEText(html, 'html')
        message.attach(body)
        return message;

    def send_mail(self, message):
        try:
            logger.info('Enviando email phishing...')
            self.server.sendmail(self.sender, self.recipients, message.as_string())
            logger.success('phishing entregue!')
        except smtplib.SMTPException:
            logger.error('Incapaz de enviar mensagem. Verifique o remetente, os destinatários e o corpo da mensagem')
            logger.error(traceback.format_exc())
            exit(1)
