# TryHackMe Advent of Cyber - Day 6: If I can't find a nice malware to use, I'm not going.

Mayor Malware slammed his hand on the table, his eyes narrowing as the report flashed on his screen. Glitch and McSkidy had uncovered his trail. But he remained confident, relying on his advanced malware to evade detection.

## Learning Objectives

1. Analyze malware behavior using sandbox tools.
2. Explore how to use YARA rules to detect malicious patterns.
3. Learn about various malware evasion techniques.
4. Implement an evasion technique to bypass YARA rule detection.

---

## Detecting Sandboxes

A sandbox is an isolated environment for analyzing code without affecting the outside system. Mayor Malware devised a method to detect sandboxes by checking the `C:\Program Files` directory in the Windows Registry:

```c
void registryCheck() {
    const char *registryPath = "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion";
    const char *valueName = "ProgramFilesDir";
    
    char command[512];
    snprintf(command, sizeof(command), "reg query \"%s\" /v %s", registryPath, valueName);
    
    int result = system(command);
    if (result == 0) {
        printf("Registry query executed successfully.\n");
    } else {
        fprintf(stderr, "Failed to execute registry query.\n");
    }
}
```

---

## Can YARA Do It?

**YARA** is a tool for identifying malware using pattern-based rules. Mayor Malware tested his creation against this rule:

```yara
rule SANDBOXDETECTED {
    meta:
        description = "Detects the sandbox by querying the registry key for Program Path"
        author = "TryHackMe"
        date = "2024-10-08"
        version = "1.1"

    strings:
        $cmd= "Software\\Microsoft\\Windows\\CurrentVersion\" /v ProgramFilesDir nocase

    condition:
        $cmd
}
```

Mayor Malware wrote a script to monitor system events and log any matches to `C:\Tools\YaraMatches.txt`.

---

## Adding More Evasion Techniques

Mayor Malware added obfuscation using Base64 encoding to hide registry queries:

```c
void registryCheck() {
    const char *encodedCommand = "RwBlAHQALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQAgAC0AUABhAHQAaAAgACIASABLAEwATQA6AFwAUwBvAGYAdAB3AGEAcgBlAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzAFwAQwB1AHIAcgBlAG4AdABWAGUAcgBzAGkAbwBuACIAIAAtAE4AYQBtAGUAIABQAHIAbwBnAHIAYQBtAEYAaQBsAGUAcwBEAGkAcgA=";
    char command[512];
    snprintf(command, sizeof(command), "powershell -EncodedCommand %s", encodedCommand);
    int result = system(command);
    if (result == 0) {
        printf("Registry query executed successfully.\n");
    } else {
        fprintf(stderr, "Failed to execute registry query.\n");
    }  
}
```

---

## Beware of FLOSS

**FLOSS**, a tool developed by Mandiant, can extract obfuscated strings from binaries. Mayor Malware tested it using:

```powershell
PS C:\Tools\FLOSS> floss.exe C:\Tools\Malware\MerryChristmas.exe |Out-file C:\tools\malstrings.txt
```

---

## Using YARA Rules on Sysmon Logs

Mayor Malware discovered that YARA rules could also monitor Sysmon logs for malware artifacts. He used the following XML filter:

```xml
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-Sysmon/Operational">
    <Select Path="Microsoft-Windows-Sysmon/Operational">
      *[System[(EventRecordID="INSERT_EVENT_RECORD_ID_HERE")]]
    </Select>
  </Query>
</QueryList>
```

---

## Questions

1. What is the flag displayed in the popup window after the EDR detects the malware?
    >THM{GlitchWasHere}
2. What is the flag found in the malstrings.txt document after running floss.exe, and opening the file in a text editor?
    >THM{HiddenClue}
