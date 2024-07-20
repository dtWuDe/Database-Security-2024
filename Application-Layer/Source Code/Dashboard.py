from MyLibary import Init_Screen
from ManageClass import Screen_Manage_Class
from ManageEMP import Screen_Manage_EMP
from MangeSTU import Screen_QLSV
import MyCrypto as crypto
import connSQL as sql
import tkinter as tk

class infor_login:
    def __init__(self,_empid, _usrname, _passwd, _pub_name, _kprivate, _kpublic, _conn, _cursor):
        self.empid = _empid
        self.usrname = _usrname
        self.passwd = _passwd
        self.pub_name = _pub_name
        self.kprivate = _kprivate
        self.kpublic = _kpublic
        self.conn = _conn
        self.cursor = _cursor

def student_dashboard_window_destroy():
    dashboard_window.attributes('-disable', False)
    student_dashboard_window.destroy()

def class_dashboard_window_destroy():
    dashboard_window.attributes('-disable', False)
    class_dashboard_window.destroy()

def emp_dashboard_window_destroy():
    dashboard_window.attributes('-disable', False)
    emp_dashboard_window.destroy()

def manage_student(login_infor): 
    global student_dashboard_window
    dashboard_window.attributes('-disable', True)
    student_dashboard_window = Screen_QLSV(dashboard_window, login_infor)
    student_dashboard_window.protocol("WM_DELETE_WINDOW", student_dashboard_window_destroy)   
    return
   

def manage_class(login_infor):
    global class_dashboard_window
    dashboard_window.attributes('-disable', True)
    class_dashboard_window = Screen_Manage_Class(dashboard_window, login_infor)
    class_dashboard_window.protocol("WM_DELETE_WINDOW", class_dashboard_window_destroy)
    return

def manage_employee(login_infor):
    global emp_dashboard_window
    dashboard_window.attributes('-disable', True)
    emp_dashboard_window = Screen_Manage_EMP(dashboard_window, login_infor)
    emp_dashboard_window.protocol("WM_DELETE_WINDOW", emp_dashboard_window_destroy)
    return

def dashboard_window_destroy(_conn, _cursor):
    sql.Disconnect(_conn, _cursor)
    dashboard_window.destroy()
    return_val.append('None')
    return

def logout(_conn, _cursor):
    sql.Disconnect(_conn, _cursor)
    dashboard_window.destroy()
    return_val.append('Logout')


def Screen_Dashboard(_conn, _cursor, _usrname, _passwd):
    global dashboard_window, return_val
    return_val = list()

    strsql = f"""
                SELECT* FROM NHANVIEN WHERE TENDN = '{_usrname}' AND MATKHAU = {_passwd}
            """

    _cursor.execute(strsql)
    column_name = [column[0] for column in _cursor.description]
    rows = _cursor.fetchall()
    # INDEX
    empid_index = column_name.index('MANV')
    pubkey_index = column_name.index('PUBKEY')
    # VALUE
    empid = rows[0][empid_index]
    pub_name = rows[0][pubkey_index]
    Kprivate = crypto.get_Krivate(pub_name, 'EMP_PUB.key')
    Kpublic = crypto.get_Kpublic(pub_name, file_name='EMP_PUB.key')

    new_login = infor_login(empid, _usrname, _passwd, pub_name, Kprivate, Kpublic, _conn, _cursor)

    dashboard_window = Init_Screen("Dashboard", width=300, height=300)
    dashboard_window.protocol("WM_DELETE_WINDOW", lambda: dashboard_window_destroy(_conn, _cursor))

    manage_class_button = tk.Button(dashboard_window, text= 'Quản lý lớp học', font=('Arial', 12), command=lambda: manage_class(new_login))
    manage_class_button.pack(pady=20, expand=True)

    manage_student_button = tk.Button(dashboard_window, text= 'Quản lý học sinh', font=('Arial', 12), command=lambda: manage_student(new_login))
    manage_student_button.pack(pady=20, expand=True)

    manage_employee_button = tk.Button(dashboard_window, text= 'Quản lý nhân viên', font=('Arial', 12), command=lambda: manage_employee(new_login))
    manage_employee_button.pack(pady=20, expand=True)

    logout_button = tk.Button(dashboard_window, text= 'Đăng xuất', font=('Arial', 12), command=lambda: logout(_conn, _cursor))
    logout_button.pack(pady=20, expand=True)
    
    dashboard_window.mainloop()

    return return_val

