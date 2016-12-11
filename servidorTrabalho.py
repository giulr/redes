from socket import * # sockets
from threading import Thread # thread
import time
def reDadoCliente(conn,addr):
    dado = conn.recv(1024);
    nickname = dado;
    nicknames.append(nickname);
    sentence = "Ola " + nickname +"!";
    conn.send(sentence);
    print nickname + " entrou na sala...";
    while 1:
        try:
            dado = conn.recv(1024);
            if dado == "sair()" or dado == '':
                print"Cliente [%s:%s]:Saiu" % (addr[0],addr[1])
                sentence = "Ate a proxima";
                conn.send(sentence)
                conn.close()
                break
            if dado == "nome(*)":
                conn.send("Digite seu novo nick: ");
                newNick = conn.recv(1024);
                print nickname + " agora e " + newNick;
                for  nick in nicknames:
                    if nick == nickname:
                       nick = newNick;
                nickname = newNick;
                sentence = "Seu novo nickname e: " + nickname;

                conn.send(sentence);
            if dado == "lista()":
                mostrarConexoes();
                sentence = "Mostrando clientes conectados ao servidor...";
                conn.send(sentence);
            #if dado == "privado()":
              #  conn.send("Digite o usuario com o qual deseja iniciar uma conversa privada: ");
              #  user = conn.recv(1024);
               # conversaPrivada(user, nickname,addr[0],addr[1]);
            else:
                msgServer = nickname + " escreveu: " + dado + "\n";
                enviarMsgTodos(serverSocket,msgServer);
                print nickname + " escreveu: " + dado;
        except:
            enviarMsgTodos(serverSocket, "Cliente offline")
#def conversaPrivada(user, nickname, addr, port):
    
def mostrarConexoes():
    print "Clientes conectados: "
    for idx, addr in enumerate(addresses):
        print "\nCliente: "
        print nicknames[idx];
        print "Endereco: ";
        print addresses[idx];
        print "Porta:"
        print ports[idx];
    
     
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
nicknames = [];
sockets = [];
addresses = [];
ports = [];
print "Servidor TCP esperando conexoes na porta %d ..." % (serverPort)
while 1:
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    print"Cliente [%s:%s]:Conectado!" % (addr[0], addr[1])
    t = Thread(target = reDadoCliente, args = (connectionSocket,addr))
    t.start()
    sockets.append(connectionSocket)
    addresses.append(addr[0])
    ports.append(addr[1])
    
    
    
    #sentence = connectionSocket.recv(1024) # recebe dados do cliente
    #capitalizedSentence = sentence.upper() # converte em letras maiusculas
    #print "Cliente %s enviou: %s, transformando em: %s" % (addr, sentence, capitalizedSentence)
    #connectionSocket.send(capitalizedSentence) # envia para o cliente o texto transformado
    #connectionSocket.close() # encerra o socket com o cliente
serverSocket.close() # encerra o socket do servidor
