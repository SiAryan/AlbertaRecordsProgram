import sqlite3
from datetime import date
today = date.today()

with sqlite3.connect('p1.db') as db:
    c = db.cursor()

# get the user city
def getUserCity(uid):
    c = db.execute('''SELECT * FROM users WHERE uid = ?''', [uid])
    #print(c.fetchone())
    return c.fetchone()[-1]

def nameExists(fname, lname):
    c = db.execute('''SELECT * FROM persons WHERE fname = ? AND lname = ?''', [fname, lname])
    row = c.fetchone()
    if not(row == None):
        return True
    else:
        return False    


def checkPartners(p1, p2):
    c = db.execute('''SELECT * FROM persons WHERE fname = ? AND lname = ?''', p1)
    row_a = c.fetchone()
    c = db.execute('''SELECT * FROM persons WHERE fname = ? AND lname = ?''', p2)
    row_b = c.fetchone()
    if not(row_a == None) and not(row_b == None):
        return [True, True]
    
    elif not(row_a == None) and row_b == None:
        return [True, False]
    elif row_a == None and not(row_b == None):
        return [False, True]
    else:
        return [False, False]

def checkregno(regno):
    c = db.execute('''SELECT * FROM registrations WHERE regno = ? ''', [regno])
    row = c.fetchone()
    print(row)
    if not(row == None):
        return True
    else:
        return False



def  checkParents(pA, pB):
    c = db.execute('''SELECT * FROM persons WHERE fname = ? AND lname = ?''', pA)
    row_a = c.fetchone()
    c = db.execute('''SELECT * FROM persons WHERE fname = ? AND lname = ?''', pB)
    row_b = c.fetchone()

    if not(row_a == None) and not(row_b == None):
        return [True, True]
    
    elif not(row_a == None) and row_b == None:
        return [True, False]
    elif row_a == None and not(row_b == None):
        return [False, True]
    else:
        return [False, False]

        
def checkUser(uid, pwd):
    c = db.execute('''SELECT * FROM users WHERE uid = ? AND pwd = ?''', [uid, pwd])
    row = c.fetchone()
    if row == None:
        return 0  
    elif not(row == None):
        return [row[0], row[2]]



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

def maxAmount(tno):
    c = db.execute('''SELECT * FROM tickets WHERE tno == ?''', [tno])
    row = c.fetchone()
    fine = row[2]
    c = db.execute('''SELECT SUM(amount) FROM payments WHERE tno = ? GROUP BY tno''', [tno])
    rowb = c.fetchone()
    if rowb == None:
        return fine
    else:
        return fine - rowb[0]

def processPayment(tno, amount):
    pdate = today.strftime("%Y-%m-%d")
   
    entry = [tno, pdate, amount]
    db.execute('''INSERT INTO payments VALUES
                    (?, ?, ?)''', entry)
    db.commit()
    


def getDriverAbstract(fname, lname, ordered):
    order = False
    if ordered == "yes":
        order = True
    elif ordered == "no":
        order = False
    c = db.execute('''SELECT regno FROM registrations WHERE fname = ? AND lname = ?''', [fname, lname])
    regno = c.fetchone()[0]
    c = db.execute('''SELECT SUM(tno) FROM tickets WHERE regno == ?''', [regno])
    num_tickets = c.fetchone()[0]
    c = db.execute('''SELECT COUNT(*) FROM demeritNotices WHERE fname = ? AND lname = ?''', [fname, lname])
    num_dem = c.fetchone()[0]
    c = db.execute('''SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? GROUP BY fname AND lname''', [fname, lname])
    total_dem = c.fetchone()[0]
    c = db.execute('''SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? AND ddate > DATE('now', '-1 year')''', [fname, lname])
    past2_dem = c.fetchone()[0]
    
    if order:
        c = db.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t, vehicles v, registrations r 
        WHERE t.regno = r.regno AND r.vin = v.vin AND r.fname = ? AND r.lname = ? ORDER by t.vdate desc''', [fname, lname])   
        ticketRow = c.fetchall()
    else:
        c = db.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t, vehicles v, registrations r 
        WHERE t.regno = r.regno AND r.vin = v.vin AND r.fname = ? AND r.lname = ? ''', [fname, lname])   
        ticketRow = c.fetchall()

    print([num_tickets, num_dem, total_dem, past2_dem])
    
    for i in ticketRow:
        print(i)


def checkValidRegistration(regno):
    c = db.execute('''SELECT r.fname, r.lname, v.make, v.model, v.year, v.color FROM registrations r, vehicles v    
        WHERE r.regno = ? AND r.vin = v.vin''', [regno])
    row = c.fetchone()
    
    print(row)
    if not(row == None):
        return True
    else:
        return False    

def issueTicket(regno, vdate, violation, fine):
    c = db.execute('''SELECT * FROM tickets GROUP BY NULL HAVING MAX(tno)''')
    run = True
    tno = None
    row = c.fetchone()
    if row == None:
        run = False
        tno = 1
    if run:
        tno = row[0] + 1
    
    entry = [tno, regno, fine, violation, vdate]
    db.execute('''INSERT INTO tickets values (?, ?, ?, ?, ?)''', entry)
    db.commit()

def FindCarOwner(make, model, year, color, plate):
    entry = [model, make, color, year, plate]
    db.execute('''SELECT * FROM vehicles v, registrations r 
                    WHERE (v.model = ? OR v.make = ? OR v.color = ? OR v.year = ? OR r.plate = ?) AND v.vin = r.vin''', entry)
    row = c.fetchall()
    for i in row:
        print(i)


def verifyTno(tno):
    c = db.execute('''SELECT * FROM tickets WHERE tno = ?''', [tno])
    row = c.fetchone()
    if not(row == None):
        return True
    else:
        return False

def checkVin(vin):
    c = db.execute('''SELECT * FROM vehicles WHERE vin = ?''', [vin])
    row = c.fetchone()
    if not(row == None):
        return True
    else:
        return False

def checkPerson(person):
    c = db.execute('''SELECT * FROM persons WHERE fname = ? AND lname = ?''', person)
    row = c.fetchone()
    if not(row == None):
        return True
    else:
        return False


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


def registerPerson(fname, lname, bdate, bplace, address, phone):
    details = [fname, lname, bdate, bplace, address, phone]
    db.execute('''INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)''', details)
    db.commit()


def main():
    
    #c = db.execute("SELECT * FROM users;")
    uid = 1
    registerBirth(uid, "o", "Singh", "female", ["kk", "Singh"], ["Seema","Singh"], "2008-04-11", "Allahabad")
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
    c = db.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM tickets t, vehicles v, registrations r 
    WHERE t.regno = r.regno AND r.vin = v.vin AND r.fname = ? AND r.lname = ? ORDER BY t.vdate desc''', [fname, lname])   
    ticketRow = c.fetchall()
  
    pA = ["Seea", "Singh"]
    pB = ["kk", "Singh"]
    #print(checkParents(pA, pB))


if __name__ == '__main__':
    main()