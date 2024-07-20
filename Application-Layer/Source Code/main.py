from login import login
from Dashboard import Screen_Dashboard


def __main__():
    # Check login
    isLogout = 'Logout'
    while isLogout == 'Logout':
        check = login()
        if check != None:
            conn, cursor, usrname, passwd = check[0]
            isLogout = Screen_Dashboard(conn, cursor, usrname, passwd)[0]
        else:
            break

if __name__ == '__main__':
    __main__()