import base64
import hashlib
import hmac
import os
import sqlite3
import struct
import time

if not os.path.isfile("secrets.db"): # Establishes a new database if needed
    print("No file named secrets.db found, creating new table...")
    conn = sqlite3.connect('secrets.db')
    c = conn.cursor()
    c.execute('CREATE TABLE secrets (name TEXT, secret TEXT, user TEXT)')
    conn.commit()
else:
    print("Located secrets.db...")
    conn = sqlite3.connect('secrets.db')
    c = conn.cursor()

def choose_secret():
    options = list()
    names = list()
    
    c.execute('SELECT * FROM secrets')
    data = c.fetchall()
    for i in data:
        n = len(options)
        options.append(n)
        names.append(i[0])

    for o in options:
        print(o, ") ", names[o], sep="")

    try:
        choice = int(input("Input the number of the service you're authenticating: "))
        if choice in options:
            print("Codes for ", names[choice], ":", sep="")
        else:
            print("Your choice is not one of the options provided.")
    except ValueError as e:
        print("Please try again, and enter one of the integers provided.\n", e)
        return
    print(generate_codes(choice))

def generate_codes(choice):
    c.execute('SELECT * FROM secrets')
    data = c.fetchall()
    record = data[choice]
    secret = record[1]

    intervals = int(time.time()) // 30
    decode = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals)
    h = hmac.new(decode, msg, hashlib.sha1).digest()
    o = h[19] & 15
    hotp = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    totp = str(hotp).zfill(6)
    return(totp)
    
choose_secret()
