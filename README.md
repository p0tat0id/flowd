# flowd
Netflow collector. Receiving v.5 packets and storing them in postgres DB.

Needed: python3.x, psycopg2 for manipulating postgresql.

Before running script: install postgresql 11 and above, create DB with name - flow, create user - flow and grant priveleges to user on DB.

If you want to run script as system service, create an unit file.

Attention! At the moment, the control of the depth of data storage in the database is not implemented.

help for use: ./flowd.py --help
usage: flowd.py [-h] [--dbuser DBUSER] [--dbuser_pass DBUSER_PASS]
                [--dbhost DBHOST] [--dbport DBPORT] [--bindaddr BINDADDR]
                [--bindport BINDPORT]

