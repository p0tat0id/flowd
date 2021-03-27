#!/usr/bin/python3
# netflow ver. 5 collector

#need install psycopg2 for manipulating postgresql (pip or packet manager)
import socket, struct, datetime, psycopg2

dbname="flow"
dbuser="flow"
dbuser_pass="12345"
dbhost="localhost"
dbport="5432"

#function try connect to DB and return TRUE if OK or False if not connect.
def try_connect_to_db():
    try:
        con = psycopg2.connect(database=dbname, user=dbuser, password=dbuser_pass, host=dbhost, port=dbport)
        return True
    except:
        return FALSE
    con.close()

#function connect connect to DB and check table exists
def is_table_exist():
    try:
        con = psycopg2.connect(database=dbname, user=dbuser, password=dbuser_pass, host=dbhost, port=dbport)
    except:
        raise SystemExit    
    cur = con.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('rawflow',))
    return (cur.fetchone()[0])    
    con.close()

#function create table for data of netflow stream
def create_table():
    con = psycopg2.connect(database=dbname, user=dbuser, password=dbuser_pass, host=dbhost, port=dbport)
    cur = con.cursor()
    cur.execute('''CREATE TABLE rawflow (srcip inet NOT NULL, srcprt integer NOT NULL, dstip inet NOT NULL,
         dstprt integer NOT NULL, numbyte integer NOT NULL, flowtime timestamp NOT NULL);''')
    con.commit()  
    con.close()
    return

def run_flow_v5_collector():
    con = psycopg2.connect(database=dbname, user=dbuser, password=dbuser_pass, host=dbhost, port=dbport)
    cur = con.cursor()
    HEADER = 24
    RECORD = 48
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('192.168.88.224', 2525))
    datagram, addr = sock.recvfrom(1500)    
    while True:
        datagram, addr = sock.recvfrom(1500)
        (ver, count) = struct.unpack('!HH',datagram[0:4])
        if ver != 5: break
        epoch = datetime.datetime.fromtimestamp(int(socket.ntohl(struct.unpack('I',datagram[8:12])[0]))).strftime('%Y-%m-%d %H:%M:%S')
        for i in range(0, count):
            try:
                base = HEADER+(i*RECORD)
                data = struct.unpack('!IIIIHH',datagram[base+16:base+36])
                protoid = (struct.unpack('!b',datagram[base+38:base+39]))[0]
                nfdata = {}
                nfdata['saddr'] = socket.inet_ntoa(datagram[base+0:base+4])
                nfdata['daddr'] = socket.inet_ntoa(datagram[base+4:base+8])
                nfdata['pcount'] = data[0]
                nfdata['bcount'] = data[1]
                nfdata['sport'] = data[4]
                nfdata['dport'] = data[5]
                print (nfdata['saddr'],':',nfdata['sport'],'--->',nfdata['daddr'],':',nfdata['dport'],'__ID proto:',protoid,'__пакетов:',nfdata['pcount'],'__байт:',nfdata['bcount'],epoch)    
                cur.execute(
                "INSERT INTO rawflow (srcip, srcprt, dstip, dstprt, numbyte, flowtime) VALUES (%s, %s, %s, %s, %s, %s)", (nfdata['saddr'], nfdata['sport'], nfdata['daddr'], nfdata['dport'], nfdata['bcount'], epoch))
                con.commit()  
            except:
                print ('some except...')
                raise SystemExit

#main code
if not (try_connect_to_db()):
    print('Error connecting to DB: ',dbname,', port:',dbport)
    raise SystemExit

if not(is_table_exist()):
    create_table()

run_flow_v5_collector()

#to be continued...





    
