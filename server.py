#Python Program to implement Server side of Chat Interface


import socket, select										#Used Libraries


def send_to_all (sock, message):								#Function to send message to all connected clients
	#Message not forwarded to server and sender itself
	for socket in connected_list:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				# if connection not available
				socket.close()
				connected_list.remove(socket)

if __name__ == "__main__":									#main function of the program
	name=""
	#dictionary to store address corresponding to username
	record={}
	# List to keep track of socket descriptors
	connected_list = []
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""The first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain with any two hosts.
 The second argument is the type of socket.SOCK_STREAM means that data or characters are read in a continuous flow."""

	server_socket.bind(("localhost", port))							#Connection of Node to host
	server_socket.listen(30) 								#Listen atmost 30 connection at one time

	# Add server socket to the list of readable connections
	connected_list.append(server_socket)

	print ("\t\t\t\tSERVER WORKING\t\t\t\t")

	while 1:
        # Get the list sockets which are ready to be read through select
		rList,wList,error_sockets = select.select(connected_list,[],[])

		for sock in rList:
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				name=sockfd.recv(buffer)
				connected_list.append(sockfd)
				record[addr]=""
				print ("record and conn list ",record,connected_list)
                
                #if username is repeated
				if name in record.values():
					sockfd.send("Username already taken!\n")
					del record[addr]
					connected_list.remove(sockfd)
					sockfd.close()
					continue
				else:
                    #add name and address
					record[addr]=name
					print ("Client (%s, %s) connected" % addr," [",record[addr],"]")
					sockfd.send("Welcome to chat room. Enter 'tata' anytime to exit\n")
					send_to_all(sockfd, "\r "+name+" joined the conversation \n")

			#Some incoming message from a client
			else:
				# Data from client
				try:
					data1 = sock.recv(buffer)
					print ("sock is: ",sock)
					data=data1[:data1.index("\n")]
					print ("\ndata received: ",data)
                    
                    #get address of client sending the message
					i,p=sock.getpeername()
					if data == "tata":
						msg="\r"+record[(i,p)]+" left the conversation \n"
						send_to_all(sock,msg)
						print ("Client (%s, %s) is offline" % (i,p)," [",record[(i,p)],"]")
						del record[(i,p)]
						connected_list.remove(sock)
						sock.close()
						continue

					else:
						msg=record[(i,p)]+": "+"\n"
						send_to_all(sock,msg)
            
                #abrupt user exit
				except:
					(i,p)=sock.getpeername()						#Return the remote address to which the socket is connected.
					send_to_all(sock, record[(i,p)]+" left the conversation unexpectedly\n")
					print ("Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n")
					del record[(i,p)]
					connected_list.remove(sock)
					sock.close()
					continue

	server_socket.close()											#Closing the server