
class Robot:
    def __init__(self):
        self.__voltage = 100

    @property
    def voltage(self):
        self.__voltage -= 7
        if self.__voltage < 0:
            self.__voltage = 100
        return self.__voltage

