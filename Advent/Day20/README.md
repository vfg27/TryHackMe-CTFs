# TryHackMe Advent of Cyber - Day 20: If you utter so much as one packet… 

McSkidy must investigate network traffic from Marta May Ware’s compromised machine to uncover Mayor Malware's plans. Using Wireshark, the goal is to identify Command and Control (C2) traffic, analyze its communication, and uncover encrypted secrets.

---

## **Learning Objectives**
1. Understand C2 communication patterns, including beacons and exfiltration.
2. Use Wireshark to filter, follow, and inspect network traffic.
3. Decrypt encrypted beacons using CyberChef.

---

## **Step 1: Setup**
1. Start the virtual machine and access the desktop environment.
2. Open Wireshark and load the provided `C2_Traffic_Analysis.pcap` file.

---

## **Step 2: Investigate Network Traffic**

### **Filter by Source IP**
Use the filter `ip.src == 10.10.229.217` to isolate outbound traffic from Marta May Ware's machine:
```plaintext
ip.src == 10.10.229.217
```
This narrows down the traffic, allowing a clearer focus on relevant packets.

### **Identify Key Packets**
- Highlighted packets include:
  - **POST /initial**: Frame 440
  - **GET /command**: Frame 457
  - **POST /exfiltrate**: Frame 476

### **Analyze Packets**
1. Select **Frame 440** and inspect the `Packet Bytes` pane to see the message: `I am in Mayor!`.
2. Right-click on **Frame 440** and select **Follow > HTTP Stream** to view the session. This reveals:
   - Sent message: `I am in Mayor!`
   - Server response: `Perfect!`

3. Follow **Frame 457**:
   - Command sent: User information request.
   - Indicates reconnaissance activity from the C2 server.

4. Inspect **Frame 476**:
   - Displays file exfiltration from Marta May Ware’s machine to the C2 server.

---

## **Step 3: Analyze C2 Beacons**
1. Beacons are periodic status updates sent to the C2 server.
   - Pattern: Regular intervals.
   - Encrypted payloads indicate confidential communication.

2. The file extracted in **Frame 476** contains the encryption key for decrypting the beacons.

---

## **Step 4: Decrypt Beacons with CyberChef**
1. Open the CyberChef tool in your browser.
2. Configure the following:
   - **Operation**: AES Decrypt (drag to the Recipe area).
   - **Mode**: ECB.
   - **Key**: Enter the decryption key from the exfiltrated file.
   - **Input**: Paste the encrypted beacon string.
3. Click **Bake** to decrypt and view the content of the beacon.

---

## Questions

1. What was the first message the payload sent to Mayor Malware’s C2?
    >I am in Mayor!
2. What was the IP address of the C2 server?
    >10.10.123.224
3. What was the command sent by the C2 server to the target machine?
    >whoami
4. What was the filename of the critical file exfiltrated by the C2 server?
    >credentials.txt
5. What secret message was sent back to the C2 in an encrypted format through beacons?
    >THM_Secret_101