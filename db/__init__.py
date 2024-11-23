import sqlite3

# > connect if db exist - create if database doesn't.
connection = sqlite3.connect('epl343.db')
# > create cursor to access the db.
cursor = connection.cursor()

createUser = """CREATE TABLE IF NOT EXISTS USER
    ( 
    UID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME VARCHAR NULL CHECK(USERNAME GLOB '[a-zA-Z0-9_]*' AND LENGTH(USERNAME) BETWEEN 6 AND 15),
    PASS_HASHED VARCHAR NULL,
    SALT BLOB NULL,

    UNIQUE (USERNAME)
    )"""


createEntry = """CREATE TABLE IF NOT EXISTS ENTRY
    (
    MIN_REQUIREMENT INTEGER NULL CHECK(MIN_REQUIREMENT >= 0),
    QNT INTEGER NULL CHECK(QNT >= 0),
    SIZE INTEGER NULL CHECK(SIZE >= 0),
    CATEGORY VARCHAR NULL CHECK(CATEGORY GLOB '[a-zA-Z ]*'),
    NAME VARCHAR NULL CHECK(NAME GLOB '[a-zA-Z ]*'),
    SUPPLIER VARCHAR NULL CHECK(SUPPLIER GLOB '[a-zA-Z ]*'),
    PHOTO VARCHAR NULL,                        
    AVG_PER_WEEK REAL NULL,
    ENTRY_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UID INTEGER NULL,
    UNAVAILABLE CHAR NULL CHECK(UNAVAILABLE IN ('T', 'F')),

    FOREIGN KEY (UID) REFERENCES USER(UID),
    UNIQUE (NAME, SIZE)
    )"""

createLog = """CREATE TABLE IF NOT EXISTS LOG
    (
    LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATE_TIME DATETIME NULL,
    QNT_DIF INTEGER NULL,
    UID INTEGER NULL,
    ENTRY_ID INTEGER NULL,

    FOREIGN KEY (ENTRY_ID) REFERENCES ENTRY(ENTRY_ID),
    FOREIGN KEY (UID) REFERENCES USER(UID)
    )"""

createPendingTrans = """CREATE TABLE IF NOT EXISTS PENDING_TRANSACTIONS
    (
    TRANS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UID_REQ_TRANS INT NULL,
    UID_ANS_TRANS INT NULL,
    ENTRY_ID INT NULL, 
    QNT INT NULL,

    FOREIGN KEY (UID_REQ_TRANS) REFERENCES USER(UID),
    FOREIGN KEY (UID_ANS_TRANS) REFERENCES USER(UID),
    UNIQUE (TRANS_ID, UID_REQ_TRANS, UID_ANS_TRANS)
    )""" 

createQuickAccess = """CREATE TABLE IF NOT EXISTS QUICK_ACCESS
    (
    UID INT NULL,
    UID_OTHER INT NULL,

    PRIMARY KEY (UID, UID_OTHER),
    FOREIGN KEY (UID) REFERENCES USER(UID),
    FOREIGN KEY (UID_OTHER) REFERENCES USER(UID)
    )"""

cursor.execute(createUser)
cursor.execute(createEntry)
cursor.execute(createLog)
cursor.execute(createPendingTrans)
cursor.execute(createQuickAccess)

connection.commit() 
connection.close()