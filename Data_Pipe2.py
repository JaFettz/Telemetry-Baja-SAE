from multiprocessing import Process,Queue,Pipe,Array
from Data_Pipe import f
import time

if __name__ == '__main__':
    parent_conn,child_conn = Pipe()
    parent_conn_1,child_conn_2 = Pipe()
    p = Process(target=f, args=(child_conn,))
    # p1 = Process(target=f, args=(child_conn_2, 7))
    p.start()
    # p1.start()
    try:
        print(parent_conn.recv())   # prints "Hello"
        print(parent_conn_1.recv())
        parent_conn.send("test")
        time.sleep(10)
        parent_conn.send([0,1,2,3])
        while True:
            print("in true")
            time.sleep(2)
    except KeyboardInterrupt:
        pass

    parent_conn.send("kill")
    print("wating for Process")
    p.join()
    print("Ending")

    

