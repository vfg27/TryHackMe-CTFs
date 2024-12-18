# TryHackMe Advent of Cyber - Day 17: He analyzed and analyzed till his analyzer was sore!

Marta May Ware is facing a crisis: the main server of the Wareville network has been disconnected, and the culprit remains unidentified. Marta contacted WareSec&Aware, Wareville's top physical security company, to access the data center's CCTV streams. However, due to privacy policies, even WareSec&Aware employees cannot view recordings.

While no records of anyone entering the data center were available, suspicions arose that the camera owner may have deleted the recordings. This theory seemed implausible, as the owner of the cameras is Byte, Glitch's loyal and protective dog.

Glitch and McSkidy teamed up to investigate the allegations against Byte. WareSec&Aware provided backup log files for analysis, but manual keyword searches yielded unreadable and inconclusive results. The logs were sent to the SOC team for advanced investigation using Splunk.

---

## Learning Objectives

In this task, participants learned:

1. How to extract custom fields in Splunk.
2. Creating parsers for custom logs.
3. Using Search Processing Language (SPL) to filter and narrow search results.
4. Investigating incidents in Splunk.

---

## Investigation Details

### Tools and Setup

- **Splunk SIEM:** Pre-ingested logs were analyzed.
- **Datasets:**
  - `web_logs`: Web connections to/from the CCTV web server.
  - `cctv_logs`: CCTV application access logs.

### Log Parsing and Field Extraction

1. **Initial Findings:**
   - Logs were improperly parsed, leading to timeline inaccuracies.
   - Splunk used ingestion time rather than the actual event timestamp.

2. **Field Extraction Process:**
   - Regular expressions were used to extract fields such as `timestamp`, `Event`, `user_id`, `UserName`, and `Session_id`.
   - Issues with inconsistent log formats required adjustments to the regex pattern.
   - Final regex:
     ```regex
     ^(?P<timestamp>\d+\-\d+\-\d+\s+\d+:\d+:\d+)\s+(?P<Event>(Login\s\w+|\w+))\s+(?P<user_id>\d+)?\s?(?P<UserName>\w+)\s+.*?(?P<Session_id>\w+)$
     ```

3. **Validation and Saving:**
   - Correctly parsed logs were saved for further analysis.

---

## Key Findings

1. **CCTV Logs Analysis:**
   - Identified failed login attempts and suspicious deletions.
   - Found recurring `Session_id` linked to failed logins.
   
2. **Event Analysis:**
   - Counts of events by users visualized using pie charts and bar charts.
   - Rare events highlighted suspicious activities, including deletions and unauthorized logins.

3. **Correlating Logs:**
   - The `Session_id` linked to failed login attempts and deletions was traced.
   - Cross-referenced `Session_id` with `web_logs` to identify the attacker's IP address: `10.11.105.33`.
   - Discovered additional `Session_id`s associated with this IP.

4. **Timeline of Events:**
   - Failed brute-force attempts on accounts.
   - Successful login using compromised credentials.
   - Camera streams watched and downloaded.
   - CCTV footage deleted.
   - Web logs revealed the attacker’s IP and session activities.
   - Correlation of logs pinpointed the attacker’s username.

---

## Conclusion

The investigation revealed that the attacker:

1. Attempted to brute-force multiple accounts.
2. Gained unauthorized access and tampered with the CCTV streams.
3. Used an IP address that linked all malicious activities.
4. Deleted critical evidence by erasing CCTV footage.

This exercise demonstrated effective log analysis using Splunk, highlighting the importance of custom field extraction and correlation of datasets to identify and track adversaries.

---

## Questions

1. Extract all the events from the cctv_feed logs. How many logs were captured associated with the successful login?
    >642
2. What is the Session_id associated with the attacker who deleted the recording?
    >rij5uu4gt204q0d3eb7jj86okt
3. What is the name of the attacker found in the logs, who deleted the CCTV footage?
    >mmalware