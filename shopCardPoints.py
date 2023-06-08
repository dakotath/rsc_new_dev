import sqlite3
import hashlib
import datetime
import random 
import os


def setupDatabasePoints(conn, cursor):
    table ="""
    CREATE TABLE pointsPurchases(
        serial VARCHAR(255),
        token VARCHAR(255),
        amount VARCHAR(255),
        isPayed VARCHAR(255)
    );
    """
    cursor.execute(table)
    conn.commit()
def setupDatabaseUsers(conn, cursor):
    table ="""
    CREATE TABLE users(
        serial VARCHAR(255),
        name VARCHAR(255) DEFAULT 'anonymous',
        points VARCHAR(255)
    );
    """
    cursor.execute(table)
    conn.commit()

def createUser(conn, cursor, serial, name="anonymous"):
    print("Creating user {} with serial {}".format(name, serial))
    cursor.execute("""
    INSERT INTO users VALUES (
        '{}',
        '{}',
        '{}'
    )
    """.format(serial, name, "0"))
    conn.commit()
    print("Created!\n")

def createTestAccounts(conn, cursor):
    print("Creating users test0 and test1")
    createUser(conn, "LU0000000 00000000", name="test0")
    createUser(conn, "LU0000000 00000001", name="test1")

def checkExistantUser(conn, cursor, serial):
    statement = '''SELECT * FROM users WHERE serial="{}"'''.format(serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)
    output = cursor.fetchall()
    conn.commit()
    if len(output) < 1:
        return False
    else:
        return True

def genPaymentToken(conn, cursor, serial, amt):
    dayPurchased = str(datetime.datetime.now().day)+str(datetime.datetime.now().month)+str(datetime.datetime.now().year)+str(random.randint(0, 100000))
    purchaseInfo = "POINTSPURCHASE:"+serial+"_"+str(amt)+"_"+dayPurchased
    token = hashlib.md5(purchaseInfo.encode()).hexdigest()
    print("Generated Info for MD5 hash:\n{}\nToken:{}".format(purchaseInfo, token))
    cursor.execute("""
    INSERT INTO pointsPurchases VALUES (
        '{}',
        '{}',
        '{}',
        'false'
    )
    """.format(serial, token, str(amt)))
    conn.commit()
    return token

def searchForPayment(conn, cursor, serial, amt, day, month, year):
    dayPurchased = str(day)+str(month)+str(year)
    purchaseInfo = "POINTSPURCHASE:"+serial+"_"+str(amt)+"_"+dayPurchased
    token = hashlib.md5(purchaseInfo.encode()).hexdigest()
    print("Searching for purchase with info:\n  RAW:{}\n  Token:{}".format(purchaseInfo, token))

    statement = '''SELECT * FROM pointsPurchases WHERE token="{}"'''.format(token)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    print("Listing result")
    output = cursor.fetchall()
    for row in output:
        print(row)
    conn.commit()
    print("Done listing\n")

def makePayment(conn, cursor, serial, token, msg):
    print("Updating stats for token "+token)

    # purchase
    statement = '''SELECT * FROM pointsPurchases WHERE token="{}" AND serial="{}"'''.format(token, serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    purchasedAmount = round(float(output[0][2])*100)
    paymentStatus = output[0][3]

    # user
    statement = '''SELECT * FROM users WHERE serial="{}"'''.format(serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    userPoints = round(float(output[0][2]))
    userName = output[0][1]
    newAmount = purchasedAmount+userPoints

    print("{} purchased {} Wii Points.\nNow has a total of {} Wii points.\nAdding to database.".format(userName, purchasedAmount, newAmount))


    cursor.execute('''UPDATE pointsPurchases SET isPayed = "{}" WHERE token="{}" AND serial="{}";'''.format(msg, token, serial))
    cursor.execute('''UPDATE users SET points = "{}" WHERE serial="{}";'''.format(newAmount, serial))
    print("done")
    conn.commit()

def modifyPoints(conn, cursor, serial, points):    
    # user
    statement = '''SELECT * FROM users WHERE serial="{}"'''.format(serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    userPoints = round(float(output[0][2]))
    userName = output[0][1]

    cursor.execute('''UPDATE users SET points = "{}" WHERE serial="{}";'''.format(points, serial))
    print("done")
    conn.commit()

def getPoints(conn, cursor, serial):    
    # user
    statement = '''SELECT * FROM users WHERE serial="{}"'''.format(serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    userPoints = round(float(output[0][2]))
    userName = output[0][1]

    print("{} checked their points balence. they have {} Wii Points.".format(userName, userPoints))
    print("done")
    conn.commit()
    return int(userPoints)

def getPaymentInfo(conn, cursor, token):
    statement = '''SELECT * FROM pointsPurchases WHERE token = "{}"'''.format(token)
  
    cursor.execute(statement)
    
    print("Listing all purchases")
    output = cursor.fetchall()
    print(output)
    conn.commit()
    return output[0]

def getPaymentInfos(conn, cursor):
    statement = '''SELECT * FROM pointsPurchases'''
  
    cursor.execute(statement)
    
    print("Listing all purchases")
    output = cursor.fetchall()
    for row in output:
        print(row)
    conn.commit()
    print("Done listing\n")

def getUserInfos(conn, cursor):
    statement = '''SELECT * FROM users'''
  
    cursor.execute(statement)
    
    print("Listing all users")
    output = cursor.fetchall()
    for row in output:
        print(row)
    conn.commit()
    print("Done listing\n")
    print(output)
    return output

def getUserInfo(conn, cursor, serial, token):
    # purchase
    statement = '''SELECT * FROM pointsPurchases WHERE token="{}" AND serial="{}"'''.format(token, serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    purchasedAmount = round(float(output[0][2])*100)
    paymentStatus = output[0][3]

    # user
    statement = '''SELECT * FROM users WHERE serial="{}"'''.format(serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    userPoints = round(float(output[0][2]))
    userName = output[0][1]
    newAmount = purchasedAmount+userPoints
    
    print("done")
    conn.commit()
    return (userName, userPoints, purchasedAmount, paymentStatus)

def getUserPoints(conn, cursor, serial):
    # user
    statement = '''SELECT * FROM users WHERE serial="{}"'''.format(serial)
    print("Executing '"+statement+"' into database.\n")
    cursor.execute(statement)

    output = cursor.fetchall()
    userPoints = round(float(output[0][2]))
    userName = output[0][1]
    
    print("done")
    conn.commit()
    return (userName, userPoints)


#testDatabaseApp()
#createUser("LU0000000 00000000", name="Dakota Thorpe")
#setupDatabaseUsers()
#setupDatabasePoints()
#genPaymentToken("LU0000000 00000000", 5.00)
#makePayment("LU0000000 00000000", "edc9701385c6ba80db0f2c5b944fdf70", "paid")
#createTestAccounts()
#getPaymentInfos()
#searchForPayment("LU0000000 00000000", 5.00, 21, 3, 2023)
#searchForPayment("LU0000000 00000001", 50.00, 21, 3, 2023)