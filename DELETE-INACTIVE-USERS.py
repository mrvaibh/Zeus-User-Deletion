from zk import ZK, const

conn = None
# create ZK instance

# For eg: 192.168.5.111
IP = input("Enter machine IP: ")

zk = ZK(IP, port=4370, timeout=60, password=0, force_udp=False, ommit_ping=False)
try:
    # connect to device
    conn = zk.connect()

    total_users = conn.get_users()

    # make a user map
    user_map = {}
    for user in total_users:
        user_map[user.user_ud] = user.uid

    print(f"Total users - {len(total_users)}")

    confirm = input(
        "Are you sure you want to delete all the employees listed in employee_inactive.txt? [y/n]")

    with open('inactive_employees.txt', 'r') as file:
        data = file.readlines()
        print(f"Users to delete - {len(data)}")
        for userid in data:
            user_id = userid.replace('\n', '')
            try:
                conn.delete_user(uid=user_map[user_id])
            except Exception as error:
                print(error)
                continue

            print(f'User {user_id} deleted')

    print("User deleted !")

except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
