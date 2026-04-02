import toml, os, datetime, re

Conf = None
ConfVars = None
ConfDirs = None
ConfNames = None
ConfLog = None

Start = True

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def LoadConf():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog

    LocalConf = toml.load("Config.toml")
    Conf = LocalConf
    ConfVars = Conf["Variables"]
    ConfDirs = Conf["DirectoryPaths"]
    ConfNames = Conf["Names"]
    ConfLog = Conf["Log"]


def Error():
    global Start
    if (Conf["SafeMode"] == 1):
            Start = False


def Speak(Text):
    if (Conf["SilentMode"] != 1):
        print(Text)


def GetConf(Parameter):
    if Parameter in Conf:
        return str(Conf[Parameter])
    
    elif Parameter in ConfVars:
        return str(ConfVars[Parameter])
    
    elif Parameter in ConfDirs:
        return str(ConfDirs[Parameter])
    
    elif Parameter in ConfNames:
        return str(ConfNames[Parameter])
    
    elif Parameter in ConfLog:
        return str(ConfLog[Parameter])
    
    return None


def Parse(String = None, Var = None, OrgFile = None, OutputDir = None):
    def Replacer(Match):
        Content = Match.group(1)

        if (Content == None or Content == ""):
            if (Var != None):
                return str(Var)
            else:
                return ""
        
        Value = GetConf(Content)
        if (Value != None):
            return Value
            
    
    Now = datetime.datetime.now()

    VarValues = {
        ConfVars["NextNum"]: "NOT ADDED",
        ConfVars["NextChar"]: "NOT ADDED",
        ConfVars["Parent"]: "NOT ADDED",
        ConfVars["OrgFileName"]: "NOT ADDED",
        ConfVars["OrgFileType"]: "NOT ADDED",
        ConfVars["Year"]: str(Now.year),
        ConfVars["Month"]: str(Now.month),
        ConfVars["Day"]: str(Now.day),
        ConfVars["Hour"]: str(Now.hour),
        ConfVars["Minute"]: str(Now.minute),
        ConfVars["Second"]: str(Now.second),
        ConfVars["VarCall"]: Var
    }

    for Key, Value in VarValues.items():
        if Key in String and Value is not None:
            String = String.replace(Key, Value)

    String = re.sub(r"%([^%]*)%", Replacer, String)

    return String


def Dir(Name):
    os.makedirs(Name, exist_ok=True)


def LogWrite(Text):
    if (ConfDirs["LogDir"] != None and ConfNames != "Unset"):
        if (ConfNames["LogFileName"] != None and ConfNames["LogFileName"] != "Unset"):
            Dir(Parse(ConfDirs["LogDir"]))
            LogFile = f"{Parse(ConfDirs["LogDir"])}/{Parse(ConfNames["LogFileName"])}.log"
            with open(LogFile, "w", encoding="utf-8") as File:
                File.write(f"{Parse(ConfLog["All"])}{Text}\n")


def ConfCheck():
    for Item in ConfVars:
        if (Item == None or Item == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Item)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()
    
    for Item in ConfDirs:
        if (Item == None or Item == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Item)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()

    for Item in ConfLog:
        if (Item == None or Item == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Item)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()


def Init():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog
    
    LoadConf()
    if (Conf != None):
        ConfCheck()

        if (Start):
            TextOutput = Parse(ConfLog["Start"])
            LogWrite(TextOutput)
            Speak(TextOutput)
            
            Main()
        
        else:
            TextOutput = Parse(ConfLog["NotStart"])
            LogWrite(TextOutput)
            Speak(TextOutput)
    
    else:
        print("NO CONFIG FOUND! Make sure the 'Config.toml' is in the same directory as 'SaraSortd.py'")


def Main():
    while True:
        pass


Init()