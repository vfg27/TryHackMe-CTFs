# TryHackMe Advent - Day 2: One man's false positive is another man's potpourri.

### Introduction
The Wareville Security Operations Center (SOC) faces its busiest time of year, processing a deluge of alerts from noisy rules deployed to secure the town. However, analysts are overwhelmed, leading to potential misclassifications of alerts as True Positives (TP) or False Positives (FP). The challenge is to investigate whether the town’s mayor, known as "Mayor Malware," is behind the chaos.

---

### Key Concepts in SOC Alert Analysis

1. **True Positives (TP) vs. False Positives (FP):**
   - **TP:** Alerts from actual malicious activities.
   - **FP:** Alerts triggered by benign activities or misconfigurations.

2. **Decision-Making Challenges:**
   - Misclassifying TPs as FPs could result in missed attacks.
   - Misclassifying FPs as TPs wastes resources and focus.

3. **SOC Superpower: User Confirmation**
   - SOC analysts can contact users directly or review Change Requests to confirm the legitimacy of activities.

4. **Challenges to Contextual Analysis:**
   - Lack of a formal Change Request process.
   - Malicious activities disguised as legitimate actions.
   - Activities by insider threats or via social engineering.

5. **Correlation for Timeline Reconstruction:**
   - Analysts gather and correlate artefacts (e.g., IP addresses, usernames, file paths) to create a comprehensive timeline of events.

---

### The Case

#### Connection Details:
- Used the Elastic SIEM interface to investigate suspicious activity reported by the Mayor's office.

#### Investigation Steps:
1. **Event Discovery:**
   - Timeframe: Dec 1, 2024, 0900–0930.
   - Observed 21 events, including repeated encoded PowerShell commands on multiple machines.

2. **Analysis of Patterns:**
   - Authentication events preceded PowerShell commands.
   - Suspicious usage of a generic admin account (service_admin), which was confirmed to have been used during administrators' absence.

3. **Source Identification:**
   - Events correlated to a single source IP address (10.0.11.11).
   - Investigation revealed a brute-force attack leading to successful authentication and PowerShell execution.

4. **Historical Context:**
   - Expanded analysis (Nov 29–Dec 1) revealed failed login attempts from a different IP (ending in .255.1), causing a spike in authentication events.

5. **Encoded Command Decoding:**
   - Decoded PowerShell command revealed benign activity: `Install-WindowsUpdate -AcceptAll -AutoReboot`.

---

### Findings

1. **True Positive Identification:**
   - Brute-force attack succeeded, leading to encoded PowerShell commands being executed.
   - However, subsequent investigation revealed the attacker updated outdated credentials in the system scripts—a potentially helpful action.

---

### Conclusion

The investigation highlights the criticality of thorough SOC analysis:
- Differentiating between TPs and FPs is crucial to avoid missteps in incident response.
- Context, correlation, and decoding reveal the true nature of incidents.
- Wareville's SOC team, assisted by McSkidy, must determine whether the Mayor or another entity is the real saboteur.

### Next Steps
- Strengthen detection rules to prevent brute-force attacks.
- Enhance user authentication mechanisms.

## Questions

1. What is the name of the account causing all the failed login attempts?

    > service_admin

2. How many failed logon attempts were observed?

    > 6791

3. What is the IP address of Glitch?

    > 10.0.255.1

4. When did Glitch successfully logon to ADM-01? Format: MMM D, YYYY HH:MM:SS.SSS

    > Dec 1, 2024 08:54:39.000

5. What is the decoded command executed by Glitch to fix the systems of Wareville?

    > Install-WindowsUpdate -AcceptAll -AutoReboot