
# Functions
def valid_username(username):
    if len(username) >= 5:  # Check if the length is greater than or equal to 5
        if username.isalnum():  # Check if all characters are alphanumeric
            if username[0].isalpha():  # Check if the first character is a letter
                return True
    return False
def valid_password(password):
    # Check the length
    if len(password) < 5:
        return False

    # Check if alphanumeric
    if not password.isalnum():
        return False

    # Check if contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check if contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if contains at least one number
    if not any(char.isdigit() for char in password):
        return False

    # If all checks pass, the password is valid
    return True

user_info = open("user_info.txt",'r') # Open file

#Extract data into lists

username = []
passw = []

for u in user_info:
    info = u.strip().split("\n") #split data into lines
    for i in info:
        if "," in i:
            user, password = i.strip().split(",") #split data into types "user" and "password"
            username.append(user)
            passw.append(password)
# Functions
def username_exists(name):
    if name in username:
        return True
    return False
def check_password(name,word):
    if name in username and word in passw:
        return True
    return False


import os
def add_user(name, word):
    found = False  # set flag
    for n in username:  # check if name is in list
        if name == n:
            found = True  # set flag true if found
            break

    if not found:
        with open("user_info.txt", "a") as add_file:
            add_file.write(f"{name},{word}\n")  # open file in append write name and password
            # update the username list
            username.append(name)
            passw.append(word)

            user_file = f'messages/{name}.txt'

            # Check if the 'messages' directory exists, create it if not
            if not os.path.exists('messages'):
                os.makedirs('messages')

            with open(user_file, 'w'):
                pass  # This creates an empty file


import datetime
def send_message(sender, receiver, message):
    # get current date and time
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%m/%d/%Y %H:%M:%S")

    # format the message string
    message_line = f"{sender}|{formatted_time}|{message}\n"

    # check if the receiver exists and create a new file if it does not
    receiver_filename = f"messages/{receiver}.txt"

    try:
        with open(receiver_filename, "a") as receiver_file:
            pass  # empty file
    except FileNotFoundError:
        with open(receiver_filename, "w") as receiver_file:
            pass  # create a new file

    # Append the message to the receiver's file
    with open(receiver_filename, "a") as receiver_file:
        receiver_file.write(message_line)
def print_messages(username):
    # Read messages from the user's file
    user_filename = f"messages/{username}.txt"

    try:
        with open(user_filename, "r") as user_file:
            messages = user_file.readlines()
    except FileNotFoundError:
        return

        # Check if there are no messages
    if not messages:
        print("No messages in your inbox!")
        return

    # Print each message
    for i, message in enumerate(messages, start=1):
        sender, timestamp, content = message.strip().split('|')
        print(f"Message #{i} received from {sender}")
        print(f"Time: {timestamp}")
        print(content)
        print()
def delete_messages(username):
    # Delete all data in the messages file for the user
    user_filename = f"messages/{username}.txt"
    with open(user_filename, "w") as user_file:
        pass  # This creates an empty file

# Main Program
print("Welcome to Facebook Messenger 2.0!")
while True:
    action = input("Would you like to (l)ogin, (r)egister or (q)uit? ") # ask for users action
    print(f"> {action}")
    if action == "r": # if r register username and pass
        print("You chose to register for an account.")
        register_name = input("Username (case sensitive) ")
        print(f"> {register_name}")
        register_pass = input("Password (case sensitive) ")
        print(f"> {register_pass}")
        duplicate = username_exists(register_name)
        if duplicate == False: # if name is duplicate send error message
            add_user(register_name,register_pass)
            print(f"Registration successful! Welcome {register_name}!")
            send_message("admin",register_name,"Welcome to Facebook Messenger!")
        else:
            print("Duplicate username, user registration has been cancelled.")

    if action == "l": # if action l login
        print("You chose to log in.")
        login_name = input("Username (case sensitive) ")
        print(f"> {login_name}")
        login_pass = input("Password (case sensitive) ")
        print(f"> {login_pass}")
        login = check_password(login_name,login_pass)
        if login == False: # if info for login doesnt exist print error message
            print("Login failed, user login has been cancelled.")
        else:
            while True: # if login successful prompt user to new menu
                print(f"You are logged in successfully as {login_name}.")
                action2 = input("Would you like to (r)ead messages, (s)end a message, (d)elete messages or (l)ogout? ")
                print(f"> {action2}")
                if action2 == "r": # if action r print user messages
                    print_messages(login_name)

                if action2 == "s": # if action s send messages
                    recipient =  input("Username of recipient ")
                    print(f"> {recipient}")
                    message = input("Your message ")
                    print(f"> {message}")
                    if username_exists(recipient): # check if recipient is a user
                        send_message(login_name,recipient,message)
                        print("Message sent!")
                    else: # if not print error message
                        print("This recipient does not exist.")
                if action2 == "d": # if action d delete messages
                    delete_messages(login_name)
                    print("Your messages have been deleted.")

                if action2 == "l": # if action l log out
                    print(f"Logging out as {login_name}.")
                    break # break out inner loop

    if action == "q": # if action q print goodbye message
        print("Goodbye! Thanks for using Facebook Messenger 2.0!")
        exit() # exit code
