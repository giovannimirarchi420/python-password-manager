# Password Manager

A secure command-line tool for managing your passwords effectively.

## Table of Contents
* [Why passwordManager?](#why-passwordmanager?)
* [Technologies and Libraries](#technologies-and-libraries)
* [Setup](#setup)
* [How to launch the tool](#how-to-launch-the-tool)
* [How it works](#how-it-works)
* [Commands](#commands)
* [Screenshot](#screenshot)
* [Author](#author)

<!-- * [License](#license) -->

## Why passwordManager?

In today's digital world, we constantly encounter new websites and platforms requiring unique passwords. Remembering these passwords securely is a challenge. passwordManager offers a solution:

  - Efficient and Secure Storage: It stores all your passwords in an encrypted database, accessible only with the master password you set upon initial launch.
  - Enhanced Security: It eliminates the need to reuse passwords across different accounts, a critical security practice.

Let passwordManager safeguard your login credentials and simplify password management.

## Technologies and Libraries

- **Python 3.9.3** (Programming Language)
- **sqlite3** (Database Management) (Included by default in Python)
- **hashlib** (Encryption) (Included by default in Python)
- **os** (Operating System Interaction) (Included by default in Python)
- **base64** (Encoding/Decoding) (Included by default in Python)
- **tabulate** (Data Presentation) (Optional, install using pip install tabulate)
- **pyAesCrypt** (Encryption Library) (Required, install using pip install pyAesCrypt)

## Setup
```
$ git clone https://github.com/giovannimirarchi420/passwordManager
$ python init.py
```
## Optional Setup for Script-like Usage:
Alteratively you can install ```pyAesCrypt``` library by yourself typing ```pip install pyAesCrypt```. 
To use this tool like a real command line script (e.g. ls, mkdir, etc..), you need to add the script directory to the env variable PATH:
```
$ cd your/script/directory
(We are into script dir)
$ pwd
(Copy the result of pwd)
$ export PATH=$PATH:path/to/passwordManager
```
**Note:** This modifies your environment variable so the script can be run from any directory. Consider this step carefully if you're unfamiliar with environment variables.

Rename pswManager.py into pswManager:
```
$ mv pswManager.py pswManager
```
Make the script executable
```
$ chmod u+x pswManager
```

## Usage
Launch the tool using ```python pswManager.py``` (or ```pswManager``` if you made it executable).
Enter the master password you set during initialization.

## How it works

Run ```python pswManager.py``` and set a master password for the tool. This password is used to access the database and commands.
The encrypted password (sha256) is stored in the ```config.psw``` file, combined with the salt, a random value.
After you choose your password, the ```config.psw``` file acts as a secure source of authentication on all subsequent restarts. This file verifies the salted password you used during initial setup.
The password stored in ```config.psw``` will act also as secret key for DB encrypting/decrypting.

## Commands

- **createpsw:** Adds a new password entry to the database.
- **view:** Lists all stored passwords.
- **remove:** Removes a specific password entry.
- **exit:** Exits the tool securely, encrypting the database.
- **change-tool-psw:** Changes the master password for the tool.
- **chgpsw:** Changes the password for a specific entry.
- **help:** Provide commands summary.

## Screenshot
![view-screen](./screenview.png)

## Author

This project was made by Giovanni Mirarchi (alias @Hemek)
- Linkedin: https://www.linkedin.com/in/giovanni-mirarchi/
  
