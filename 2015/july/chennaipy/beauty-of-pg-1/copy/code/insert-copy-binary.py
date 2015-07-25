#>env/bin/python

import psycopg2
from io import BytesIO
from struct import pack

conn = psycopg2.connect('dbname=test_copy user=postgres')
cur = conn.cursor()

rows = (
        {'some_text':'chennaiPy','some_int':7,'some_double':2494.94,'some_boolean':True}
        ,{'some_text':'IMSc','some_int':14,'some_double':2494.94,'some_boolean':False}
        ,{'some_text':'July 25','some_int':28,'some_double':249.94,'some_boolean':True})

# > big endian, 
# h 2 byte integer (smallint) 
# i integer
# q 8 byte integer (long long)
# d 8 byte float (double)
# ? boolean
# s char

# create a new byte stream
cy = BytesIO()

# 11-byte sequence PGCOPY\n\377\r\n\0
cy.write(pack('>11s',b'PGCOPY\n\377\r\n\0'))

# Flags field
cy.write(pack('>i',0))

# length in bytes of remainder of header; currently, this is zero
cy.write(pack('>i',0))

for row in rows:
    # 16-bit integer count of the number of fields in the tuple
    # this is done for every tuple 
    cy.write(pack('>h',4))

    text_len = len(row['some_text'].encode('utf-8'))

    # 32-bit length word
    cy.write(pack('>i',text_len))
    # followed by that many bytes of field data
    cy.write(pack('>'+str(text_len)+'s',row['some_text'].encode('utf-8')))

    cy.write(pack('>i', 8))
    cy.write(pack('>q', row['some_int']))

    cy.write(pack('>i', 8))
    cy.write(pack('>d', row['some_double']))

    cy.write(pack('>i', 1))
    cy.write(pack('>?', row['some_boolean']))

# file trailer consists of a 16-bit integer word containing -1
cy.write(pack('>h', -1))

cy.seek(0)

#f = open('/tmp/output', 'wb')
#f.write(cy.getvalue())
#f.close()

cur.copy_expert("COPY random_test_table (some_text, some_int, some_double, some_boolean) FROM STDIN BINARY", cy)

conn.commit()

cur.close()
conn.close()
