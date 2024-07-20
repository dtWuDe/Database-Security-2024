import tkinter as tk
from tkinter import ttk, messagebox
import MyLibary as ml

def Load_Class_Table(class_table):
    if ml.has_column_heading(class_table) == False:
        ml.Load_Data_Table(Table=class_table, table_name='LOP', cursor=cursor, mode='full')
    else:
        ml.Load_Data_Table(Table=class_table, table_name='LOP', cursor=cursor, mode='data')

def Load_Subject_Table(subject_table):
    if ml.has_column_heading(subject_table) == False:
        ml.Load_Data_Table(Table=subject_table, table_name='HOCPHAN', cursor=cursor, mode='full')
    else:
        ml.Load_Data_Table(Table=subject_table, table_name='HOCPHAN', cursor=cursor, mode='data')
    None


def sql_Insert_Class():
    class_id = class_id_entry.get()
    class_name = class_name_entry.get()
    class_emp = empid

    strsql = """
                INSERT INTO LOP VALUES(?, ?, ?)
            """
    cursor.execute(strsql, (class_id, class_name, class_emp))
    cursor.commit()
    Load_Class_Table(class_table)
    insert_class_window_destroy()
    None

# write into database
def sql_Insert_subject():
    subject_id = subject_id_entry.get()
    subject_name = subject_name_entry.get()
    credit_number = subject_credit_entry.get()

    if ml.is_number(credit_number) == False:
        messagebox.showwarning('Invalid credit number', 'Please re-enter credit number', parent=insert_subject_window)
        return
    
    strsql = """
                INSERT INTO HOCPHAN VALUES(?, ?, ?)
            """
    cursor.execute(strsql, (subject_id, subject_name, int(credit_number)))
    cursor.commit()
    Load_Subject_Table(subject_table)
    insert_subject_window_destroy()

def exit_program(window):
    window.destroy()

def insert_class_window_destroy():
    window.attributes('-disable', False)
    insert_class_window.destroy()

def Insert_Class():
    global insert_class_window
    insert_class_window = ml.Init_Screen(title="Thêm lớp học", width=500, height=400)
    insert_class_window.protocol("WM_DELETE_WINDOW", insert_class_window_destroy)
    window.attributes('-disable', True)

    # Title frame
    title_frame = tk.Frame(insert_class_window)
    title_frame.pack(pady=20)

    title_label = tk.Label(title_frame, text='THÊM LỚP HỌC', font=('Arial', 12, 'bold'))
    title_label.pack()
    # Input frame
    input_frame = tk.Frame(insert_class_window)
    input_frame.pack()
    global class_id_entry, class_name_entry, class_emp_entry
    class_id_label = tk.Label(input_frame, text='Mã lớp ', font=('Arial', 12))
    class_id_label.grid(row=0, column=0, pady=20, sticky='w')

    class_id_entry = tk.Entry(input_frame, font=('Arial', 12))
    class_id_entry.grid(row=0, column=1, pady=20)

    class_name_label = tk.Label(input_frame, text='Tên lớp ', font=('Arial', 12))
    class_name_label.grid(row=1, column=0, pady=20, sticky='w')

    class_name_entry = tk.Entry(input_frame, font=('Arial', 12))
    class_name_entry.grid(row=1, column=1, pady=20)

    class_emp_label = tk.Label(input_frame, text='Mã NV ', font=('Arial', 12))
    class_emp_label.grid(row=2, column=0, pady=20, sticky='w')

    class_emp_entry = tk.Entry(input_frame, font=('Arial', 12))
    class_emp_entry.grid(row=2, column=1, pady=20)
    class_emp_entry.delete(0, tk.END)
    class_emp_entry.insert(0, empid)
    class_emp_entry.config(state='disabled')

    button_frame = tk.Frame(insert_class_window)
    button_frame.pack(padx=20, pady=20)

    confirm_button = tk.Button(button_frame, text='Xác nhận', font=('Arial', 12), command=sql_Insert_Class)
    confirm_button.pack(side='left', padx=20)
    
    exit_button = tk.Button(button_frame, text='Hủy', font=('Arial', 12), width=8, command=insert_class_window_destroy)
    exit_button.pack(side='left', padx= 20)

    insert_class_window.mainloop()
    None

def insert_subject_window_destroy():
    window.attributes('-disable', False)
    insert_subject_window.destroy()

def Insert_Subject():
    global insert_subject_window
    insert_subject_window = ml.Init_Screen(title="Thêm học phần", width=500, height=400)
    insert_subject_window.protocol("WM_DELETE_WINDOW", insert_subject_window_destroy)
    window.attributes('-disable', True)
    # Title frame
    title_frame = tk.Frame(insert_subject_window)
    title_frame.pack(pady=20)

    title_label = tk.Label(title_frame, text='THÊM HỌC PHẦN ', font=('Arial', 12, 'bold'))
    title_label.pack()
    # Input frame
    input_frame = tk.Frame(insert_subject_window)
    input_frame.pack()
    global subject_id_entry, subject_name_entry, subject_credit_entry
    subject_id_label = tk.Label(input_frame, text='Mã học phần ', font=('Arial', 12))
    subject_id_label.grid(row=0, column=0, pady=20, sticky='w')

    subject_id_entry = tk.Entry(input_frame, font=('Arial', 12))
    subject_id_entry.grid(row=0, column=1, pady=20)

    subject_name_label = tk.Label(input_frame, text='Tên học phần ', font=('Arial', 12))
    subject_name_label.grid(row=1, column=0, pady=20, sticky='w')

    subject_name_entry = tk.Entry(input_frame, font=('Arial', 12))
    subject_name_entry.grid(row=1, column=1, pady=20)

    subject_credit_label = tk.Label(input_frame, text='Số TC ', font=('Arial', 12))
    subject_credit_label.grid(row=2, column=0, pady=20, sticky='w')

    subject_credit_entry = tk.Entry(input_frame, font=('Arial', 12))
    subject_credit_entry.grid(row=2, column=1, pady=20)

    button_frame = tk.Frame(insert_subject_window)
    button_frame.pack(padx=20, pady=20)

    confirm_button = tk.Button(button_frame, text='Xác nhận', font=('Arial', 12), command=sql_Insert_subject)
    confirm_button.pack(side='left', padx=20)

    exit_button = tk.Button(button_frame, text='Hủy', font=('Arial', 12), width=8, command=insert_subject_window_destroy)
    exit_button.pack(side='left', padx= 20)

    insert_subject_window.mainloop()
    None

def exit_program():
    dashboard.attributes('-disable', False)
    window.destroy()
    None

def Screen_Manage_Class(_dashboard, login_infor):
    global dashboard, window, conn, cursor, empid
    conn, cursor, empid, dashboard = login_infor.conn, login_infor.cursor, login_infor.empid, _dashboard

    window = ml.Init_Screen(title="Quản lý lớp học", width=800, height=800)
    window.protocol("WM_DELETE_WINDOW", exit_program)
    title_frame = tk.Frame(window)
    title_frame.pack(pady=20)
    # Title
    title_label = tk.Label(title_frame, text='QUẢN LÝ LỚP HỌC', font=('Arial', 12, 'bold'))
    title_label.grid()

    # CLASS_FRAME
    class_frame = tk.Frame(window, highlightbackground='black', highlightthickness=1.5)
    class_frame.pack(fill='both', expand=True, padx=10, pady=10)

    class_title = tk.Label(class_frame, text='Thông tin lớp học', font=('Arial', 10, 'bold'))
    class_title.pack(anchor='nw', padx=20, pady=20)

    class_table_frame = tk.Frame(class_frame)
    class_table_frame.pack()
    global class_table
    class_table = ttk.Treeview(class_table_frame)
    class_table.pack()

    add_class_button = tk.Button(class_frame, text='Thêm', font=('Arial', 12), command=Insert_Class)
    add_class_button.pack(pady=10, padx=10, side='left')
    # Load content of class table
    Load_Class_Table(class_table)

    # subject_FRAME
    subject_frame = tk.Frame(window, highlightbackground='black', highlightthickness=1.5)
    subject_frame.pack(fill='both', expand='true', padx=10, pady=10)

    subject_title = tk.Label(subject_frame, text='Thông tin học phần', font=('Arial', 10, 'bold'))
    subject_title.pack(anchor='nw', padx=20, pady=20)

    subject_table_frame = tk.Frame(subject_frame)
    subject_table_frame.pack()
    global subject_table
    subject_table = ttk.Treeview(subject_table_frame)
    subject_table.pack()

    add_subject_button = tk.Button(subject_frame, text='Thêm', font=('Arial', 12), command=Insert_Subject)
    add_subject_button.pack(pady=10, padx=10, side='left')
    # Load content of subject table
    Load_Subject_Table(subject_table)

    return window
    None