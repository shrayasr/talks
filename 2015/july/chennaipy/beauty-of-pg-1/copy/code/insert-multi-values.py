#!env/bin/python

import psycopg2

conn = psycopg2.connect('dbname=test_copy user=postgres')
cur = conn.cursor()

rows = ({'some_text':'chennaiPy','some_int':7,'some_double':3.14,'some_boolean':True}
    ,{'some_text':'IMSc','some_int':14,'some_double':6.28,'some_boolean':False}
    ,{'some_text':'July 25','some_int':28,'some_double':9.42,'some_boolean':True})

cur.executemany("INSERT INTO random_test_table(some_text, some_int, some_double, some_boolean) VALUES (%(some_text)s, %(some_int)s, %(some_double)s, %(some_boolean)s)",(rows))

conn.commit()

cur.close()
conn.close()
