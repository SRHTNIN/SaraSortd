import toml, os

Conf = None

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def LoadConf():
    global Conf

    LocalConf = toml.load("Config.toml")
    Conf = LocalConf


def Init():
    global Conf
    
    LoadConf()
    if (Conf != None):
        Main()


def Main():
    global Conf

    Clear()
    print(Conf)


Init()