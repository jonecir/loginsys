#!python3

from configs.dbconn import DBConnectionHandler
from controller.user_repo import UsersRepository

repo1 = UsersRepository(DBConnectionHandler)

while True:
    print("========== [MENU] ==========")
    uoption = int(
        input('Enter 1 to register\nEnter 2 to Login\nEnter 3 to exit\n'))

    if uoption == 1:
        uname = input('Enter your username:')
        uemail = input('Enter your email:')
        upwd = input('Enter your password:')
        
        result = repo1.insert(uname, uemail, upwd)

        if result == 1:
            print("You have been registered!")
        elif result == 2:
            print("Invalid username length!")
        elif result == 3:
            print("Invalid email address!")
        elif result == 4:
            print("Invalid password lenght!")
        elif result == 5:
            print("User already exists!")
        else:
            print("An error has occurred! Please contact your vendor.")
    elif uoption == 2:
        uemail = input('Enter email:')
        upwd = input('Enter your password:')
        result = repo1.select_user(uemail, upwd)
        if (result == None):
            print(result)
            print("Invalid username or password!")
        else:
            print(result)
            print('You have logged in successfuly!')
    else:
        break

