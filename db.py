import sys
import os
import sqlite3
from contextlib import closing

import os 

from objects import Item

conn = None


def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = dir_path = os.path.dirname(os.path.realpath(__file__)) + r"\db\itemDB.sqlite"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "db/itemDB.sqlite"
        
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_Item(row):
    #print(row["name"]) #debugging
    #print(row["cost"]) #debugging
    return Item(row["name"], row["cost"])

def getList():
    query = '''SELECT name, cost FROM Items'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

        table = []
        for row in results:
            table.append(make_Item(row))
        '''for item in table:
            print(item)'''#debugging
        return table

def getItem(itemName):
    sql = '''SELECT name FROM Items WHERE name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (itemName,))
        result = c.fetchone()

        if result == None:
            return False
        else:
            return True

def addItem(item):
    sql = '''INSERT INTO Items (name, cost)
             VALUES (?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (item.name, item.cost))
        conn.commit()

def removeItem(itemName):
    sql = '''DELETE FROM Items WHERE name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (itemName,))
        test = conn.commit()
        #print("Test", test) #debugging

def ConfirmDelete(itemName):
    sql = '''SELECT name FROM Items WHERE name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (itemName,))
        result = c.fetchone()

        if result == None:
            return True
        else:
            return False
