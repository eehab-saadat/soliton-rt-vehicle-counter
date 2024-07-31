from threading import Thread

class INSTANCE:
    __threads = []

    def __init__(self):
        pass

    def add(self, func: callable, args: tuple = ()) -> None:
        thread = Thread(target=func, args=args).start()
        self.__threads.append(thread)

    def stop_all(self):
        for thread in self.__threads:
            thread.join()