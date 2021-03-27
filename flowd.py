#!/usr/bin/python3
# netflow ver. 5 collector

import socket, struct, datetime, psycopg2

#функция создает таблицу для хранения данных netflow
def create_table():
    #соединяемся с БД
    con = psycopg2.connect(
      database="flow", 
      user="flow", 
      password="12345", 
      host="127.0.0.1", 
      port="5432"
    )

    #print("Подключение к БД выполнено успешно... ")
    cur = con.cursor()
    #формируем sql-запрос на создание таблицы
    cur.execute('''CREATE TABLE rawflow  
         (srcip inet NOT NULL,
         srcprt integer NOT NULL,
         dstip inet NOT NULL,
         dstprt integer NOT NULL,
         numbyte integer NOT NULL,
         flowtime timestamp NOT NULL);''')

    #print("Таблица создана...")
    con.commit()  
    con.close()
    return

def drop_table():
    #подключаемся к БД
    con = psycopg2.connect(
      database="flow", 
      user="flow", 
      password="12345", 
      host="127.0.0.1", 
      port="5432"
    )

    #print("Подключение к БД выполнено успешно...")
    cur = con.cursor()
    #формируем запрос на удаление таблицы rawflow
    cur.execute('''DROP TABLE rawflow''')

    #print("удаление таблицы выполнено успешно...")
    
    con.commit()  
    con.close()
    return

#drop_table()
#create_table()

con = psycopg2.connect(
database="flow", 
user="flow", 
password="12345", 
host="127.0.0.1", 
port="5432"
)

#print("Database opened successfully")
cur = con.cursor()


#размер заголовка и записи
#Значения взяты  из http://www.cisco.com/c/en/us/td/docs/net_mgmt/netflow_collection_engine/3-6/user/guide/format.html#wp1006108
HEADER = 24
RECORD = 48

#Создаем сокет UDP и запускаем прослушиватель
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#адрес и порт на котором ждем данные
sock.bind(('192.168.88.251', 2525))

datagram, addr = sock.recvfrom(1500)
    
while True:
    #Принимаем данные с маршрутизатора
    datagram, addr = sock.recvfrom(1500)
    
    #struct.unpack - распаковывает строку, содержащую упакованные данные структуры Си в соответствие с данными форматов 
    #возвращает кортеж, даже если строка содержит один элемент
    #строка должна содержать количество информации указнное форматом
    #распаковка двоичных данных
    (ver, count) = struct.unpack('!HH',datagram[0:4])
    
    if ver != 5: break
    
    #преобразование 32-битного целого числа из сети в машинную последовательность байт
    #время на маршрутизаторе в формате epoch/Unix timestamp конвертируем в формате %Y-%m-%d %H:%M:%S
    epoch = datetime.datetime.fromtimestamp(int(socket.ntohl(struct.unpack('I',datagram[8:12])[0]))).strftime('%Y-%m-%d %H:%M:%S')
    
    #Перебор данных
    for i in range(0, count):
        try:
            base = HEADER+(i*RECORD)

            #data = struct.unpack('!IIIIHH',datagram[base+16:base+36])
            data = struct.unpack('!IIIIHH',datagram[base+16:base+36])

            protoid = (struct.unpack('!b',datagram[base+38:base+39]))[0]

            nfdata = {}
            
            # print (data1[0])
            
            #socket.inet_ntoa - преобразование IP адреса в 32-разрядном двоичном формате в формат строки
            nfdata['saddr'] = socket.inet_ntoa(datagram[base+0:base+4])
            nfdata['daddr'] = socket.inet_ntoa(datagram[base+4:base+8])
            nfdata['pcount'] = data[0]
            nfdata['bcount'] = data[1]
            #nfdata['proto'] = data[3]
            nfdata['sport'] = data[4]
            nfdata['dport'] = data[5]
            #print (nfdata['saddr'],':',nfdata['sport'],'--->',nfdata['daddr'],':',nfdata['dport'],'__ID proto:',protoid,'__пакетов:',nfdata['pcount'],'__байт:',nfdata['bcount'],epoch)    
            #cur = con.cursor()
            cur.execute(
            "INSERT INTO rawflow (srcip, srcprt, dstip, dstprt, numbyte, flowtime) VALUES (%s, %s, %s, %s, %s, %s)", (nfdata['saddr'], nfdata['sport'], nfdata['daddr'], nfdata['dport'], nfdata['bcount'], epoch))
        
            con.commit()  
            #con.close()
                            #print("Record inserted successfully")  
        except:
            #print ('some except...')
            #print('Ошибка:\n', traceback.format_exc())
            continue    
        #print ('src=';nfdata['saddr'],nfdata['sport'],nfdata['daddr'],nfdata['dport'],nfdata['pcount'],nfdata['bcount'],epoch)

    
