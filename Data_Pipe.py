from multiprocessing import Process,Pipe
import time

def f(child_conn):
    Mode = True
    while Mode:
        last = "Nothing"
        for i in range(6):
            msg = str(i)
            child_conn.send(msg)
            if child_conn.poll():
                last = child_conn.recv()
            print("internal data: ", i)
            time.sleep(1)
            print(last)
            if last == "kill":
                Mode = False
    print("internal closing")
    time.sleep(10)
    child_conn.close()
