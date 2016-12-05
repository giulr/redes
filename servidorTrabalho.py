# redes

from socket import * # sockets
from threading import Thread # thread
import time

#conn e coneccao com socet

#tratamento do conn.recv()
def receberCliente(conn):
    try:
        dado = conn.recv(1024)
    except Exception as all:
        print "Erro: 11 Desconectar cliente!"
        dado = '//stop()'
    return dado

#tratamento de conn.send()
def mandarTodosClientes(conn, mensagem):
    try:
        conn.send(mensagem)
        print conn
    except Exception as e:
        print "Erro: 22 Cliente nao existe!"

def reDadoCliente(conn,addr):
    dado = receberCliente(conn)
    nickname = dado
    sentence = "Ola " + nickname +"\n" + nickname + " >>"
    mandarTodosClientes(conn, sentence)
    print nickname + " entrou na sala..."
    while 1:
        dado = receberCliente(conn)
        if dado == "//stop()":
            print"Cliente [%s:%s]:Saiu" % (addr[0],addr[1])
            conn.close()
            break
        if dado == "//nick()":
            mandarTodosClientes(conn,"Digite seu novo nick: ")
            nickname = receberCliente(conn)
            sentence = "Seu novo nickname e: " + nickname
            mandarTodosClientes(conn, sentence)
        else:
            msgServer = dado
            #+ " \n" + nickname + ">>"
            for i in connections:
                mandarTodosClientes(connections, msgServer)
            print nickname + " disse: " + dado


#variaveis globais
serverName = 'localhost' # ip do servidor (em branco)
serverPort = 12000 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para "ouvir" conexoes
connections = []
addresses = []

while 1:
    print "Servidor TCP esperando conexoes na porta %d ..." % (serverPort)
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    print"Cliente [%s:%s]:Conectado!" % (addr[0], addr[1])
    t = Thread(target = reDadoCliente, args = (connectionSocket,addr))
    t.start()
    connections.append(connectionSocket);



    #sentence = connectionSocket.recv(1024) # recebe dados do cliente
    #capitalizedSentence = sentence.upper() # converte em letras maiusculas
    #print "Cliente %s enviou: %s, transformando em: %s" % (addr, sentence, capitalizedSentence)
    #connectionSocket.send(capitalizedSentence) # envia para o cliente o texto transformado
    #connectionSocket.close() # encerra o socket com o cliente
serverSocket.close() # encerra o socket do servidor
