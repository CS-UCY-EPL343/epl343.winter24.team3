import sqlite3
import hashlib

# > connect if db exist - create if database doesn't.
connection = sqlite3.connect('epl343.db')

#needs uid also
def search_inventory(query):
    # > create cursor to access the db.
    cursor = connection.cursor()
    searchInv = """SELECT * FROM ENTRY WHERE NAME LIKE '%?%'"""
    cursor.execute(searchInv, (query))
    rows = cursor.fetchall()
    connection.close()
    return rows    

#assume that uid is given as int?
def getQuickSwitchUsers(uid):
    # > create cursor to access the db.
    cursor = connection.cursor()
    qsUsers = """SELECT U.USERNAME FROM USER U WHERE U.UID IN(SELECT Q.USER_OTHER FROM QUICK_ACCESS Q WHERE Q.UID = (?))"""
    cursor.execute(qsUsers, (uid))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_user_uid(new_username):
    # > create cursor to access the db.
    cursor = connection.cursor()
    getUid = """SELECT UID FROM USER WHERE USERNAME = (?)"""
    cursor.execute(getUid, (new_username))
    uid = cursor.fetchall()
    connection.close()
    return uid

def validate_user(new_username, password):
    # > create cursor to access the db.
    cursor = connection.cursor()
    validate = """SELECT PASS_HASHED FROM USER WHERE USERNAME = (?)"""
    cursor.execute()
    pw = cursor.fetchall()
    connection.close()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password == pw:
        return True
    else:
        return False    

def addQuickSwitchUser(uid, new_username):
    # > create cursor to access the db.
    new_uid = get_user_uid(new_username)
    cursor = connection.cursor()
    newQSuser = """INSERT INTO QUICK_ACCESS (UID, UID_OTHER) VALUES (?, ?)"""
    cursor.execute(newQSuser, (uid, new_uid))
    connection.commit()
    connection.close()

def isUsernameTaken(username):
    cursor = connection.cursor()
    getUid = """SELECT UID FROM USER WHERE USERNAME = (?)"""
    cursor.execute(getUid, (username))
    uid = cursor.fetchall()
    connection.close()
    if not uid:
        return False
    else:
        return True

def set_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # > create cursor to access the db.
    cursor = connection.cursor()
    newUser = """INSERT INTO USER (USERNAME, PASS_HASHED) VALUES (?, ?)"""
    cursor.execute(newUser, (username, hashed_password))
    connection.commit()
    connection.close()

def getInventoryData(uid):
    # > create cursor to access the db.
    cursor = connection.cursor()
    getInv = """SELECT * FROM ENTRY WHERE UID = (?) ORDER BY NAME DESC"""
    cursor.execute(getInv, (uid))
    rows = cursor.fetchall()
    connection.close()
    return rows

def getCategoryOptions(uid):
    # > create cursor to access the db.
    cursor = connection.cursor()
    getCat = """SELECT DISTINCT CATEGORY FROM ENTRY WHERE UID = (?)"""
    cursor.execute(getCat, (uid))
    rows = cursor.fetchall()
    connection.close()
    return rows

def getSupplierOptions(uid):
    # > create cursor to access the db.
    cursor = connection.cursor()
    getSup = """SELECT DISTINCT SUPPLIER FROM ENTRY WHERE UID = (?)"""
    cursor.execute(getSup, (uid))
    rows = cursor.fetchall()
    connection.close()
    return rows

#item_uid = entry_id?
def updateEntry(entry_id, name, size, category, supplier, minreq, photo, qnt):
    cursor = connection.cursor()
    updEntry = """UPDATE ENTRY SET NAME = (?), SIZE = (?), CATEGORY = (?), SUPPLIER = (?), MINREQ = (?), PHOTO = (?), QNT = (?) WHERE ENTRY_ID = (?)"""
    cursor.execute(updEntry, (name, size, category, supplier, minreq, photo, qnt, entry_id))
    connection.commit()
    connection.close()

def createEntry(name, size, category, supplier, minreq, photo, qnt):
    cursor = connection.cursor()
    createEntry = """INSERT INTO ENTRY (NAME, SIZE, CATEGORY, SUPPLIER, MINREQ, PHOTO, QNT) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(createEntry, (name, size, category, supplier, minreq, photo, qnt))
    connection.commit()
    connection.close()

#def getFilteredInventory(uid, category, supplier, qnt_filter):

#def generateReport(uid):

#does a user also get the transactions they requested themselves??
def getPendingTransactions(uid):
    # > create cursor to access the db.
    cursor = connection.cursor()
    pendingTrans = """SELECT * FROM PENDING_TRANSACTIONS WHERE UID_ANS_TRANS = (?)"""
    cursor.execute(pendingTrans, (uid))
    rows = cursor.fetchall()
    connection.close()
    return rows

#not needed 
def user_exists(to_user):
    return isUsernameTaken(to_user)

def addTransaction(uid, to_uid, entry_id, qnt):
    cursor = connection.cursor()
    createTrans = """INSERT INTO PENDING_TRANSACTIONS (UID_REQ_TRANS, UID_ANS_TRANS, ENTRY_ID, QNT) VALUES (?, ?, ?, ?)"""
    cursor.execute(createTrans, (uid, to_uid, entry_id, qnt))
    connection.commit()
    connection.close()

def transaction_exists(trans_id):
    cursor = connection.cursor()
    getUid = """SELECT UID_REQ_TRANS FROM PENDING_TRANSACTIONS WHERE TRANS_ID = (?)"""
    cursor.execute(getUid, (trans_id))
    uid = cursor.fetchall()
    connection.close()
    if not uid:
        return False
    else:
        return True

#how should answer work?
#def answertransaction(trans_id, answer):

def IncreaseQuantity(entry_id, qnt):
    cursor = connection.cursor()
    old_qnt = getQuantity(entry_id)
    incQnt = "UPDATE ENTRY SET QNT = (?) WHERE ENTRY_ID = (?)"
    cursor.execute(incQnt, ((int(old_qnt[0])+qnt), entry_id))
    connection.commit()
    connection.close()

#error handling if old qnt < qnt ?
def DecreaseQuantity(entry_id, qnt):
    cursor = connection.cursor()
    old_qnt = getQuantity(entry_id)
    decQnt = "UPDATE ENTRY SET QNT = (?) WHERE ENTRY_ID = (?)"
    cursor.execute(decQnt, ((int(old_qnt[0])-qnt), entry_id))
    connection.commit()
    connection.close()

def getQuantity(entry_id):
    cursor = connection.cursor()
    getQnt = """SELECT QNT FROM ENTRY WHERE ENTRY_ID = (?)"""
    cursor.execute(getQnt, (entry_id))
    qnt = cursor.fetchall()
    connection.close()
    return qnt