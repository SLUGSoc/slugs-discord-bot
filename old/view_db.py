#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('secrets.db')
c = conn.cursor()

def print_db():
    c.execute('SELECT * FROM secrets')
    data = c.fetchall()

    head = ('name:', 'secret:', 'user:')
    for i in data:
        for j in range(0,3):
            print (head[j], i[j])
        print ('\n')
        
print_db()
while True:
    string = input('Command (Leave blank to reprint):\n')
    if string == '':
        print_db()
    else:
        c.execute(string)
        results = c.fetchall()
        for i in results:
            print(i)
            print('\n')
        conn.commit()
    
