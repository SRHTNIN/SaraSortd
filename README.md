# SaraSortd
A python daemon that can automatically sort your files to your liking without using AI.

It's made by Sarah, hence the name. :3

## Dependencies
toml: Use ```pip install toml``` to install toml.

## Config explanation

### SaraSortd Config (Config.toml)

```
Title = "SaraSortd Config" # NOTE: Do not change the title.

SafeMode = 1 # If SaraSortd should stop if an error with the config appears. 1 is stop, 0 is continue.
SilentMode = 0 # If SaraSortd should write stuff to the terminal as well.

CheckInput = 10 # How many seconds it takes for SaraSortd to check input directories for new files to sort.

[Variables] # Only use these in config files, not the actual file names themselves.
NextNum = "*" # The next available number. If 1 already exists, 2 will be used. Starts at 1.
NextChar = "&" # The next available character. If A already exists, B will be used.

Parent = "@" # The name of the parent directory.

OrgFileName = "\~" # The original name of the sorted file. If "blahblah.txt" gets sorted, "~" would be equal to "blahblah".
OrgFileType = "^" # The original file type of the sorted file. If "example.png" gets sorted, "^" would be equal to ".png".

Year = "[y]" # The current year, E.G. "2026".
Month = "[m]" # The date of the current month, E.G. "03".
Day = "[d]" # The date of the current day, E.G. "27".

Hour = "[h]" # The current hour, E.G. "12".
Minute = "[n]" # The current minute, E.G. "44".
Second = "[s]" # The current second, E.G. "11".

VarCall  = "%%" # The characters used at the start and end of variable calls. The first character is to the left; second is to the right. NOTE: If any parameters in the config uses just "%%", it gets a variable from the program itself, not from the config.

[DirectoryPaths]
RootDir = "/home/sarah/TESTDIR" # Parent directory. Directory where all SaraSortd directories live.
InputDir = ["%RootDir%"] # If files get put here, they'll be sorted.
OutputDir = ["%RootDir%/Output"] # Where sortted files go.
LogDir = "%RootDir%/.Logs" # Where log files from SaraSortd go.
FailedDir ="%RootDir%/.Failed" # For files that failed to be sorted.

[Names]
LogFileName = "[y].[m].[d]._*" # Name of log files.
DirConfName = ".@Config" # Name of config files for directories.

[Log]
All = "[h]:[n]:[s] | " # What to put at the start of all lines in Log file.

Start = "Started: SaraSortd" # When SaraSortd starts.
NotStart = "Error: Failed to start SaraSortd." # When SaraSortd fails to start for some reason.

Sorted = "Sorted: %% to %%." # When a file gets sorted.
ValueSet = "Set: %% to be %% in %%." # When a value in a config is set.

WrongType = "Error: %% is not a %%." # When a parameter in the config is of the wrong type. E.G. setting a text parameter to be a list.
Unset = "Error: %% is not set." # When a parameter in the config is not set. %% is the parameter that wasn't set.
```

### Directory Config (DirConfig.toml)

```
Title = "Unset" # NOTE: Do not change the title.

Files = [
    {Pattern = "?", NewFileName = "~^", NextNum = 1, NextChar = "A"},
]
# Pattern: the pattern used to sort files here. * is a wildcard, ? is a one-character wildcard.
# E.G: if Pattern is "*.png", all files ending with .png will end up here.

# NewFileName: the pattern for the new names of the files that get sorted here.

# NextNum and Nextchar: used to keep track of the next
# available number and character for file names.

LastFile = "Unset" # The last modified file in the directory.
ParentDir = "Unset" # The name of the parent directory.
```