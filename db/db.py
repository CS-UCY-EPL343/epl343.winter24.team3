import sqlite3
import hashlib
import os

def search_inventory(uid, query):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    searchInv = """SELECT * FROM ENTRY WHERE UID = (?) AND NAME LIKE '%?%'"""
    cursor.execute(searchInv, (uid, query))
    rows = cursor.fetchall()
    connection.close()
    return rows    

def get_quick_switch_users(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    qsUsers = """SELECT U.USERNAME FROM USER U WHERE U.UID IN(SELECT Q.USER_OTHER FROM QUICK_ACCESS Q WHERE Q.UID = (?))"""
    cursor.execute(qsUsers, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_user_uid(new_username):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getUid = """SELECT UID FROM USER WHERE USERNAME = (?)"""
    cursor.execute(getUid, (new_username,))
    uid = cursor.fetchall()
    connection.close()
    return uid

def validate_user(new_username, password):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    validate = """SELECT PASS_HASHED, SALT FROM USER WHERE USERNAME = ?"""
    cursor.execute(validate, (new_username,))
    values = cursor.fetchall()
    pw, salt = values[0]
    connection.close()
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    if hashed_password == pw:
        return True
    else:
        return False    

def add_quick_switch_user(uid, new_username):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    new_uid = get_user_uid(new_username)
    cursor = connection.cursor()
    newQSuser = """INSERT INTO QUICK_ACCESS (UID, UID_OTHER) VALUES (?, ?)"""
    cursor.execute(newQSuser, (uid, new_uid))
    connection.commit()
    connection.close()

def user_exists(username):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    getUid = """SELECT UID FROM USER WHERE USERNAME = (?)"""
    cursor.execute(getUid, (username,))
    uid = cursor.fetchall()
    connection.close()
    if not uid:
        return False
    else:
        return True

def set_user(username, password):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    #encrypt password
    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    # > create cursor to access the db.
    cursor = connection.cursor()
    newUser = """INSERT INTO USER (USERNAME, PASS_HASHED, SALT) VALUES (?, ?, ?)"""
    cursor.execute(newUser, (username, hashed_password, salt))
    connection.commit()
    connection.close()

def get_inventory_data(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getInv = """SELECT * FROM ENTRY WHERE UID = (?) ORDER BY NAME DESC"""
    cursor.execute(getInv, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_category_options(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getCat = """SELECT DISTINCT CATEGORY FROM ENTRY WHERE UID = (?)"""
    cursor.execute(getCat, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_supplier_options(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getSup = """SELECT DISTINCT SUPPLIER FROM ENTRY WHERE UID = (?)"""
    cursor.execute(getSup, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def update_entry(entry_id, name, size, category, supplier, minreq, photo, qnt, unav): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    old_qnt = get_quantity(entry_id)
    updEntry = """UPDATE ENTRY SET NAME = (?), SIZE = (?), CATEGORY = (?), SUPPLIER = (?), MIN_REQUIREMENT = (?), PHOTO = (?), QNT = (?), UNAVAILABLE = (?) WHERE ENTRY_ID = (?)"""
    cursor.execute(updEntry, (name, size, category, supplier, minreq, photo, qnt, unav, entry_id))
    connection.commit()
    connection.close()
    if old_qnt[0] > qnt:
        add_log_ent(entry_id, (qnt - old_qnt[0]))

def create_entry(name, size, category, supplier, minreq, photo, qnt):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    createEntry = """INSERT INTO ENTRY (NAME, SIZE, CATEGORY, SUPPLIER, MIN_REQUIREMENT, PHOTO, QNT, UNAVAIlABLE) VALUES (?, ?, ?, ?, ?, ?, ?, 'F')"""
    cursor.execute(createEntry, (name, size, category, supplier, minreq, photo, qnt))
    connection.commit()
    connection.close()

def get_filtered_inventory(uid, category, supplier, qnt_filter): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()

    getAll = """SELECT * FROM ENTRY WHERE UID = (?)"""
    filterCat = """SELECT * FROM ENTRY WHERE UID = (?) AND CATEGORY = (?)"""
    filterSup = """SELECT * FROM ENTRY WHERE UID = (?) AND SUPPLIER = (?)"""
    filterUnav = """SELECT * FROM ENTRY WHERE UID = (?) AND UNAVAILABLE = 'T"""
    filterZero = """SELECT * FROM ENTRY WHERE UID = (?) AND QNT = 0"""
    filterBelowMin = """SELECT * FROM ENTRY WHERE UID = (?) AND (QNT<MIN_REQUIREMENT)"""
    filterCloseToMin = """SELECT * FROM ENTRY WHERE UID = (?) AND (QNT>MIN_REQUIREMENT) AND (QNT<=MIN_REQUIREMENT+5)"""
    filterMany = """SELECT * FROM ENTRY WHERE UID = (?) AND (QNT>=MIN_REQUIREMENT+5)"""

    if category == '':
        cursor.execute(getAll, (uid,))
    else:
        cursor.execute(filterCat, (uid, category))
    catFilter = cursor.fetchall()

    if supplier == '':
        cursor.execute(getAll, (uid,))
    else:
        cursor.execute(filterSup, (uid, supplier))
    supFilter = cursor.fetchall()

    if qnt_filter == '':
        cursor.execute(getAll, (uid,))
    elif qnt_filter == 'unavailable':
        cursor.execute(filterUnav, (uid,))
    elif qnt_filter == 'zero':
        cursor.execute(filterZero, (uid,))
    elif qnt_filter == 'below_minimum':
        cursor.execute(filterBelowMin, (uid,))
    elif qnt_filter == 'close_to_minimum':
        cursor.execute(filterCloseToMin, (uid,))
    elif qnt_filter == 'many':
        cursor.execute(filterMany, (uid,))
    qntFilter = cursor.fetchall()

    finalFilter = [x for x in catFilter if x in supFilter and x in qntFilter]
    return finalFilter

def generate_report(uid): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    report = """SELECT * FROM LOG WHERE (UID = (?)) AND (DATE <= datetime('now', 'localtime') AND (DATE <= datetime('now','-7 days', 'localtime'))"""
    cursor.execute(report, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_pending_transactions(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    pendingTrans = """SELECT * FROM PENDING_TRANSACTIONS WHERE UID_ANS_TRANS = (?)"""
    cursor.execute(pendingTrans, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def add_transaction(uid, to_uid, entry_id, qnt):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    createTrans = """INSERT INTO PENDING_TRANSACTIONS (UID_REQ_TRANS, UID_ANS_TRANS, ENTRY_ID, QNT) VALUES (?, ?, ?, ?)"""
    cursor.execute(createTrans, (uid, to_uid, entry_id, qnt))
    connection.commit()
    connection.close()

def transaction_exists(trans_id):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    getUid = """SELECT UID_REQ_TRANS FROM PENDING_TRANSACTIONS WHERE TRANS_ID = (?)"""
    cursor.execute(getUid, (trans_id,))
    uid = cursor.fetchall()
    connection.close()
    if not uid:
        return False
    else:
        return True

#if reqUser sends bottles, qnty negative?
def answer_transaction(trans_id, answer): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    if answer:
        getTrans = """SELECT UID_REQ_TRANS, UID_ANS_TRANS, ENTRY_ID, QNT FROM PENDING TRANSACTIONS WHERE TRANS_ID = (?)"""
        cursor.execute(getTrans, (trans_id,))
        values = cursor.fetchall()
        uidReq, uidAns, entry_id_req, qnt = values[0]
        getAnsEid = """SELECT A.ENTRY_ID FROM ENTRY R, ENTRY A WHERE R.ENTRY_ID = (?) AND A.UID = (?) AND A.NAME = R.NAME AND A.SIZE = R.SIZE"""
        cursor.execute(getAnsEid, (entry_id_req, uidAns))
        values = cursor.fetchall()
        entry_id_ans = values[0]
        increase_quantity(entry_id_req, qnt)
        decrease_quantity(entry_id_ans, qnt)
    delTrans = """DELETE FROM PENDING_TRANSACTIONS WHERE TRANS_ID = (?)"""
    cursor.execute(delTrans, (trans_id,))
    connection.commit()
    connection.close()

def increase_quantity(entry_id, qnt):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    old_qnt = get_quantity(entry_id)
    incQnt = "UPDATE ENTRY SET QNT = (?) WHERE ENTRY_ID = (?)"
    cursor.execute(incQnt, ((int(old_qnt[0])+qnt), entry_id))
    connection.commit()
    connection.close()
    add_log_ent(entry_id, qnt)

def decrease_quantity(entry_id, qnt): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    old_qnt = get_quantity(entry_id)
    if(old_qnt[0]<qnt):
        raise ValueError("Value bigger than quantity in stock!")
    decQnt = "UPDATE ENTRY SET QNT = (?) WHERE ENTRY_ID = (?)"
    cursor.execute(decQnt, ((int(old_qnt[0])-qnt), entry_id))
    connection.commit()
    connection.close()
    add_log_ent(entry_id, -(qnt))

def get_quantity(entry_id):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    getQnt = """SELECT QNT FROM ENTRY WHERE ENTRY_ID = (?)"""
    cursor.execute(getQnt, (entry_id,))
    qnt = cursor.fetchall()
    connection.close()
    return qnt

def add_log_ent(entry_id, qnt_dif):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db') 
    cursor = connection.cursor()
    getUid = """SELECT UID FROM ENTRY WHERE ENTRY_ID = (?)"""
    cursor.execute(getUid, (entry_id,))
    uid = cursor.fetchall()
    updateLog = """INSERT INTO LOG (UID, ENTRY_ID, QNT_DIF, DATE_TIME) VALUES (?, ?, ?, datetime('now', 'localtime'))"""
    cursor.execute(updateLog, (uid[0], qnt_dif, entry_id))
    connection.commit()
    connection.close()

def drop_all():
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('epl343.db')
    cursor = connection.cursor()
    
    dropQuickAccess = """DROP TABLE QUICK_ACCESS"""
    dropPendingTrans = """DROP TABLE PENDING_TRANSACTIONS"""
    dropLog = """DROP TABLE LOG"""
    dropEntry = """DROP TABLE ENTRY"""
    dropUser = """DROP TABLE USER"""

    cursor.execute(dropQuickAccess)
    cursor.execute(dropPendingTrans)
    cursor.execute(dropLog)
    cursor.execute(dropEntry)
    cursor.execute(dropUser)
    connection.commit()
    connection.close()
