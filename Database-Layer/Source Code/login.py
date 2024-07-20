import tkinter as tk
import connSQL as sql
from tkinter import messagebox
import screenQLSV as qlsv

def login(entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()
    # Connect with system admin role
    conn, cursor =  sql.Connect_SQL('localhost', 'QLSVNhom', 'sa', 'sa@123')
    
    # Check which table the value 'SV01' belongs to
    strsql =   f"""
                    SELECT 
                        CASE 
                            WHEN EXISTS (SELECT MANV FROM NHANVIEN WHERE MANV = CAST(? AS VARCHAR(20))) THEN 'NHANVIEN'
                            ELSE 'UNKNOWN'
                        END       
                """
    cursor.execute(strsql, username)
    result = cursor.fetchone()
    role = result[0]
    
    # Assign attribute
    if role == 'UNKNOWN':
        messagebox.showinfo("Login Failed", "This account doesn't exist. Enter a different account")
        return
    elif role == 'NHANVIEN':
        id_column = "MANV"
    else:
        messagebox.showerror("Error!")

    # Check the existence of the account
    strsql = f"""
                SELECT 
                    CASE
                        WHEN EXISTS (SELECT {id_column} FROM {role} WHERE {id_column} = CAST(? AS VARCHAR(20)) AND MATKHAU = HASHBYTES('SHA1', CAST(? AS NVARCHAR(20)))) THEN 'SUCCESS'
                        ELSE 'FAILED'
                    END 
            """
    cursor.execute(strsql, (username, password))    
    result = cursor.fetchone()
    status = result[0]

    if status == 'SUCCESS':
        messagebox.showinfo("Login Successful", "You have successfully logged in!")
        conn_user, cursor_user = sql.Connect_SQL('localhost', 'QLSVNhom', entry_username.get(), entry_password.get())
        window.destroy()
        qlsv.Screen_QLSV(conn_user, cursor_user)

        return True
    elif status == 'FAILED':
        messagebox.showerror("Login Failed", "Invalid username or password.")

    sql.Disconnect_SQL(conn, cursor)
    

def exit_program():
    window.destroy()

def login_QLSV():
    # Create the main window
    global window
    window = tk.Tk()
    window.title("Login")

    # Set the window size
    window_width = 500
    window_height = 200
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Create a frame to hold the labels and entry fields
    frame = tk.Frame(window)
    frame.pack(pady=20)

    # Create labels, entry fields, and buttons
    label_username = tk.Label(frame, text="Username:", font=("Arial", 12))
    label_username.grid(row=0, column=0, sticky="e")

    entry_username = tk.Entry(frame, font=("Arial", 12))
    entry_username.grid(row=0, column=1)

    label_password = tk.Label(frame, text="Password:", font=("Arial", 12))
    label_password.grid(row=1, column=0, sticky="e")

    entry_password = tk.Entry(frame, show="*", font=("Arial", 12))
    entry_password.grid(row=1, column=1)

    frame_buttons = tk.Frame(window)
    frame_buttons.pack(pady=10)

    button_login = tk.Button(frame_buttons, text="Login", font=("Arial", 12), command=lambda: login(entry_username, entry_password))
    button_login.pack(side="left", padx=10, pady=10)

    button_exit = tk.Button(frame_buttons, text="Exit", font=("Arial", 12), command=lambda: exit_program())
    button_exit.pack(side="left", padx=10, pady=10)

    # Start the main event loop
    window.mainloop()   

