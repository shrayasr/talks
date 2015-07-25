#!env/bin/python

import psycopg2

conn = psycopg2.connect('dbname=test_copy user=postgres')
cur = conn.cursor()

row = {'some_text':"chennaiPy",'some_int':7,'some_double':3.14,'some_boolean':True}

cur.execute("INSERT INTO random_test_table(some_text, some_int, some_double, some_boolean) VALUES (%s, %s, %s, %s)",(row['some_text'],insert_me['some_int'],insert_me['some_double'],insert_me['some_boolean'])) 

conn.commit()

cur.close()
conn.close()
