# TryHackMe Advent of Cyber - Day 7: Oh, no. I'M SPEAKING IN CLOUDTRAIL!

Care4Wares' infrastructure is hosted in AWS, utilizing **EC2 instances** for virtualized workloads. The Wareville SOC team is adapting to tools for analyzing cloud-based logs, focusing on **AWS CloudWatch** and **CloudTrail** to investigate anomalies.

---

## AWS CloudWatch

AWS CloudWatch is a monitoring platform offering insight into AWS environments by tracking:
- **Log Events:** Timestamped records of application events.
- **Log Streams:** Collections of log events from single sources.
- **Log Groups:** Collections of log streams, grouped logically by services or hosts.

### Key Features:
- System and application metric monitoring.
- Querying application logs using filter patterns.
- Installation of a **CloudWatch Agent** is required for capturing metrics.

---

## AWS CloudTrail

CloudTrail tracks actions within AWS, such as user, role, or service activities. Features include:
- **Event History:** Logs actions for the last 90 days.
- **Custom Trails:** Tailored monitoring beyond the default retention period.
- JSON-formatted events, which can be delivered to CloudWatch.

### Example Insights:
- Track actions like `ListObjects` for specific S3 buckets.
- Identify IP addresses and User Agents linked to AWS actions.

---

## JSON Log Analysis with JQ

**JQ** is a lightweight tool for transforming and filtering JSON data, ideal for analyzing CloudTrail logs. Example usage includes:
- Filtering records by fields like `eventSource` or `bucketName`.
- Outputting tabular data for clarity.

---

## Investigating the Case of Dry Funds

### Incident Summary
1. A donation flyer link was sent on **November 28th**.
2. Donations stopped after **November 29th** despite reported successful transactions.
3. An investigation revealed the S3 bucket file had been altered to include incorrect account details.

### Investigation Steps
1. Used **CloudTrail Logs** to trace activity on the bucket.
2. Found user **glitch** accessed the bucket and uploaded a modified flyer.
3. Determined **McSkidy’s account** was compromised to create the glitch user.

---

## Logs Don’t Lie

### Amazon RDS Logs Investigation
Analyzed database logs to identify donation recipients:
- Donations redirected to **Mayor Malware’s account** after altering the flyer.

### Key Findings
| Timestamp           | Source            | Event                                   |
|---------------------|-------------------|-----------------------------------------|
| **2024-11-28 15:22** | RDS Logs         | Last donation to Care4Wares Fund.       |
| **2024-11-28 15:22** | CloudTrail Logs  | Flyer with bank details was modified.   |
| **2024-11-28 15:23** | RDS Logs         | First donation to Mayor Malware.        |

---

## Conclusion

The investigation uncovered evidence of a compromised account, unauthorized user creation, and fund redirection. The use of AWS monitoring tools like CloudWatch, CloudTrail, and JQ was critical in identifying and addressing the security breach.

**Security tools and vigilance are essential in cloud environments to detect and mitigate malicious activities.**

---

## Questions

1. What is the other activity made by the user glitch aside from the ListObject action?
    >PutObject
2. What is the source IP related to the S3 bucket activities of the user glitch?
    >53.94.201.69
3. Based on the eventSource field, what AWS service generates the ConsoleLogin event?
    >signin.amazonaws.com
4. When did the anomalous user trigger the ConsoleLogin event?
    >2024-11-28T15:21:54Z
5. What was the name of the user that was created by the mcskidy user?
    >glitch
6. What type of access was assigned to the anomalous user?
    >AdministratorAccess
7. Which IP does Mayor Malware typically use to log into AWS?
    >53.94.201.69
8. What is McSkidy's actual IP address?
    >31.210.15.79
9. What is the bank account number owned by Mayor Malware?    
    >2394 6912 7723 1294