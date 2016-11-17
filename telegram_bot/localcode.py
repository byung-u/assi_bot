#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from typing import List

def local_code_check() -> None:
    conn = sqlite3.connect('local.db')    
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS localcode
                 (code text PRIMARY KEY, destrict text, loc text)''')
    conn.commit()
    
    f = open('loc_code.txt')
    for d in f.readlines():
        data = d.split()
        c.execute('''INSERT OR REPLACE INTO localcode VALUES 
                     ("%s", "%s", "%s")''' % (data[0], data[1], data[2]))

    conn.commit()

    f.close()
    conn.close()


def select_local_code(district: str) -> List[str]:
    loc = []
    conn = sqlite3.connect('local.db')    
    c = conn.cursor()
   #c.execute("SELECT * FROM localcode WHERE code LIKE '?'", ('%'+district+'%'))
    c.execute("select * from localcode where loc like ?", ('%'+district+'%',))
    for data in c.fetchall():
        loc.append(data)

    return loc
    
