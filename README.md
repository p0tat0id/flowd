# flowd
Netflow collector. Receiving v.5 packets and storing them in postgres DB.

Needed: python3.x, psycopg2 for manipulating postgresql.

Before running script: install postgresql 11 and above, create DB with name - flow, create user - flow and grant priveleges to user on DB.

If you want to run script as system service, create an unit file.

Attention! At the moment, the control of the depth of data storage in the database is not implemented.

./flowd.py --help
usage: flowd.py [-h] [--dbuser DBUSER] [--dbuser_pass DBUSER_PASS]
                [--dbhost DBHOST] [--dbport DBPORT] [--bindaddr BINDADDR]
                [--bindport BINDPORT]

Description of arguments

optional arguments:
  -h, --help            show this help message and exit
  --dbuser DBUSER       postgresql DB user name (default: "flow")
  --dbuser_pass DBUSER_PASS
                        postgresql DB user password (default: "12345")
  --dbhost DBHOST       address postgresql DB server (default: "localhost")
  --dbport DBPORT       postgresql DB server port (default: "5432")
  --bindaddr BINDADDR   flow listen address (default: "192.168.88.224")
  --bindport BINDPORT   flow listen port (default: "2525")
