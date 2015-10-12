# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import csv
import os
import sqlite3
import codecs

from pprint import pprint
#from random import  


def from_sap():
    fp_pol = open("./objasnienia.sap", mode="rb")
    fp_eng = open("./hasla.sap", mode="rb")

    raw_pol = fp_pol.read()
    raw_eng = fp_eng.read()

    fp_eng.close()
    fp_pol.close()




    #map_pol = list(map(lambda l: l[:-1].decode("windows-1250", errors='ignore'), raw_pol.split(b"\x00\x00\x00")))[10:]

    map_pol = []
    a = 0
    last = ""
    for i in raw_pol.split(b"\x00\x00\x00")[10:]:
        try:
            l = i[:-1].decode("windows-1250", errors='ignore').lower()
            if r"\x" in l.__repr__():
                l = l[:-1]
                if r"\x" in l.__repr__():
                    raise Exception

     
            map_pol.append(l)
        except Exception as e:
            a += 1
            #print("Exception pol:", l)

    map_eng = []
    a = 0
    last = ""
    for i in raw_eng.split(b"\x00\x00\x00")[24:][::2]:
        try:
            l = i.decode("ascii", errors='strict').lower()
            if l == last:
                raise Exception

            last = l
            if r"\x" in l.__repr__():
                l = l[:-1]
                if r"\x" in l.__repr__():
                    raise Exception



            
            map_eng.append(l)
        except:
            a += 1
            #print("Exception eng", i)

    print ("Errors decode: {}".format(a))
    print (len(map_pol), len(map_eng))
    #print (list(map_eng)[248].__repr__())
    #map_eng = list(map(lambda l: l.decode("windows-1250", errors='strict'), raw_eng.split(b"\x00\x00\x00")))[24:][::2]
    #map_eng = list(raw_eng.split(b"\x00\x00\x00")[24:][::2])

def from_csv():
    cr = csv.reader(open("./test3.csv", mode="rt"))
    ret = []
    count = 0
    for row in cr:
        count += 1
        cols = row[0].decode("utf-8").split(";")
        pol = ""
        for i, col in enumerate(cols):
            if i == 0:
                continue
            if col:
                pol += col
        pol = pol.replace("+", ";").replace('"', "").strip()
        eng = cols[0].strip()
        ret.append((eng, pol))


    return ret


def save_to_cvs(ret):
    with open("./test4.csv", mode="w") as fp:
        a = csv.writer(fp, delimiter=';')
        a.writerows(ret)

def save_to_sql(ret):

    con = sqlite3.connect('./test.db')

    with con:

        cur = con.cursor()
        cur.execute("PRAGMA encoding='UTF-8';")
        #cur.commit()
        cur.execute("DROP TABLE IF EXISTS ajt")

        cur.execute("CREATE TABLE ajt(id INT PRIMARY KEY, ang string, pol string)")
        for i, row in enumerate(ret):

            statment = u"INSERT INTO ajt(id, ang, pol) VALUES({},'{}','{}');".format(i, 
                unicode(row[0]).replace("'", "''").strip(),
                unicode(row[1]).replace("'", "''").strip())
            try:
                cur.execute(statment)
            except Exception as e:
                print (e)
                print (statment)
                raise Exception

        con.commit()

def read_from_txt(file_=None):

    if not os.path.exists(file_):
        print ("Brak pliku")
        return


    ret = []
    with codecs.open(file_, "rb", encoding="cp1250") as fp:
        for line in fp.readlines():
            if line.startswith("#") or len(line) < 3:
                continue

            line = line.replace("@@", "@")

            if line.find("%") != -1:
                # przekierunkowanie
                ret_line = line.split("%")
                ret_line[1] = "%" + ret_line[1]
                ret.append(ret_line)
                continue

            if line.find("@") != -1:
                # wyrażenie wieloczłonowe
                ret_line = line.split("@")
                ret_line[1] = "@" + ret_line[1]
                ret.append(ret_line)
                continue

            if line.find("$") != -1:
                # wyrażenie standardowe
                ret_line = line.split("$", 1)
                ret_line[1] = "$" + ret_line[1]
                ret.append(ret_line)
                continue

            #raise("Błąd lini")
            print (line)

    print ("Baza przerobiona")
    return ret


save_to_sql(read_from_txt(file_="./sap.txt"))
