import tkinter as tk
from tkinter import ttk, messagebox
import MyLibary as ml
import MyCrypto as crypto
import pyodbc


def update_window_destroy():
    window.attributes('-disable', False)
    update_window.destroy()

def insert_mark_window_destroy():
    window.attributes('-disable', False)
    insert_mark_window.destroy()

def config_state(_state: {'normal', 'disable', 'readonly'}):
    entry_empid.config(state=_state)
    entry_email.config(state=_state)
    entry_fullname.config(state=_state)
    entry_usrname.config(state=_state)
    entry_passwd.config(state=_state)
    entry_sal.config(state=_state)

def load_MALOP(_class_option_menu, _class_var):
    strsql = f"SELECT MALOP FROM LOP WHERE MANV = '{entry_empid.get()}'"

    cursor.execute(strsql)
    rows = cursor.fetchall()
    
    # Clear the existing data in the OptionMenu
    _class_var.set("")  # Clear the current selection
    _class_option_menu['menu'].delete(0, tk.END)
    
    # Load the data into the OptionMenu
    for row in rows:
        _class_option_menu['menu'].add_command(label=row[0], command=tk._setit(_class_var, row[0]))
    if rows:
        _class_var.set(rows[0][0])

    # Close the database connection

def Load_Data_Table(_table_name, _treeview, _class_var=None, _id_class=None, _width=100, _minwidth=100,):
    # Clear existing data in the Treeview
    _treeview.delete(*_treeview.get_children())
    # SELECT DATA FROM TABLE
    strsql = f"""
                    SELECT* 
                    FROM {_table_name}
              """
    if _class_var == None:
        id_class = _id_class
    else:
        id_class = _class_var.get()

    if _table_name == "SINHVIEN":
        
        strsql += f" WHERE MALOP = '{id_class}'"
    elif _table_name == "BANGDIEM":
        strsql += f" WHERE MASV IN (SELECT MASV FROM SINHVIEN WHERE MALOP IN ('{id_class}'))"

    cursor.execute(strsql)
    rows = cursor.fetchall()
    
    if ml.has_column_heading(_treeview) == False:
        column_names = [column[0] for column in cursor.description]
        _treeview['columns'] = tuple(column_names)

        _treeview.column("#0", width=0, minwidth=0, anchor="center")
        for column in column_names:
            _treeview.column(column, width=_width, minwidth=_minwidth, anchor="center")
            _treeview.heading(column, text=column)

    # Insert data into the Treeview
    for row in rows:
        if _table_name == 'BANGDIEM':
            if row[2] != None:
                row[2] = crypto.decryptRSA(row[2], privKey=Kprivate)

        values = (row[0],) + row[1:]  # Exclude the first column
        
        _treeview.insert(parent='', index='end', values=values)
    None

def Load_EMP_Infor(_usrname, _passwd):
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
    if ciphertext_sal!= None:
        decrypted_sal = crypto.decryptRSA(ciphertext_sal, Kprivate)
        entry_sal.delete(0, tk.END)
        entry_sal.insert(0, decrypted_sal)
    
    entry_usrname.delete(0, tk.END)
    entry_usrname.insert(0, data[4])

    entry_passwd.delete(0, tk.END)
    entry_passwd.insert(0, "********")

    config_state(_state='disable')
    None

def sql_update_student(_id_student, _id_class, _fullname, _address, _birthday, _usrname):
    fullname = _fullname.get()
    address = _address.get()
    birthday = _birthday.get()
    usrname = _usrname.get()
    id_class = _id_class
    id_student = _id_student

    strsql = f"""
                UPDATE SINHVIEN
                SET HOTEN = ?, NGAYSINH = ?, DIACHI = ?, TENDN = ?
                WHERE MASV = '{id_student}'
             """
    param = (fullname, birthday, address, usrname)
    cursor.execute(strsql, param)
    affected_rows = cursor.rowcount
    
    window.attributes('-disable', False)
    if affected_rows > 0:
        conn.commit()
        messagebox.showinfo("SUCESS", f"Update successful. {affected_rows} rows updated.", parent=update_window)
        Load_Data_Table(_table_name='SINHVIEN', _treeview=treeview_SINHVIEN, _id_class=id_class)
        update_window.destroy()
    else:
        messagebox.showinfo("FAILED", "No rows updated.", parent=update_window)
        update_window.destroy()
    
    None

def Update_Student():
    # get the contents of the currently focused rows
    treeview_content = treeview_SINHVIEN.item(treeview_SINHVIEN.focus())

    # get indext of MALOP in treeview
    malop_index = treeview_SINHVIEN["columns"].index("MALOP")
    if treeview_content["values"] == '':
        messagebox.showwarning("No selection","Please select a student to update", parent=window)
        return
    
    
    malop = treeview_content["values"][malop_index]  
    strsql = f"""
                SELECT MANV FROM LOP WHERE MALOP = '{malop}'
              """
    cursor.execute(strsql)
    administration_of_student = cursor.fetchall()[0][0]
    if entry_empid.get() != administration_of_student:
        messagebox.showwarning("No permission","You don't have permission to update this student", parent=window)
        return
    

    MaSV_index = treeview_SINHVIEN["columns"].index("MASV")
    MaSV = treeview_content["values"][MaSV_index]

    global update_window
    update_window = ml.Init_Screen(MaSV, width=400, height=300)
    window.attributes('-disable', True)
    update_window.protocol("WM_DELETE_WINDOW", update_window_destroy)    

    student_frame.pack()

    frame = tk.Frame(update_window)
    frame.pack(pady=20)

    # Ho ten entry
    HoTen_index = treeview_SINHVIEN["columns"].index("HOTEN")
    HoTen = treeview_content["values"][HoTen_index]  
    # Dia chi entry
    DiaChi_index = treeview_SINHVIEN["columns"].index("DIACHI")
    DiaChi = treeview_content["values"][DiaChi_index]  
    # Ngay sinh entry
    NgaySinh_index = treeview_SINHVIEN["columns"].index("NGAYSINH")
    NgaySinh = treeview_content["values"][NgaySinh_index]  
    # Ten dang nhap entry
    TENDN_index = treeview_SINHVIEN["columns"].index("TENDN")
    TenDN = treeview_content["values"][TENDN_index]  

    label_HoTen = tk.Label(frame, text="Họ tên", font=("Arial", 12))
    label_HoTen.grid(row=0, column=0, sticky="w")
    
    entry_HoTen = tk.Entry(frame, font=("Arial", 12))
    entry_HoTen.grid(row=0, column=1, pady=10, padx=10)
    entry_HoTen.insert(0, HoTen) # default value

    label_NgaySinh = tk.Label(frame, text="Ngày sinh", font=("Arial", 12))
    label_NgaySinh.grid(row=1, column=0, sticky="w")

    entry_NgaySinh = tk.Entry(frame, font=("Arial", 12))
    entry_NgaySinh.grid(row=1, column=1, pady=10, padx=10)
    entry_NgaySinh.insert(0, NgaySinh)    

    label_DiaChi = tk.Label(frame, text="Địa chỉ", font=("Arial", 12))
    label_DiaChi.grid(row=2, column=0, sticky="w")

    entry_DiaChi = tk.Entry(frame, font=("Arial", 12))
    entry_DiaChi.grid(row=2, column=1, pady=10, padx=10)
    entry_DiaChi.insert(0, DiaChi) 

    label_TENDN = tk.Label(frame, text="Tên đăng nhập", font=("Arial", 12))
    label_TENDN.grid(row=3, column=0, sticky="w")

    entry_TENDN = tk.Entry(frame, font=("Arial", 12))
    entry_TENDN.grid(row=3, column=1, pady=10, padx=10)
    entry_TENDN.insert(0, TenDN) 
    
    button_student_frame = tk.Frame(update_window)   
    button_student_frame.pack()

    button_update = tk.Button(button_student_frame, text="Cập nhật", font=("Arial", 12), command=lambda: sql_update_student(_id_student=MaSV, _id_class=malop, _fullname=entry_HoTen, _address=entry_DiaChi, _birthday=entry_NgaySinh, _usrname=entry_TENDN))
    button_update.pack(side="left", anchor='w', padx=10)

    button_cancel = tk.Button(button_student_frame, text="Hủy", font=("Arial", 12))
    button_cancel.pack(side="left", anchor='w', padx=10)
    None

def sql_insert_student(_classid):
    stdid = entry_input_stdid.get()
    fullname = entry_input_fullname.get()
    birthday = entry_input_birthday.get()
    address = entry_input_address.get()
    classid = _classid
    usrname = entry_input_usrname.get()
    passwd = entry_input_passwd.get()
    repasswd = entry_input_repasswd.get()
    hash_passwd = crypto.hash_sha1(passwd)

    if stdid == '' or birthday == '' or fullname == '' or usrname == '' or passwd == '' or address == '' or repasswd == '':
        messagebox.showwarning('Invalid input', 'Please enter complete information', parent=insert_student_window)
        return

    if passwd != repasswd:
        messagebox.showwarning('Invalid input', 'Please re-enter your password', parent=insert_student_window)
        return

    strsql = f"""
                INSERT INTO SINHVIEN VALUES (?, ?, ?, ?, ?, ?, {hash_passwd})
            """
    
    params = (stdid, fullname, birthday, address, classid, usrname)
    
    try:
        cursor.execute(strsql, params)
        cursor.commit()
        messagebox.showinfo('Success', 'Inserted successfully', parent=insert_student_window)
        Load_Data_Table(_table_name='SINHVIEN', _treeview=treeview_SINHVIEN, _id_class=classid)
        insert_student_window_destroy()

    except pyodbc.Error as e:
        messagebox.showinfo('Error', f'FAIL: {str(e)}', parent=insert_student_window)
        insert_student_window_destroy()
        return

    None

def insert_student_window_destroy():
    window.attributes('-disable', False)
    insert_student_window.destroy()

def Insert_Student(class_var):
    # Check employee has managed any class
    classid = class_var.get()
    if classid == '':
        messagebox.showwarning('Invalid input', 'You have not managed any class', parent=window)
        return
    
    global insert_student_window
    
    insert_student_window = ml.Init_Screen(f'Thêm sinh viên lớp {classid}', width=500, height=480)
    insert_student_window.protocol("WM_DELETE_WINDOW", insert_student_window_destroy)
    window.attributes('-disable', True)

    label_title = tk.Label(insert_student_window, text='NHẬP THÔNG TIN NHÂN VIÊN', font=('Arial', 12, 'bold'))
    label_title.pack()

    input_frame = tk.Frame(insert_student_window)
    input_frame.pack(pady=20)

    global entry_input_stdid, entry_input_fullname, entry_input_birthday, entry_input_address, entry_input_usrname, entry_input_passwd, entry_input_repasswd
    
    label_stdid = tk.Label(input_frame, text='Mã SV', font=('Arial', 12))
    label_stdid.grid(pady=10, row=0, column=0, sticky='w')

    entry_input_stdid = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_stdid.grid(pady=10, row=0, column= 1)

    label_fullname = tk.Label(input_frame, text='Họ tên', font=('Arial', 12))
    label_fullname.grid(pady=10, row=1, column=0, sticky='w')

    entry_input_fullname = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_fullname.grid(pady=10, row=1, column=1)

    label_birthday = tk.Label(input_frame, text='Ngày sinh', font=('Arial', 12))
    label_birthday.grid(pady=10, row=2, column=0, sticky='w')

    entry_input_birthday = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_birthday.grid(pady=10, row=2, column=1)

    label_address = tk.Label(input_frame, text='Địa chỉ', font=('Arial', 12))
    label_address.grid(pady=10, row=3, column=0, sticky='w')

    entry_input_address = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_address.grid(pady=10, row=3, column=1)

    label_usrname = tk.Label(input_frame, text='Tên đăng nhập', font=('Arial', 12))
    label_usrname.grid(pady=10, row=4, column=0, sticky='w')

    entry_input_usrname = tk.Entry(input_frame, font=('Arial', 12))
    entry_input_usrname.grid(pady=10, row=4, column=1)

    label_passwd = tk.Label(input_frame, text='Mật khẩu', font=('Arial', 12))
    label_passwd.grid(pady=10, row=5, column=0, sticky='w')

    entry_input_passwd = tk.Entry(input_frame, show='*',  font=('Arial', 12))
    entry_input_passwd.grid(pady=10, row=5, column=1)

    label_repasswd = tk.Label(input_frame, text='Xác nhận mật khẩu', font=('Arial', 12))
    label_repasswd.grid(pady=10, row=6, column=0, sticky='w')

    entry_input_repasswd = tk.Entry(input_frame, show='*',  font=('Arial', 12))
    entry_input_repasswd.grid(pady=10, row=6, column=1)

    button_frame = tk.Frame(insert_student_window)
    button_frame.pack(pady=10)

    button_confirm = tk.Button(button_frame, text='Xác nhận', font=('Arial', 12), command=lambda: sql_insert_student(classid))
    button_confirm.pack(pady=10, padx=10, side='left')

    button_exit = tk.Button(button_frame, text='Huỷ', font=('Arial', 12), command=insert_student_window_destroy)
    button_exit.pack(pady=10, padx=10, side='left')

    insert_student_window.mainloop()
    

def SINHVIEN_Tab():
    # Create a variable to store the selected class
    class_var = tk.StringVar()

    class_option_menu = tk.OptionMenu(student_frame, class_var,"")
    class_option_menu.pack(side="top", anchor="w")
    class_option_menu.config(width=15)

    # TreeView frame
    global treeview_SINHVIEN
    treeview_SINHVIEN = tk.Frame(student_frame)
    treeview_SINHVIEN = ttk.Treeview(student_frame)
    treeview_SINHVIEN.pack(pady=2)
    
    # taskbar QLSV
    taskbar_Frame = tk.Frame(student_frame)
    taskbar_Frame.pack(pady=2)

    update_button = tk.Button(taskbar_Frame, text="Thêm sinh viên", command=lambda: Insert_Student(class_var))
    update_button.pack(side="left", anchor="w", padx=10)
    
    update_button = tk.Button(taskbar_Frame, text="Chỉnh sửa thông tin", command=Update_Student)
    update_button.pack(side="left", anchor="w", padx=10)

    # Load class_id 
    load_MALOP(_class_option_menu=class_option_menu, _class_var=class_var)
    
    Load_Data_Table(_treeview=treeview_SINHVIEN, _class_var=class_var, _table_name='SINHVIEN')
    # handle event if class is changed
    class_var.trace_add('write', lambda *args: Load_Data_Table(_treeview=treeview_SINHVIEN, _class_var=class_var, _table_name='SINHVIEN'))




def sql_insert_mark(_id_std, _id_course, _id_class, _mark):
    id_std = _id_std.get()
    id_course = _id_course.get()
    mark = _mark.get()
    # ensure valid mark
    if ml.is_number(mark) == False or float(mark) < 0 or float(mark) > 10:
        messagebox.showwarning('Invalid mark', 'Please re-enter mark', parent=insert_mark_window)
        return
    # encrypt mark before write into database
    encrypted_mark = '0x' + crypto.encryptRSA(str(mark), Kpublic).hex()
    
    strsql = f"""
                INSERT INTO BANGDIEM VALUES  (?, ?, {encrypted_mark})
            """
    params = (id_std, id_course)
    cursor.execute(strsql, params)
    affected_rows = cursor.rowcount

    window.attributes('-disable', False)
    if affected_rows > 0:
        conn.commit()
        # Re-load data in BANGDIEM table
        Load_Data_Table(_table_name='BANGDIEM', _treeview=treeview_BANGDIEM, _id_class=_id_class)
        insert_mark_window.destroy()
    else:
        messagebox.showinfo("FAILED", "No rows updated.", parent=insert_mark_window)
        insert_mark_window.destroy()


# handle the event of inserting marks for students in the BANGDIEM table
def Insert_Mark(_class_var):
    MaLop = _class_var.get()

    global insert_mark_window
    insert_mark_window = ml.Init_Screen(title="Nhập bảng điểm", width=300, height=300)
    window.attributes('-disable', True)
    insert_mark_window.protocol("WM_DELETE_WINDOW", insert_mark_window_destroy)

    info_frame = tk.Frame(insert_mark_window)
    info_frame.pack(pady=20)

    label_MaSV = tk.Label(info_frame, text=f"MaSV", font=("Arial", 12))
    label_MaSV.grid(row=0, column=0, sticky="w", pady=5, padx=10)

    entry_MaSV = tk.Entry(info_frame, text=f"MaSV", font=("Arial", 12))
    entry_MaSV.grid(row=0, column=1, pady=5)

    label_MaHP = tk.Label(info_frame, text=f"MaHP", font=("Arial", 12))
    label_MaHP.grid(row=1, column=0, sticky="w", pady=5, padx=10)

    entry_MaHP = tk.Entry(info_frame, text=f"MaHP", font=("Arial", 12))
    entry_MaHP.grid(row=1, column=1, pady=5)

    label_DIEMTHI = tk.Label(info_frame, text="Điểm thi ", font=("Arial", 12))
    label_DIEMTHI.grid(row=2, column=0, sticky="w", pady=5)

    entry_DIEMTHI = tk.Entry(info_frame, font=("Arial", 12))
    entry_DIEMTHI.grid(row=2, column=1, pady=5)

    button_XacNhan_frame = tk.Frame(insert_mark_window)   
    button_XacNhan_frame.pack(pady=20)
    
    button_XacNhan = tk.Button(button_XacNhan_frame, text="Xác nhận", command=lambda: sql_insert_mark(entry_MaSV, entry_MaHP, MaLop, entry_DIEMTHI))
    button_XacNhan.grid(pady=20, sticky="e")


def BANGDIEM_Tab():
    # Create a variable to store the selected class
    class_var = tk.StringVar()

    # class option menu of mark tab
    class_option_menu = tk.OptionMenu(mark_frame, class_var,"")
    class_option_menu.pack(side="top", anchor="w")
    class_option_menu.config(width=15)

    # TreeView frame
    global treeview_BANGDIEM
    treeview_BANGDIEM = tk.Frame(mark_frame)
    treeview_BANGDIEM = ttk.Treeview(mark_frame)
    treeview_BANGDIEM.pack(pady=2)

    # insert mark frame
    taskbar_Frame = tk.Frame(mark_frame)
    taskbar_Frame.pack(pady=2)

    insert_button = tk.Button(taskbar_Frame, text="Nhập điểm bảng điểm", command=lambda: Insert_Mark(class_var))
    insert_button.pack(side='top', anchor='w')

    # Load class_id
    load_MALOP(_class_option_menu=class_option_menu, _class_var=class_var)

    # Load data in BANGDIEM table
    Load_Data_Table(_treeview=treeview_BANGDIEM, _table_name='BANGDIEM', _class_var=class_var, _width=250, _minwidth=250)
    
    # Load data in LOP table when class_var is changed
    class_var.trace_add('write', lambda *args: Load_Data_Table(_treeview=treeview_BANGDIEM, _table_name='BANGDIEM', _class_var=class_var, _width=250, _minwidth=250))

def exit_program():
    dashboard.attributes('-disable', False)
    window.destroy()

# QLSV
def Screen_QLSV(_dashboard, login_infor):
    global dashboard, window, Kprivate, Kpublic, conn, cursor
    conn, cursor, Kprivate, Kpublic, dashboard = login_infor.conn, login_infor.cursor, login_infor.kprivate, login_infor.kpublic, _dashboard

    window = ml.Init_Screen(title="Quản lý sinh viên", width=800, height=500)
    window.protocol("WM_DELETE_WINDOW", exit_program)

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
    
    tab_frame = tk.Frame(window, highlightbackground='black', highlightthickness=1.5)
    tab_frame.pack(fill='both', expand=True, padx=(10, 10), pady=(10, 10))
    # Load employee information that is currently logged in
    usrname, passwd = login_infor.usrname, login_infor.passwd
    Load_EMP_Infor(usrname, passwd)

    tab_control = ttk.Notebook(tab_frame)
    # Create table "chinh sua"
    edit_tab = ttk.Frame(tab_control)
    tab_control.add(edit_tab, text="Chỉnh sửa")

    # Create tab "Nhập điểm"
    mark_tab = ttk.Frame(tab_control)
    tab_control.add(mark_tab, text="Nhập điểm")

    tab_control.pack(expand=False, fill=tk.BOTH)

    global student_frame, mark_frame

    student_frame = tk.Frame(edit_tab)
    student_frame.pack()

    mark_frame = tk.Frame(mark_tab)
    mark_frame.pack()

    #Render content of edit information of student tab
    SINHVIEN_Tab()
    # Render content of insert point tab
    BANGDIEM_Tab()
    # window.mainloop()
    return window
