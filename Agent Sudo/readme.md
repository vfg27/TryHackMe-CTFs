# Agent Sudo
You found a secret server located under the deep sea. Your task is to hack inside the server and reveal the truth. 

```
ip = 10.10.141.77
```

## Nmap

```
nmap -sC -sV -oN initial.log 10.10.141.77
```

>21/tcp open  ftp     vsftpd 3.0.3
>
>22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
>
>80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))

## Task 1.

```
nikto -h http://10.10.141.77 | tee nikto.log
```


