import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import connSQL as sql

def update_sql(MaSV, entry_HoTen, entry_NgaySinh, entry_DiaChi):
    HoTen = entry_HoTen.get()
    NgaySinh = entry_NgaySinh.get()
    DiaChi = entry_DiaChi.get()

    strsql = f"""
                UPDATE SINHVIEN
                SET HOTEN = '{HoTen}', NGAYSINH = '{NgaySinh}', DIACHI = '{DiaChi}'
                WHERE MASV = '{MaSV}'
             """
    g_cursor.execute(strsql)
    affected_rows = g_cursor.rowcount

    if affected_rows > 0:
        g_conn.commit()
        messagebox.showinfo("SUCESS", f"Update successful. {affected_rows} rows updated.")
        load_data_TABLE('SINHVIEN', treeview_SINHVIEN)
        update_window.destroy()
    else:
        messagebox.showinfo("FAILED", "No rows updated.")
        update_window.destroy()

def update_student():
    # get the contents of the currently focused rows
    treeview_content = treeview_SINHVIEN.item(treeview_SINHVIEN.focus())

    # get indext of MALOP in treeview
    malop_index = treeview_SINHVIEN["columns"].index("MALOP")
    if treeview_content["values"] == '':
        messagebox.showwarning("Chưa chọn sinh viên","Vui lòng chọn sinh viên cần chỉnh sửa thông tin!")
        return
    
    
    malop = treeview_content["values"][malop_index]  
    strsql = f"""
                SELECT MANV FROM LOP WHERE MALOP = '{malop}'
              """
    g_cursor.execute(strsql)
    administration_of_student = g_cursor.fetchall()[0][0]
    if current_user != administration_of_student:
        messagebox.showwarning("Chưa cấp quyền","Bạn không thể thay đổi thông tin sinh viên bạn không quản lý")
        return
    

    MaSV_index = treeview_SINHVIEN["columns"].index("MASV")
    MaSV = treeview_content["values"][MaSV_index]

    global update_window
    update_window = tk.Tk()
    update_window.title(MaSV)
    update_window_height = 200
    update_window_width = 400
    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()
    x_coordinate = (screen_width - update_window_width) // 2
    y_coordinate = (screen_height - update_window_height) // 2
    update_window.geometry(f"{update_window_width}x{update_window_height}+{x_coordinate}+{y_coordinate}")

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

    label_HoTen = tk.Label(frame, text="Họ tên:", font=("Arial", 12))
    label_HoTen.grid(row=0, column=0, sticky="e")
    
    entry_HoTen = tk.Entry(frame, font=("Arial", 12))
    entry_HoTen.grid(row=0, column=1)
    entry_HoTen.insert(0, HoTen) # default value

    label_NgaySinh = tk.Label(frame, text="Ngày sinh:", font=("Arial", 12))
    label_NgaySinh.grid(row=1, column=0, sticky="e")

    entry_NgaySinh = tk.Entry(frame, font=("Arial", 12))
    entry_NgaySinh.grid(row=1, column=1)
    entry_NgaySinh.insert(0, NgaySinh)    

    label_DiaChi = tk.Label(frame, text="Địa chỉ:", font=("Arial", 12))
    label_DiaChi.grid(row=2, column=0, sticky="e")

    entry_DiaChi = tk.Entry(frame, font=("Arial", 12))
    entry_DiaChi.grid(row=2, column=1)
    entry_DiaChi.insert(0, DiaChi) 
    
    button_update_frame = tk.Frame(update_window)   
    button_update_frame.pack(pady=20)
    
    button_update = tk.Button(button_update_frame, text="Cập nhật", font=("Arial", 12), command=lambda: update_sql(MaSV, entry_HoTen, entry_NgaySinh, entry_DiaChi))
    button_update.pack(side="left", padx=10, pady=10)

    



def load_MALOP(class_var, class_option_menu):
    # Connect to the SQL Server database
    connection, cursor = sql.Connect_SQL('localhost', 'QLSVNhom', 'sa', 'sa@123')
    cursor.execute("SELECT MALOP FROM LOP")
    rows = cursor.fetchall()
    
    # Clear the existing data in the OptionMenu
    class_var.set("")  # Clear the current selection
    class_option_menu['menu'].delete(0, tk.END)
    
    # Load the data into the OptionMenu
    for row in rows:
        class_option_menu['menu'].add_command(label=row[0], command=tk._setit(class_var, row[0]))
    
    if rows:
        class_var.set(rows[0][0])

    # Close the database connection
    cursor.close()
    connection.close()

def load_structure_TABLE(TABLE_NAME, treeview):
    # Clear existing data in the Treeview
    treeview.delete(*treeview.get_children())

    # Connect to the database
    conn, cursor = sql.Connect_SQL('localhost', 'QLSVNhom', 'sa', 'sa@123')

    # Execute SELECT query
    cursor.execute(f"""
                        SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = '{TABLE_NAME}';
                   """)
    column_names = cursor.fetchall()
    column_names = [column[0] for column in column_names]
    treeview['columns'] = tuple(column_names)

    treeview.column("#0", width=0, minwidth=0, anchor="center")
    for column in column_names:
        treeview.column(column, width=100, minwidth=100, anchor="center")
        treeview.heading(column, text=column)

    cursor.close()
    conn.close()


def load_data_TABLE(TABLE_NAME, treeview):
    # Clear existing data in the Treeview
    treeview.delete(*treeview.get_children())
    # SELECT DATA FROM TABLE
    strsql = f"""
                    SELECT* 
                    FROM {TABLE_NAME}
              """
    
    if TABLE_NAME == "SINHVIEN":
        malop = class_var.get()
        strsql += f" WHERE MALOP = '{malop}'"

    g_cursor.execute(strsql)
    rows = g_cursor.fetchall()

    # Insert data into the Treeview
    for row in rows:
        values = (row[0],) + row[1:]  # Exclude the first column
        treeview.insert(parent='', index='end', values=values)


def Update_SINHVIEN_Tab():
    # taskbar QLSV
    taskbar_Frame = tk.Frame(update_frame)
    taskbar_Frame.pack(pady=2)


    update_button = tk.Button(taskbar_Frame, text="Chỉnh sửa thông tin", command=lambda: update_student())
    update_button.pack(side="top", anchor="w")

    # LOP select list box
    listbox_frame = tk.Frame(update_frame)
    listbox_frame.pack(pady=2)

    # Create a variable to store the selected class
    global class_var
    class_var = tk.StringVar()

    class_option_menu = tk.OptionMenu(update_frame, class_var,"")
    class_option_menu.pack(side="top", anchor="w")

    load_MALOP(class_var, class_option_menu)

    # TreeView frame
    global treeview_SINHVIEN
    treeview_SINHVIEN = tk.Frame(update_frame)
    treeview_SINHVIEN = ttk.Treeview(update_frame)
    treeview_SINHVIEN.pack(pady=2)
    load_structure_TABLE('SINHVIEN', treeview_SINHVIEN)
    load_data_TABLE('SINHVIEN', treeview_SINHVIEN)

    class_var.trace_add('write', lambda *args: load_data_TABLE('SINHVIEN', treeview_SINHVIEN))

    # window.protocol('WM_DELETE_WINDOW', lambda: on_close(conn, cursor, window))

def insert_sql(MASV, MAHP, DIEM):    
    # Get MaLop of current SINHVIEN
    strsql = f"""
                SELECT MANV 
                FROM LOP
                WHERE MALOP IN (SELECT MALOP FROM SINHVIEN WHERE MASV = '{MASV}')
             """
    g_cursor.execute(strsql)
    administrator_of_student = g_cursor.fetchall()[0][0]
    
    if current_user != administrator_of_student:
        messagebox.showwarning("Chưa cấp quyền", "Bạn không có quyền nhập điểm cho sinh viên hiện tại")
        return
    
    strsql = f"""
                UPDATE BANGDIEM 
                SET DIEMTHI = ENCRYPTBYASYMKEY(ASYMKEY_ID('{current_user}'),CAST('{DIEM}' AS VARCHAR(MAX)))
                WHERE MASV = '{MASV}' AND MAHP = '{MAHP}'
             """
    g_cursor.execute(strsql)

    affected_rows = g_cursor.rowcount

    if affected_rows > 0:
        g_conn.commit()
        messagebox.showinfo("SUCCESS",f"Update successful. {affected_rows} rows updated.")
        load_data_TABLE('BANGDIEM', treeview_BANGDIEM)
        insert_window.destroy()
    else:
        messagebox.showinfo("FAILED", "No row updated")

    pass


def insert_bangdiem():
    treeview_content = treeview_BANGDIEM.item(treeview_BANGDIEM.focus())
    # Handle if not select user for update
    if treeview_content["values"] == '':
        messagebox.showwarning("Chưa chọn Sinh Viên", "Vui lòng chọn Sinh viên cần chỉnh sửa")
        return
    
    MaSV_index = treeview_BANGDIEM["column"].index("MASV")
    MaSV = treeview_content["values"][MaSV_index]

    MaHP_index = treeview_BANGDIEM["column"].index("MAHP")
    MaHP = treeview_content["values"][MaHP_index]

    strsql = f"""
                SELECT MANV 
                FROM LOP 
                WHERE MALOP IN (SELECT MALOP FROM SINHVIEN WHERE MASV = '{MaSV}')
             """
    g_cursor.execute(strsql)
    administration_of_student = g_cursor.fetchall()[0][0] 

    if administration_of_student != current_user:
        messagebox.showwarning("Chưa cấp quyền", "Bạn không được phép nhập điểm sinh viên bạn không quản lý")
        return

    global insert_window
    insert_window = tk.Tk()
    insert_window.title("Nhập bảng điểm")

    insert_window_width = 300
    insert_window_height = 300
    insert_window_screen_height = insert_window.winfo_screenheight()
    insert_window_screen_width = insert_window.winfo_screenwidth()
    insert_window_x_coordinate = (insert_window_screen_width - insert_window_width) // 2
    insert_window_y_coordinate = (insert_window_screen_height - insert_window_height) // 2
    insert_window.geometry(f"{insert_window_width}x{insert_window_height}+{insert_window_x_coordinate}+{insert_window_y_coordinate}")

    info_frame = tk.Frame(insert_window)
    info_frame.pack(pady=20)

    label_MaSV = tk.Label(info_frame, text=f"MaSV: {MaSV}", font=("Arial", 12))
    label_MaSV.grid(row=0, column=0, sticky="w", pady=5, padx=10)

    label_MaHP = tk.Label(info_frame, text=f"MaHP: {MaHP}", font=("Arial", 12))
    label_MaHP.grid(row=1, column=0, sticky="w", pady=5, padx=10)

    label_DIEMTHI = tk.Label(info_frame, text="Điểm thi: ", font=("Arial", 12))
    label_DIEMTHI.grid(row=2, column=0, sticky="w", pady=5, padx=10)

    entry_DIEMTHI = tk.Entry(info_frame, font=("Arial", 12))
    entry_DIEMTHI.grid(row=2, column=1, sticky="w", pady=5, padx=0)

    button_XacNhan_frame = tk.Frame(insert_window)   
    button_XacNhan_frame.pack(pady=20)
    
    button_XacNhan = tk.Button(info_frame, text="Xác nhận", command=lambda: insert_sql(MASV=MaSV, MAHP=MaHP, DIEM=entry_DIEMTHI.get()))
    button_XacNhan.grid(pady=20, sticky="e")
    
    pass

def Insert_BANGDIEM_Tab():
    taskbar_Frame = tk.Frame(insert_frame)
    taskbar_Frame.pack(pady=2)

    insert_button = tk.Button(taskbar_Frame, text="Nhập điểm bảng điểm", command=lambda: insert_bangdiem())
    insert_button.pack(side='top', anchor='w')

    # TreeView frame
    global treeview_BANGDIEM
    treeview_BANGDIEM = tk.Frame(insert_frame)
    treeview_BANGDIEM = ttk.Treeview(insert_frame)
    treeview_BANGDIEM.pack(pady=2)
    load_structure_TABLE('BANGDIEM', treeview_BANGDIEM)
    load_data_TABLE(TABLE_NAME='BANGDIEM', treeview=treeview_BANGDIEM)
    pass

def on_close(window):
    sql.Disconnect_SQL(g_conn, g_cursor)
    window.destroy()

def Screen_QLSV(conn, cursor):
    # def Screen_QLSV(conn, cursor):
    #     # Tạo cửa sổ giao diện
    global g_conn, g_cursor
    g_conn = conn
    g_cursor = cursor

    strsql = """
                SELECT SUSER_SNAME();
             """
    g_cursor.execute(strsql)
    global current_user
    current_user = g_cursor.fetchall()[0][0]

    window = tk.Tk()
    window.title("Quản lý sinh viên")

    # Set the window size
    window_width = 800
    window_height = 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    tab_control = ttk.Notebook(window)
    # Create table "chinh sua"
    edit_tab = ttk.Frame(tab_control)
    tab_control.add(edit_tab, text="Chỉnh sửa")

    # Create tab "Nhập điểm"
    score_tab = ttk.Frame(tab_control)
    tab_control.add(score_tab, text="Nhập điểm")

    tab_control.pack(expand=False, fill=tk.BOTH)

    global update_frame, insert_frame

    update_frame = tk.Frame(edit_tab)
    update_frame.pack()

    insert_frame = tk.Frame(score_tab)
    insert_frame.pack()

    Update_SINHVIEN_Tab()
    Insert_BANGDIEM_Tab()

    window.mainloop()