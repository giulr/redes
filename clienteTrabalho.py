from socket import * #socket
from threading import Thread # thread
import time
import re  
def trocaDados(connSocket, nameServer, papel, nick):
    check = 'NOT A CRITERIA';
    while 1:
        #print check; #print para verificar a posicao de um valor na string (testes)
        if check[0] == "pvt": #flag de iniciar uma conexao privada
            request = raw_input();
            if request == "S": #aceita uma solicitacao de conexao privada
                port = " 13000"
                msg = "//flag " + nameServer;
                sentence = msg + port;
                enviarServidor(sentence , connSocket);
                papel = 'SERVIDOR'
                tServer = Thread (target = ReceberConexao, args = (nameServer, papel, AceitaMaxConn, nick));
                tServer.start();
                connSocket.close();
        if len(check) >= 5 and check[4] == "//flag": #verifica se a string tem uma flag com o endereco do server p2p
            server = check[5];
            port = 13000;
            papel = 'CLIENTE';
            tClient = Thread (target = ConectarAServidorPrivado, args = (server, port,nick));
            tClient.start();
            connSocket.close();
            break;
        else:
            print "You: "
            request = raw_input();
            if request == "mais()": #mostra ao usuario outras opcoes
                mais();
            if request == "nome()": #muda nick
                enviarServidor(request, connSocket);
                answer = receberServidor(connSocket);
                print answer;
                request = raw_input();
                enviarServidor(request,connSocket);
                answer = receberServidor(connSocket);
                nickname = answer;
                print answer;
                
            else:
                enviarServidor(request, connSocket);
                answer = receberServidor(connSocket);
                check = answer.split();
                if answer == "FIM": #finaliza conexao
                    time.sleep(1)
                    connSocket.close();
                    print "Voce saiu do chat!\nAte a proxima!"
                    time.sleep(3)
                    break;
                if check[0] == "pvt":
                    print answer;
                else:
                    print answer;
        
       
#--------------------------------------------------------------------------------------------------------------------------------------#
def RecebeDados(ConnSocket, address, papel): #funcao util somente para testes 
    #a variavel papel diz respeito ao papel que esta sendo realizado, se de cliente normal ou de servidor do chat privado
    if papel == "CLIENTE":
        print "CLIENTE"
    elif papel == "SERVIDOR":
        print "SERVIDOR"
#--------------------------------------------------------------------------------------------------------------------------------------#
def ConectarAServidor(nameServer, portServer): #faz uma conexao a um server
    clientSocket = socket(AF_INET, SOCK_STREAM) # criacao do socket TCP
    clientSocket.connect((nameServer, portServer)) # conecta o socket ao servidor
    nick = defineNickName(clientSocket);
    nicknames.append(nick);
    t = Thread(target = trocaDados, args = (clientSocket, nameServer, 'CLIENTE', nick))
    t.start()
    return clientSocket

def ConectarAServidorPrivado(nameServer, portServer,nick): #faz uma conexao a um server
    clientSocket = socket(AF_INET, SOCK_STREAM) # criacao do socket TCP
    clientSocket.connect((nameServer, portServer)) # conecta o socket ao servidor
   # nick = defineNickName(clientSocket);
    #nicknames.append(nick);
    t = Thread(target = trocaDados, args = (clientSocket, nameServer, 'CLIENTE', nick))
    t.start()
    return clientSocket
#--------------------------------------------------------------------------------------------------------------------------------------#
def ReceberConexao(nameServer, portServer, maxConn, nick): #vira um server para conexoes privadas
    serverSocket = socket(AF_INET, SOCK_STREAM) # criacao do socket TCP
    portServer = 13000;
    serverSocket.bind((nameServer, portServer)) # bind do ip do servidor com a porta
    serverSocket.listen(maxConn) # socket pronto para "ouvir" conexoes
    print nick + " Ouvindo..."
    print portServer
    while 1:
        connectionSocket, addr = serverSocket.accept() # aceita a conexao do cliente (chat privado)
        #print "Conectado a " + str(addr[0]) + str(addr[1])
        t = Thread(target = trocaDados, args = (connectionSocket, addr, 'SERVIDOR', nick))
        t.start()        
#--------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------#
def defineNickName(connSocket): #muda nick name
    tes = 1;
    while tes:
        request = raw_input("Digite seu Nickname: ")
        try:
            nome = request.split()
            request = nome[0]
        except Exception as all:
            print"Erro 1"
            time.sleep(10)
            request = ''

        if request != '':
            tes = 0
            enviarServidor(request, connSocket)
            nickname = request
            cliente = 'CLIENTE'
            answer = receberServidor(connSocket)
            #t = Thread(target = trocaDados, args = (connSocket, addr)
            #t.start()
            
            print answer
            return nickname;
        else:
            print "Por favor Digite seu nome sem ser apenas espaco e tenha algum nome ou algo to tipo."
            tes = 1
#--------------------------------------------------------------------------------------------------------------------------------------#
    
#--------------------------------------------------------------------------------------------------------------------------------------#
def receberServidor(connSocket): #recebe msgs de um servidor
    dado = connSocket.recv(1024) # recebe do servidor a resposta
    return dado
#--------------------------------------------------------------------------------------------------------------------------------------#
def enviarServidor(arg, connSocket): #envia msgs para o servidor
    if arg == '':
        connSocket.send(" ")
    else:
        connSocket.send(arg)
#--------------------------------------------------------------------------------------------------------------------------------------#
#Parametros globais fixos e pre-definidos
AceitaMaxConn = 1
serverName = 'localhost'
serverPort = 12000
nicknames = [];
#print "Cliente ou servidor? [C/S]";
#resposta = raw_input()
resposta = 'C'; #definindo C como padrao ja que esse e o cliente

if resposta == "C":
    print 'Bem- vindo ao nosso chat, para mais informacoes digite mais()'
    connSocket = ConectarAServidor(serverName, serverPort);
elif resposta == "S":
    ReceberConexao(serverName, serverPort, AceitaMaxConn);
    #serverSocket.close(); # encerra o socket do servidor    
            
       

def mais():
    print 'Digite nome() para alterar o seu Nickname\n'
    print "Digite lista() para mostrar todos os participantes do chat\n"
    print 'Digite sair() para sair do chat\n'

  
