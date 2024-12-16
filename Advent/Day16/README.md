# TryHackMe Advent of Cyber - Day 16: The Wareville’s Key Vault grew three sizes that day.

#### Learning Objectives

1. Learn about Azure, its purpose, and its use cases.  
2. Understand Azure services such as Azure Key Vault and Microsoft Entra ID.  
3. Learn how to interact with an Azure tenant using Azure Cloud Shell.

---

### Introduction to Azure

McSkidy’s role as Wareville’s cybersecurity expert led her to Azure’s cloud services to manage increasing demand. Azure, as a Cloud Service Provider (CSP), offered her scalable infrastructure and access to over 200 cloud services such as identity management and data ingestion. This enabled her to replace costly and underused on-premises infrastructure. The two key Azure services relevant to this investigation are:

1. **Azure Key Vault:** Securely stores and manages secrets like API keys, passwords, and cryptographic keys. Vault owners can enable auditing and grant permissions to vault consumers.
   
2. **Microsoft Entra ID (formerly Azure Active Directory):** An identity and access management (IAM) service that organises and secures user access to resources. Users create Entra ID accounts, and admins assign permissions to them.

---

### Assumed Breach Scenario

McSkidy decided to perform an Assumed Breach test to evaluate how far an attacker could go once inside Wareville’s Azure tenant. This approach simulates an initial foothold and explores potential attack paths.

---

### Connecting to the Environment

1. Generate credentials through the connection card.
2. Log in to the Azure Portal using the generated credentials.
3. Configure language settings if needed (e.g., switch to English).
4. Launch Azure Cloud Shell (select Bash).

---

### Azure CLI and Cloud Shell

Azure Cloud Shell provides a browser-based CLI for managing Azure resources. Commands are structured as `az GROUP SUBGROUP ACTION OPTIONAL_PARAMETERS`. For example:

```bash
az ad user list
```
This command lists all users in the Azure tenant.

---

### Investigation Steps

1. **Enumerate Users:**
   
   ```bash
   az ad user list
   ```
   Filter accounts starting with `wvusr-`:

   ```bash
   az ad user list --filter "startsWith('wvusr-', displayName)"
   ```
   One account, `wvusr-backupware`, has an unusual parameter: a password stored in its field.

2. **Enumerate Groups:**

   ```bash
   az ad group list
   ```
   One group, `Secret Recovery Group`, is particularly interesting due to its description. List its members:

   ```bash
   az ad group member list --group "Secret Recovery Group"
   ```
   The `wvusr-backupware` account appears again.

3. **Investigate Role Assignments:**
   
   ```bash
   az role assignment list --assignee REPLACE_WITH_SECRET_RECOVERY_GROUP_ID --all
   ```
   This command revealed that the `Secret Recovery Group` had the `Key Vault Secrets User` role assigned to the `warevillesecrets` vault.

4. **Pivot to `wvusr-backupware`:**
   Clear the current Azure session and log in with the new credentials:

   ```bash
   az account clear
   az login -u EMAIL -p PASSWORD
   ```

5. **Explore Vault Access:**
   With access to the `Key Vault Secrets User` role, investigate secrets stored in the `warevillesecrets` vault:

   ```bash
   az keyvault secret list --vault-name warevillesecrets
   ```

---

## Questions

1. What is the password for backupware that was leaked?
    >R3c0v3r_s3cr3ts!
2. What is the group ID of the Secret Recovery Group?
    >7d96660a-02e1-4112-9515-1762d0cb66b7
3. What is the name of the vault secret?
    >aoc2024
4. What are the contents of the secret stored in the vault?
    >WhereIsMyMind1999