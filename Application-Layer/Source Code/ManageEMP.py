import tkinter as tk
from hashlib import sha1
from tkinter import ttk, messagebox
import MyLibary as ml 
import MyCrypto as crypto
import pyodbc

class emp_infor:
    def __init__(self, usrname, passwd, pub_name, kprivate):
        self.usrname = usrname
        self.passwd = passwd
        self.pub_name = pub_name
        self.kprivate = kprivate

def config_state(_state: {'normal', 'disable', 'readonly'}):
    entry_empid.config(state=_state)
    entry_email.config(state=_state)
    entry_fullname.config(state=_state)
    entry_usrname.config(state=_state)
    entry_passwd.config(state=_state)
    entry_sal.config(state=_state)

def clear_entry():
    entry_empid.delete(0, tk.END)  
    entry_email.delete(0, tk.END)  
    entry_fullname.delete(0, tk.END)  
    entry_usrname.delete(0, tk.END)  
    entry_passwd.delete(0, tk.END)  
    entry_sal.delete(0, tk.END)  

def Load_ALL_EMP():
    strsql = f"""
                SELECT tendn, matkhau FROM NHANVIEN
            """
    cursor.execute(strsql)
    rows = cursor.fetchall()

    for row in rows:
        Load_EMP_Table(row[0], '0x' + row[1].hex())


def Load_EMP_Table(tendn, MK):
    strsql = f"""
                EXEC SP_SEL_PUBLIC_ENCRYPT_NHANVIEN {tendn}, {MK};
            """
    cursor.execute(strsql)
    rows = cursor.fetchall()

    if ml.has_column_heading(table_emp) == 0:
        column_name = [column[0] for column in cursor.description]

        global sal_index
        sal_index = column_name.index('LUONG')
        
        table_emp['column'] = tuple(column_name)
        table_emp.column('#0', width=0, minwidth=0, anchor='center')
        for column in column_name:
            table_emp.column(column, width=190, minwidth=190, anchor='w')
            table_emp.heading(column, text=column) 

        
    exists_id = [table_emp.item(item)['values'][0] for item in table_emp.get_children()]
    for row in rows:
        if row[0] not in exists_id:
            values = list(row)
            # for handle first employee is inserted
            if values[sal_index] != None:
                pub_name = values[0] + 'PUB'
                Kprivate = crypto.get_Krivate(pub_name, 'EMP_PUB.key')
                values[sal_index] = crypto.decryptRSA(values[sal_index], Kprivate)

            table_emp.insert(parent='', index='end', values=values)
    
    None

def commit_data():
    conn.commit()
    for emp in emp_array:
        crypto.write_key('EMP_PUB.key', emp.pub_name, emp.kprivate)
        Load_EMP_Table(emp.usrname, emp.passwd)

    emp_array.clear()
        
            

def exit_program():
    dashboard.attributes('-disable', False)
    window.destroy()
    None

def sql_insert_emp():
    empid = entry_input_empid.get()
    email = entry_input_email.get()
    fullname = entry_input_fullname.get()
    usrname = entry_input_usrname.get()
    passwd = entry_input_passwd.get()
    sal = entry_input_sal.get()
    repasswd = entry_input_repasswd.get()

    if empid == '' or email == '' or fullname == '' or usrname == '' or passwd == '' or sal == '' or repasswd == '':
        messagebox.showwarning('Invalid input', 'Please enter complete information', parent=insert_window)
        return

    if passwd != repasswd:
        messagebox.showwarning('Invalid input', 'Please re-enter your password', parent=insert_window)
        return

    if ml.is_number(sal) == False or int(sal) < 0:
        messagebox.showwarning('Invalid input', 'Please re-enter salary', parent=insert_window)
        return

    hash_passwd = '0x' + sha1(passwd.encode('utf-8')).hexdigest()
    pub = empid + 'PUB'

    params = (empid, fullname, email, usrname, pub)
    Kpublic, Kprivate = crypto.genKeyRSA(pub_name=pub, file_name='EMP_PUB.key')
    string_sal = sal
    encrypted_sal = '0x' + crypto.encryptRSA(string_sal, pubKey=Kpublic).hex()

    strsql = f"""
                DECLARE @ReturnValue INT;
                EXEC @ReturnValue = SP_INS_PUBLIC_ENCRYPT_NHANVIEN ?, ?, ?, {encrypted_sal}, ?, {hash_passwd}, ?;
                SELECT @ReturnValue AS ReturnValue;
            """

    try:
        cursor.execute(strsql, params)
        cursor.nextset()  # Move to the next result set

        result = cursor.fetchone()
        return_value = result[0]

        if return_value == 0:
            messagebox.showinfo('Success', 'Inserted successfully', parent=window)
            new_emp = emp_infor(usrname=usrname, passwd=hash_passwd, pub_name=pub, kprivate=Kprivate)
            emp_array.append(new_emp)
            insert_window_destroy()
        else:
            messagebox.showinfo('Error', 'Procedure execution failed', parent=insert_window)
            insert_window_destroy()
    except pyodbc.Error as e:
        messagebox.showinfo('Error', f'Procedure execution failed: {str(e)}', parent=window)
        insert_window_destroy()
        return
    
    None


def insert_window_destroy():
    window.attributes('-disable', False)
    insert_window.destroy()

def insert_emp():
    global insert_window

    insert_window = ml.Init_Screen('Thêm nhân viên', width=400, height=500)
    window.attributes('-disable', True)
    insert_window.protocol("WM_DELETE_WINDOW", insert_window_destroy)

    label_title = tk.Label(insert_window, text='NHẬP THÔNG TIN NHÂN VIÊN', font=('Arial', 12, 'bold'))
    label_title.pack()

    input_frame = tk.Frame(insert_window)
    input_frame.pack(pady=20)

    global entry_input_empid, entry_input_email, entry_input_usrname, entry_input_fullname, entry_input_sal, entry_input_passwd, entry_input_repasswd
    label_empid = tk.Label(input_frame, text='Mã NV', font=('Arial', 12))
    label_empid.grid(pady=10, row=0, column=0, sticky='w')

    entry_input_empid = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_empid.grid(pady=10, row=0, column= 1)

    label_email = tk.Label(input_frame, text='Email', font=('Arial', 12))
    label_email.grid(pady=10, row=1, column=0, sticky='w')

    entry_input_email = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_email.grid(pady=10, row=1, column=1)

    label_usrname = tk.Label(input_frame, text='Tên đăng nhập', font=('Arial', 12))
    label_usrname.grid(pady=10, row=2, column=0, sticky='w')

    entry_input_usrname = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_usrname.grid(pady=10, row=2, column=1)

    label_fullname = tk.Label(input_frame, text='Họ tên', font=('Arial', 12))
    label_fullname.grid(pady=10, row=3, column=0, sticky='w')

    entry_input_fullname = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_fullname.grid(pady=10, row=3, column=1)

    label_sal = tk.Label(input_frame, text='Lương', font=('Arial', 12))
    label_sal.grid(pady=10, row=4, column=0, sticky='w')

    entry_input_sal = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_sal.grid(pady=10, row=4, column=1)

    label_passwd = tk.Label(input_frame, text='Mật khẩu', font=('Arial', 12))
    label_passwd.grid(pady=10, row=5, column=0, sticky='w')

    entry_input_passwd = tk.Entry(input_frame, show='*',  font=('Arial', 12))
    entry_input_passwd.grid(pady=10, row=5, column=1)

    label_repasswd = tk.Label(input_frame, text='Xác nhận mật khẩu', font=('Arial', 12))
    label_repasswd.grid(pady=10, row=6, column=0, sticky='w')

    entry_input_repasswd = tk.Entry(input_frame, show='*',  font=('Arial', 12))
    entry_input_repasswd.grid(pady=10, row=6, column=1)

    button_frame = tk.Frame(insert_window)
    button_frame.pack(pady=10)

    button_confirm = tk.Button(button_frame, text='Xác nhận', font=('Arial', 12), command=sql_insert_emp)
    button_confirm.pack(pady=10, padx=10, side='left')

    button_exit = tk.Button(button_frame, text='Huỷ', font=('Arial', 12), command=insert_window_destroy)
    button_exit.pack(pady=10, padx=10, side='left')
    None

def Load_EMP_Infor(_usrname, _passwd, _Kprivate):
    strsql = f"""
                SELECT* FROM NHANVIEN WHERE TENDN = '{_usrname}' AND MATKHAU = {_passwd}
            """
    cursor.execute(strsql)
    data = cursor.fetchall()[0]

    config_state(_state='normal')

    entry_empid.delete(0, tk.END)
    entry_empid.insert(0, data[0])

    entry_fullname.delete(0, tk.END)
    entry_fullname.insert(0, data[1])

    entry_email.delete(0, tk.END)
    entry_email.insert(0, data[2])
    
    ciphertext_sal = data[3]
    if ciphertext_sal != None:
        decrypted_sal = crypto.decryptRSA(ciphertext_sal, _Kprivate)
        entry_sal.delete(0, tk.END)
        entry_sal.insert(0, decrypted_sal)
    
    entry_usrname.delete(0, tk.END)
    entry_usrname.insert(0, data[4])

    entry_passwd.delete(0, tk.END)
    entry_passwd.insert(0, "********")

    config_state(_state='disable')
    None

def Screen_Manage_EMP(_dashboard, login_infor):
    global dashboard, window, conn, cursor, emp_array
    
    # Store information of employees that are not inserted into the database
    emp_array = []

    conn, cursor, dashboard = login_infor.conn, login_infor.cursor, _dashboard

    window = ml.Init_Screen(title="Danh sách nhân viên", width=800, height=500)
    window.protocol("WM_DELETE_WINDOW", exit_program)

    title_frame = tk.Frame(window)
    title_frame.pack(pady=10)
    # Title
    title_label = tk.Label(title_frame, text='DANH MỤC NHÂN VIÊN', font=('Arial', 12, 'bold'))
    title_label.grid()

    # Employee information 
    infor_frame = tk.Frame(window, highlightbackground='black', highlightthickness=1.5)
    infor_frame.pack()

    label_title = tk.Label(infor_frame, text='Thông tin nhân viên', font=('Arial', 10))
    label_title.grid(sticky='n')
    # Employee id 
    global entry_empid, entry_email, entry_usrname, entry_fullname, entry_sal, entry_passwd
    label_empid = tk.Label(infor_frame, text='Mã NV', font=('Arial', 12))
    label_empid.grid(padx=10, pady=(30, 0), row=0, column=0, sticky='w')

    entry_empid = tk.Entry(infor_frame, font=('Arial', 12), state='disabled')
    entry_empid.grid(pady=(30, 0), row=0, column= 1)

    label_email = tk.Label(infor_frame, text='Email', font=('Arial', 12))
    label_email.grid(padx=10, row=1, column=0, sticky='w')

    entry_email = tk.Entry(infor_frame, font=('Arial', 12), state='disabled')
    entry_email.grid(row=1, column=1)

    label_usrname = tk.Label(infor_frame, text='Tên đăng nhập', font=('Arial', 12))
    label_usrname.grid(pady=(0, 10), padx=10, row=2, column=0, sticky='w')

    entry_usrname = tk.Entry(infor_frame, font=('Arial', 12), state='disabled')
    entry_usrname.grid(pady=(0, 10), row=2, column=1)

    label_fullname = tk.Label(infor_frame, text='Họ tên', font=('Arial', 12))
    label_fullname.grid(pady=(30, 0), padx=(30, 0), row=0, column=2, sticky='w')

    entry_fullname = tk.Entry(infor_frame, font=('Arial', 12), state='disabled')
    entry_fullname.grid(pady=(30, 0), padx=(0, 10),row=0, column=3)

    label_sal = tk.Label(infor_frame, text='Lương', font=('Arial', 12))
    label_sal.grid(padx=(30, 0), row=1, column=2, sticky='w')

    entry_sal = tk.Entry(infor_frame, font=('Arial', 12), state='disabled')
    entry_sal.grid(padx=(0, 10),row=1, column=3)

    label_passwd = tk.Label(infor_frame, text='Mật khẩu', font=('Arial', 12))
    label_passwd.grid(pady=(0, 10), padx=(30, 0), row=2, column=2, sticky='w')

    entry_passwd = tk.Entry(infor_frame, show='*',  font=('Arial', 12), state='disabled')
    entry_passwd.grid(pady=(0, 10), padx=(0, 10), row=2, column=3)

    usrname, passwd, kprivate = login_infor.usrname, login_infor.passwd, login_infor.kprivate
    Load_EMP_Infor(usrname, passwd, kprivate)

    # List employee 
    global table_emp
    table_emp = ttk.Treeview(window)
    table_emp.pack(pady=(20, 0))

    Load_ALL_EMP()
    
    # Button frame
    button_frame = tk.Frame(window)
    button_frame.pack(pady=(20, 0))

    button_insert = tk.Button(button_frame, text='Thêm', font=('Arial', 12), command=insert_emp)
    button_insert.pack(side='left', padx=20)

    button_delete = tk.Button(button_frame, text='Xóa', font=('Arial', 12))
    button_delete.pack(side='left', padx=20)

    button_update = tk.Button(button_frame, text='Sửa', font=('Arial', 12))
    button_update.pack(side='left', padx=20)

    button_save = tk.Button(button_frame, text='Ghi/Lưu', font=('Arial', 12), command=commit_data)
    button_save.pack(side='left', padx=20)

    button_none = tk.Button(button_frame, text='Không', font=('Arial', 12))
    button_none.pack(side='left', padx=20)

    button_exit = tk.Button(button_frame, text='Thoát', font=('Arial', 12), command=exit_program)
    button_exit.pack(side='left', padx=20)
    # window.mainloop()
    return window

