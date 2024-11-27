import sqlite3
import hashlib
import os

#return all entries or none when query is empty?
def search_inventory(uid, query):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    searchInv = """SELECT * FROM ENTRY WHERE UID = (?) AND NAME LIKE (?)"""
    cursor.execute(searchInv, (uid, '%' + query + '%'))
    rows = cursor.fetchall()
    connection.close()
    return rows    

# Should return a list of the usernames. # TO
def get_quick_switch_users(uid: int) -> list[str]:
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    qsUsers = """SELECT U.USERNAME FROM USER U WHERE U.UID IN(SELECT Q.UID_OTHER FROM QUICK_ACCESS Q WHERE Q.UID = (?))"""
    cursor.execute(qsUsers, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_user_uid(new_username): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getUid = """SELECT UID FROM USER WHERE USERNAME = (?)"""
    cursor.execute(getUid, (new_username,))
    uid = cursor.fetchall()
    connection.close()
    try:
        return uid[0][0]
    except IndexError:
        raise Exception(f"Could not find user with username {new_username}") # TO

def validate_user(new_username: str, password: str) -> bool:
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    validate = """SELECT PASS_HASHED, SALT FROM USER WHERE USERNAME = ?"""
    cursor.execute(validate, (new_username,))
    values = cursor.fetchall()
    # Not registered
    if not values:
        return False
    pw, salt = values[0]
    connection.close()
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    if hashed_password == pw:
        return True
    else:
        return False    

def add_quick_switch_user(uid: int, new_username: str):
    new_uid = get_user_uid(new_username)
    if new_uid == uid:
        raise ValueError("Quick Access User can't be same as current user!")
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    newQSuser = """INSERT INTO QUICK_ACCESS (UID, UID_OTHER) VALUES (?, ?)"""
    cursor.execute(newQSuser, (uid, new_uid[0]))
    connection.commit()
    connection.close()

def user_exists(username: str) -> bool: 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    getUid = """SELECT UID FROM USER WHERE USERNAME = (?)"""
    cursor.execute(getUid, (username,))
    uid = cursor.fetchall()
    connection.close()
    if not uid:
        return False
    else:
        return True

def set_user(username: str, password: str) -> bool:
    try:
        # > connect if db exist - create if database doesn't.
        connection = sqlite3.connect('./db/epl343.db')
        #encrypt password
        salt = os.urandom(16)
        hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
        # > create cursor to access the db.
        cursor = connection.cursor()
        newUser = """INSERT INTO USER (USERNAME, PASS_HASHED, SALT) VALUES (?, ?, ?)"""
        cursor.execute(newUser, (username, hashed_password, salt))
        connection.commit()
        connection.close()
        return True
    except:
        return False

# Should return a dictionary with keys the column_names.lower() and values the results of the query  # TO
def get_inventory_data(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getInv = """SELECT * FROM ENTRY WHERE UID = (?) ORDER BY NAME DESC"""
    cursor.execute(getInv, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

# Should return a list of the category names. # TO
def get_category_options(uid: int) -> list[str]: 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getCat = """SELECT DISTINCT CATEGORY FROM ENTRY WHERE UID = (?)"""
    cursor.execute(getCat, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

# Should return a list of the category names. # TO
def get_supplier_options(uid: int) -> list[str]: 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getSup = """SELECT DISTINCT SUPPLIER FROM ENTRY WHERE UID = (?)"""
    cursor.execute(getSup, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def update_entry(entry_id, name, size, category, supplier, minreq, photo, qnt, unav): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    old_qnt = get_quantity(entry_id)
    updEntry = """UPDATE ENTRY SET NAME = (?), SIZE = (?), CATEGORY = (?), SUPPLIER = (?), MIN_REQUIREMENT = (?), PHOTO = (?), QNT = (?), UNAVAILABLE = (?) WHERE ENTRY_ID = (?)"""
    cursor.execute(updEntry, (name, size, category, supplier, minreq, photo, qnt, unav, entry_id))
    connection.commit()
    connection.close()
    if old_qnt != qnt:
        add_log_ent(entry_id, (qnt - old_qnt))

def create_entry(name, size, category, supplier, minreq, photo, qnt, uid):
    try:
        # > connect if db exist - create if database doesn't.
        connection = sqlite3.connect('./db/epl343.db')
        cursor = connection.cursor()
        createEntry = """INSERT INTO ENTRY (NAME, SIZE, CATEGORY, SUPPLIER, MIN_REQUIREMENT, PHOTO, QNT, UNAVAILABLE, UID) VALUES (?, ?, ?, ?, ?, ?, ?, 'F', ?)"""
        cursor.execute(createEntry, (name, size, category, supplier, minreq, photo, qnt, uid))
        connection.commit()
        connection.close()
    except:
        return

# Same as get_inventroy_data.  # TO
def get_filtered_inventory(uid: int, category: str, supplier: str, qnt_filter: str) -> list[str]: 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()

    getAll = """SELECT * FROM ENTRY WHERE UID = (?)"""
    filterCat = """SELECT * FROM ENTRY WHERE UID = (?) AND CATEGORY = (?)"""
    filterSup = """SELECT * FROM ENTRY WHERE UID = (?) AND SUPPLIER = (?)"""
    filterUnav = """SELECT * FROM ENTRY WHERE UID = (?) AND UNAVAILABLE = 'T'"""
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
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    report = """SELECT * FROM LOG WHERE UID = (?) AND DATE_TIME <= datetime('now', 'localtime') AND DATE_TIME >= datetime('now','-7 days', 'localtime')"""
    cursor.execute(report, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_pending_transactions(uid):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    pendingTrans = """SELECT * FROM PENDING_TRANSACTIONS WHERE UID_ANS_TRANS = (?)"""
    cursor.execute(pendingTrans, (uid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def add_transaction(uid, to_uid, entry_id, qnt): 
    if uid == to_uid:
        raise ValueError("Can't send transaction request to self!")
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    createTrans = """INSERT INTO PENDING_TRANSACTIONS (UID_REQ_TRANS, UID_ANS_TRANS, ENTRY_ID, QNT) VALUES (?, ?, ?, ?)"""
    cursor.execute(createTrans, (uid, to_uid, entry_id, qnt))
    connection.commit()
    connection.close()

def transaction_exists(trans_id):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
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
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    if answer:
        getTrans = """SELECT UID_REQ_TRANS, UID_ANS_TRANS, ENTRY_ID, QNT FROM PENDING_TRANSACTIONS WHERE TRANS_ID = (?)"""
        cursor.execute(getTrans, (trans_id,))
        values = cursor.fetchall()
        try:
            uidReq, uidAns, entry_id_req, qnt = values[0]
        except IndexError:
            return
        getAnsEid = """SELECT A.ENTRY_ID FROM ENTRY A, ENTRY R WHERE R.ENTRY_ID = (?) AND A.UID = (?) AND A.NAME = R.NAME AND A.SIZE = R.SIZE"""
        cursor.execute(getAnsEid, (entry_id_req, uidAns))
        values = cursor.fetchall()
        try:
            entry_id_ans = values[0][0]
        except ValueError:
            return
        decrease_quantity(entry_id_ans, qnt)
        increase_quantity(entry_id_req, qnt)
    delTrans = """DELETE FROM PENDING_TRANSACTIONS WHERE TRANS_ID = (?)"""
    cursor.execute(delTrans, (trans_id,))
    connection.commit()
    connection.close()

def increase_quantity(entry_id, qnt):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    old_qnt = get_quantity(entry_id)
    incQnt = "UPDATE ENTRY SET QNT = (?) WHERE ENTRY_ID = (?)"
    cursor.execute(incQnt, ((old_qnt+qnt), entry_id))
    connection.commit()
    connection.close()
    add_log_ent(entry_id, qnt)

def decrease_quantity(entry_id, qnt):
    old_qnt = get_quantity(entry_id)
    if(old_qnt<qnt):
       raise ValueError("Value bigger than quantity in stock!")
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    cursor = connection.cursor()
    decQnt = "UPDATE ENTRY SET QNT = (?) WHERE ENTRY_ID = (?)"
    cursor.execute(decQnt, ((old_qnt-qnt), entry_id))
    connection.commit()
    connection.close()
    add_log_ent(entry_id, -(qnt))

def get_quantity(entry_id): 
    """
    Throws:
    - IndexError if entry_id is not found.
    """
    try:
        # > connect if db exist - create if database doesn't.
        connection = sqlite3.connect('./db/epl343.db')
        cursor = connection.cursor()
        getQnt = """SELECT QNT FROM ENTRY WHERE ENTRY_ID = (?)"""
        cursor.execute(getQnt, (entry_id,))
        qnt = cursor.fetchall()
        connection.close()
        return qnt[0][0]
    except IndexError:
        print("🐍 File: db/db.py | Line: 301 | get_quantity ~ entry_id:", entry_id) # TO
        raise IndexError

def add_log_ent(entry_id, qnt_dif):
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db') 
    cursor = connection.cursor()
    getUid = """SELECT UID FROM ENTRY WHERE ENTRY_ID = (?)"""
    cursor.execute(getUid, (entry_id,))
    uid = cursor.fetchall()
    updateLog = """INSERT INTO LOG (UID, ENTRY_ID, QNT_DIF, DATE_TIME) VALUES (?, ?, ?, datetime('now', 'localtime'))"""
    cursor.execute(updateLog, (uid[0][0], qnt_dif, entry_id))
    connection.commit()
    connection.close()

def drop_all(): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
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

def get_entry_id(uid, name, size, supplier): 
    # > connect if db exist - create if database doesn't.
    connection = sqlite3.connect('./db/epl343.db')
    # > create cursor to access the db.
    cursor = connection.cursor()
    getUid = """SELECT ENTRY_ID FROM ENTRY WHERE NAME = (?) AND UID = (?) AND SIZE = (?) AND SUPPLIER = (?)"""
    cursor.execute(getUid, (name, uid, size, supplier))
    uid = cursor.fetchall()
    connection.close()
    try:
        return uid[0][0]
    except IndexError:
        return None

if __name__ == "__main__":
    try:
        drop_all()
    except sqlite3.OperationalError:
        ...
    finally:
        import __init__

    set_user('user_1', 'password1')
    set_user('user_2', 'paSSWORD2')
    uid1 = get_user_uid('user_1')
    uid2 = get_user_uid('user_2')
    create_entry('poto', 1000, 'vodka', 'maria', 10, '', 100, uid1)
    create_entry('poto', 1000, 'vodka', 'giorkos', 10, '', 100, uid2)
    create_entry('poto', 500, 'vodka', 'marios', 10, '', 100, uid1)
    create_entry('poto', 500, 'vodka', 'giorkos', 10, '', 100, uid1)
    create_entry('allo_poto', 1000, 'gin', 'giorkos', 10, '', 100, uid1)
    add_transaction(uid1, uid2, 1, 10)
    add_transaction(uid2, uid1, 3, 20)
    print(transaction_exists(1))
    answer_transaction(1, True)
    print(transaction_exists(1))
    print(generate_report(uid1))
    print(get_inventory_data(uid1))
    print('\n')
    update_entry(1, 'poto', 1000, 'vodka', 'maria', 10, '', 0, 'F')
    print(get_inventory_data(uid1))
    print('\n')
    print(get_filtered_inventory(uid1, '', '', 'zero'))
    print('\n')
    print(get_filtered_inventory(uid1, 'gin', '', ''))
    print('\n')
    print(get_pending_transactions(uid1))
    print('\n')
    print(get_pending_transactions(uid2))
    print('\n') 