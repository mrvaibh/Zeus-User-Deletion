from zk import ZK, const


def delete_users(IP):
    conn = None

    # create ZK instance
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

# Code starts here
with open('machine_list.txt', 'r') as file:
    data = file.readlines()
    for ip in data:
        ip = ip.replace('\n', '')
        delete_users(ip)
