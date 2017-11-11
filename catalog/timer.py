import time
next_check = int(time.time()) + 5

def check_update_db():
    print('Current Time: ' + str(int(time.time())) + ', Next Schedule Run: ' + str(next_check))
    return (int(time.time()) > next_check)

def update_timer():
    return  int(time.time()) + 5
    # print('Current Time: ' + str(int(time.time())) + ', Next Schedule Run: ' + str(next_check))

    


