import getpass
import sys
import Methods as m

uid = None

STARTSCREEN = "startScreen"
LOGINSCREEN = "loginScreen"
AGENTSCREEN = "agentScreen"
OFFICERSCREEN = "officerScreen"
AGENTSUBSCREEN = "agentSubscreen"
OFFICERSUBSCREEN = "officerSubscreen"

def exit():
    print("Exiting the program...")
    sys.exit()

def loginScreen():
    print("===============================================================")
    print("Please log in...")
    userType = 0
    while userType == 0:
        username = getInput(LOGINSCREEN, "Username: ")
        print("Password: ", end='')
        password = getpass.getpass()
        userType = getUserType(username, password)
        if userType == 0:
            print("Username or password not found.\nRe-enter credentials...")
        else:
            break
    print()
    if userType == 1:
        agentScreen()
    elif userType == 2:
        officerScreen()

def startScreen(databaseName):
    print("===============================================================")
    print("Welcome to the Alberta Records program.")
    print("You can type in commands at any time, these will be specified for each screen.")
    printCommands(STARTSCREEN)
    while True:
        _ = getInput(STARTSCREEN, "> ")
        print("Please type a valid command.")

def registerBirth():
    print("===============================================================")
    print("Enter birth details:")
    fname = getInput(AGENTSUBSCREEN, "First name: ")
    lname = getInput(AGENTSUBSCREEN, "Last name: ")
    # TODO Aryan : Check if the name already exists DONE
    existsAlready = m.nameExists(fname, lname)
    if existsAlready == True:
        print("This person already exists, cannot register.")
        print("===============================================================")
        return
    gender = getInput(AGENTSUBSCREEN, "Gender: ")
    bday = getInput(AGENTSCREEN, "Birth Date: ")
    bplace = getInput(AGENTSUBSCREEN, "Birth place: ")
    m_fname = getInput(AGENTSUBSCREEN, "Mother's first name: ")
    m_lname = getInput(AGENTSUBSCREEN, "Mother's last name: ")
    f_fname = getInput(AGENTSUBSCREEN, "Father's first name: ")
    f_lname = getInput(AGENTSUBSCREEN, "Father's last name: ")
    # TODO Aryan : Check if both parents are in the database DONE
    pB = [m_fname, m_lname]
    pA = [f_fname, f_lname]
    intable =  m.checkParents(pA, pB)
    motherFound = intable[1]
    fatherFound = intable[0]
    
    if motherFound == False:
        registerPerson(AGENTSUBSCREEN, "Mother")
    if fatherFound == False:
        registerPerson(AGENTSUBSCREEN, "Father")
    # TODO Aryan : Register the birth DONE
    m.registerBirth(uid, fname, lname, gender, pA, pB, bday, bplace)
    print("The birth has been recorded. Congratulations to the parents.")
    print("===============================================================")
    return

def registerMarriage():
    print("===============================================================")
    print("Enter marriage details:")
    p1_fname = getInput(AGENTSUBSCREEN, "Partner 1 first name: ")
    p1_lname = getInput(AGENTSUBSCREEN, "Partner 1 last name: ")
    p2_fname = getInput(AGENTSUBSCREEN, "Partner 2 first name: ")
    p2_lname = getInput(AGENTSUBSCREEN, "Partner 2 last name: ")
    # TODO Aryan : Check if both the partners are in the database DONE
    p1 = [p1_fname, p1_lname]
    p2 = [p2_fname, p2_lname]
    intable = m.checkPartners(p1, p2)
    partner1Found = intable[0]
    partner2Found = intable[1]
    if partner1Found == False:
        registerPerson(AGENTSUBSCREEN, "Partner 1")
    if partner2Found == False:
        registerPerson(AGENTSUBSCREEN, "Partner 2")
    # TODO Aryan : Register the marriage DONE
    m.registerMarrige(uid, p1, p2)
    print("The marriage has been recorded. Congratulations to the couple.")
    print("===============================================================")
    return

def renewRegistration():
    print("===============================================================")
    print("Enter the registrations's details:")
    regnoValid = False
    while regnoValid == False:
        regno = getInput(AGENTSUBSCREEN, "Registration number: ")
        # TODO Aryan : Verify if it's a valid registration number  DONE
        valid = m.checkregno(regno)
        if not(valid):
            print("Registration number invalid, please try again...")
        else:
            break
    m.renewRegistration(regno)
    # TODO Aryan : Set the new expiry data for the registration DONE
    print("The registration has been renewed.")
    return

def agentScreen():
    print("===============================================================")
    print("Welcome to the Agent home page.")
    printCommands(AGENTSCREEN)
    while True:
        _ = getInput(AGENTSCREEN, "> ")
        print("Please type a valid command.")

def processBill():
    print("===============================================================")
    print("Enter details about the bill of sale:")
    vin = ""
    currentowner_fname = ""
    currentowner_lname = ""
    vinValid = False
    nameMatches = False
    while vinValid == False:
        vin = getInput(AGENTSUBSCREEN, "Vin: ")
        vinValid = m.checkVin(vin)
        # TODO Aryan : Verify if the vin is in the database DONE
        if vinValid == False:
            print("That vin was not found in the database! Please re-enter...")
    while nameMatches == False:
        currentowner_fname = getInput(AGENTSUBSCREEN, "Current owner first name: ")
        currentowner_lname = getInput(AGENTSUBSCREEN, "Current owner last name: ")
        # TODO Aryan : Verify if the name matches the name registered DONE
        nameMatches = m.checkPerson([currentowner_fname, currentowner_lname])
        if nameMatches == False:
            print("That name was not found in the database! Please re-enter...")
    newowner_fname = getInput(AGENTSUBSCREEN, "New owner first name: ")
    newowner_lname = getInput(AGENTSUBSCREEN, "New owner last name: ")
    # TODO Aryan : Check that the person exitsts DONE
    newownerExists = m.checkPerson([newowner_fname, newowner_lname])
    if newownerExists == False:
        print("That name was not found in the database! Transaction cannot be completed.")
        agentScreen()
    plateno = getInput(AGENTSUBSCREEN, "Plate number: ")
    # TODO Aryan : Record the new registration in the database DONE
    m.processBillOfSale(vin, [newowner_fname, newowner_lname], [currentowner_fname, currentowner_lname], plateno)
    print("The bill of sale has been recorded.")
    print("===============================================================")
    return

def processPayment():
    print("===============================================================")
    print("Enter details about the ticket payment:")
    tno = ""
    tnoValid = False
    while tnoValid == False:
        tno = getInput(AGENTSUBSCREEN, "Ticket number: ")
        # TODO Aryan : Verify it's a valid tno DONE
        tnoValid = m.verifyTno(tno)
        if tnoValid == False:
            print("Ticket number invalid! Please enter a valid ticket number...")
    maxAmount = m.maxAmount(tno)
    # TODO Aryan : Calculate the max payment amount using queries DONE
    # maxAmount = {database.tickets.fine} - sum{{database.payments.amount}} DONE
    amount = 0
    amountValid = False
    while amountValid == False:
        amount = int(getInput(AGENTSUBSCREEN, "Amount: "))
        amountValid = amount <= maxAmount
        if amountValid == False:
            print("Amount being paid cannot exceed $" + str(maxAmount) + ", please re-enter...")
    m.processPayment(tno, amount)
    print("The payment has been recorded.")
    print("===============================================================")
    return

def getAbstract():
    print("===============================================================")
    print("Query a person's driver abstract given a name...")
    fname = getInput(AGENTSUBSCREEN, "First name: ")
    lname = getInput(AGENTSUBSCREEN, "Last name: ")
    validResponse = False
    ordering = ""
    while validResponse == False:
        ordering = getInput(AGENTSUBSCREEN, "Order from latest to oldest (yes,no)? ")
        if ordering == "yes" or ordering == "no":
            validResponse = True
        else:
            print("Please enter a response of either 'yes' or 'no'.")
    # TODO Aryan : Query the database and report the results DONE  
    m.getDriverAbstract(fname, lname, ordering)
    print("===============================================================")
    return

def officerScreen():
    print("===============================================================")
    print("Welcome to the Officer home page.")
    printCommands(OFFICERSCREEN)
    while True:
        _ = getInput(OFFICERSCREEN, "> ")
        print("Please type a valid command.")

def issueTicket():
	print("===============================================================")
	print("Issue a ticket to a given registration number:")
	regno = ""
	regnoValid = False
	while regnoValid == False:
		regno = getInput(OFFICERSUBSCREEN, "Registration number: ")
		# TODO Aryan : Check if the registration number is valid DONE
		regnoValid = m.checkValidRegistration(regno)

		if regnoValid == False:
			print("No information was found under that registration number")
	print("---------------------------------------------------------------")
    # TODO Aryan : Display the information found under the registration number DONE

	print("---------------------------------------------------------------")
	vdate = getInput(OFFICERSUBSCREEN, "Violation date: ")
	vtext = getInput(OFFICERSUBSCREEN, "Violation text: ")
	vfine = getInput(OFFICERSUBSCREEN, "Fine amount: ")
    # TODO Aryan : Record the ticket DONE
	m.issueTicket(regno, vdate, vtext, vfine)
	print("The registration has been ticketed.")
	print("===============================================================")
	return

def findCarOwner():
	print("===============================================================")
	print("Find a car owner given the car's information:")
	make = ""
	model = ""
	year = ""
	color = ""
	plate = ""
	while make == "" and model == "" and year == "" and color == "" and plate == "":
		make = getInput(OFFICERSUBSCREEN, "Make: ")
		model = getInput(OFFICERSUBSCREEN, "Model: ")
		year = getInput(OFFICERSUBSCREEN, "Year: ")
		color = getInput(OFFICERSUBSCREEN, "Color: ")
		plate = getInput(OFFICERSUBSCREEN, "Plate: ")
		if make == "" and model == "" and year == "" and color == "" and plate == "":
			print("Please provide one or more of the given specifications...")
	print("---------------------------------------------------------------")
	# TODO Aryan : Query these values and show the results
	m.FindCarOwner(make, model, year, color, plate)
	print("===============================================================")
	return

screenRules = {
    STARTSCREEN : {
        "/exit" : [exit, "Exits the program."],
        "/login" : [loginScreen, "Allows the user to log in."]
    },
    LOGINSCREEN : {
        "/exit" : [exit, "Exits the program."],
        "/back" : [startScreen, "Moves back to the introduction screen."]
    },
    AGENTSCREEN : {
        "/exit" : [exit, "Exits the program."],
        "/logout" : [loginScreen, "Logs the user out and returns to the login screen."],
        "/register a birth" : [registerBirth, "Allows the user to register a new birth."],
        "/register a marriage" : [registerMarriage, "Allows the user to register a marriage."],
        "/renew registration" : [renewRegistration, "Renew a vehicle registration."],
        "/process bill" : [processBill, "Process a bill of sale."],
        "/process payment" : [processPayment, "Process a payment."],
        "/get abstract" : [getAbstract, "Gets a driver abstract."]
    },
    OFFICERSCREEN : {
        "/exit" : [exit, "Exits the program."],
        "/logout" : [loginScreen, "Logs the user out and returns to the login screen."],
        "/issue a ticket" : [issueTicket, "Issue a ticket."],
        "/find car owner" : [findCarOwner, "Find a car owner."]
    },
    AGENTSUBSCREEN : {
        "/exit" : [exit, "Exits the program."],
        "/logout" : [loginScreen, "Logs the user out and returns to the login screen."],
        "/back" : [agentScreen, "Moves back to the Agent home screen."]
    },
    OFFICERSUBSCREEN : {
        "/exit" : [exit, "Exits the program."],
        "/logout" : [loginScreen, "Logs the user out and returns to the login screen."],
        "/back" : [officerScreen, "Moves back to the Officer home screen."]
    }
}

def getPersonDetails():
    fname = input("First name: ")
    lname = input("Last name: ")
    birthdate = input("Birth date: ")
    birthplace = input("Birth place: ")
    address = input("Address: ")
    phoneNum = input("Phone number: ")
    ret = {"fname": fname, "lname": lname, "birthdate": birthdate, "birthplace": birthplace, "address": address, "phone": phoneNum}
    return ret

def registerPerson(personStr):
    print("---------------------------------------------------------------")
    print("The " + personStr + "'s details were not found in the database!")
    print("Please enter the " + personStr + "'s details:")
    details = dict()
    while True:
        details = getPersonDetails()
        if details["fname"] == "" or details["lname"] == "":
            print("First name or last name cannot be blank! Re-enter details...")
        else:
            break
    # TODO Aryan : Store these values in the database DONE
    m.registerPerson(details['fname'], details['lname'], details['birthdate'], details['birthplace'], details['address'], details['phone'])

    print("---------------------------------------------------------------")

def printCommands(screen):
    print("---------------------------------------------------------------")
    print("Commands here are:")
    global screenRules
    ourScreenRules = screenRules[screen]
    for command in ourScreenRules.keys():
        print(command + " => " + ourScreenRules[command][1])
    print("---------------------------------------------------------------")

def getPersonDetails(parentScreen):
    fname = getInput(parentScreen, "First name: ")
    lname = getInput(parentScreen, "Last name: ")
    birthdate = getInput(parentScreen, "Birth date: ")
    birthplace = getInput(parentScreen, "Birth place: ")
    address = getInput(parentScreen, "Address: ")
    phoneNum = getInput(parentScreen, "Phone number: ")
    ret = {"fname": fname, "lname": lname, "birthdate": birthdate, "birthplace": birthplace, "address": address, "phone": phoneNum}
    return ret

def registerPerson(parentScreen, personStr):
    print("---------------------------------------------------------------")
    print("The " + personStr + "'s details were not found in the database!")
    print("Please enter the " + personStr + "'s details:")
    details = dict()
    while True:
        details = getPersonDetails(parentScreen)
        if details["fname"] == "" or details["lname"] == "":
            print("First name or last name cannot be blank! Re-enter details...")
        else:
            break
    # TODO Aryan : Store these values in the database DONE
    m.registerPerson(details['fname'], details['lname'], details['birthdate'], details['birthplace'], details['address'], details['phone'])
    print("---------------------------------------------------------------")

def printCommands(screen):
    print("---------------------------------------------------------------")
    print("Commands here are:")
    global screenRules
    ourScreenRules = screenRules[screen]
    for command in ourScreenRules.keys():
        print(command + " => " + ourScreenRules[command][1])
    print("---------------------------------------------------------------")

def getInput(screen, printStr):
    global screenRules
    ourScreenRules = screenRules[screen]
    ret = input(printStr)
    if ret in ourScreenRules.keys():
        ourScreenRules[ret][0]()
        return ""
    else:
        return ret

""" This method will return 0 for invalid, 1 for agent, 2 for officer """
def getUserType(username, password):
    # TODO Aryan : Validate the username and password logins DONE
    # TODO Aryan : Find the user's type DONE
    row = m.checkUser(username, password)
    if row == 0:
        return 0
    else:
        #print(row)
        global uid 
        uid = row[0] 
        if row[1] == "Agent":
            return 1
        elif row[1] == "Traffic Officer":
            return 2
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter the name of the database as a command-line argument.")
        sys.exit()
