# TryHackMe Advent of Cyber - Day 14: Even if we're horribly mismanaged, there'll be no sad faces on SOC-mas! 

In the town of Wareville, McSkidy assigns Glitch to secure the GiftScheduler, a crucial service for scheduling Christmas presents. However, Mayor Malware devises a sinister plan to exploit vulnerabilities in the system, redirect presents, and blame Glitch for the sabotage. This scenario sets the stage for learning key cybersecurity concepts and techniques.

---

## Learning Objectives
This task teaches:
- **Self-Signed Certificates**: Understanding their risks and use cases.
- **Man-in-the-Middle (MitM) Attacks**: How adversaries intercept and manipulate traffic.
- **Using Burp Suite**: Leveraging it to intercept and analyze network traffic.

---

## Key Concepts

### Certificates and Secure Communication
1. **Certificate Components**:
   - **Public Key**: Used for encrypting data.
   - **Private Key**: Decrypts the data.
   - **Metadata**: Contains details like the issuing Certificate Authority (CA), validity, and hashing algorithm.

2. **Certificate Authority (CA)**:
   - Trusted third-party that validates certificates.
   - Ensures secure connections via a handshake, verification, key exchange, and decryption.

3. **Self-Signed vs. Trusted CA Certificates**:
   - Self-signed certificates are less trusted and vulnerable to MitM attacks.
   - Trusted CA certificates are verified by a third party and ensure integrity.

---

## Attack Details

### Preparation
1. **Add Host Entry**:
   - Prevent DNS logs by locally resolving `gift-scheduler.thm`:
     ```bash
     echo "10.10.157.204 gift-scheduler.thm" >> /etc/hosts
     ```
   - Verify the entry with:
     ```bash
     cat /etc/hosts
     ```

2. **Access the Target**:
   - Navigate to `https://gift-scheduler.thm` and accept the self-signed certificate risk.
   - Login using **Mayor Malware's credentials**:
     - **Username**: `mayor_malware`
     - **Password**: `G4rbag3Day`

---

### Exploiting Vulnerabilities
1. **Start Burp Suite**:
   - Launch Burp Suite and configure it:
     - Toggle off `Intercept` to avoid delays.
     - Add a proxy listener on port `8080` and bind it to the AttackBox's IP.

2. **Setup Traffic Redirection**:
   - Divert Wareville's traffic to the AttackBox:
     ```bash
     echo "CONNECTION_IP wareville-gw" >> /etc/hosts
     ```
   - Simulate user traffic with:
     ```bash
     ./route-elf-traffic.sh
     ```

3. **Intercept Traffic**:
   - Use Burp Suite's HTTP History to monitor incoming requests.
   - Extract credentials from POST requests to compromise privileged accounts.

---

## Outcome
Mayor Malware successfully intercepted traffic, exploiting the system's reliance on self-signed certificates and user negligence. By using Burp Suite as a MitM tool, he obtained sensitive credentials and disrupted the GiftScheduler.

## Questions

1. What is the name of the CA that has signed the Gift Scheduler certificate?
    >THM
2. Look inside the POST requests in the HTTP history. What is the password for the snowballelf account?
    >c4rrotn0s3
3. Use the credentials for any of the elves to authenticate to the Gift Scheduler website. What is the flag shown on the elves’ scheduling page?
    >THM{AoC-3lf0nth3Sh3lf}
4. What is the password for Marta May Ware’s account?
    >H0llyJ0llySOCMAS!

Mayor Malware finally succeeded in his evil intent: with Marta May Ware’s username and password, he can finally access the administrative console for the Gift Scheduler. G-Day is cancelled!

5. What is the flag shown on the admin page?
    >THM{AoC-h0wt0ru1nG1ftD4y}