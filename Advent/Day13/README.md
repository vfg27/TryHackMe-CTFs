# TryHackMe Advent of Cyber - Day 13: It came without buffering! It came without lag!

In the city of Wareville, an illegal app is discovered tracking cars without sufficient justification. The Glitch, a security enthusiast, collaborates with McSkidy to investigate how the app is leaking user positions and identify the vulnerabilities in its implementation.

---

## Learning Objectives
1. **Understand WebSockets and their vulnerabilities.**
2. **Learn WebSocket Message Manipulation techniques.**

---

## Key Concepts

### Introduction to WebSocket
- **What are WebSockets?**
  - Persistent communication between the browser and server.
  - Efficient for live chat apps, real-time games, and live data feeds.
  - Features:
    - Minimal overhead.
    - Fast data flow.
    - Constant two-way communication after an initial handshake.

- **Traditional HTTP Requests vs. WebSocket:**
  - HTTP: Request-response cycle, inefficient for frequent updates.
  - WebSocket: Open connection allows real-time updates without repeated requests.

### WebSocket Vulnerabilities
1. **Weak Authentication and Authorization:**
   - Lack of built-in user authentication/session validation.
2. **Message Tampering:**
   - Data interception and modification if encryption is absent.
3. **Cross-Site WebSocket Hijacking (CSWSH):**
   - Attacker manipulates a user's WebSocket connection to another site.
4. **Denial of Service (DoS):**
   - Exploits the persistent connection by flooding the server with messages.

### WebSocket Message Manipulation
- Exploit: Intercept and modify WebSocket messages during transmission.
- Dangers:
  - Unauthorized actions (e.g., impersonation, financial transactions).
  - Elevated privileges.
  - Data corruption.
  - Server disruption through malicious requests.

---

## Exploitation Steps

### 1. Setup
- Navigate to `http://MACHINE_IP`.
- Use **AttackBox** to proxy traffic via Burp Suite:
  - Configure Burp Suite Proxy settings.
  - Enable proxy intercept.

### 2. Track a User
- Open the **Reindeer Tracker** app.
- Click the "Track" button.
- Observe intercepted WebSocket traffic in Burp Suite:
  - Example: Tracking user with ID `5`.

### 3. Manipulate Request
- Modify the `userId` parameter from `5` to another ID (e.g., `8`).
- Forward the manipulated request.
- Verify:
  - Check the **community reports** for the updated user being tracked.

### 4. Additional Manipulation Tests
- Explore the possibility of posting messages under different user IDs by intercepting and altering WebSocket communications.

---

## Conclusion
The CTF demonstrates how WebSocket vulnerabilities can compromise application integrity and user privacy. Proper security measures such as:
- Authentication mechanisms,
- Message validation,
- Encryption, and robust logging are essential to mitigate these risks.

---

## Questions

1. What is the value of Flag1?
    >THM{dude_where_is_my_car}
2. What is the value of Flag2?
    >THM{my_name_is_malware._mayor_malware}