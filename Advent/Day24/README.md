# TryHackMe Advent of Cyber - Day 24: You can’t hurt SOC-mas, Mayor Malware!

Mayor Malware has sabotaged Wareville’s smart lighting system, leaving the city’s factories and halls in darkness. McSkidy needs your help to analyze MQTT traffic, identify the malicious commands, and turn the lights back on using the correct MQTT message.

---

## **Learning Objectives**
1. Understand the basics of the MQTT protocol.
2. Use Wireshark to analyze MQTT traffic.
3. Reverse engineer network protocols.
4. Use MQTT commands to control IoT devices.

---

## **Background**

### **What is MQTT?**
MQTT (Message Queuing Telemetry Transport) is a lightweight protocol commonly used for IoT communication. It employs a publish/subscribe model:

- **MQTT Broker**: Connects publishing and subscribing devices.
- **MQTT Clients**: IoT devices that publish or subscribe to messages.
- **MQTT Topics**: Classify messages so clients can subscribe only to relevant ones.

---

## **Challenge Walkthrough**

### **Step 1: Analyze the Challenge Setup**
1. Navigate to the challenge directory:
   ```bash
   cd ~/Desktop/MQTTSIM/challenge/
   ./challenge.sh
   ```
2. Three windows will open:
   - MQTT broker.
   - Lights controller interface.
   - MQTT client logs.
3. Verify that the lights controller interface is non-functional.

### **Step 2: Analyze Captured Traffic**
1. Open Wireshark and load the captured MQTT traffic:
   ```bash
   File > Open > challenge.pcapng
   ```
2. Apply a filter to view MQTT traffic:
   ```
   mqtt
   ```
3. Analyze MQTT packets to:
   - Identify the topic related to the lights.
   - Determine the message used to turn the lights on or off.

---

### **Step 3: Publish the Correct Command**
Use the `mosquitto_pub` utility to send the correct MQTT message:
1. **Command Structure**:
   ```bash
   mosquitto_pub -h localhost -t "<topic>" -m "<message>"
   ```
   - `-h localhost`: Specifies the MQTT broker (running locally).
   - `-t <topic>`: MQTT topic identified from Wireshark traffic.
   - `-m <message>`: Message to publish, e.g., `"on"` or `"off"`.

2. Example Command:
   ```bash
   mosquitto_pub -h localhost -t "lights/control" -m "on"
   ```

3. Run the command and verify that the lights turn on.

---

## **Expected Outcome**
- The lights controller interface will display a flag after successfully turning on the lights.
- Document the correct topic and message for future reference.

---

## **Key Lessons Learned**
1. **MQTT Security**:
   - Secure MQTT brokers with authentication and encryption.
   - Limit topic access to authorized devices.
2. **Traffic Analysis**:
   - Use Wireshark to investigate IoT communication patterns.
   - Filter protocol-specific traffic for efficient analysis.
3. **IoT Device Control**:
   - Understand IoT protocols to mitigate risks and respond to incidents effectively.

---

## **Conclusion**
By analyzing MQTT traffic and sending the correct command, you helped McSkidy restore Wareville’s smart lighting system. This challenge demonstrates the importance of securing IoT protocols and highlights how simple misconfigurations can be exploited to disrupt critical systems.


## Questions

1. What is the flag?
    >THM{Ligh75on-day54ved}
