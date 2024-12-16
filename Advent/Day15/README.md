# TryHackMe Advent of Cyber - Day 15: Be it ever so heinous, there's no place like Domain Controller. 

Ahead of SOC-mas, the SOC team decided to perform a routine security check on one of their Active Directory (AD) domain controllers. To their dismay, they discovered signs of a potential breach. With the situation escalating, the team triggered the panic alarm. There’s only one person who can save the day: you.

---

### Learning Objectives
- Understand the structure and components of Active Directory.
- Explore common Active Directory attacks.
- Investigate a security breach in an Active Directory environment.

---

### Introducing Active Directory

Active Directory (AD) is a foundational Directory Service in most enterprise networks. It stores information about objects like users, computers, and groups. These objects are structured to facilitate easy access and management.

#### Key Components of Active Directory
- **Domains:** Logical groupings of network resources governed by common security policies.
- **Organizational Units (OUs):** Containers that group objects (e.g., users, devices) within a domain for administrative control.
- **Forest:** A collection of one or more domains sharing the same schema and configuration.
- **Trust Relationships:** Enable users in one domain to access resources in another domain.

Example Distinguished Name (DN):
```
DN=CN=Mayor Malware, OU=Management, DC=wareville, DC=thm
```

#### Core AD Components
- **Domain Controllers (DCs):** Servers managing AD authentication and authorizations.
- **Global Catalog (GC):** A searchable database containing a subset of AD information.
- **LDAP:** Protocol for accessing and managing directory data.
- **Kerberos Authentication:** Provides secure authentication using ticketing systems.

---

### Group Policy

Group Policy Objects (GPOs) allow administrators to enforce domain-wide policies, such as password requirements, software deployments, and firewall settings. GPOs can be linked to domains, OUs, or sites for granular control.

**Example: Configuring a Password Policy**
1. Open *Group Policy Management* (`gpmc.msc`).
2. Create a new GPO named "Password Policy".
3. Edit the GPO:
   - Navigate to `Computer Configuration > Policies > Windows Settings > Security Settings > Account Policies > Password Policy`.
   - Configure:
     - Minimum password length: 12 characters.
     - Enforce password history: 10 passwords.
     - Maximum password age: 90 days.
     - Password complexity: Enabled.
4. Link the GPO to the domain or desired OU.

---

### Common Active Directory Attacks

1. **Golden Ticket Attack**
   - Exploits Kerberos by forging a Ticket Granting Ticket (TGT) using the krbtgt account password hash.
   - **Detection:**
     - Event ID 4768: TGT requests for privileged accounts.
     - Event ID 4672: Special privileges assigned to users.

2. **Pass-the-Hash**
   - Uses password hashes to authenticate without knowing plaintext passwords.
   - **Mitigation:**
     - Enforce strong password policies.
     - Conduct regular privilege audits.
     - Implement multi-factor authentication.

3. **Kerberoasting**
   - Requests and extracts service tickets for offline cracking of service account passwords.
   - **Mitigation:**
     - Use strong passwords for service accounts.

4. **Pass-the-Ticket**
   - Steals Kerberos tickets for unauthorized authentication.
   - **Detection:**
     - Event ID 4768: Unusual TGT requests.
     - Event ID 4624: Successful logins from suspicious devices or locations.

5. **Malicious GPOs**
   - Attackers create GPOs to deploy malware, disable security features, or establish persistence.
   - **Mitigation:**
     - Regularly audit GPOs for unauthorized changes.

6. **Skeleton Key Attack**
   - Installs malware allowing attackers to bypass account passwords using a master key.

---

### Investigating the Breach

#### Reviewing Group Policy Objects
Use PowerShell to audit GPOs:

1. List all GPOs:
   ```powershell
   Get-GPO -All
   ```

2. Export a GPO for analysis:
   ```powershell
   Get-GPOReport -Name "SetWallpaper" -ReportType HTML -Path ".\SetWallpaper.html"
   ```
   Open the exported file in a browser to review configurations, permissions, and applied devices.

3. Identify recently modified GPOs:
   ```powershell
   Get-GPO -All | Where-Object { $_.ModificationTime } | Select-Object DisplayName, ModificationTime
   ```

#### Using Event Viewer

The Windows Event Viewer logs system activity. Key Event IDs to monitor:

| **Event ID** | **Description**                              |
|--------------|----------------------------------------------|
| 4624         | User account login                          |
| 4625         | Failed login attempt                        |
| 4672         | Special privileges assigned                 |
| 4768         | TGT request for a privileged account        |

Example:
- Review login history under the *Security* tab.

#### Auditing User Accounts

1. Check for locked accounts:
   ```powershell
   Search-ADAccount -LockedOut | Select-Object Name, SamAccountName, LockedOut, LastLogonDate, DistinguishedName
   ```

2. List all users and their group memberships:
   ```powershell
   Get-ADUser -Filter * -Properties MemberOf | Select-Object Name, SamAccountName, @{Name="Groups";Expression={$_.MemberOf}}
   ```

---

## Questions

1. On what day was Glitch_Malware last logged in? Answer format: DD/MM/YYYY
    >07/11/2024
2. What event ID shows the login of the Glitch_Malware user?
    >4624
3. Read the PowerShell history of the Administrator account. What was the command that was used to enumerate Active Directory users?
    >Get-ADUser -Filter * -Properties MemberOf | Select-Object Name
4. Look in the PowerShell log file located in Application and Services Logs -> Windows PowerShell. What was Glitch_Malware's set password?
    >SuperSecretP@ssw0rd!
5. Review the Group Policy Objects present on the machine. What is the name of the installed GPO?
    >Malicious GPO - Glitch_Malware Persistence