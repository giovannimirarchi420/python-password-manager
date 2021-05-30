import sqlite3
import hashlib
import os
import base64
from tabulate import tabulate
import pyAesCrypt
from getpass import getpass

pas = ''

def cryptdb(secret):
    global pas
    
    encrypted_data = pyAesCrypt.encryptFile('./psw_db.db', './psw_db.encrypt', secret)
    os.remove('psw_db.db')

def decryptdb(secret):
    global pas
    
    plain_data = pyAesCrypt.decryptFile('./psw_db.encrypt', './psw_db.db', secret)
    os.remove('psw_db.encrypt')

def checkPassword(password):
    f = open('config.psw', 'rb')
    data = f.read()
    f.close()
    salt = data[:32]
    key = data[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key == new_key

def startup():
    #Check if user already exist
    if not os.path.isfile('config.psw'):
        while not setPassword():
            pass
    
    else:
        return login()  #If the password is correct, the tools can go next 
    

def login():
   
    if os.path.isfile('./config.psw'):
        password = getpass()
        global pas
        pas = password
        if checkPassword(pas):
            print("Trying to decrypt database...")
            decryptdb(pas)
            try:
                #Decrypt test
                db = sqlite3.connect('psw_db.db')
                db.close()
            except:
                print("Database decryption fault.")
                exit()
            print("Welcome!")
            return True #If the password is correct, returt true to startup() method
        print("Incorrect password")
        exit() #If password is incorrect, exit from tool
    else:
        print("File config.psw not found but a previous register exist, please restore the config.psw file, or try to reinstall the tool\nResinstalling the tool all password saved in db will be lose.")
    exit()
    
def removeEntry(input_id):
    db = sqlite3.connect('psw_db.db');
    cursor = db.cursor()
    data_cursor = cursor.execute('SELECT ID from psw_table where id = ?', (input_id))
    data = data_cursor.fetchall()
    if len(data) == 0:
        print('Some error occurred, probably there are no entry with this id')
        return
    db.execute('''DELETE FROM psw_table WHERE ID = {};'''.format(int(input_id)))
    db.commit()
    db.close()
    print("Record removed correctly")

def setPassword():
    global pas
    print("Please choose a password")
    salt = os.urandom(32) # Remember this
    password = getpass()
    print('Please type again')
    password_check = getpass()
    if(password == password_check):
        pas = password
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        f = open('config.psw', 'wb')
        f.write(salt)
        f.write(key)
        f.close()
        return True
    else:
        print("Passwords do not match")
        
    return False

def change_password():
    os.remove('config.psw')
    while not setPassword():
        pass
    
def createpsw():
    try:
        db = sqlite3.connect('psw_db.db')
        cursor = db.cursor()
    except:
        print('Error establishing connection with database')
        exit()

    #Getting data from user
    username = input('Insert username: ')
    email = input('Insert email: ')
    password = input('Insert password: ')
    url = input('Insert the url: ')
    sitename = input('Insert the sitename: ')
    sql = "INSERT INTO psw_table (username, email, password, sitename, url) VALUES (?,?,?,?,?)"
    cursor.execute(sql, (username, email, password, url, sitename))
    #Execute query and commit
    db.commit()
    db.close()

def view():
    try:
        db = sqlite3.connect('psw_db.db');
    except:
        print('Error establishing connection with database')
        exit()
    cursor = db.execute("SELECT ID, USERNAME, EMAIL, PASSWORD, SITENAME, URL FROM psw_table;")
    data = []
    for row in cursor:
        arr = [str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])]
        data.append(arr)
    db.close()
    return data

def chgpsw():
    id = input('Select the entry id to change password:')
    try:
        int_id = int(id)
    except:
        print('Please enter an integer number')
        return False
    db = sqlite3.connect('psw_db.db')
    cursor = db.cursor()
    data_cursor = cursor.execute('SELECT ID from psw_table where id = ?', (id))
    data = data_cursor.fetchall()
    #Check if exist and entry with the selected id
    if len(data) == 0:
        print('Some error occurred, probably there are no entry with this id')
        db.close()
        return

    new_password = input('Enter the new password: ')
    new_password_again = input('Enter the new password again: ')

    if new_password == new_password_again:

        cursor.execute('UPDATE psw_table SET password = ? WHERE ID = ?', (new_password, id))
        db.commit()
        db.close()
        print('Password changed succesfully')
    else:
        print('Passwords do not match, retry')
            
    
def help():
    #show the list of commnads
    print('view            -   View all saved password')
    print('createpsw       -   Create a new record for saving a password')
    print('remove          -   Remove a record from db')
    print('exit            -   Exit from the tool')
    print('change-tool-psw -   Change the passowrd for pswManager tool')
    print('chgpsw          -   Change the password for the selected entry')
    
startup()
print('Type help for the list of command')
#Main cicle of the tool
while True:
    
    input_data = input('pswmanager>').strip()

    if input_data == 'help':
        help()

    #Create a new entry into db
    elif input_data == 'createpsw':
        createpsw()

    #View all entry into db
    elif input_data == 'view':
        data = view()
        print(tabulate(data, headers=["ID", "Username", "E-mail", "Password", "Sitename", "Url"]))


    #Exit from tool
    elif input_data == 'exit':
        print('Database encrypting...')
        cryptdb(pas) #Encrypt db and byby "Chiudi il gas e vieni via, big cit."  <3
        print('Done, goodbye')
        break

    #Remove an entry into db
    elif input_data == 'remove':
        input_id = input("Select the id: ")
        try:
            removeEntry(input_id)

        except:
            print('Some error occurred, probably there are no entry with this id')

    elif input_data == 'change-tool-psw':
        change_password()

    elif input_data == 'chgpsw':
        chgpsw()
    else:
        print('Error, this command does not exist, type "help" for the command list')

