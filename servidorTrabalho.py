from socket import * # sockets
from threading import Thread # thread
import time
def reDadoCliente(conn,addr, papel, nickname):
    while 1:
        check = "NOT A CRITERIA"
        try:
            dado = conn.recv(1024);
            check = dado.split();
            #pego = 0
	    #contador = contador + 1
	    #dado = conn.recv(1024);
	    #tempo2 = time.clock()

            #if tempo2 - tempo1 >= 10.0:
               # tempo1 = time.clock()
               # contador = 0

            #if contador >= 5 or pego > 30:
               # sentence = "Escreveu rapido demais!\nPorfavor Espere 5s"
                #conn.send(sentence)
                #time.sleep(5)
                #contador = 0
                #pego = pego + 1
                #sentence = "Ja se passaram 5s, Pode continuar, mas cuidado!"
                #conn.send(sentence)
            if dado == "sair()":
                print"Cliente (%s)[%s:%s]:Saiu" % (nickname, addr[0],addr[1])
                sentence = "FIM";
                conn.send(sentence)
                conn.close()
                break
            if dado == "nome()":
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
                enviarMsgTodos(serverSocket, sentence);
                
            if dado == "privado()":
                conn.send("Digite o usuario com o qual deseja iniciar uma conversa privada: ");
                user = conn.recv(1024); #falta checar se o nickname existe
                sendRequest(user, nickname, addr);
               
            if dado == "S":
                print "RESPONDEU SIM"
                
                #fechar conexao
            #if check[0] == "localhost":
                #conn.send("Inciando conexao privada!");
                
            else:
                msgServer = nickname + " escreveu: " + dado + "\n";
                
                enviarMsgTodos(serverSocket,msgServer);
                print nickname + " escreveu: " + dado;
        except:
           flag = 1;
           

#def RecebeDados(ConnSocket, address, papel):
    #print "oi"
    #a variavel papel diz respeito ao papel que esta sendo realizado, se de cliente normal ou de servidor do chat privado
    #if papel == "CLIENTE":
        #print "CLIENTE"
    #elif papel == "SERVIDOR":
        #print "SERVIDOR"
        
def ConectarAServidor(nameServer, portServer):
    clientSocket = socket(AF_INET, SOCK_STREAM) # criacao do socket TCP
    clientSocket.connect((nameServer, portServer)) # conecta o socket ao servidor
    t = Thread(target = RecebeDados, args = (clientSocket, nameServer, 'CLIENTE'))
    t.start()
def ReceberConexao(nameServer, portServer, maxConn):
    serverSocket = socket(AF_INET, SOCK_STREAM) # criacao do socket TCP
    serverSocket.bind((nameServer, portServer)) # bind do ip do servidor com a porta
    serverSocket.listen(maxConn) # socket pronto para "ouvir" conexoes
    print "Ouvindo..."
    while 1:
        connSocket, addr = serverSocket.accept() # aceita a conexao do cliente (chat privado)
        #print "Conectado a (%s:%s)" %(addr[0], (addr[1])
	#recebe e define o nickname do novo cliente
        sockets.append(connSocket)
	nickname = DefineNickName(connSocket)
	addresses.append(addr);
        t = Thread(target = reDadoCliente, args = (connSocket, addr, 'SERVIDOR', nickname))
        t.start()
def DefineNickName(ConnSocket):
    dado = ConnSocket.recv(1024);
    nickname = dado;
    nicknames.append(nickname);
    sentence = "Ola " + nickname +"!";
    ConnSocket.send(sentence);
    print nickname + " entrou na sala...";
    return nickname;
    
def sendRequest(user, nickname, address):
    for idx, nick in enumerate(nicknames):
        if nick == user:
            #socket[idx].send("TETSE");
            sockets[idx].send("pvt " + nickname + " quer iniciar uma conversa privada. Aceita? Responda [S/N]\n");
            #sockets[idx].send(address);
    
def srcNickName(user):
    for idx, nick in enumerate(nicknames):
        if nick == user:
            return idx;

     
def mostrarConexoes():
    print "Clientes conectados: "
    for idx, addr in enumerate(addresses):
        print "\nCliente: "
        print nicknames[idx];
        print "Endereco: ";
        print addresses[idx];
        
    
     
def enviarMsgTodos(serverSocket, mensagem):
    for socket in sockets:
        if socket != serverSocket :
            try :
                socket.send(mensagem)
            except :
                socket.close()
                if socket in sockets:
                    sockets.remove(socket)

#variaveis globais
serverName = 'localhost' # ip do servidor (em branco)
serverPort = 12000 # porta a se conectar
serverSocket = ''
#serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
#serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
#serverSocket.listen(10) # socket pronto para "ouvir" conexoes
AceitaMaxConn = 15
nicknames = [];
sockets = [];
addresses = [];
ports = [];
print "Servidor TCP esperando conexoes na porta %d ..." % (serverPort)
print "Cliente ou servidor? [C/S]";
#resposta = raw_input();
#resposta.upper();
resposta = "S";
if resposta == "C":
    ConectarAServidor(serverName, serverPort)    
elif resposta == "S":
    ReceberConexao(serverName, serverPort, AceitaMaxConn)
    serverSocket.close() # encerra o socket do servidor  

#while 1:
    #connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
    #print"Cliente [%s:%s]:Conectado!" % (addr[0], addr[1])
    #t = Thread(target = reDadoCliente, args = (connectionSocket,addr))
    #t.start()
    #sockets.append(connectionSocket)
    #addresses.append(addr[0])
    #ports.append(addr[1])
    
    
    
    
