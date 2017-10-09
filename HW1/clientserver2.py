# -*- coding: utf-8 -*-

import socket
import threading

def run_listener(port):
	fp = open('listener_of_{}.txt'.format(port), "w")
	print('Creating socket...')
	sock = socket.socket() #Создаем сокет
	print('Bindong adress and port...')
	sock.bind(('localhost', port)) #Указываем для сокета порты для прослушивания и хост
	print('Configuring listening...')
	sock.listen(1) # Подключаемся и указываем  максимальное количество подключений в очереди
	while True:
		print('Waiting for connection...')
		conn, addr = sock.accept() #Возвращает кортеж из двух элементов адрес нового сокета и адрес клиента
		print('Beggining to process incoming connection...')
		fp.write(u'FROM:{}\n'.format(addr))
		while True:         #Читаем по 1024 байта с помощью recvк
			data = conn.recv(1024)
			if not data:
				break
			#conn.send(data.upper())
			print('Recived chunk:"{}"'.format(data.decode('utf-8')))
			print()
			fp.write(data.decode('utf-8'))
		fp.write(u'\n')
		fp.flush()
	print('Closing connection...')
	conn.close()
	fp.close()
	
def run_sender(port):
	user_input = None
	while user_input!= '':
		user_input = input("Please, enter message text for sending to listener:")
		if user_input == '':
			break
		print('Creating socket...')
		conn = socket.socket()
		print('Connecting to listener...')
		try:
			conn.connect( ("localhost", port) )
		except ConnectionError as e:
			print('Connection error, try to send again')
			continue
		user_input = user_input.encode('utf-8')
		print('Sending data to listener...')
		conn.send(user_input)
		print('Closing connection...')
		conn.close()


listener_port = int(input('Enter port to listen from:'))
sender_port = int(input('Enter port to send to:'))


t2 = threading.Thread(target = run_listener, args = (listener_port,))
t2.start()

t1 = threading.Thread(target = run_sender, args = (sender_port,))
t1.start()

