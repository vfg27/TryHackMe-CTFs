# TryHackMe Advent of Cyber - Day 22: It's because I'm kubed, isn't it?

An alert from McSkidy’s dashboard highlights unusual activity in a Kubernetes environment. Suspicious logs and unauthorized access indicate a breach involving Mayor Malware, prompting an investigation into the compromise and misuse of Kubernetes clusters.

---

## **Learning Objectives**
- Understand Kubernetes and its importance in modern architecture.
- Explore challenges in Digital Forensics and Incident Response (DFIR) in ephemeral environments.
- Use log analysis for DFIR in Kubernetes.

---

## **Kubernetes: A Primer**
### Transition to Microservices
Modern companies, like Netflix, transitioned from monolithic to microservices architectures to improve scalability. Containers, lightweight and efficient, became the preferred method to host microservices.

### Kubernetes: The Orchestrator
Kubernetes automates container management:
- Scales resources to handle traffic changes.
- Ensures high availability and portability.
- Organizes workloads in **pods** running on **nodes** within a **cluster**.

---

## **DFIR Basics**
### Key Components
1. **Digital Forensics**: Post-incident analysis to trace attack vectors and collect evidence.
2. **Incident Response**: Real-time containment, remediation, and system recovery.

### Challenges in Kubernetes
Ephemeral workloads—often running for less than five minutes—make evidence collection difficult. Visibility tools like **Kubernetes audit logging** are crucial to answer key questions:
- What happened?
- Who initiated it?
- Where and when did it occur?

---

## **Investigation Walkthrough**

### 1. **Initialize the Kubernetes Cluster**
Start the Kubernetes cluster using Minikube:
```bash
minikube start
kubectl get pods -n wareville
```
Verify that all pods are running in the `wareville` namespace.

---

### 2. **Analyzing Pod Logs**
Access the `naughty-or-nice` pod to investigate Apache logs:
```bash
kubectl exec -n wareville naughty-or-nice -it -- /bin/bash
cat /var/log/apache2/access.log
```
- Observed a suspicious request to `shelly.php`.
- Further analysis required remote log backups stored in `/home/ubuntu/dfir_artefacts/`.

---

### 3. **Docker Registry Logs**
Inspect the Docker registry logs:
```bash
docker logs <CONTAINER_ID>
```
Identify unauthorized requests:
- Connections from unexpected IP `10.10.130.253`.
- HTTP `PATCH` methods indicating Mayor Malware pushed a malicious image.

---

### 4. **Role-Based Access Control (RBAC) Misconfiguration**
Review the `mayor-user` role and its permissions:
```bash
kubectl describe rolebinding mayor-user-binding -n wareville
kubectl describe role mayor-user -n wareville
```
Key findings:
- **`exec` permission** allowed Mayor Malware to shell into the `morality-checker` pod.
- Using the `job-runner-sa` service account, Mayor Malware accessed the `pull-creds` secret.

---

### 5. **Audit Log Analysis**
Filter audit logs for Mayor Malware's activity:
```bash
cat audit.log | grep --color=always '"user":{"username":"mayor-malware"'
```
- **Attempted actions**: Listed secrets, roles, and pods.
- **Successful actions**: Escalated privileges via the `job-runner` role and accessed sensitive credentials.

---

### 6. **Compromised Credentials**
Decode the `pull-creds` secret:
```bash
kubectl get secret pull-creds -n wareville -o jsonpath='{.data.\.dockerconfigjson}' | base64 --decode
```
Finding: **Push and pull credentials were identical**, allowing Mayor Malware to:
- Pull the `wishlistweb` image.
- Inject a malicious web shell.
- Push the compromised image back to the registry.

---

## **Key Lessons Learned**
1. **RBAC Misconfiguration**: Avoid granting excessive permissions (e.g., `exec`) to non-admin roles.
2. **Credential Management**:
   - Use separate credentials for push and pull actions.
   - Regularly rotate and audit credentials.
3. **Visibility and Logging**:
   - Enable Kubernetes audit logs for comprehensive tracking.
   - Maintain backups of ephemeral logs.

---

## **Conclusion**
Mayor Malware exploited misconfigured permissions and weak credential policies to compromise the Kubernetes cluster. By following DFIR best practices and implementing robust security measures, McSkidy ensured the breach was contained and future attacks prevented.


## Questions

1. What is the name of the webshell that was used by Mayor Malware?
    >shelly.php
2. What file did Mayor Malware read from the pod?
    >db.php
3. What tool did Mayor Malware search for that could be used to create a remote connection from the pod?
    >nc
4. What IP connected to the docker registry that was unexpected?
    >10.10.130.253
5. At what time is the first connection made from this IP to the docker registry?
    >29/Oct/2024:10:06:33 +0000
6. At what time is the updated malicious image pushed to the registry?
    >29/Oct/2024:12:34:28 +0000
7. What is the value stored in the "pull-creds" secret?
    >{"auths":{"http://docker-registry.nicetown.loc:5000":{"username":"mr.nice","password":"Mr.N4ughty","auth":"bXIubmljZTpNci5ONHVnaHR5"}}}