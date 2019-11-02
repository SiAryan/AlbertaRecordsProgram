import sqlite3
import time

with sqlite3.connect('p1.db') as db:
    c = db.cursor()
# get the user city


def getUserCity(c):
    return c.fetchone()[-1]



def registerBirth(user, fname, lname, gender, parentA, parentB, bday, bplace):
    regplace = getUserCity(user)   
    date = time.strftime("%Y-%M-%D")
    f_fname = parentA[0]
    f_lname = parentA[1]
    m_fname = parentB[0]
    m_lname = parentB[1]
    
    c = db.execute('''SELECT * FROM births GROUP BY regno HAVING MAX(regno)''')
    if (c.fetchone() == None): 
        regno = 1   
    elif (c.fetchone() != None): 
        regno = c.fetchone()[0] + 1
    
    motherinfo = [db.execute('''SELECT * FROM persons WHERE fname == (?) AND lname == (?)''',parentB).fetchone()[-2], db.execute('''SELECT * FROM persons WHERE fname == (?) AND lname == (?)''',parentB).fetchone()[-1]] 
    address = motherinfo[0]
    phone = motherinfo[1]
    
    entry = [regno, fname, lname, date, regplace, gender, f_fname, f_lname, m_fname, m_lname]
    entry2 = [fname, lname, bday, bplace, address, phone]
    c.execute('''INSERT INTO births VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', entry)
    db.commit()

    c.execute('''INSERT INTO persons VALUES
                (?, ?, ?, ?, ?, ?)''', entry2)
    db.commit()


def registerMarrige(user, pA, pB):
    date = time.strftime("%Y-%M-%D")
    regno = 0
    c = db.execute('''SELECT * FROM marriages GROUP BY regno HAVING MAX(regno)''')
    if (c.fetchone() == None): 
        regno = 1   
    elif (c.fetchone() != None): 
        regno = c.fetchone()[0] + 1
    regplace = getUserCity(user)
    fnameA = pA[0]
    lnameA = pA[1]
    fnameB = pA[0]
    lnameB = pB[1]
    entry = [regno, date, regplace, fnameA, lnameA, fnameB, lnameB]

    c.execute('''INSERT INTO marriages VALUES 
            (?, ?, ?, ?, ?, ?, ?)''', entry)
    db.commit()


def main():
    
    c = db.execute("SELECT * FROM users;")
    #registerBirth(c, "k", "Singh", "female", ["kk", "Singh"], ["Seema","Singh"], "2008-04-11", "Allahabad")
    
    #c = db.execute("SELECT * FROM users;")
    #registerMarrige(c, ["kk","Singh"], ["Seema", "Singh"])
    #c.execute('''SELECT * FROM users''')
    #print(getUserCity(c))
    #c = db.execute('''SELECT MAX(regno) FROM births''')
    #print(c.fetchone())
    #c = db.execute('''SELECT * FROM persons WHERE fname == (?) AND lname == (?)''', ["Seema","Singh"])
    #print(c.fetchone()[-1])
    c = db.execute('''SELECT * FROM births GROUP BY regno HAVING MAX(regno)''')
    print(c.fetchone()[0])




if __name__ == '__main__':
    main()