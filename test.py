from zk import ZK, const

# Clipboard Logic
import ctypes

CF_TEXT = 1

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p

def get_clipboard_text():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return value.decode("utf-8")
    finally:
        user32.CloseClipboard()

def delete_users(IP):
    conn = None

    # create ZK instance
    zk = ZK(IP, port=4370, timeout=60, password=0, force_udp=False, ommit_ping=False)

    try:
        # connect to device
        conn = zk.connect()

        print(f'\n=========== Attempting IP - {IP} ===========')

        total_users = conn.get_users()

        # make a user map
        user_map = {}
        for user in total_users:
            user_map[user.user_id] = user.uid

        data = get_clipboard_text().strip().split('\r')

        print(f"Users to delete - {len(data)}/{len(total_users)}")
        for paycode in data:
            user_id = paycode.strip()
            try:
                conn.delete_user(uid=user_map[user_id])
            except Exception as error:
                print("Can't delete user:", error)
                continue
            print(f'User {user_id} deleted')

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()

# Code starts here
with open('machine_list.txt', 'r') as file:
    data = file.readlines()
    for ip in data:
        ip = ip.replace('\n', '')
        delete_users(ip)
