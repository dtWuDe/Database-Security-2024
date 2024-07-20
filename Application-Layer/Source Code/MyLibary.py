import tkinter as tk

# Load column heading and data of table if mode is 'full', justs row data if mode is 'data'
def Load_Data_Table(Table, table_name, cursor, mode={'full', 'data'},):
    strsql = f"SELECT* FROM {table_name}"
    cursor.execute(strsql)

    column_name = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    exist_id = [Table.item(item)['values'][0] for item in Table.get_children()]
    for row in rows:
        if row[0] not in exist_id:       
            values = list(row)
            Table.insert(parent='', index='end', values=values)

    if mode == 'data':
        return
    
    Table['column'] = tuple(column_name)
    Table.column('#0', width=0, minwidth=0, anchor='center')
    for column in column_name:
        Table.column(column, width=250, minwidth=200, anchor='w')
        Table.heading(column, text=column) 

# Create new window
def Init_Screen(title: str, width: int, height: int):
    init_window = tk.Tk()
    init_window.title(title)
    window_width = width
    window_height = height
    screen_width = init_window.winfo_screenwidth()
    screen_height = init_window.winfo_screenheight() 
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    init_window.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')
    
    return init_window
    None

# Check if table has column heading
def has_column_heading(treeview):
    columns = treeview["columns"]
    for column in columns:
        heading = treeview.heading(column)
        if heading:
            return True
    return False

# Check if score is an integer
def is_number(score):
    try:
        int_score = float(score)
        return True  # The score is an integer
    except ValueError:
        return False  # The score is not an integer


