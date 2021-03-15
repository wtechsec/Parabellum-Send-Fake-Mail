import sys
import argparse
from spoofer.commands import cli, wizard

parser = argparse.ArgumentParser(description='MAIL SPOOFING', allow_abbrev=False)

##Comandos permitidos: "wizard" ou "cli"
subparsers = parser.add_subparsers(title='commands', dest='command', help='Allowed commands', required=True)
wizard_subparser = subparsers.add_parser('wizard', help='Use o assistente passo a passo')
wizard_subparser.set_defaults(func=wizard.run)

cli_subparser = subparsers.add_parser('cli', help='Passe argumentos diretamente')
cli_subparser.set_defaults(func=cli.run)

##Excluir mutuamente "--noauth" e "--username"
noauth_or_username = cli_subparser.add_mutually_exclusive_group(required=True)
noauth_or_username.add_argument('--noauth', dest='noauth', action='store_true', help='Desativar verificação de autenticação')
noauth_or_username.add_argument('--username', dest='username', type=str, help='SMTP username')

##Faça a senha obrigatória se "--username" estiver presente
cli_subparser.add_argument('--password', dest='password', required='--username' in sys.argv, type=str, help='Senha SMTP (necessária com --username)')

required = cli_subparser.add_argument_group('argumentos requeridos')
required.add_argument('--host', dest='host', required=True, type=str, help='SMTP hostname')
required.add_argument('--port', dest='port', type=int, required=True, help='SMTP port number')

##Argumentos de composição de email
required.add_argument('--sender', dest='sender', required=True, type=str, help='Endereço do remetente (por exemplo, spoofed@domain.com) ')
required.add_argument('--name', dest='name', required=True, type=str, help='Nome do remetente (por exemplo, John wiki) ')
required.add_argument('--recipients', dest='recipients', required=True, type=str, nargs='+', help='Endereços de destinatários (por exemplo, vítima@domínio.com ...) ')
required.add_argument('--subject', dest='subject', required=True, type=str, help='Subject line')
required.add_argument('--filename', dest='filename', required=True, type=str, help='Nome do arquivo do corpo da mensagem (por exemplo, exemplo.html) ')
