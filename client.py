#Python Program to implement Client side of Chat Interface



import socket, select, string, sys, os					#Used Libraries


def display() :								#Helper functions used for formatting
	you="You: "
	sys.stdout.write(you)
	sys.stdout.flush()

def main():

    if len(sys.argv)<2:
        host = input("Enter host ip address: ")				#IP Address as "localhost"
    else:
        host = sys.argv[1]

    port = 5001								#Port Used
    
    #asks for user name
    name=raw_input(" CREATING NEW ID:\n Enter username: ")		
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""The first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain with any two hosts.
 The second argument is the type of socket.SOCK_STREAM means that data or characters are read in a continuous flow."""
    s.settimeout(2)
    #settimeout() function is set for 2 sec delay.


    # connecting host
    try :
        s.connect((host, port))
    except :
        print (" Can't connect to the server")
        sys.exit()

    #if connected to host
    s.send(name)
    display()


    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list , [], [])
        
        for sock in rList:
            #incoming message from server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print ("\rDISCONNECTED!!\n")
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    display()
        
            #user entered a message
            else :
                msg=sys.stdin.readline()
                s.send(msg)
                display()

if __name__ == "__main__":
    main()