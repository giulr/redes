from socket import * # sockets
from threading import Thread # thread
import time

#conn e coneccao com socet

#tratamento do conn.recv()
def receberCliente(conn):
    try:
        dado = conn.recv(1024)
    except Exception as all:
        print "Erro: S:12 Desconectar cliente!"
        dado = '//stop()'
        conn.close()
    return dado

#tratamento de conn.send()
def mandarCliente(conn, mensagem):
    try:
        conn.send(mensagem)
    except Exception as e:
        print "Erro: S:22 Cliente nao existe!"

def removeConnAddr(addr):
    posicao = posaddr(addr)
    del connList[posicao]
    del addrList[posicao]
    del nickList[posicao]

def addConnAddr(conn,ddr,name):
    connList[len(connList):] = [conn]
    addrList[len(addrList):] = [addr]
    nickList[len(nickList):] = [name]

#retornar posicao do endereco
def posaddr(addr):
    if addr in addrList:
        return addrList.index(addr)
    else:
        print "Erro S:39 Endereco nao existe!"

#Mandar para todos.
def mandarParaTodos(mensagem):
    for i in connList:
        mandarCliente(i,mensagem)

def reDadoCliente(conn,addr):
    dado = receberCliente(conn)
    nickList[posaddr(addr)] = dado
    nickname = dado
    sentence = "Ola " + nickname +"\n" + nickname + " >>"
    mandarCliente(conn, sentence)
    print nickname + " entrou na sala..."
    #mandarParaTodos(m)
    while 1:
        dado = receberCliente(conn)
        if dado == "//stop()":
            print"%s >> Saiu!" % nickList[posaddr(addr)]
            removeConnAddr(addr)
            break
        elif dado == "//nick()":
            mandarCliente(conn,"Digite seu novo nick: ")
            nickname = receberCliente(conn)
            sentence = "Seu novo nickname e: " + nickname
            mandarCliente(conn, sentence)
        else:
            msgServer = dado + " \n" + nickname + ">>"
            mandarCliente(conn, msgServer)
            print nickname + " disse: " + dado


#variaveis globais
serverName = 'localhost' # ip do servidor (em branco)
serverPort = 12000 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para "ouvir" conexoes
connList = [] #lista de coneccoes
addrList = [] #lista de enderecos
nickList = [] #lista de nomes
while 1:
    print "Servidor TCP esperando conexoes na porta %d ..." % (serverPort)
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    addConnAddr(connectionSocket,addr,"SemNome")

    print"Cliente [%s:%s]:Conectado!\nLista de nomes:" % (addr[0], addr[1])
    print nickList
    t = Thread(target = reDadoCliente, args = (connectionSocket,addr))
    t.start()

    #sentence = connectionSocket.recv(1024) # recebe dados do cliente
    #capitalizedSentence = sentence.upper() # converte em letras maiusculas
    #print "Cliente %s enviou: %s, transformando em: %s" % (addr, sentence, capitalizedSentence)
    #connectionSocket.send(capitalizedSentence) # envia para o cliente o texto transformado
    #connectionSocket.close() # encerra o socket com o cliente
serverSocket.close() # encerra o socket do servidor
