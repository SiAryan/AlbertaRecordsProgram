import sqlite3
from datetime import date
today = date.today()

with sqlite3.connect('p1.db') as db:
    c = db.cursor()

# get the user city
def getUserCity(c):
    return c.fetchone()[-1]

def renewRegistration(regno):
    pdate = today.strftime("%Y-%m-%d")
    nums = pdate.split('-')
    nums[0] = str(int(nums[0]) + 1)
    fdate = '-'.join(nums)
    entry = [pdate, fdate]
    db.execute('''UPDATE registrations SET regdate=?, expiry=?''', entry)
    db.commit()

def processBillOfSale(vin, cname, nname, plate):
    pdate = today.strftime("%Y-%m-%d")
    nums = pdate.split('-')
    nums[0] = str(int(nums[0]) + 1)
    fdate = '-'.join(nums)

    c = db.execute('''SELECT * FROM registrations GROUP BY NULL HAVING MAX(regno)''')
    run = True
    regno = 1
    row = c.fetchone()
    
    if row == None:
        run = False
    if run:
       regno = row[0] + 1
    entry = [regno, pdate, fdate, plate, vin, nname[0], nname[1]]
    db.execute('''INSERT INTO registrations VALUES
                (?, ?, ?, ?, ?, ? , ?)''', entry)
    db.commit()

def processPayment(tno, amount):
    pdate = today.strftime("%Y-%m-%d")
    c = db.execute('''SELECT * FROM tickets WHERE tno == ?''', [tno])
    row = c.fetchone()
    fine = row[2]
    if amount > fine:
        return
    c = db.execute('''SELECT SUM(amount) FROM payments WHERE tno = ? GROUP BY tno''', [tno])
    rowb = c.fetchone()
    if rowb == None:
        entry = [tno, pdate, amount]
        db.execute('''INSERT INTO payments VALUES
                        (?, ?, ?)''', entry)
        db.commit()
    elif amount <= (fine-rowb[0]):
        entry = [tno, pdate, amount]
        db.execute('''INSERT INTO payments VALUES
                        (?, ?, ?)''', entry)
        db.commit()
    else:
        return

def getDriverAbstract(fname, lname):
    c = db.execute('''SELECT regno FROM registrations WHERE fname = ? AND lname = ?''', [fname, lname])
    regno = c.fetchone()[0]
    c = db.execute('''SELECT SUM(tno) FROM tickets WHERE regno == ?''', [regno])
    num_tickets = c.fetchone()[0]
    c = db.execute('''SELECT COUNT(*) FROM demeritNotices WHERE fname = ? AND lname = ?''', [fname, lname])
    num_dem = c.fetchone()[0]
    c = db.execute('''SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? GROUP BY fname AND lname''')
    total_dem = c.fetchone()[0]
    c = db.execute('''SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? AND ddate > DATE('now', '-1 year')''')
    past2_dem = c.fetchone()[0]

def registerBirth(user, fname, lname, gender, parentA, parentB, bday, bplace):
    regplace = getUserCity(user)   
    date = today.strftime("%Y-%m-%d")
    f_fname = parentA[0]
    f_lname = parentA[1]
    m_fname = parentB[0]
    m_lname = parentB[1]
   
    c = db.execute('''SELECT * FROM births GROUP BY NULL HAVING MAX(regno)''')
    run = True
    regno = None
    row = c.fetchone()
    if row == None:
        run = False
        regno = 1
    if run:
        regno = row[0] + 1
       
    
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
    date = today.strftime("%Y-%m-%d")
    
    c = db.execute('''SELECT * FROM marriages GROUP BY NULL HAVING MAX(regno)''')
    run = True
    regno = 1
    row = c.fetchone()
    
    if row == None:
        run = False
    if run:
       regno = row[0] + 1
        

    regplace = getUserCity(user)
    fnameA = pA[0]
    lnameA = pA[1]
    fnameB = pB[0]
    lnameB = pB[1]
    entry = [regno, date, regplace, fnameA, lnameA, fnameB, lnameB]

    c.execute('''INSERT INTO marriages VALUES 
            (?, ?, ?, ?, ?, ?, ?)''', entry)
    db.commit()




def main():
    
    #c = db.execute("SELECT * FROM users;")
    #registerBirth(c, "g", "Singh", "female", ["kk", "Singh"], ["Seema","Singh"], "2008-04-11", "Allahabad")
    #regno = 1
    #c = db.execute('''SELECT * FROM registrations WHERE regno == ?''', [regno])
    #print(c.fetchone())
    #c = db.execute("SELECT * FROM users;")
    #registerMarrige(c, ["kk","Singh"], ["Seema", "Singh"])
    #c.execute('''SELECT * FROM users''')
    #print(getUserCity(c))
    #c = db.execute('''SELECT MAX(regno) FROM births''')
    #print(c.fetchone())
    #c = db.execute('''SELECT * FROM persons WHERE fname == (?) AND lname == (?)''', ["Seema","Singh"])
    #print(c.fetchone()[-1])
    #processBillOfSale(1, ["Aryan","Singh"], ["Luke","Kapeluck"], "abc123")
    #renewRegistration(regno)
    fname = "Aryan"
    lname = "Singh"
    c = db.execute('''SELECT regno FROM registrations WHERE fname = ? AND lname = ?''', [fname, lname])
    regno = c.fetchone()[0]
    c = db.execute('''SELECT SUM(tno) FROM tickets WHERE regno == ?''', [regno])
    num_tickets = c.fetchone()[0]
    c = db.execute('''SELECT COUNT(*) FROM demeritNotices WHERE fname = ? AND lname = ?''', [fname, lname])
    num_dem = c.fetchone()[0]    
    c = db.execute('''SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? AND ddate > DATE('now', '-1 year')''', [fname, lname])
    past2_dem = c.fetchone()[0]
    print(past2_dem)
    

if __name__ == '__main__':
    main()