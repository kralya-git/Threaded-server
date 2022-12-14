import socket, threading,sys

def acceptance(conn, addr):
	# Запускаем непрерывный цикл приема сообщений от клиентов
	while True:
		# Попытка получить сообщение от клиента
		try:
			data = conn.recv(1024)
		except (ConnectionResetError, ConnectionAbortedError):
			# В случае получения ошибки соединения - об этом выводится сообщение
			print(f'Client {addr} aborted connection')
			# Инициируем эту ошибку (выведется не весь traceback, так как знаем что и где разорвано)
			raise
			# Дополнительно, из-за ошибки остановится поток, так как он больше не нужен
		# При удачном приёме информации - выводится информация (кто и что отправил)
		print(f'accepted from {addr}:$ {data.decode()}')
		# Отправляем клиенту его же сообщение, так как это еще эхо сервер
		conn.send(data)


# Устанавливаем лимит вывода глубины сообщений об ошибке
# В случае разрыва соединения клиентом - поток будет закрываться 
# Тогда на экране сервера выведется код ошибки разрыва соединения, а не полный traceback
sys.tracebacklimit = 0
# Создаем объект сокета
sock = socket.socket()
# Задаем ему IP-адрес, с которого будем принимать подключение (то есть любой и порт 9090)
sock.bind(('', 9090))
# Начинаем прослушивать сокет (ожидаем соединение клиентов)
sock.listen(0)

# Начинаем бесконечный цикл приёма клиентов
while True:
	# Принимаем соединение от клиента
	conn, addr = sock.accept()
	# Выводим присоединившегося клиента на экран
	print(f'connected {addr}')
	# Создаем поток с функцией acceptance, передаем данные клиента, делаем поток даемонов, а затем запускаем поток
	threading.Thread(target = acceptance, args = (conn, addr), daemon = True).start()
