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

SilentMode = 0 # If SaraSortd should write things it does, to the terminal.

CheckInput = 3 # How many seconds it takes for SaraSortd to check input directories for new files to sort.

DotFiles = 0 # If SaraSortd should sort files that begin with ".". This is mainly for linux users, since hidden files always have "." in front of them.

Logging = 1 # If SaraSortd's logging system should be active. If this is 0, nothing will be logged into files.

OverwriteDirConf = 0 # If SaraSortd should overwrite directory configs with DirConfig.toml. 0 is no, 1 is yes.

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
RootDir = "Unset" # A variable directory. This doesn't NEED to exist for the program to work. It's more of a shorthand for other paths to use! You could add more of these. E.G: Add ImageDir = "%RootDir%/Images", then you could set OutputDir to be "%ImageDir%".

InputDir = ["%RootDir%"] # If files get put here, they'll be sorted. This is a list, so you can add multiple. E.G: ["%RootDir%", "%RootDir%/input"]

OutputDir = ["%RootDir%/Output"] # Where sorted files go. This is a list, so you can add multiple. E.G: ["%RootDir%/Output", "%RootDir%/Output2"]. The output directories have separate config files.

LogDir = "%RootDir%/.Logs" # Where log files from SaraSortd go.

FailedDir ="%RootDir%/.Failed" # For files that failed to be sorted.

[Names]
LogFileName = "[y].[m].[d]._*" # Name for log files.

DirConfName = ".@Config" # Name for config files for directories.

[Log]
All = "[h]:[n]:[s] | " # What to put at the start of all lines in Log file.

Start = "Started: SaraSortd" # When SaraSortd starts.

NotStart = "Error: Failed to start SaraSortd." # When SaraSortd fails to start for some reason.

Stop = "\nStopped SaraSortd." # When SaraSortd stops for whatever reason. Usually when you interrupt it in the terminal you ran it in.

MatchPattern = "Checking %%." # When a file that's trying to be sorted gets checked against a pattern.
# %% here is the file against the pattern. E.G: "picture.png against *.jpg"

Sorted = "Sorted: %%." # When a file gets sorted and where.
# %% here is the oldfile to the newfile, E.G: "picture.png to SortedPicture.png".

NotSorted = "Error: Failed to sort %%. No valid output directory." # When a file from an input directory fails to be sorted to an output directory.
# %% here is the path of the file. E.G: "/home/janedoe/picture.png".

ValueSet = "Set: %%." # When a value in a config is set.
# %% here is the parameter and what it got set to. E.G: "Title to TestDir Config File".

Unset = "Error: %% is not set." # When a value isn't set.
# %% here is just the parameter who's value was either "Unset" or None. E.G: "RootDir".
```

### Output Directory Config (DirConfig.toml)

The output directory config references the SaraSortd config (Config.toml). This means that you can, for example, use the character assigned to "NextNum" in Config.toml in this config (DirConfig.toml). This applies to all Variables in the SaraSortd config (Config.toml).

```
Title = "Unset" # The title of the config. This currently does nothing for SaraSortd, so it can be anything. It gets automatically updated when DirConfig.toml gets copied to an output directory.

LastFile = "Unset" # The last file that was sorted to this directory. It gets automatically updated whenever a file gets sorted to this directory.

ParentDir = "Unset" # The name of this directory. It gets automatically updated when DirConfig.toml gets copied to an output directory.

[[Files]] # The double brackets means that you can add multiple types of files to be sorted here. Just copy [[Files]] and all the parameters under it, and paste it under or over this section, then you may change the values of the new parameters. E.G:

# [[Files]]
# Pattern = "*.png"
# NewFileName = "GoodImage^"
# NextNum = 1
# NextChar = "A"
# CaseSensitive = 0
# [[Files]]
# Pattern = "*.jpg"
# NewFileName = "BetterImage^"
# NextNum = 1
# NextChar = "A"
# CaseSensitive = 0

# Will sort .png files to this directory and rename them to "GoodImage.png", but also sort .jpg files into this directory yet rename those to "BetterImage.jpg".

Pattern = "*" # A pattern used to sort files to this directory. * is a wildcard; ? is a one-character wildcard. E.G: if Pattern is "*.png", all files ending with .png will end up here.

NewFileName = "~^" # A pattern for the new names of the files that get sorted to this directory from matching this "Pattern".

NextNum = 1 # Used to keep track of the next available number for file names. It gets automatically incremented when NextNum is used in NewFileName, and a file gets sorted to this directory and renamed.

NextChar = "A" # Used to keep track of the next available letter for file names. It gets automatically incremented (E.G: A into B) when NextChar is used in NewFileName, and a file gets sorted to this directory and renamed.

CaseSensitive = 0 # Whether this "Pattern" is case-sensitive or not. 1 is yes, 0 is no. E.G: if CaseSensitive = 1 and this "Pattern" is "*.PNG", a file named "picture.png" won't get sorted to this directory. if CaseSensitive = 0 and this "Pattern" is "*.PNG", a file named "picture.png" *will* get sorted to this directory. 
```
