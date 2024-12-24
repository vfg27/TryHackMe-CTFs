# TryHackMe Advent of Cyber - Day 23: You wanna know what happens to your hashes?

Glitch discovered a password-protected PDF file on a discarded tablet belonging to Mayor Malware. This CTF involves using password-cracking techniques to uncover the file's contents and uncover the evidence.

---

## **Learning Objectives**
By completing this challenge, you will learn about:
1. Hash functions and values.
2. Storing hashed passwords securely.
3. Cracking hashes using wordlists and rules.
4. Extracting and cracking passwords for encrypted documents.

---

## **Background**
### **Hash Functions**
- A hash function takes an input and returns a fixed-size value.
- Example: **SHA-256** creates a 256-bit hash value, regardless of input size.
- For secure password storage, passwords should be hashed with a **salt** to prevent common attacks like rainbow table lookups.

Example:
- Password: `password`
- Hashed (MD5): `ce1bccda287f1d9e6d80dbd4cb6beb60`
- With Salt: `hash(password + salt)`

### **Common Passwords**
Many users pick simple, memorable passwords. For example, the most common passwords include:
1. `123456`
2. `password`
3. `qwerty`

Mayor Malware might create passwords based on his cat, Fluffy, or his title (e.g., `m4y0r2024`).

---

## **Challenge Breakdown**

### **Step 1: Analyze the Password Hash**
1. **Locate the Hash**:
   - Path: `/home/user/AOC2024/hash1.txt`
   - Content: `d956a72c83a895cb767bb5be8dba791395021dcece002b689cf3b5bf5aaa20ac`
2. **Identify the Hash Type**:
   ```bash
   cd AOC2024/
   cat hash1.txt
   python hash-id.py
   ```
   Output suggests the hash type is **SHA-256**.

### **Step 2: Crack the Password Hash**
#### **Attempt 1: RockYou Wordlist**
Use `John the Ripper` with the `rockyou.txt` wordlist:
```bash
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt
```
If unsuccessful, apply rules to test transformations:
```bash
john --format=raw-sha256 --rules=wordlist --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt
```

#### **Attempt 2: Custom Wordlist**
1. Create a custom wordlist (`wordlist.txt`) with:
   - Fluffy
   - FluffyCat
   - Mayor
   - Malware
   - MayorMalware
2. Use the custom wordlist with more extensive rules:
```bash
john --rules=single --wordlist=wordlist.txt hash1.txt
```
3. Recover the password and verify using:
```bash
john --format=raw-sha256 --show hash1.txt
```

---

### **Step 3: Crack the PDF File**
1. **Generate a PDF Hash**:
   Convert the password-protected PDF into a crackable hash using `pdf2john.pl`:
   ```bash
   pdf2john.pl private.pdf > pdf.hash
   cat pdf.hash
   ```

2. **Crack the PDF Hash**:
   Use `John the Ripper` with the custom wordlist:
   ```bash
   john --rules=single --wordlist=wordlist.txt pdf.hash
   ```
3. Once cracked, open the PDF with the recovered password to uncover the evidence.

---

## **Key Takeaways**
1. **Hash Storage Best Practices**:
   - Use modern algorithms (e.g., bcrypt, Argon2).
   - Incorporate salts to improve security.
2. **Password Cracking**:
   - Wordlists like `rockyou.txt` are valuable but not always sufficient.
   - Custom wordlists based on target profiling increase success rates.
3. **Document Security**:
   - Secure sensitive files with strong, unique passwords.
   - Avoid predictable patterns when setting passwords.

---

## **Conclusion**
By cracking the hash and opening the PDF, Glitch has uncovered Mayor Malware’s secrets, advancing the investigation. This challenge underscores the importance of understanding hashing, secure password storage, and cracking techniques for offensive and defensive security roles.


## Questions

1. Crack the hash value stored in hash1.txt. What was the password?
    >fluffycat12
2. What is the flag at the top of the private.pdf file?
    >THM{do_not_GET_CAUGHT}
