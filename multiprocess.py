

from multiprocessing import Process

def f(task):
    for i in range(0,1000):
        print(task, i)


if __name__ == '__main__':
    p1 = Process(target=f, args=('task1',))
    p1.start()

    p2 = Process(target=f, args=('task2',))
    p2.start()


    #p.join()

