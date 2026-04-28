# SaraSortd
(Version = "5.1")

A python daemon that can automatically sort your files to your liking without using AI.

It's made by Sarah, hence the name. :3

## Usage

SaraSortd is for people who don't want to manually sort files, people who want to organise files, and people who want an automatic naming standard for their files.

Example use-cases:

- Sorting log files from multiple programs into one directory.

- Sorting downloaded github repositories to a directory for your IDE.

- Regularly cloning important files into a backup directory.

## Dependencies

python

toml: Use ```pip install toml``` to install toml.

## Versioning

If the first number in the version goes up, it means that old config files will not work with the new SaraSortd.py.

If the second number in the version goes up, something new got added, but your old config files will still work just fine.

## Installation

Here's an [installation video](https://youtu.be/ZMIaOhZA0kE).
Here's a step-by-step tutorial (in case you don't want to watch the video).

1. Install ZIP-file.
2. Unzip ZIP-file wherever you want the program to live.
3. Navigate to the new SaraSortd directory in your terminal.
4. Edit your config files to your liking.
5. Run ```python SaraSortd.py``` to run the program. (This will make new directories for you.)
6. Edit your output directories' configs.

## Config explanation

### SaraSortd Config (GlobalConf.toml)

```
Title = "SaraSortd Config" # NOTE: Do not change the title. This is so that the program knows which config file is which.

Version = "5.1" # Just the version number for the config file.

SafeMode = 1 # If SaraSortd should stop if an error with the config appears. 1 is stop, 0 is continue.

SilentMode = 0 # If SaraSortd should write things it does, to the terminal.

CheckInput = 3 # How many seconds it takes for SaraSortd to check input directories for new files to sort.

DotFiles = 0 # If SaraSortd should sort files that begin with ".". This is mainly for linux users, since hidden files always have "." in front of them.

Logging = 1 # If SaraSortd's logging system should be active. If this is 0, nothing will be logged into files.

OverwriteDirConf = 0 # If SaraSortd should overwrite directory configs with the config templates. 0 is no, 1 is yes.

[Variables] # Only use these in config files, not the actual file names themselves.
NextNum = "*" # The next available number. If 1 already exists, 2 will be used.

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

FileHistoryName = ".@History" # Name for file history files. This keeps track of sorted files if an input and output are the same directory.

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


### Output Directory Config (OutputDirConf.toml)

The output directory config references the SaraSortd config (GlobalConf.toml). This means that you can, for example, use the character assigned to "NextNum" in GlobalConf.toml in this config (OutputDirConf.toml). This applies to all Variables in the SaraSortd config (GlobalConf.toml).

```
Title = "Unset" # NOTE: Do not change the title. This is so that the program knows which config file is which.

Version = "5.1" # The version number of the config.

LastFile = "Unset" # The last file that was sorted to this directory. It gets automatically updated whenever a file gets sorted to this directory.

ParentDir = "Unset" # The name of this directory. It gets automatically updated when this config gets copied to an output directory.

ValidInputDirs = ["*"] # Directories that are valid for sorting. Basically, if a file is from one of these directories, they can be sorted here. * is a wildcard; ? is a one-character wilcard. E.G: if "ValidInputDirs = ["/TestDir/*"]" any file from any directory in "/TestDir" will be allowed to be sorted here.

FileLimit = 0 # The max limit of files a directory can have. If this is 0, then there's no limit.

DeleteOrg = 1 # If SaraSortd should delete the original file or not. If this is 1, then sorted files will be 'moved' to an output directory. If not, they will be 'copied' to an output directory.

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
# Overwrite = 1

# Will sort .png files to this directory and rename them to "GoodImage.png", but also sort .jpg files into this directory yet rename those to "BetterImage.jpg".

Pattern = "*" # A pattern used to sort files to this directory. * is a wildcard; ? is a one-character wildcard. E.G: if Pattern is "*.png", all files ending with .png will end up here.

NewFileName = "~^" # A pattern for the new names of the files that get sorted to this directory from matching this "Pattern".

NextNum = 1 # Used to keep track of the next available number for file names. If you change NextNum to be 01 or 001 instead of 1, it'll still work. 09 => 10. It gets automatically incremented when NextNum is used in NewFileName, and a file gets sorted to this directory and renamed.

NextChar = "A" # Used to keep track of the next available letter for file names. If you change NextChar to be AA or AAA instead of A, it'll still work. AZ => BA. It gets automatically incremented (E.G: A into B or AA into AB then AZ into BA) when NextChar is used in NewFileName, and a file gets sorted to this directory and renamed.

CaseSensitive = 0 # Whether this "Pattern" is case-sensitive or not. 1 is yes, 0 is no. E.G: if CaseSensitive = 1 and this "Pattern" is "*.PNG", a file named "picture.png" won't get sorted to this directory. If CaseSensitive = 0 and this "Pattern" is "*.PNG", a file named "picture.png" *will* get sorted to this directory.

Overwrite = 1 # Whether this specific file type can be overwritten by others of the same type. 0 is no, 1 is yes.
```

### Input Directory Config (InputDirConf.toml)

```
Title = "Unset" # NOTE: Do not change the title. This is so that the program knows which config file is which.

Version = "5.1"

ParentDir = "Unset" # The name of this directory. It gets automatically updated when this config gets copied to an output directory.
```
