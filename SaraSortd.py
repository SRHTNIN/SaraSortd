import toml, os, datetime, re, shutil, fnmatch, time

ConfPath = "./Config.toml"

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


def LoadGlobalConf():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog

    LocalConf = toml.load(ConfPath)
    Conf = LocalConf
    ConfVars = Conf["Variables"]
    ConfDirs = Conf["DirectoryPaths"]
    ConfNames = Conf["Names"]
    ConfLog = Conf["Log"]


def CheckConf(Path = ConfPath):
    ConfData = toml.load(Path)

    def CheckDict(Data):
        for Key, Value in Data.items():
            if isinstance(Value, dict):
                CheckDict(Value)
            else:
                if Value is None or Value == "Unset":
                    TextOutput = Parse(String = ConfLog["Unset"], Path = Path, VarCall = Key)
                    LogWrite(TextOutput)
                    Speak(TextOutput)
                    Error()

    CheckDict(ConfData)


def GetConf(Parameter, *Paths):
    for Path in Paths:
        ConfData = toml.load(Path)
    
        if Parameter in ConfData:
            return (ConfData[Parameter])
        
        for Key, Value in ConfData.items():
            if (isinstance(Value, dict)):
                if (Parameter in Value):
                    return Value[Parameter]
    
    return None


def UpdateConf(Path, Parameter, Value, Append = False):
    ConfData = toml.load(Path)

    Section = None
    for Table, Data in ConfData.items():
        if (isinstance(Data, dict) and Parameter in Data):
            Section = Table
            break
    
    if (Section == None):
        TargetData = ConfData
    
    else:
        TargetData = ConfData[Section]

    if (not Append):
        TargetData[Parameter] = Value
    
    else:
        if (Parameter not in TargetData):
            TargetData[Parameter] = []
        
        if (Value not in TargetData[Parameter]):
            TargetData[Parameter].append(Value)

    if (Section == None):
        ConfData = TargetData
    
    else:
        ConfData[Section] = TargetData

    with open(Path, 'w', encoding='utf-8') as File:
        toml.dump(ConfData, File)
    
    TextOutput = Parse(String = ConfLog["ValueSet"], VarCall = f"{Parameter} to {Value}")
    LogWrite(TextOutput)
    Speak(TextOutput)


def Error():
    global Start
    if (Conf["SafeMode"] == 1):
            Start = False


def Speak(Text):
    if (Conf["SilentMode"] != 1):
        print(Text)


def Parse(String = None, Path = ConfPath, 
          NextNum = None, 
          NextChar = None,
          Parent = None,
          OrgFile = None,
          VarCall = None):
    
    def Replacer(Match):
        Content = Match.group(1)

        if (Content == None or Content == ""):
            if (VarCall != None):
                return str(VarCall)
            else:
                return ""
        
        Value = GetConf(Content, Path)
        if (Value != None):
            return Value
            
    
    Now = datetime.datetime.now()
    if (OrgFile != None):
        OrgFileName, OrgFileType = os.path.splitext(OrgFile)
    else:
        OrgFileName = None
        OrgFileType = None

    VarValues = {
        ConfVars["NextNum"]: NextNum,
        ConfVars["NextChar"]: NextChar,
        ConfVars["Parent"]: Parent,
        ConfVars["OrgFileName"]: OrgFileName,
        ConfVars["OrgFileType"]: OrgFileType,
        ConfVars["Year"]: str(Now.year),
        ConfVars["Month"]: str(Now.month),
        ConfVars["Day"]: str(Now.day),
        ConfVars["Hour"]: str(Now.hour),
        ConfVars["Minute"]: str(Now.minute),
        ConfVars["Second"]: str(Now.second),
        ConfVars["VarCall"]: VarCall
    }

    for Key, Value in VarValues.items():
        if Key in String and Value is not None:
            String = String.replace(Key, Value)

    VarCall0 = re.escape(ConfVars["VarCall"][0])
    VarCall1 = re.escape(ConfVars["VarCall"][1])

    Pattern = f"{VarCall0}(.*?){VarCall1}"

    String = re.sub(Pattern, Replacer, String)
    return String


def Clone(Source, Destination, NewName, Delete = False):
    Dir(Destination, Output = False, CopyConf = False)
    shutil.copy2(Source, Destination)

    BaseName = os.path.basename(Source)
    shutil.move(os.path.join(Destination, BaseName), os.path.join(Destination, NewName))

    if (Delete):
        os.remove(Source)


def Dir(Path, Output = True, CopyConf = True):
    ParentName = os.path.basename(Path)
    os.makedirs(Path, exist_ok=True)
    
    if (CopyConf):
        Clone("DirConfig.toml", Path, f"{Parse(String = ConfNames["DirConfName"], Path = ConfPath, Parent = ParentName)}.toml")  
        
        UpdateConf(f"{Path}/{Parse(String = ConfNames["DirConfName"], Path = ConfPath, Parent = ParentName)}.toml", "ParentDir", ParentName)
        UpdateConf(f"{Path}/{Parse(String = ConfNames["DirConfName"], Path = ConfPath, Parent = ParentName)}.toml", "Title", f"{ParentName} Config")

    if (Output):
        ParsedPath = Parse(String = Path)
        ParsedOutputs = [Parse(String = Dir) for Dir in ConfDirs["OutputDir"]]
        if (ParsedPath not in ParsedOutputs):
            UpdateConf(ConfPath, "OutputDir", Path, True)


def LogWrite(Text):
    if (ConfDirs["LogDir"] != None and ConfNames != "Unset"):
        if (ConfNames["LogFileName"] != None and ConfNames["LogFileName"] != "Unset"):
            Dir(Parse(String = ConfDirs["LogDir"], Path = ConfPath), Output = False, CopyConf = False)
            LogFile = f"{Parse(String = ConfDirs["LogDir"], Path = ConfPath)}/{Parse(String = ConfNames["LogFileName"], Path = ConfPath)}.log"
            with open(LogFile, "a", encoding="utf-8", buffering=1) as File:
                File.write(f"{Parse(String = ConfLog["All"], Path = ConfPath)}{Text}\n")


def DecideNewPath(FilePath):
    UnsortedFile = os.path.basename(FilePath)

    for Output in ConfDirs["OutputDir"]:
        Output = Parse(String = Output, Path = ConfPath)
        
        ParentName = os.path.basename(Output)

        DirConfName = Parse(String = ConfNames["DirConfName"], Path = ConfPath, Parent = ParentName)
        DirConfPath = f"{Output}/{DirConfName}.toml"

        if not os.path.exists(DirConfPath):
            continue

        FileConf = GetConf("Files", DirConfPath)

        if not FileConf:
            continue

        for File in FileConf:
            Pattern = File["Pattern"]

            TextOutput = Parse(ConfLog["MatchPattern"], VarCall = f"{UnsortedFile} against {Pattern}")
            LogWrite(TextOutput)
            Speak(TextOutput)

            if fnmatch.fnmatch(UnsortedFile, Pattern):
                NewFileName = File["NewFileName"]
                NewFileName = Parse(String = NewFileName, Path = DirConfPath, OrgFile = UnsortedFile)
                return f"{Output}/{NewFileName}"


def Sort(FilePath):
    NewPath = DecideNewPath(FilePath)

    if (NewPath == None):
        Dir(Parse(String =  ConfDirs["FailedDir"]), Output = False, CopyConf = False)
        NewName = os.path.basename(FilePath)
        Clone(FilePath, Parse(String =  ConfDirs["FailedDir"]), NewName, True)

        TextOutput = Parse(String = ConfLog["NotSorted"], VarCall = FilePath)
        LogWrite(TextOutput)
        Speak(TextOutput)
        return

    NewDirPath = os.path.dirname(NewPath)    

    NextNum = GetConf("NextNum", f"{NewDirPath}/{Parse(String = ConfNames["DirConfName"], Parent = os.path.basename(NewDirPath))}.toml")
    NextChar = GetConf("NextChar", f"{NewDirPath}/{Parse(String = ConfNames["DirConfName"], Parent = os.path.basename(NewDirPath))}.toml")

    NewName = Parse(os.path.basename(FilePath), NextNum = NextNum, NextChar = NextChar)

    try:
        Clone(FilePath, NewDirPath, NewName, True)
        
        TextOutput = Parse(String = ConfLog["Sorted"], VarCall = f"{FilePath} to {NewDirPath}/{NewName}")
        LogWrite(TextOutput)
        Speak(TextOutput)


    except Exception:
        Dir(Parse(String =  ConfDirs["FailedDir"]), Output = False, CopyConf = False)
        NewName = os.path.basename(FilePath)
        Clone(FilePath, Parse(String =  ConfDirs["FailedDir"]), NewName, True)

        TextOutput = Parse(String = ConfLog["NotSorted"], VarCall = FilePath)
        LogWrite(TextOutput)
        Speak(TextOutput)
        return


def Init():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog
    
    LoadGlobalConf()
    if (Conf != None):
        CheckConf()
        
        if (Start):
            TextOutput = Parse(String = ConfLog["Start"], Path = ConfPath)
            LogWrite(TextOutput)
            Speak(TextOutput)

            Main()
        
        else:
            TextOutput = Parse(String = ConfLog["NotStart"])
            LogWrite(TextOutput)
            Speak(TextOutput)
    
    else:
        print("NO CONFIG FOUND! Make sure the 'Config.toml' is in the same directory as 'SaraSortd.py'")


def Main():
    for Output in ConfDirs["OutputDir"]:
        Output = Parse(String = Output)
        Dir(Output)

    while True:
        for Input in ConfDirs["InputDir"]:
            InputPath = Parse(Input)
            
            if not os.path.exists(InputPath):
                continue

            for FileName in os.listdir(InputPath):
                FilePath = os.path.join(InputPath, FileName)

                if os.path.isfile(FilePath):
                        FileName = os.path.basename(FilePath)
                        if (FileName.startswith(".") and Conf["DotFiles"] == 0):
                            continue
                        Sort(FilePath)
                    
        time.sleep(Conf.get("CheckInput", 10))


Init()