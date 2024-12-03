# TryHackMe Advent - Day 3: Even if I wanted to go, their vulnerabilities wouldn't allow it.

In this task, we will explore how the SOC team uncovered what happened (**Operation Blue**) and how the attacker exploited vulnerabilities (**Operation Red**). Let's dive in!

---

## Learning Objectives
- Understand **log analysis** using tools like ELK.  
- Learn how to investigate with **Kibana Query Language (KQL)**.  
- Discover **Remote Code Execution (RCE)** via insecure file uploads.  

---

## Operation Blue: Investigating Attacks with ELK

### Why ELK?
Log analysis helps SOC teams investigate incidents efficiently. The ELK stack (**Elasticsearch**, **Logstash**, and **Kibana**) centralizes log management, simplifying detection and investigation.

### Steps in Kibana
1. Access **Kibana** at `http://10.10.213.132:5601`.
2. Go to **Discover** under **Analytics** and select the `wareville-rails` index.
3. Adjust the time range to **October 1, 2024, 00:00 to 23:30**.

#### UI Essentials
- **Search Bar**: Query logs with **KQL**.  
- **Timeline**: Event frequency visualization.  
- **Documents**: Log entry details.  

---

## Operation Red: Exploiting Vulnerabilities

### Overview
The Glitch exploited an **insecure file upload** vulnerability to perform **Remote Code Execution (RCE)** on the website.

---

### Steps to Identify and Exploit the Vulnerability

1. **Insecure File Upload**  
   - The website allowed users to upload files without proper validation.  
   - Attackers uploaded a malicious file, e.g., `backdoor.php`, disguised as an image.

2. **Inspecting the Upload Feature**  
   - Check the file upload field for restrictions.  
   - If no validation is enforced, attempt to upload a PHP payload.  

3. **Executing RCE**  
   - Once uploaded, access the malicious file via the server's URL (e.g., `http://<server>/uploads/backdoor.php`).  
   - Use this backdoor to execute arbitrary commands.

---

### Mitigation Techniques
- **File Type Validation**: Only allow specific, safe file extensions.  
- **Content Scanning**: Check files for malicious content before processing.  
- **Restrict Execution**: Store uploaded files outside web-accessible directories.  

This completes the investigation into how the attacker compromised the site and what security measures could prevent such incidents.

## Steps to Solve the Challenge

1. **BLUE Questions**: These questions are answered directly by analyzing the dashboard. 

2. **RED Question**: To analyze how the attacker inserted the backdoor:
   - Access the admin panel at `http://frostypines.thm/admin/`.
   - Add a new fake room where the image file is the malicious file.
   - Navigate to `http://frostypines.thm/media/images/rooms/shell.php` to trigger the backdoor.

3. Using the backdoor:
   - Establish a reverse shell to gain terminal access.
   - Stabilize the shell session.
   - Execute the following command to locate the flag:
     ```bash
     find / -name 'flag.txt'
     ```
   - Once the flag file is found, print its contents to retrieve the flag.
## Questions

1. BLUE: Where was the web shell uploaded to?
    >/media/images/rooms/shell.php
2. BLUE: What IP address accessed the web shell?
    >10.11.83.34
3. RED: What is the contents of the flag.txt?
    >THM{Gl1tch_Was_H3r3}