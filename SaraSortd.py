import datetime
import fnmatch
import os
import re
import shutil
import time
import toml

# Version = "6.0"

ConfPath = "./GlobalConf.toml"

Conf = None
ConfVars = None
ConfDirs = None
ConfNames = None
ConfLog = None

Start = True


def Clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


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
            return ConfData[Parameter]

        for Key, Value in ConfData.items():
            if isinstance(Value, dict):
                if Parameter in Value:
                    return Value[Parameter]
            elif isinstance(Value, list):
                for Item in Value:
                    if isinstance(Item, dict) and Parameter in Item:
                        return Item[Parameter]

    return None


def UpdateConf(Path, Parameter, Value, Append = False):
    ConfData = toml.load(Path)

    def UpdateInData(Data):
        if isinstance(Data, dict):
            if Parameter in Data:
                if not Append:
                    Data[Parameter] = Value

                else:
                    Data.setdefault(Parameter, [])

                    if Value not in Data[Parameter]:
                        Data[Parameter].append(Value)

                return True
            else:
                for Key, DataValue in Data.items():
                    if UpdateInData(DataValue):
                        return True

        elif isinstance(Data, list):
            for Item in Data:
                if UpdateInData(Item):
                    return True

        return False

    Updated = UpdateInData(ConfData)

    if not Updated:
        if not Append:
            ConfData[Parameter] = Value

        else:
            ConfData.setdefault(Parameter, [])
            if Value not in ConfData[Parameter]:
                ConfData[Parameter].append(Value)

    with open(Path, "w", encoding="utf-8") as File:
        toml.dump(ConfData, File)

    TextOutput = Parse(String = ConfLog["ValueSet"], VarCall = f"{Parameter} to {Value}")
    LogWrite(TextOutput)
    Speak(TextOutput)


def Error():
    global Start
    if Conf["SafeMode"] == 1:
        Start = False


def Speak(Text):
    if Conf["SilentMode"] != 1:
        print(Text)


def Parse(
    String = None,
    Path = ConfPath,
    NextNum = None,
    NextChar = None,
    Parent = None,
    OrgFile = None,
    VarCall = None,
):

    def Replacer(Match):
        Content = Match.group(1)

        if Content is None or Content == "":
            if VarCall is not None:
                return str(VarCall)
            else:
                return ""

        Value = GetConf(Content, Path)
        if Value is not None:
            return Value

    Now = datetime.datetime.now()
    if OrgFile is not None:
        OrgFileName, OrgFileType = os.path.splitext(OrgFile)
    else:
        OrgFileName = None
        OrgFileType = None

    VarValues = {
        ConfVars["NextNum"]: str(NextNum),
        ConfVars["NextChar"]: str(NextChar),
        ConfVars["Parent"]: str(Parent),
        ConfVars["OrgFileName"]: str(OrgFileName),
        ConfVars["OrgFileType"]: str(OrgFileType),
        ConfVars["Year"]: str(Now.year),
        ConfVars["Month"]: str(Now.month).rjust(2, "0"),
        ConfVars["Day"]: str(Now.day).rjust(2, "0"),
        ConfVars["Hour"]: str(Now.hour).rjust(2, "0"),
        ConfVars["Minute"]: str(Now.minute).rjust(2, "0"),
        ConfVars["Second"]: str(Now.second).rjust(2, "0"),
        ConfVars["VarCall"]: str(VarCall),
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
    if (os.path.dirname(Source) == Destination):
        FileHistoryPath = f"{Destination}/{Parse(ConfNames["FileHistoryName"], Parent = os.path.basename(Destination))}.toml"
        print("FileHistoryPath:",FileHistoryPath)

        if not os.path.exists(FileHistoryPath):
            with open(FileHistoryPath, "w", encoding = "utf-8") as HistoryFile:
                toml.dump({"Title": f"{os.path.basename(Destination)} History", "History": []}, HistoryFile)

        HistoryFileData = toml.load(FileHistoryPath)
        if (NewName not in HistoryFileData["History"]):
            HistoryFileData["History"].append(NewName)
            with open(FileHistoryPath, "w", encoding = "utf-8") as HistoryFile:
                toml.dump(HistoryFileData, HistoryFile)

        os.rename(Source, os.path.join(Destination, NewName))
        return

    Dir(Destination, Output = False, CopyConf = False)
    shutil.copy2(Source, Destination)

    BaseName = os.path.basename(Source)
    shutil.move(os.path.join(Destination, BaseName), os.path.join(Destination, NewName))

    if Delete:
        os.remove(Source)


def Dir(Path, Output = True, CopyConf = "OutputDirConf.toml"):
    ParentName = os.path.basename(Path)
    os.makedirs(Path, exist_ok=True)

    if CopyConf:
        if "Out" in CopyConf:
            NewDirConf = f"{Parse(String = ConfNames['OutDirConfName'], Path = ConfPath, Parent = ParentName)}.toml"

            if Conf["OverwriteDirConf"] == 1 or not os.path.exists(os.path.join(f"{Path}/{NewDirConf}")):
                Clone(CopyConf, Path, NewDirConf)
                UpdateConf(
                    f"{Path}/{Parse(String = ConfNames['OutDirConfName'], Path = ConfPath, Parent = ParentName)}.toml",
                    "ParentDir",
                    ParentName,
                )

                UpdateConf(
                    f"{Path}/{Parse(String = ConfNames['OutDirConfName'], Path = ConfPath, Parent = ParentName)}.toml",
                    "Title",
                    f"{ParentName} Config",
                )

        if "In" in CopyConf:
            NewDirConf = f"{Parse(String = ConfNames['InDirConfName'], Path = ConfPath, Parent = ParentName)}.toml"

            if Conf["OverwriteDirConf"] == 1 or not os.path.exists(os.path.join(f"{Path}/{NewDirConf}")):
                Clone(CopyConf, Path, NewDirConf)
                UpdateConf(
                    f"{Path}/{Parse(String = ConfNames['InDirConfName'], Path = ConfPath, Parent = ParentName)}.toml",
                    "ParentDir",
                    ParentName,
                )

                UpdateConf(
                    f"{Path}/{Parse(String = ConfNames['InDirConfName'], Path = ConfPath, Parent = ParentName)}.toml",
                    "Title",
                    f"{ParentName} Config",
                )

    if Output:
        ParsedPath = Parse(String = Path)
        ParsedOutputs = [Parse(String = Dir) for Dir in ConfDirs["OutputDir"]]
        if ParsedPath not in ParsedOutputs:
            UpdateConf(ConfPath, "OutputDir", Path, True)


def LogWrite(Text):
    if GetConf("Logging", ConfPath) == 1:
        if ConfDirs["LogDir"] is not None and ConfNames != "Unset":
            if (
                ConfNames["LogFileName"] is not None
                and ConfNames["LogFileName"] != "Unset"
            ):
                Dir(Parse(String = ConfDirs["LogDir"], Path = ConfPath), Output = False, CopyConf = False)
                LogFile = f"{Parse(String = ConfDirs['LogDir'], Path = ConfPath)}/{Parse(String = ConfNames['LogFileName'], Path = ConfPath)}.log"
                with open(LogFile, "a", encoding = "utf-8", buffering = 1) as File:
                    File.write(f"{Parse(String = ConfLog['All'], Path = ConfPath)}{Text}\n")


def DecideNewPath(FilePath):
    UnsortedFile = os.path.basename(FilePath)

    for Output in ConfDirs["OutputDir"]:
        Output = Parse(String = Output, Path = ConfPath)

        ParentName = os.path.basename(Output)

        OutDirConfName = Parse(String = ConfNames["OutDirConfName"], Path = ConfPath, Parent = ParentName)
        OutDirConfPath = f"{Output}/{OutDirConfName}.toml"

        ValidInputDirs = GetConf("ValidInputDirs", OutDirConfPath)

        for ValidInputDir in ValidInputDirs:
            ValidInputDir = Parse(String = ValidInputDir, Parent = GetConf("ParentDir", OutDirConfPath))

            TextOutput = Parse(String = ConfLog["MatchPattern"], VarCall = f"{os.path.dirname(FilePath)} against {ValidInputDir}")
            LogWrite(TextOutput)
            Speak(TextOutput)

            InputDirValid = fnmatch.fnmatchcase(os.path.dirname(FilePath), ValidInputDir)
            if (InputDirValid):
                break

        if not os.path.exists(OutDirConfPath) or not InputDirValid:
            continue

        OutputFiles = 0

        FileLimitConf = GetConf("FileLimit", OutDirConfPath)

        if FileLimitConf > 0:
            for OutputFile in os.listdir(Output):
                if OutputFile.startswith("."):
                    continue
                if os.path.isfile(os.path.join(Output, OutputFile)):
                    OutputFiles += 1

            if OutputFiles >= FileLimitConf:
                continue

        FileConf = GetConf("Files", OutDirConfPath)

        if not FileConf:
            continue

        for File in FileConf:
            Pattern = File["Pattern"]

            TextOutput = Parse(String = ConfLog["MatchPattern"], VarCall = f"{UnsortedFile} against {Pattern}")
            LogWrite(TextOutput)
            Speak(TextOutput)

            if File["CaseSensitive"] == 1:
                Match = fnmatch.fnmatchcase(UnsortedFile, Pattern)

            else:
                Match = fnmatch.fnmatch(UnsortedFile.lower(), Pattern.lower())

            if Match:
                NewFileName = File["NewFileName"]

                NewFileName = Parse(String = NewFileName, Path = OutDirConfPath, OrgFile = UnsortedFile, NextNum = File["NextNum"], NextChar = File["NextChar"], Parent = ParentName)

                if File["Overwrite"] == 0 and os.path.exists(os.path.join(Output, NewFileName)):
                    continue

                if ConfVars["NextNum"] in File["NewFileName"]:
                    ConfData = toml.load(OutDirConfPath)
                    Width = len(File["NextNum"])
                    NewNum = str((int(File["NextNum"]) + 1)).rjust(Width, "0")
                    print(File["NextNum"],"=>",NewNum)

                    for Item in ConfData.get("Files", []):
                        if Item.get("Pattern") == File["Pattern"]:
                            Item["NextNum"] = NewNum
                            break

                    with open(OutDirConfPath, "w", encoding="utf-8") as ConfFile:
                        toml.dump(ConfData, ConfFile)

                    TextOutput = Parse(String = ConfLog["ValueSet"], VarCall = f"NextNum to {NewNum}")
                    LogWrite(TextOutput)
                    Speak(TextOutput)

                if ConfVars["NextChar"] in File["NewFileName"]:
                    CurrentChar = File["NextChar"]
                    CurrentChar = CurrentChar.upper()
                    Result = list(CurrentChar)

                    Count = len(Result) - 1

                    while Count >= 0:
                        if Result[Count] == "Z":
                            Result[Count] = "A"
                            Count -= 1

                        else:
                            Result[Count] = chr(ord(Result[Count]) + 1)
                            break

                    else:
                        Result.insert(0, "A")

                    NewChar = "".join(Result)

                    ConfData = toml.load(OutDirConfPath)

                    for Item in ConfData.get("Files", []):
                        if Item.get("Pattern") == File["Pattern"]:
                            Item["NextChar"] = NewChar
                            break

                    with open(OutDirConfPath, "w", encoding="utf-8") as ConfFile:
                        toml.dump(ConfData, ConfFile)

                    TextOutput = Parse(String = ConfLog["ValueSet"], VarCall = f"NextChar to {NewChar}")
                    LogWrite(TextOutput)
                    Speak(TextOutput)

                return f"{Output}/{NewFileName}"


def Sort(FilePath):
    NewPath = DecideNewPath(FilePath)

    if NewPath is None:
        Dir(Parse(String = ConfDirs["FailedDir"]), Output = False, CopyConf = False)
        NewName = os.path.basename(FilePath)
        Clone(FilePath, Parse(String = ConfDirs["FailedDir"]), NewName, True)

        TextOutput = Parse(String = ConfLog["NotSorted"], VarCall = FilePath)
        LogWrite(TextOutput)
        Speak(TextOutput)
        return

    NewDirPath = os.path.dirname(NewPath)
    NewName = os.path.basename(NewPath)

    if (GetConf("DeleteOrg", f"{NewDirPath}/{Parse(String = ConfNames['OutDirConfName'], Parent = (os.path.basename(NewDirPath)))}.toml") == 1):
        Delete = True

    else:
        Delete = False

    try:
        Clone(FilePath, NewDirPath, NewName, Delete)
        UpdateConf(f"{NewDirPath}/{Parse(String = ConfNames['OutDirConfName'], Parent = os.path.basename(NewDirPath))}.toml", "LastFile", NewName)

        TextOutput = Parse(String = ConfLog["Sorted"], VarCall = f"{FilePath} to {NewDirPath}/{NewName}")
        LogWrite(TextOutput)
        Speak(TextOutput)

    except Exception:
        Dir(Parse(String = ConfDirs["FailedDir"]), Output = False, CopyConf = False)
        NewName = os.path.basename(NewPath)
        Clone(FilePath, Parse(String = ConfDirs["FailedDir"]), NewName, Delete)

        TextOutput = Parse(String = ConfLog["NotSorted"], VarCall = FilePath)
        LogWrite(TextOutput)
        Speak(TextOutput)
        return


def Init():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog

    LoadGlobalConf()
    if Conf is not None:
        CheckConf()

        if Start:
            for InputDir in ConfDirs["InputDir"]:
                InputDir = Parse(String = InputDir, Path = ConfPath, Parent = os.path.basename(os.path.dirname(InputDir)))
                Dir(InputDir, Output = False, CopyConf = "InputDirConf.toml")

            for Output in ConfDirs["OutputDir"]:
                Output = Parse(String = Output, Parent = os.path.basename(os.path.dirname(Output)))
                Dir(Output)

                OutDirConfPath = f"{Output}/{Parse(String = ConfNames["OutDirConfName"], Parent = os.path.basename(Output))}.toml"
                ConfData = toml.load(OutDirConfPath)

                for Item in ConfData.get("Files", []):
                    Character = re.escape(ConfVars["NextChar"])
                    Matches = re.findall(f"{Character}+", Item["NewFileName"])
                    Width = max((len(Match) for Match in Matches), default=0)

                    if Width > 0:
                        Item["NextChar"] = Item["NextChar"].upper().rjust(Width, "A")

                with open(OutDirConfPath, "w", encoding = "utf-8") as ConfFile:
                    toml.dump(ConfData, ConfFile)

            TextOutput = Parse(String = ConfLog["Start"], Path = ConfPath)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Main()

        else:
            TextOutput = Parse(String = ConfLog["NotStart"])
            LogWrite(TextOutput)
            Speak(TextOutput)

    else:
        print("NO CONFIG FOUND! Make sure the 'GlobalConf.toml' is in the same directory as 'SaraSortd.py'")


def Main():
    try:
        while True:
            for Input in ConfDirs["InputDir"]:
                RecurseDir = False

                InputPath = Parse(Input)

                if not os.path.exists(InputPath):
                    continue

                InputDirConfPath = f"{InputPath}/{Parse(ConfNames["InDirConfName"], Parent = os.path.basename(InputPath))}.toml"
                InputDirConf = toml.load(InputDirConfPath)

                for Output in ConfDirs["OutputDir"]:
                    OutputPath = Parse(Output)

                    if (OutputPath == InputPath):
                        RecurseDir = True
                        FileHistoryPath = f"{InputPath}/{Parse(ConfNames["FileHistoryName"], Parent = os.path.basename(InputPath))}.toml"

                        if not os.path.exists(FileHistoryPath):
                            with open(FileHistoryPath, "w", encoding = "utf-8") as HistoryFile:
                                toml.dump({"Title": f"{os.path.basename(InputPath)} History", "History": [] }, HistoryFile)

                for FileName in os.listdir(InputPath):
                    FilePath = f"{InputPath}/{FileName}"
                    if os.path.isdir(FilePath) and InputDirConf["SortDirs"] == 0:
                        continue

                    FileName = os.path.basename(FilePath)
                    if FileName.startswith(".") and Conf["DotFiles"] == 0:
                        continue

                    for ConfFile in InputDirConf["Files"]:
                        if ConfFile["CaseSensitive"] == 1:
                            Match = fnmatch.fnmatchcase(FileName, Parse(ConfFile["Pattern"], Parent = os.path.basename(InputPath)))

                        else:
                            Match = fnmatch.fnmatchcase(FileName.lower(), (Parse(ConfFile["Pattern"], Parent = os.path.basename(InputPath))).lower())

                        if Match:
                            break

                    if Match:
                        if os.path.isdir(FilePath) and InputDirConf["SortDirs"] == 1:
                            TextOutput = Parse(String = ConfLog["Zipping"], VarCall = FilePath)
                            LogWrite(TextOutput)
                            Speak(TextOutput)

                            shutil.make_archive(FilePath, "zip", FilePath)

                            try:
                                os.rmdir(FilePath)

                            except PermissionError:
                                TextOutput = Parse(String = ConfLog["NoPermission"], VarCall = f"remove directory {InputPath}/{FileName}")
                                LogWrite(TextOutput)
                                Speak(TextOutput)
                                continue

                            FilePath = f"{FilePath}.zip"

                        if RecurseDir:
                            HistoryFile = toml.load(FileHistoryPath)

                            if (Parse(FileName, Parent = os.path.basename(InputPath)) in HistoryFile["History"]):
                                continue

                        Sort(FilePath)

            time.sleep(Conf.get("CheckInput", 10))

    except KeyboardInterrupt:
        TextOutput = GetConf("Stop", ConfPath)
        LogWrite(TextOutput)
        Speak(TextOutput)

Init()
