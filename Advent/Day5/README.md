# TryHackMe Advent of Cyber - Day 5: SOC-mas XX-what-ee? 

## Story Overview

In the cheerful town of Wareville, Software and his team worked tirelessly to complete their projects before Christmas. Inspired by a conversation with a young boy who wished for a teddy bear, Software proposed a platform for sharing Christmas wishes. With the enthusiastic backing of Mayor Malware, the platform quickly became a hit among the townspeople.

However, the rush to release the application left a critical oversight: insufficient security testing. Now, it's up to you to secure the platform, ensuring it remains a safe space for Wareville’s holiday joy.

---

## Learning Objectives

- **Understand XML**: Learn about XML as a data format and its role in web applications.
- **Explore XXE Vulnerabilities**: Understand XML External Entities and their exploitation potential.
- **Learn to Exploit**: Identify and exploit XXE vulnerabilities in a safe testing environment.
- **Mitigation Techniques**: Implement strategies to prevent XXE vulnerabilities.

---

## Important Concepts

### Extensible Markup Language (XML)
XML structures data in a human- and machine-readable format, using tags to organize information.  
Example:
```xml
<people>
  <name>Glitch</name>
  <address>Wareville</address>
</people>
```

### Document Type Definition (DTD)
Defines the structure and allowed elements in an XML document.  
Example:
```xml
<!DOCTYPE people [
  <!ELEMENT people (name, address)>
  <!ELEMENT name (#PCDATA)>
  <!ELEMENT address (#PCDATA)>
]>
```

### Entities in XML
Entities act as placeholders for data or external references. Improper handling can lead to vulnerabilities.  
Example with an external entity:
```xml
<!DOCTYPE people [
  <!ENTITY ext SYSTEM "http://example.com/resource.txt">
]>
```

---

## XML External Entity (XXE) Vulnerability

XXE attacks exploit how XML parsers process external entities, allowing attackers to access sensitive files or systems.  
Example of an XXE payload:
```xml
<!DOCTYPE foo [
  <!ENTITY payload SYSTEM "file:///etc/passwd">
]>
<foo>&payload;</foo>
```

This malicious payload attempts to read the contents of `/etc/passwd` on a server and can result in information disclosure.

---

## Exploiting XXE: A Step-by-Step Approach

1. **Identify XML Input**: Locate XML data inputs (e.g., file uploads, user submissions) in the application.
2. **Test for XXE**: Craft XML payloads containing external entities to test the parser's handling of them.
3. **Observe the Behavior**: Examine responses from the server. If the application discloses sensitive information or behaves unexpectedly, it may be vulnerable to XXE.

---

## Mitigation Strategies

- **Disable External Entity Processing**: Ensure XML parsers are configured to prevent the processing of external entities.
- **Use Secure Parsers**: Utilize libraries or parsers that automatically disable external entity processing.
- **Input Validation**: Properly validate and sanitize user inputs to ensure they do not contain malicious XML.
- **Limit Permissions**: If external entities are necessary, ensure they are properly constrained and cannot access sensitive resources.

---

## Conclusion

By understanding and mitigating XXE vulnerabilities, you can safeguard applications like the Wareville Christmas Wish Platform from malicious exploitation. As with any security issue, proactive testing and validation are key to ensuring a safe and secure environment.


## Questions

1. What is the flag discovered after navigating through the wishes?
    >THM{Brut3f0rc1n6_mY_w4y}
2. What is the flag seen on the possible proof of sabotage?
    >THM{m4y0r_m4lw4r3_b4ckd00rs}