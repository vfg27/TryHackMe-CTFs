# TryHackMe Advent of Cyber - Day 4: I’m all atomic inside!

As SOC-mas approached, Glitch, a skilled security engineer in Wareville, began strengthening the town's defenses. His proactive actions raised alarms within the SOC team, leading to the use of the Atomic Red Team framework for investigation.

---

## Learning Objectives
1. **Identify malicious techniques** using the MITRE ATT&CK framework.
2. **Simulate attacks** using Atomic Red Team tests.
3. **Create detection rules** from simulated attack artefacts.

---

## Detection Gaps and Kill Chain Strategy
### Challenges in Detection:
1. Threat actors continuously adapt, creating new techniques.
2. The overlap between anomalous and legitimate behavior complicates rule creation.

### Unified Cyber Kill Chain:
- Aim to **detect and mitigate threats** throughout the chain, ensuring gaps in one phase are covered later.

---

## MITRE ATT&CK Framework
- A **comprehensive collection** of tactics, techniques, and procedures (TTPs) used by threat actors.
- Provides theoretical insights into attack methods.

---

## Atomic Red Team Framework
- A library of red team test cases mapped to the MITRE ATT&CK framework.
- Tests can be executed manually or automatically to detect gaps.

---

## Emulating and Detecting T1566.001 (Spearphishing Attachment)

### Steps:
1. **Test Simulation**:
   - Command: `Invoke-AtomicTest T1566.001 -TestNumbers 1`
   - Simulates downloading a malicious macro-enabled attachment.
   - Logs artefacts: PowerShell commands, file creation.

2. **Analyze Logs**:
   - Use Sysmon event logs to identify indicators of compromise (IOCs):
     - PowerShell command: `Invoke-WebRequest`
     - File creation: `PhishingAttachment.xlsm`.

3. **Cleanup**:
   - Remove artefacts with: `Invoke-AtomicTest T1566.001 -TestNumbers 1 -Cleanup`.

---

## Questions and Answers

1. **What was the flag found in the .txt file that is found in the same directory as the PhishingAttachment.xlsm artefact?**  
   > `THM{GlitchTestingForSpearphishing}`

2. **What ATT&CK technique ID would be our point of interest?**  
   > `T1059`

3. **What ATT&CK subtechnique ID focuses on the Windows Command Shell?**  
   > `T1059.003`

4. **What is the name of the Atomic Test to be simulated?**  
   > `Simulate BlackByte Ransomware Print Bombing`

5. **What is the name of the file used in the test?**  
   > `Wareville_Ransomware.txt`

6. **What is the flag found from this Atomic Test?**  
   > `THM{R2xpdGNoIGlzIG5vdCB0aGUgZW5lbXk=}`
