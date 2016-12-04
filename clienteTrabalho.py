from socket import * #socket
from threading import Thread # thread
import time

# definicao das variaveis
serverName = 'localhost' # ip do servidor
serverPort = 12000 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
nickname = ''
def iniciarConexao():
    tes = 1
    print 'Bem- vindo ao nosso chat, para mais informacoes digite //mais()'
    while tes:
        clientResponse = raw_input('Digite o seu nickname: ')
        try:
            nome = clientResponse.split()
            clientResponse = nome[0]
        except Exception as all:
            print"Erro 1"
            time.sleep(10)
            clientResponse = ''

        if clientResponse != '':
            tes = 0
            enviarServidor(clientResponse)
            nickname = clientResponse
            serverResponse = receberServidor()
            print serverResponse
        else:
            print "Porfavor Digite seu nome sem ser apenas espaco e tenha algum nome ou algo to tipo."
            tes = 1

def receberServidor():
    dado = clientSocket.recv(1024) # recebe do servidor a resposta
    return dado

def enviarServidor(arg):
    if arg == '':
        clientSocket.send(" ")
    else:
        clientSocket.send(arg)

def mais():
    print 'Digite //nick() para alterar o seu Nickname/n'
    print 'Digite //stop() para sair do chat'
iniciarConexao()
while 1:
    clientResponse = raw_input()
    if clientResponse == "//mais()":
        mais()
    if clientResponse == "//nick()":
        enviarServidor(clientResponse)
        serverResponse = receberServidor()
        print serverResponse
        clientResponse = input()
        enviarServidor(clientResponse)
        serverResponse = receberServidor()
        nickname = serverResponse
        print serverResponse
    else:
        enviarServidor(clientResponse)
        serverResponse = receberServidor()
        print serverResponse
        if serverResponse == "Ate a proxima!":
            time.sleep(1)
            clientSocket.close()
