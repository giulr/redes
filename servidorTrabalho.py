from socket import * # sockets
from threading import Thread # thread

def reDadoCliente(conn,addr):
    dado = conn.recv(1024);
    nickname = dado;
    sentence = "Ola " + nickname +"!";
    conn.send(sentence);
    print nickname + " entrou na sala...";
    while 1:
        try:
            dado = conn.recv(1024);
            if dado == "//stop" or dado == '':
                print"Cliente [%s:%s]:Saiu" % (addr[0],addr[1])
                sentence = "Ate a proxima";
                conn.send(sentence)
                conn.close()
                break
            if dado == "altNick":
                conn.send("Digite seu novo nick: ");
                nickname = conn.recv(1024);
                sentence = "Seu novo nickname e: " + nickname;
                conn.send(sentence);
            else:
                msgServer = nickname + " disse: " + dado;
                enviarMsgTodos(serverSocket,msgServer);
                print nickname + " disse: " + dado;
        except:
            enviarMsgTodos(serverSocket, "Cliente offline")
def enviarMsgTodos(serverSocket, mensagem):
    for socket in sockets:
        if socket != serverSocket :
            try :
                socket.send(mensagem)
            except :
                socket.close()
                print "erro"
                if socket in sockets:
                    sockets.remove(socket)

#variaveis globais
serverName = 'localhost' # ip do servidor (em branco)
serverPort = 12000 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(10) # socket pronto para "ouvir" conexoes
sockets = [];
addresses = [];
while 1:
    print "Servidor TCP esperando conexoes na porta %d ..." % (serverPort)
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    print"Cliente [%s:%s]:Conectado!" % (addr[0], addr[1])
    t = Thread(target = reDadoCliente, args = (connectionSocket,addr))
    t.start()
    sockets.append(connectionSocket)
    
    
    
    
    #sentence = connectionSocket.recv(1024) # recebe dados do cliente
    #capitalizedSentence = sentence.upper() # converte em letras maiusculas
    #print "Cliente %s enviou: %s, transformando em: %s" % (addr, sentence, capitalizedSentence)
    #connectionSocket.send(capitalizedSentence) # envia para o cliente o texto transformado
    #connectionSocket.close() # encerra o socket com o cliente
serverSocket.close() # encerra o socket do servidor
