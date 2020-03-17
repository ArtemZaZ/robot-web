
class Battery:
    def __init__(self):
        self.__imagesDict = {
            "5%": open("battery/img/5_p.png", 'rb').read(),
            "15%": open("battery/img/15_p.png", 'rb').read(),
            "25%": open("battery/img/25_p.png", 'rb').read(),
            "50%": open("battery/img/50_p.png", 'rb').read(),
            "75%": open("battery/img/75_p.png", 'rb').read(),
            "100%": open("battery/img/100_p.png", 'rb').read(),
            "charging": open("battery/img/charging.png", 'rb').read(),
            "none": open("battery/img/none.png", 'rb').read()
        }

    def getImage(self, voltage):
        if not (0 < voltage < 100):
            return self.__imagesDict["none"]
        elif voltage > 75:
            return self.__imagesDict["100%"]
        elif voltage > 50:
            return self.__imagesDict["75%"]
        elif voltage > 25:
            return self.__imagesDict["50%"]
        elif voltage > 15:
            return self.__imagesDict["25%"]
        elif voltage > 5:
            return self.__imagesDict["15%"]
        elif voltage >= 0:
            return self.__imagesDict["5%"]

