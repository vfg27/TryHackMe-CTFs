# TryHackMe Advent of Cyber - Day 12: If I can’t steal their money, I’ll steal their joy!

This challenge centers on identifying and exploiting race condition vulnerabilities in a banking application. The narrative follows Glitch as they uncover security flaws that allow unauthorized fund transfers due to improper handling of concurrent requests.

## Key Learning Objectives
1. **Understanding Race Condition Vulnerabilities**:
   - Concept of race conditions and their impact on web applications.
   - Differences between HTTP/1.1 and HTTP/2 in enabling timing attacks.

2. **Exploiting Race Conditions**:
   - Using Burp Suite to intercept and manipulate HTTP requests.
   - Executing race condition attacks in a controlled environment.

3. **Mitigation Strategies**:
   - Implementing atomic transactions.
   - Using mutex locks for resource access.
   - Applying rate limits on critical operations.

---

## Exploiting the Vulnerability

### Identifying the Issue
- Discrepancies in account balances due to simultaneous requests exploiting race conditions during fund transfers.

### Tools and Setup
1. **Environment Setup**:
   - Access Wareville Bank’s application via `http://MACHINE_IP:5000/`.
   - Use Burp Suite to intercept HTTP requests.

2. **Interception**:
   - Capture POST requests during fund transfers.
   - Duplicate requests using Burp Suite’s Repeater tool.

### Attack Execution
1. **Duplicate Requests**:
   - Create multiple instances of the same request to exploit timing gaps.
2. **Send in Parallel**:
   - Use Burp Suite’s tab grouping feature to execute requests simultaneously.
3. **Observe Results**:
   - Check for anomalies like negative balances or inflated recipient accounts.

---

## Code Review
- Example vulnerable code snippet:
  ```python
  if user['balance'] >= amount:
      conn.execute('UPDATE users SET balance = balance + ? WHERE account_number = ?',
                   (amount, target_account_number))
      conn.commit()

      conn.execute('UPDATE users SET balance = balance - ? WHERE account_number = ?',
                   (amount, session['user']))
      conn.commit()
  ```
- Issue: Lack of atomic transactions, leading to inconsistent database states.

---

## Mitigation Strategies
1. **Atomic Transactions**:
   - Ensure operations are completed as a single unit.
2. **Mutex Locks**:
   - Prevent concurrent access to shared resources.
3. **Rate Limits**:
   - Limit request frequency to reduce abuse potential.

---

## Key Takeaways
1. Race conditions demonstrate critical security flaws in web applications that must be addressed to prevent exploitation.
2. Proper coding practices and system configurations are essential for maintaining secure applications.
3. Education and awareness of race condition vulnerabilities can help improve overall cybersecurity defenses.

---

## Questions

1. What is the flag value after transferring over $2000 from Glitch's account?
    >THM{WON_THE_RACE_007}