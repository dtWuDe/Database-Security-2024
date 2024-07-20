import os
import tkinter as tk
import connSQL as sql
from tkinter import messagebox
from hashlib import sha1
from dotenv import load_dotenv

load_dotenv(os.path.join('connect.config'))

SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME") 
UID = os.getenv("UID")
PWD = os.getenv("PWD")

def login_check():
    usrname = entry_usrname.get()
    passwd = entry_passwd.get()
    if usrname == '' or passwd == '':
        messagebox.showinfo("Invalid username or password", "Please re-enter your username and password")
        return
    # Connect with system admin role
    conn, cursor =  sql.Connect(SERVER_NAME, DATABASE_NAME, UID, PWD)
    
    # Check which table the value 'SV01' belongs to
    strsql =   f"""
                    SELECT 
                        CASE 
                            WHEN EXISTS (SELECT MANV FROM NHANVIEN WHERE TENDN = ?) THEN 'NHANVIEN'
                            ELSE 'UNKNOWN'
                        END       
                """
    cursor.execute(strsql, usrname)
    result = cursor.fetchone()
    role = result[0]
    
    # Assign attribute
    if role == 'UNKNOWN':
        messagebox.showinfo("Login Failed", "This account doesn't exist. Enter a different account.")
        return
    elif role == 'NHANVIEN':
        id_column = "MANV"
    else:
        messagebox.showerror("Error!")

    hash_passwd = '0x' + sha1(passwd.encode('utf-8')).hexdigest()

    # Check the existence of the account
    strsql = f"""
                SELECT 
                    CASE
                        WHEN EXISTS (SELECT {id_column} FROM {role} WHERE TENDN = ? AND MATKHAU = {hash_passwd}) THEN 'SUCCESS'
                        ELSE 'FAILED'
                    END 
            """
    
    cursor.execute(strsql, (usrname))
    result = cursor.fetchone()
    status = result[0]

    if status == 'SUCCESS':
        messagebox.showinfo("Login Successful", "You have successfully logged in.")
        return_val.append([conn, cursor, usrname, hash_passwd])
        exit_program()
        return
    elif status == 'FAILED':
        messagebox.showerror("Login Failed", "The password that you've entered is incorrect.")

    sql.Disconnect(conn, cursor)
    None


def exit_program():
    login_window.destroy()
    None

def login():
    global login_window, return_val
    return_val = list()
    login_window = tk.Tk()
    login_window.title('Màn hình đăng nhập')

    # setting height and width of screen login
    login_window_width = 500
    login_window_height = 200
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x_coordinate = (screen_width - login_window_width) // 2
    y_coordinate = (screen_height - login_window_height) // 2
    login_window.geometry(f'{login_window_width}x{login_window_height}+{x_coordinate}+{y_coordinate}')

    # label and entry for input information of user
    infor_frame = tk.Frame(login_window) 
    infor_frame.pack(pady=30)

    global entry_usrname, entry_passwd
    label_usrname = tk.Label(infor_frame, text='Username ', font=('Arial', 12))
    label_usrname.grid(row=0, column=0, sticky='e')

    entry_usrname = tk.Entry(infor_frame, font=('Arial', 12))
    entry_usrname.grid(row=0, column=1, sticky='e')


    label_passwd = tk.Label(infor_frame, text='Password', font=('Arial', 12))
    label_passwd.grid(row=1, column=0)

    entry_passwd = tk.Entry(infor_frame, show='*', font=("Arial", 12))
    entry_passwd.grid(row=1, column=1)

    # login and exit button
    button_frame = tk.Frame(login_window)
    button_frame.pack()
    
    button_login = tk.Button(button_frame, text='Login', font=('Arial', 12), command=login_check)
    button_login.pack(side='left', padx=10, pady=10)

    button_exit = tk.Button(button_frame, text='Exit', font=('Arial', 12), command=exit_program)
    button_exit.pack(side='left', padx=10, pady=10)

    login_window.mainloop()

    if return_val != []:
        return return_val
    else:
        return None